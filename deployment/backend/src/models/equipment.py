from typing import List

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