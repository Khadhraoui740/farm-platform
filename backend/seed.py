from datetime import date
from sqlalchemy.orm import Session

import models


def seed_if_empty(db: Session):
    has_fields = db.query(models.Field).first()
    if has_fields:
        return

    field_a = models.Field(name="Parcelle Nord", area_ha=2.4, location="Zone A")
    field_b = models.Field(name="Parcelle Sud", area_ha=1.8, location="Zone B")
    db.add_all([field_a, field_b])
    db.flush()

    db.add_all([
        models.PlantRecord(
            field_id=field_a.id,
            crop_name="Tomate",
            stage="Croissance",
            planted_on=date(2026, 2, 10),
            expected_harvest=date(2026, 4, 20),
        ),
        models.PlantRecord(
            field_id=field_b.id,
            crop_name="Pomme de terre",
            stage="Semis",
            planted_on=date(2026, 2, 25),
            expected_harvest=date(2026, 6, 15),
        ),
    ])

    db.add_all([
        models.CommodityPrice(
            commodity="Tomate",
            market="Marché central",
            unit="€/kg",
            price=1.6,
            price_date=date(2026, 3, 1),
        ),
        models.CommodityPrice(
            commodity="Pomme de terre",
            market="Marché central",
            unit="€/kg",
            price=0.9,
            price_date=date(2026, 3, 1),
        ),
    ])

    db.add_all([
        models.WaterUsage(source="Forage", liters=3200),
        models.WaterUsage(source="Réseau", liters=1100),
    ])

    db.add_all([
        models.ElectricityGeneration(source="Solaire", kwh_generated=145.2, kwh_consumed=89.4),
        models.ElectricityGeneration(source="Réseau", kwh_generated=0, kwh_consumed=37.1),
    ])

    db.add_all([
        models.FarmTask(
            title="Vérifier irrigation parcelle Nord",
            category="Eau",
            status="todo",
            notes="Contrôler débit et pression",
        ),
        models.FarmTask(
            title="Nettoyer panneaux solaires",
            category="Énergie",
            status="in_progress",
            notes="Prévoir intervention matin",
        ),
        models.FarmTask(
            title="Contrôle sanitaire tomates",
            category="Plantes",
            status="done",
            notes="Aucun parasite détecté",
        ),
    ])

    db.commit()
