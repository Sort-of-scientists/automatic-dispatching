import os
import dvc.api

from fastapi import FastAPI
from typing import List

from src.models import FailureModel, EquipmentModel, NumberModel


app = FastAPI()


failure_model = FailureModel()
equipment_model = EquipmentModel()
number_model = NumberModel()



@app.get("/")
def read_root():
    return {"service_name": "serial-number"}


@app.post("/equipment")
def predict_equipment(texts: List[str]):
    return equipment_model.predict(texts)


@app.post("/failure")
def predict_failure(texts: List[str]):
    return failure_model.predict(texts)


@app.post("/number")
def predict_number(texts: List[str]):
    return number_model.predict(texts)