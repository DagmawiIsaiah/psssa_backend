from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/account_type", tags=["Account Type"])


@router.get("/", response_model=list[schemas.AccountType])
def get_all_account_type(db: Session = Depends(get_db)):
    account_types = db.query(models.AccountType).all()
    return account_types


@router.get("/{id}", response_model=schemas.AccountType)
def get_account_type_by_id(id: int, db: Session = Depends(get_db)):
    account_type = db.query(models.AccountType).filter(models.AccountType.id == id).first()
    return account_type
