from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from lib.sarima import *
from lib.preprocess import *
from lib.prophet import *

app = FastAPI()


class Input(BaseModel):
    data_path: str
    periods: int
    model: str


@app.get("/ping")
def pong():
    return {"ping": "pong"}


@app.post("/predict")
def forecast(input: Input):
    data_path = input.data_path
    df = preprocess(data_path)

    if input.model == "Prophet":
        prediction_list = predict_prophet(df, input.periods)
    elif input.model == "Arima":
        prediction_list = predict_sarima(df, input.periods)
    else:
        raise HTTPException(
            status_code=400, detail="Invalid model provided as input!")

    if not prediction_list:
        raise HTTPException(status_code=400, detail="Error in model!")

    response_object = {"data_path": input.data_path, "periods": input.periods,
                       "model": input.model, "forecasts": prediction_list}
    return response_object
