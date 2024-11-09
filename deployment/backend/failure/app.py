from fastapi import FastAPI
from typing import List

from pydantic import BaseModel

from transformers import pipeline


class Prediction(BaseModel):
    label: str
    score: float
    

class TextClassifier:
    def __init__(self, model_path: str, tokenizer_path: str):
        self.classifier = pipeline("text-classification", model=model_path, tokenizer=tokenizer_path)

    def predict(self, texts: List[str]) -> List[str]:
        return self.classifier(texts)


app = FastAPI()
text_classifier = TextClassifier(model_path="./text_classifier_failure", tokenizer_path="./text_classifier_failure")


@app.get("/")
def read_root():
    return {}


@app.post("/predict")
def predict(texts: List[str]) -> List[Prediction]:
    predictions = text_classifier.predict(texts)    
    return [Prediction(label=pred["label"], score=pred["score"]) for pred in predictions]
