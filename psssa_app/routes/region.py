from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/region", tags=["Region"])


@router.post("/create", response_model=schemas.Region)
def create_region(region: schemas.RegionCreate, db: Session = Depends(get_db)):
    new_region = models.Region(**region.model_dump())
    db.add(new_region)
    db.commit()
    db.refresh(new_region)
    return new_region


@router.get("/", response_model=list[schemas.Region])
def get_all_region(db: Session = Depends(get_db)):
    regions = db.query(models.Region).all()
    return regions


@router.get("/{id}", response_model=schemas.Region)
def get_region_by_id(id: int, db: Session = Depends(get_db)):
    region = db.query(models.Region).filter(models.Region.id == id).first()
    return region


@router.put("/id")
def update_user(id: int, db: Session = Depends(get_db)):
    pass
