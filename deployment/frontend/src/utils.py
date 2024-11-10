import json
import requests

from typing import Dict, List

from .constants import *

def send_request_to_models_backend(text: str) -> Dict[str, Dict]:
    response = {}

    for model in ENDPOINTS.keys():
        if model != "database" and model != "multilabel":
            response[model] = requests.post(
                url=ENDPOINTS[model], json=[text]
            )

            response[model] = json.loads(response[model].text)[0]

    return response


def insert_message_to_database(text: str, failure: str, failure_score: float, equipment: str, equipment_score: float, number: str):
    response = requests.post(url=ENDPOINTS["database"]["insert"], json={
        "text": text, "failure": failure, "equipment": equipment, "number": number,
        "failure_score": failure_score, "equipment_score": equipment_score
    })

    return response.status_code


def list_numbers():
    response = requests.get(url=ENDPOINTS["database"]["numbers"])

    return json.loads(response.text)


def get_message_by_number(number: str):
    response = requests.get(url=ENDPOINTS["database"]["message"], params={"number": number})

    return json.loads(response.text)


def get_messages(equipment: str, failure: str):
    if equipment == "Все":
        equipment = None

    if failure == "Все":
        failure = None
    
    response = requests.get(url=ENDPOINTS["database"]["filter"], params={
        "equipment": equipment, "failure": failure
    })

    return json.loads(response.text)


def send_request_to_multilabel_model(text: str) -> List[Dict[str, float]]:
    response = requests.post(
        url=ENDPOINTS["multilabel"], json=[text]
    )

    return json.loads(response.text)[0]