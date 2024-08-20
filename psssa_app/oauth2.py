from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


from datetime import datetime, timedelta, timezone

from . import models
from .database import SessionLocal, get_db

oauth2scheme = OAuth2PasswordBearer(tokenUrl="login")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "bfe6bf9e7a057bc886f114b768515a60d4453b85c9fc0b1c402f7dc700f2d6c7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10


def get_user_by_id(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = int(payload.get("user_id"))
        if id is None:
            raise credentials_exception
        
        with SessionLocal() as db:
            user = get_user_by_id(id, db)
            
            if user is None:
                raise credentials_exception
            
        return user
    except JWTError:
        raise credentials_exception
    

def get_current_user(token: str = Depends(oauth2scheme)):
    creadential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token=token, credentials_exception=creadential_exception)
