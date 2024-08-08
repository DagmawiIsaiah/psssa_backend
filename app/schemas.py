from typing import Optional
from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True
        

class Region(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class RegionCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True
        

class City(BaseModel):
    region_id: int
    name: str

    class Config:
        orm_mode = True


class CityCreate(BaseModel):
    region_id: int
    name: str

    class Config:
        orm_mode = True


class Status(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class AccountType(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Record(BaseModel):
    id: int
    region_id: int
    category_id: int
    city_id: int
    name: str
    pension_number: str

    class Config:
        orm_mode = True


class RecordCreate(BaseModel):
    region_id: int
    category_id: int
    city_id: int
    name: str
    pension_number: str

    class Config:
        orm_mode = True
        

class User(BaseModel):
    id: int
    account_type_id: int
    region_id: int
    city_id: int
    name: str
    password: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    account_type_id: int
    region_id: int
    city_id: int
    name: str
    password: str

    class Config:
        orm_mode = True


class UserReturn(BaseModel):
    account_type_id: int
    region_id: int
    city_id: int
    name: str
    
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
