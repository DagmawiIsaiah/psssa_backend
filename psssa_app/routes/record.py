from fastapi import Body, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_

from psssa_app import oauth2

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/record", tags=["Record"])


@router.post("/create", response_model=schemas.Record)
def create_record(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    new_record = models.Record(**record.model_dump())
    new_record.status_id = 1
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@router.get("/{pension_number}", response_model=schemas.Record)
def get_record(
    pension_number: str = None,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    query = db.query(models.Record).filter(models.Record.pension_number
                                           == pension_number)

    records = query.filter(
        or_(
            models.Record.city_id == user.city_id,
            models.Record.created_city_id == user.city_id,
        )
    ).first()

    if not records:
        raise HTTPException(status_code=404, detail="No records found")

    return records


@router.put("/update/")
def update_record(
    id: int = Body(...),
    new_status: int = Body(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):

    query = db.query(models.Record).filter(models.Record.id
                                           == id)

    db_record = query.filter(
        or_(
            models.Record.city_id == user.city_id,
            models.Record.created_city_id == user.city_id,
        )
    ).first()
    
    if not db_record:
        raise HTTPException(status_code=404, detail="Item not found")
    db_record.status_id = new_status
    db.commit()
    db.refresh(db_record)
    return db_record
