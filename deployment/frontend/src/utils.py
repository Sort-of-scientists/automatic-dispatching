import json
import requests

from typing import Dict

from .constants import *

def send_request_to_models_backend(text: str) -> Dict[str, Dict]:
    response = {}

    for model in ENDPOINTS.keys():
        if model != "database":
            response[model] = requests.post(
                url=ENDPOINTS[model], json=[text]
            )

            response[model] = json.loads(response[model].text)[0]

    return response


def insert_message_to_database(text: str, failure: str, equipment: str, number: str):
    response = requests.post(url=ENDPOINTS["database"]["insert"], json={
        "text": text, "failure": failure, "equipment": equipment, "number": number
    })

    return response.status_code


def list_numbers():
    response = requests.get(url=ENDPOINTS["database"]["numbers"])

    return json.loads(response.text)


def get_message_by_number(number: str):
    response = requests.get(url=ENDPOINTS["database"]["message"], params={"number": number})

    return json.loads(response.text)


def get_messages(equipment: str, failure: str):
    response = requests.get(url=ENDPOINTS["database"]["filter"], params={
        "equipment": equipment, "failure": failure
    })

    return json.loads(response.text)