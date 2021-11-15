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
