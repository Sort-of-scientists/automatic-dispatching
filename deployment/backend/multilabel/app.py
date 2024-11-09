from fastapi import FastAPI
from typing import List

from pydantic import BaseModel

from transformers import pipeline


class Prediction(BaseModel):
    label: str
    score: float
    

class TextMultiLabelClassifier:
    def __init__(self, model_path: str, tokenizer_path: str, k: int):
        self.classifier = pipeline("text-classification", model=model_path, tokenizer=tokenizer_path, top_k=k)

    def predict(self, texts: List[str]) -> List[str]:
        return self.classifier(texts)
    
    
def filter_results(results):
    return [item for item in results if item['score'] > 0.3]


app = FastAPI()
text_classifier = TextMultiLabelClassifier(model_path="./model/multilabel_classifier_failure",
                                           tokenizer_path="./model/multilabel_classifier_failure", k=20)


@app.get("/")
def read_root():
    return {}


@app.post("/predict")
def predict(texts: List[str]) -> List[Prediction]:
    predictions = text_classifier.predict(texts)   
    filtered_predictions = [filter_results(pred) for pred in predictions] 
    return [[Prediction(label=pred["label"], score=pred["score"]) for pred in multilabel_list] for multilabel_list in filtered_predictions]
