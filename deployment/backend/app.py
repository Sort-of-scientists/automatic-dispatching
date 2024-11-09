import os
import dvc.api

from fastapi import FastAPI
from typing import List

from src.models import FailureModel, EquipmentModel, NumberModel
from src.models import TrieEquipmentModel, TrieFailureModel, RegexNumberModel


app = FastAPI()


failure_model = TrieFailureModel("src/models/trie_failure.yaml")
equipment_model = TrieEquipmentModel("src/models/trie_equipment.yaml")
number_model = RegexNumberModel("")



@app.get("/")
def read_root():
    return {"hello": "world"}


@app.post("/equipment")
def predict_equipment(texts: List[str]):
    return equipment_model.predict(texts)


@app.post("/failure")
def predict_failure(texts: List[str]):
    return failure_model.predict(texts)


@app.post("/number")
def predict_number(texts: List[str]):
    return number_model.predict(texts)
