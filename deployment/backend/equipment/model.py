from typing import List

from flair.data import Sentence
from flair.models import TextClassifier


model = TextClassifier.load('model.pt')


class PredictionInfo:
    """
    Class with prediction info (label, score)

    ex.:
    label = "Сервер"
    score = "0.8713"
    """
    def __init__(self, sentence: Sentence):
        self.label: str = sentence.tag
        self.score: float = sentence.score


def predict_labels(texts: List[str]) -> List[PredictionInfo]:
    sentences = [Sentence(text) for text in texts]
    model.predict(sentences)
    return [PredictionInfo(sentence) for sentence in sentences]

