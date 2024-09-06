from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
# from typing import Annotated

from .. import models
from ..database import get_db
from .. import utils, oauth2


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="", tags=["Auth"])


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.name == user_credentials.username).first()

    if user:
        if not utils.verify_pwd(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                                "Invalid Credentials": "Invalid Credentials"})
        # utils.verify_pwd(user_credentials.password, user.password)
        access_token = oauth2.create_access_token(data={"user_id": user.id})
        return {"token": access_token, "token_type": "bearer",
                "user": user}

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                        "Invalid Credentials": "Invalid Credentials"})


@router.post("/update_password")
def update_password(new_password: str, db: Session = Depends(get_db),
                    user: models.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user.id).first()
    if user:
        hashed_password = pwd_context.hash(new_password)
        user.password = hashed_password
        db.commit()
        db.refresh(user)
        return {"status": "200"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                            "Invalid Credentials": "Invalid Credentials"})


@router.get("/logout")
def logout(id: int, db: Session = Depends(get_db)):

    return {"status": "200"}
