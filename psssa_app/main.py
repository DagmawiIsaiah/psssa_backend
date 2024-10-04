from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routes import auth, user, record

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow PUT, POST, GET, etc.
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(record.router)
app.include_router(user.router)
