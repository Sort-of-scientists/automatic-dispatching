import random

from fastapi import FastAPI
from typing import List

from pydantic import BaseModel

class Prediction(BaseModel):
    label: str
    score: float

app = FastAPI()


@app.get("/")
def read_root():
    return {}


@app.post("/predict")
def predict(texts: List[str]) -> List[Prediction]:
    return [Prediction(label="Ноутбук", score=random.uniform(0, 1)) for _ in range(len(texts))]

