from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base


class EnergyType(Base):
    __tablename__ = "energy_types"

    energy_type = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    abbreviation = Column(String(255))
    co2_per_kwh = Column(Float)
    is_renewable = Column(Boolean)
    is_non_emitting = Column(Boolean)

class EnergyProfile(Base):
    __tablename__ = "energy_profiles"

    energy_profile_code = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))

class EnergySource(Base):
    __tablename__ = "energy_sources"

    source_id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Float)
    name = Column(String(255))
    energy_profile_code = Column(Integer)
    energy_type = Column(Integer)

class Province(Base):
    __tablename__ = "provinces"

    province_code = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    abbreviation = Column(String(255))
    energy_profile_code = Column(Integer)