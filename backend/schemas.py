from datetime import date, datetime
from pydantic import BaseModel, Field


class FieldBase(BaseModel):
    name: str
    area_ha: float = Field(gt=0)
    location: str


class FieldCreate(FieldBase):
    pass


class FieldRead(FieldBase):
    id: int

    class Config:
        from_attributes = True


class PlantRecordBase(BaseModel):
    field_id: int
    crop_name: str
    stage: str
    planted_on: date
    expected_harvest: date | None = None


class PlantRecordCreate(PlantRecordBase):
    pass


class PlantRecordRead(PlantRecordBase):
    id: int

    class Config:
        from_attributes = True


class CommodityPriceBase(BaseModel):
    commodity: str
    market: str
    unit: str
    price: float = Field(gt=0)
    price_date: date


class CommodityPriceCreate(CommodityPriceBase):
    pass


class CommodityPriceRead(CommodityPriceBase):
    id: int

    class Config:
        from_attributes = True


class WaterUsageBase(BaseModel):
    source: str
    liters: float = Field(gt=0)


class WaterUsageCreate(WaterUsageBase):
    pass


class WaterUsageRead(WaterUsageBase):
    id: int
    recorded_at: datetime

    class Config:
        from_attributes = True


class ElectricityGenerationBase(BaseModel):
    source: str
    kwh_generated: float = Field(ge=0)
    kwh_consumed: float = Field(ge=0)


class ElectricityGenerationCreate(ElectricityGenerationBase):
    pass


class ElectricityGenerationRead(ElectricityGenerationBase):
    id: int
    recorded_at: datetime

    class Config:
        from_attributes = True


class FarmTaskBase(BaseModel):
    title: str
    category: str
    status: str = "todo"
    due_date: date | None = None
    notes: str | None = None


class FarmTaskCreate(FarmTaskBase):
    pass


class FarmTaskUpdate(BaseModel):
    title: str | None = None
    category: str | None = None
    status: str | None = None
    due_date: date | None = None
    notes: str | None = None


class FarmTaskRead(FarmTaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardSummary(BaseModel):
    total_fields: int
    total_area_ha: float
    active_crops: int
    avg_commodity_price: float
    total_water_liters: float
    total_kwh_generated: float
    total_kwh_consumed: float
    energy_balance_kwh: float
    total_tasks: int
    open_tasks: int
