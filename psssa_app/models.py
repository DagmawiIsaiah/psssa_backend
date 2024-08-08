from sqlalchemy import Column, Integer, String

from .database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String(100), nullable=False) # Civil, Military, Police, undertaking


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String(150), nullable=False)


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    region_id = Column(Integer, nullable=False)
    name = Column(String(150), nullable=False)


class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String(150), nullable=False) # Pending, Accepted


class AccountType(Base):
    __tablename__ = "account_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String(20), nullable=False) # Admin, User


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    region_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    city_id = Column(Integer, nullable=False)
    name = Column(String(150), nullable=False)
    pension_number = Column(String(255), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    account_type_id = Column(Integer, nullable=False)
    region_id = Column(Integer, nullable=False)
    city_id = Column(Integer, nullable=False)
    name = Column(String(150), nullable=False)
    password = Column(String(255), nullable=False)
    