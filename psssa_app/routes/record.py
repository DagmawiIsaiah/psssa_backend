from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_

from psssa_app import oauth2

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/record", tags=["Record"])


@router.post("/create", response_model=schemas.Record)
def create_record(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    new_record = models.Record(**record.model_dump())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@router.get("/", response_model=list[schemas.Record])
def get_all_records(db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    if user.account_type_id == 1:
        return db.query(models.Record).all()
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/{id}", response_model=schemas.Record)
def get_record_by_id(id: int, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    record = db.query(models.Record).filter(
        models.Record.id == id, or_(models.Record.created_city_id == user.city_id, models.Record.city_id == user.city_id)).first()
    return record


@router.put("/id")
def update_record(id: int, record: schemas.Record, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    db_record = db.query(models.RecordCreate).filter(or_(
        models.Record.city_id == user.city_id, models.Record.created_city_id == user.city_id)).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Item not found")
    db_record = models.Record(**record.model_dump())
    db.commit()
    db.refresh(db_record)
    return db_record
