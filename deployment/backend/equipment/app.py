from fastapi import FastAPI
from typing import List


app = FastAPI()


@app.get("/")
def read_root():
    return {}


@app.post("/predict")
def predict(texts: List[str]) -> List[str | None]:
    return ["string"]
