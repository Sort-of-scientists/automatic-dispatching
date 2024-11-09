import re

from fastapi import FastAPI
from typing import List

from pydantic import BaseModel
from unidecode import unidecode


class Prediction(BaseModel):
    label: str
    score: float


class RegexNumberModel:

    def __init__(self) -> None:
        self.serial_number_regex = re.compile(r'([A-ZА-Я]{1,3}\d{7,15})')

    def predict(self, texts: List[str]) -> List[str]:
        predicts = [re.findall(self.serial_number_regex, text.upper()) for text in texts]
        predicts = [unidecode(p[0]) if len(p) > 0 else 'Уточнить' for p in predicts]
        return predicts


app = FastAPI()


@app.get("/")
def read_root():
    return {}


@app.post("/predict")
def predict(texts: List[str]) -> List[Prediction]:
    model = RegexNumberModel()
    predicts = model.predict(texts)
    return [Prediction(label=number, score=1. if number != 'Уточнить' else 0.) for number in predicts]
