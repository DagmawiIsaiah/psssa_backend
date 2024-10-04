from sqlalchemy import Column, Integer, String

from .database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, 
        nullable=False
    )
    region_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    city_id = Column(Integer, nullable=False)
    created_city_id = Column(Integer, nullable=False)
    status_id = Column(Integer, nullable=False)
    name = Column(String(150), nullable=False)
    pension_number = Column(String(255), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer, primary_key=True, nullable=False, index=True, 
        autoincrement=True
    )
    account_type_id = Column(Integer, nullable=False)
    region_id = Column(Integer, nullable=False)
    city_id = Column(Integer, nullable=False)
    name = Column(String(150), nullable=False)
    password = Column(String(255), nullable=False)
