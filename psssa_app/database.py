from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dev_db = {
    "user": "psssadb_owner",
    "password": "yZX3uGCINgW0",
    "host": "ep-dark-term-a5g4i01f.us-east-2.aws.neon.tech",
    "database": "psssadb",
    "port": "5432",
}

SQLALCHEMY_DATABASE_URL = f"postgresql://{dev_db['user']}:{dev_db['password']}@{dev_db['host']}:{dev_db['port']}/{dev_db['database']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
