import db
from fastapi import FastAPI

db.create_all()

app = FastAPI()