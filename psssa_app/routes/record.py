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
def get_record(
    category_id: int | None = None,
    region_id: int | None = None,
    city_id: int | None = None,
    status_id: int | None = None,
    pention_number: str | None = None,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    query = db.query(models.Record)

    if category_id is not None:
        query = query.filter(models.Record.category_id == category_id)
    if region_id is not None:
        query = query.filter(models.Record.region_id == region_id)
    if city_id is not None:
        query = query.filter(models.Record.city_id == city_id)
    if status_id is not None:
        query = query.filter(models.Record.status_id == status_id)
    if pention_number is not None:
        query = query.filter(models.Record.pention_number == pention_number)

    records = query.filter(
        or_(
            models.Record.city_id == user.city_id,
            models.Record.created_city_id == user.city_id,
        )
    ).all()

    if not records:
        raise HTTPException(status_code=404, detail="No records found")

    return records


@router.put("/id")
def update_record(
    id: int,
    record: schemas.RecordCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    db_record = (
        db.query(models.RecordCreate)
        .filter(
            or_(
                models.Record.city_id == user.city_id,
                models.Record.created_city_id == user.city_id,
            )
        )
        .first()
    )
    if not db_record:
        raise HTTPException(status_code=404, detail="Item not found")
    db_record = models.Record(**record.model_dump())
    db.commit()
    db.refresh(db_record)
    return db_record
