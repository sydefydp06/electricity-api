from typing import List, Optional

from sqlalchemy.sql.elements import _truncated_label

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

# import models
# import schemas

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Just going to create a dictionary for now. Not sure how it would fit into current database.
# TODO: Probably should add this to the database, but that might need further discussion.
# key is first letter of postal code, value is province_code in db.
postal_to_province = {
    'A': 23,    # Newfoundland and Labrador
    'B': 20,    # Nova Scotia
    'C': 22,    # Prince Edward Island
    'E': 21,    # New Brunswick
    'G': 19,    # Eastern Quebec
    'H': 19,    # Metropolitan Montreal
    'J': 19,    # Western Quebec
    'K': 18,    # Eastern Ontario
    'L': 18,    # Central Ontario
    'M': 18,    # Metropolitan Ontario
    'N': 18,    # Southwestern Ontario
    'P': 18,    # Northern Ontario
    'R': 17,    # Manitoba
    'S': 16,    # Saskatchewan
    'T': 15,    # Alberta
    'V': 14,    # British Columbia
    'X': 25,    # Northwest Territories and Nunavut
    'Y': 24,    # Yukon
}

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    # return {"message": "Hello World"}
    return RedirectResponse(url="/docs/")


@app.get("/energy-types/", response_model=List[schemas.EnergyType])
def show_records(db: Session = Depends(get_db)):
    records = db.query(models.EnergyType).all()
    return records


@app.get("/energy-profile/")
def get_profile_from_postal(postal_code: Optional[str] = None, province: Optional[str] = None, db: Session = Depends(get_db)):
    records = {}
    # get postal code and province from energy_profiles depending on input parameters
    try:
        if postal_code != None:
            records['energy_profile_code'] = db.query(models.Province).\
                filter(models.Province.province_code == postal_to_province[postal_code[0].upper()]).\
                    first().energy_profile_code
            records['province_name'] = db.query(models.Province).\
                filter(models.Province.province_code == postal_to_province[postal_code[0].upper()]).\
                    first().name
        elif province != None and postal_code == None:
            records['province_name'] = db.query(models.Province).\
                filter(models.Province.abbreviation == province.upper()).first().name
            records['energy_profile_code'] = db.query(models.Province).\
                filter(models.Province.abbreviation == province.upper()).first().energy_profile_code
        else:   # TODO: Check if there is mismatch between province and postal code parameter
            return {"ERROR":"no data"}  # TODO: Throw real error message
    except AttributeError:
        return {"ERROR":"invalid parameter"}    # TODO: Throw real error message
    # get energy producers from that province
    records['sources'] = db.query(models.EnergySource, models.EnergyType).\
        filter(models.EnergySource.energy_type == models.EnergyType.energy_type).\
            filter(models.EnergySource.energy_profile_code == records['energy_profile_code']).all()
    # calculate percent renewable and percent non emitting
    # calculate emissions
    mw_total = 0    # This data is in MW
    mw_renewable = 0
    mw_non_emitting = 0
    records['emissions'] = 0    # This data will be kg CO2 emitted per hour
    for element in records['sources']:
        mw_total += element.EnergySource.quantity
        if element.EnergyType.is_renewable == True:
            mw_renewable += element.EnergySource.quantity
        if element.EnergyType.is_non_emitting == True:
            mw_non_emitting += element.EnergySource.quantity
        records['emissions'] += element.EnergySource.quantity * element.EnergyType.co2_per_kwh
    records['percent_renewable'] = mw_renewable / mw_total if mw_total > 0 else 'no data'
    records['percent_non_emitting'] = mw_non_emitting / mw_total if mw_total > 0 else 'no data'
    return records
