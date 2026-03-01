from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from database import Base


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    area_ha = Column(Float, nullable=False)
    location = Column(String, nullable=False)

    plants = relationship("PlantRecord", back_populates="field", cascade="all, delete-orphan")


class PlantRecord(Base):
    __tablename__ = "plant_records"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)
    crop_name = Column(String, nullable=False)
    stage = Column(String, nullable=False)
    planted_on = Column(Date, nullable=False)
    expected_harvest = Column(Date, nullable=True)

    field = relationship("Field", back_populates="plants")


class CommodityPrice(Base):
    __tablename__ = "commodity_prices"

    id = Column(Integer, primary_key=True, index=True)
    commodity = Column(String, nullable=False, index=True)
    market = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    price_date = Column(Date, nullable=False)


class WaterUsage(Base):
    __tablename__ = "water_usage"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    liters = Column(Float, nullable=False)
    recorded_at = Column(DateTime, nullable=False, server_default=func.now())


class ElectricityGeneration(Base):
    __tablename__ = "electricity_generation"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    kwh_generated = Column(Float, nullable=False)
    kwh_consumed = Column(Float, nullable=False)
    recorded_at = Column(DateTime, nullable=False, server_default=func.now())


class FarmTask(Base):
    __tablename__ = "farm_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    status = Column(String, nullable=False, default="todo")
    due_date = Column(Date, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
