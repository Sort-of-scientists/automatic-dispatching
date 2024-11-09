import random
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

from model import predict_labels


class Prediction(BaseModel):
    label: str
    score: float


app = FastAPI()


@app.get("/")
def read_root():
    return {}


@app.post("/predict")
def predict(texts: List[str]) -> List[Prediction]:
    return [Prediction(label=prediction.label, score=prediction.score)
            for prediction in predict_labels(texts)]

