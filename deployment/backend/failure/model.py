from typing import List
from flair.data import Sentence

from nn import FailureModel


class PredictionInfo:
    """
    Class with prediction info (label, score)

    ex.:
    label = "Диск"
    score = "0.8713"
    """
    def __init__(self, sentence: Sentence):
        self.label: str = sentence.tag
        self.score: float = sentence.score


# model = FailureModel('final-model.pt')
model = None


def predict_labels(texts: List[str]) -> List[PredictionInfo]:
    """
    Predicting labels for user message and getting scores for each label

    :param texts: user's messages to classify
    :return List[PredictionInfo]: predicted label and score for each message
    """
    sentences = model.predict(texts, batch_size=8)
    return [PredictionInfo(sentence) for sentence in sentences]
