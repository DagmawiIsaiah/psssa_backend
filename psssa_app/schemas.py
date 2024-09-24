from typing import Optional
from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True
        

class Region(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RegionCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True
        

class City(BaseModel):
    id: int
    region_id: int
    name: str

    class Config:
        from_attributes = True


class CityCreate(BaseModel):
    region_id: int
    name: str

    class Config:
        from_attributes = True


class Record(BaseModel):
    id: int
    region_id: int
    category_id: int
    city_id: int
    created_city_id: int
    status_id: int
    name: str
    pension_number: str

    class Config:
        from_attributes = True


class RecordCreate(BaseModel):
    region_id: int
    category_id: int
    city_id: int
    created_city_id: int
    name: str
    pension_number: str

    class Config:
        from_attributes = True
        

class User(BaseModel):
    id: int
    account_type_id: int
    region_id: int
    city_id: int
    name: str
    password: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    account_type_id: int
    region_id: int
    city_id: int
    name: str
    password: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    account_type_id: int
    region_id: int
    city_id: int
    name: str
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
