from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Annotated

from .. import models, schemas
from ..database import get_db
from .. import utils, oauth2


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="", tags=["Auth"])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == user_credentials.username).first()
    
    if user:
        utils.verify_pwd(user_credentials.password, user.password)
        access_token = oauth2.create_access_token(data={"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"Invalid Credentials": "Invalid Credentials"})


@router.get("/logout")
def logout(id: int, db: Session = Depends(get_db)):
    
    return {"status": "200"}

