from fastapi import Body, Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from .. import utils
from psssa_app import oauth2

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
def get_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


@router.put("/update_password", response_model=schemas.UserResponse)
def update_password(
    user_id: int = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.password = utils.hash(new_password)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_user, synchronize_session=True)
    db.commit()
    db.refresh(db_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
