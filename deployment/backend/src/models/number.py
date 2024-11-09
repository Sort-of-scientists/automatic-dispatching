import re

from typing import List


class NumberModel:
    """
    Модель для определения серийного номера.
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
        Возвращает список серийных номеров.

        Parameters
        ----------
        texts : List[str]

        Returns
        -------
        List[str]

        """
        return ["string"]


class RegexNumberModel(NumberModel):

    def __init__(self, path: str) -> None:
        self.serial_number_regex = re.compile(r'([A-ZА-Я]{1,3}\d{7,15})')

    def predict(self, texts: List[str]) -> List[str]:
        predicts = [re.findall(self.serial_number_regex, text.upper()) for text in texts]
        predicts = [p[0] if len(p) > 0 else None for p in predicts]
        return predicts
