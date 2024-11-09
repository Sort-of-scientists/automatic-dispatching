import yaml
import spacy

from typing import List
from flashtext import KeywordProcessor


MODEL = 'ru_core_news_sm'


class FailureModel:
    """
    Модель для определения точки отказа.
    """

    def __init__(self, path: str) -> None:
        """
        Инициалиирует модель.

        Parameters
        ----------
        path : str
            Путь до папки/файла с моделью.
        """

        pass

    def predict(self, texts: List[str]) -> List[str]:
        """
        Возвращает список точек отказа.

        Parameters
        ----------
        texts : List[str]

        Returns
        -------
        List[str]

        """
        return ["string"]


class TrieFailureModel(FailureModel):

    def __init__(self, path: str) -> None:
        self.keyword_processor = KeywordProcessor()
        with open(path, 'r') as stream:
            types_dict = yaml.safe_load(stream)
        self.keyword_processor.add_keywords_from_dict(types_dict)

        self.nlp = spacy.load(MODEL)

    def predict(self, texts: List[str]) -> List[str]:
        lemmas = self._prepare_data(texts)

        keywords = [self.keyword_processor.extract_keywords(text) for text in lemmas]
        predicts = [kw if kw else 'Материнская плата' for kw in keywords]

        return predicts

    def _prepare_data(self, texts):
        docs = self.nlp.pipe(texts)
        lemmas = [' '.join([word.lemma_ for word in doc]) for doc in docs]
        return lemmas
