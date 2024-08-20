from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from .. import utils

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/create", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hash_password = utils.hash(user.password)
    user.password = hash_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


@router.put("/id")
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Item not found")
    db_user = models.User(**user.model_dump())
    db_user.password = utils.hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_user, synchronize_session=False)
    db.commit()
    db.refresh(db_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

