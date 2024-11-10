import re

from fastapi import FastAPI
from typing import List

from pydantic import BaseModel


class Prediction(BaseModel):
    label: str
    score: float


class RegexNumberModel:

    def __init__(self) -> None:
        self.serial_number_regex = re.compile(r'([A-ZА-Я]{1,3}\d{7,15})')
        self.mapper = {
            'А': 'A',
            'В': 'B',
            'Е': 'E',
            'З': 'Z',
            'К': 'K',
            'М': 'M',
            'Н': 'H',
            'О': 'O',
            'Р': 'P',
            'С': 'C',
            'Т': 'T',
            'У': 'Y',
            'Х': 'X'
        }

    def predict(self, texts: List[str]) -> List[str]:
        predicts = [re.findall(self.serial_number_regex, text.upper()) for text in texts]       
        upd_preds = []

        for p in predicts:
            p = p[0] if len(p) > 0 else 'Уточнить'
            if p != 'Уточнить':
                p = self._replace(p)
            upd_preds.append(p)

        return upd_preds

    def _replace(self, predict):
        for key in self.mapper.keys():
            predict = predict.replace(key, self.mapper[key])
        return predict


app = FastAPI()


@app.get("/")
def read_root():
    return {}


@app.post("/predict")
def predict(texts: List[str]) -> List[Prediction]:
    model = RegexNumberModel()
    predicts = model.predict(texts)
    return [Prediction(label=number, score=1. if number != 'Уточнить' else 0.) for number in predicts]
