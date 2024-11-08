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