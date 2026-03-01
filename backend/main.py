from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db
from seed import seed_if_empty

app = FastAPI(title="Farm Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed_if_empty(db)
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/fields", response_model=schemas.FieldRead)
def create_field(payload: schemas.FieldCreate, db: Session = Depends(get_db)):
    item = models.Field(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/fields", response_model=list[schemas.FieldRead])
def list_fields(db: Session = Depends(get_db)):
    return db.query(models.Field).order_by(models.Field.name.asc()).all()


@app.post("/plants", response_model=schemas.PlantRecordRead)
def create_plant_record(payload: schemas.PlantRecordCreate, db: Session = Depends(get_db)):
    item = models.PlantRecord(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/plants", response_model=list[schemas.PlantRecordRead])
def list_plants(field_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(models.PlantRecord)
    if field_id:
        query = query.filter(models.PlantRecord.field_id == field_id)
    return query.order_by(models.PlantRecord.planted_on.desc()).all()


@app.post("/commodity-prices", response_model=schemas.CommodityPriceRead)
def create_commodity_price(payload: schemas.CommodityPriceCreate, db: Session = Depends(get_db)):
    item = models.CommodityPrice(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/commodity-prices", response_model=list[schemas.CommodityPriceRead])
def list_commodity_prices(
    commodity: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(models.CommodityPrice)
    if commodity:
        query = query.filter(models.CommodityPrice.commodity.ilike(f"%{commodity}%"))
    return query.order_by(models.CommodityPrice.price_date.desc()).all()


@app.post("/water-usage", response_model=schemas.WaterUsageRead)
def create_water_usage(payload: schemas.WaterUsageCreate, db: Session = Depends(get_db)):
    item = models.WaterUsage(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/water-usage", response_model=list[schemas.WaterUsageRead])
def list_water_usage(db: Session = Depends(get_db)):
    return db.query(models.WaterUsage).order_by(models.WaterUsage.recorded_at.desc()).all()


@app.post("/electricity", response_model=schemas.ElectricityGenerationRead)
def create_electricity(payload: schemas.ElectricityGenerationCreate, db: Session = Depends(get_db)):
    item = models.ElectricityGeneration(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/electricity", response_model=list[schemas.ElectricityGenerationRead])
def list_electricity(db: Session = Depends(get_db)):
    return db.query(models.ElectricityGeneration).order_by(models.ElectricityGeneration.recorded_at.desc()).all()


@app.post("/tasks", response_model=schemas.FarmTaskRead)
def create_task(payload: schemas.FarmTaskCreate, db: Session = Depends(get_db)):
    item = models.FarmTask(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/tasks", response_model=list[schemas.FarmTaskRead])
def list_tasks(status: str | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(models.FarmTask)
    if status:
        query = query.filter(models.FarmTask.status == status)
    return query.order_by(models.FarmTask.created_at.desc()).all()


@app.patch("/tasks/{task_id}", response_model=schemas.FarmTaskRead)
def update_task(task_id: int, payload: schemas.FarmTaskUpdate, db: Session = Depends(get_db)):
    item = db.query(models.FarmTask).filter(models.FarmTask.id == task_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


@app.get("/dashboard/summary", response_model=schemas.DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db)):
    total_fields = db.query(func.count(models.Field.id)).scalar() or 0
    total_area = db.query(func.coalesce(func.sum(models.Field.area_ha), 0)).scalar() or 0
    active_crops = db.query(func.count(models.PlantRecord.id)).scalar() or 0
    avg_price = db.query(func.coalesce(func.avg(models.CommodityPrice.price), 0)).scalar() or 0
    total_water = db.query(func.coalesce(func.sum(models.WaterUsage.liters), 0)).scalar() or 0
    total_gen = db.query(func.coalesce(func.sum(models.ElectricityGeneration.kwh_generated), 0)).scalar() or 0
    total_cons = db.query(func.coalesce(func.sum(models.ElectricityGeneration.kwh_consumed), 0)).scalar() or 0
    total_tasks = db.query(func.count(models.FarmTask.id)).scalar() or 0
    open_tasks = db.query(func.count(models.FarmTask.id)).filter(models.FarmTask.status != "done").scalar() or 0

    return schemas.DashboardSummary(
        total_fields=total_fields,
        total_area_ha=round(float(total_area), 2),
        active_crops=active_crops,
        avg_commodity_price=round(float(avg_price), 2),
        total_water_liters=round(float(total_water), 2),
        total_kwh_generated=round(float(total_gen), 2),
        total_kwh_consumed=round(float(total_cons), 2),
        energy_balance_kwh=round(float(total_gen - total_cons), 2),
        total_tasks=total_tasks,
        open_tasks=open_tasks,
    )
