from typing import List

from flair.data import Sentence
from flair.models import TextClassifier


class FailureModel:
    """
    Initializing model and creating predict-method
    """
    def __init__(self, model_path):
        """
        :param model_path: path to our model location
        """
        self.model = TextClassifier.load(model_path)

    def predict(self, texts: List[str], batch_size=8) -> List[Sentence]:
        """

        :param texts: list of strings
        :param batch_size: how many sentences process at the same time
        :return: list of flair.Sentence, which have labels and scores for this labels
        """
        sentences = [Sentence(text) for text in texts]
        self.model.predict(sentences, mini_batch_size=batch_size)
        return sentences


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
