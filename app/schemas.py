# from datetime import date
from pydantic import BaseModel


class EnergyType(BaseModel):
    energy_type: int
    name: str
    abbreviation: str
    co2_per_kwh: float
    is_renewable: bool
    is_non_emitting: bool

    class Config:
        orm_mode = True

class EnergyProfile(BaseModel):
    energy_profile_code: int
    name: str

    class Config:
        orm_mode = True

class EnergySource(BaseModel):
    source_id: int
    quantity: float
    name: str
    energy_profile_code: int
    energy_type: int

    class Config:
        orm_mode = True

class Province(BaseModel):
    province_code: int
    name: str
    abbreviation: str
    energy_profile_code: int

    class Config:
        orm_mode = True