from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/category", tags=["Category"])


@router.get("/", response_model=list[schemas.Category])
def get_all_category(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories


@router.get("/{id}", response_model=schemas.Category)
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    return category
