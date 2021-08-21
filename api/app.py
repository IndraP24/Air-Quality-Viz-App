from fastapi import FastAPI
from pydantic import BaseModel

from lib.main import *

app = FastAPI()


class Input(BaseModel):
    data_path: str
    periods: int


@app.get("/ping")
def pong():
    return {"ping": "pong"}


@app.post("/predict")
def forecast(input: Input):
    data_path = input.data_path
    df = preprocess(data_path)
