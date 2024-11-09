import requests
import json

from typing import Dict

MODELS_ENDPOINT = "http://backend:8000/"


def make_request(text: str) -> Dict[str, str]:
    """
    Возвращает ответ от 3 моделей.
    """

    response = {}

    for route in ["failure", "equipment", "number"]:
        response[route] = json.loads(
            requests.post(
                url=MODELS_ENDPOINT + route, json=[text]
            ).text
        )[0]

    return response