from typing import List

from flair.data import Sentence
from flair.models import TextClassifier


class EquipmentModel:
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

