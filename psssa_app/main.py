from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routes import auth, user, city, record, region, category

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
    # replace with the domain of your frontend app
    "http://localhost.tiangolo.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(category.router)
app.include_router(city.router)
app.include_router(record.router)
app.include_router(region.router)
app.include_router(user.router)
