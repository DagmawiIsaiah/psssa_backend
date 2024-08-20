from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/status", tags=["Status"])


@router.get("/", response_model=list[schemas.Status])
def get_all_status(db: Session = Depends(get_db)):
    status = db.query(models.Status).all()
    return status


@router.get("/{id}", response_model=schemas.Status)
def get_status_by_id(id: int, db: Session = Depends(get_db)):
    status = db.query(models.Status).filter(models.Status.id == id).first()
    return status
