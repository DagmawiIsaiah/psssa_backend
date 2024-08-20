from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routes import auth, user, city, record, region, category, status, account_type

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
    "http://localhost.tiangolo.com", # replace with the domain of your frontend app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_type.router)
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(city.router)
app.include_router(record.router)
app.include_router(region.router)
app.include_router(status.router)
app.include_router(user.router)
