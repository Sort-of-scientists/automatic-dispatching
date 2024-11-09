import re
import yaml
import spacy

from typing import List
from flashtext import KeywordProcessor


MODEL = 'ru_core_news_sm'


class EquipmentModel:
    """
    Модель для определения типа устройства.
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
        Возвращает список типов устройств.

        Parameters
        ----------
        texts : List[str]

        Returns
        -------
        List[str]

        """
        return ["string"]


class TrieEquipmentModel(EquipmentModel):

    def __init__(self, path: str) -> None:
        self.keyword_processor = KeywordProcessor()
        with open(path, 'r') as stream:
            types_dict = yaml.safe_load(stream)
        self.keyword_processor.add_keywords_from_dict(types_dict)

        self.nlp = spacy.load(MODEL)
        self.notebook_regex = re.compile(r'((HK|НК)(\d{1,})?(-\d{4})?)')
        self.disk_regex = r'(dd.?\d{3,})'

    def predict(self, texts: List[str]) -> List[str]:
        lemmas = self._prepare_data(texts)

        keywords = [self.keyword_processor.extract_keywords(text) for text in lemmas]
        predict_type = [x[0] if len(x) > 0 else None for x in keywords]
        notebooks = ['Ноутбук' if len(re.findall(self.notebook_regex, text)) > 0 else None for text in texts]
        disks = ['СХД' if len(re.findall(self.disk_regex, text)) > 0 else None for text in texts]

        predicts = []
        for i in range(len(texts)):
            pred = notebooks[i] if notebooks[i] else predict_type[i]
            pred = pred if pred else disks[i]
            predicts.append(pred)

        return predicts

    def _prepare_data(self, texts):
        docs = self.nlp.pipe(texts)
        lemmas = [' '.join([word.lemma_ for word in doc]) for doc in docs]
        return lemmas
