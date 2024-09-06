from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/city", tags=["City"])


@router.post("/create", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    new_city = models.City(**city.model_dump())
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


@router.get("/", response_model=list[schemas.City])
def get_all_city(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    return cities


@router.get("/region/{region_id}", response_model=schemas.City)
def get_all_city_in_region(region_id: int, db: Session = Depends(get_db)):
    cities = db.query(models.City).filter(models.City.region_id == region_id).all()
    return cities


@router.get("/{id}", response_model=schemas.City)
def get_city_by_id(id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == id).first()
    return city


@router.put("/id")
def update_user(id: int, db: Session = Depends(get_db)):
    pass
