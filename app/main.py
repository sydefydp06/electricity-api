from typing import List

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
