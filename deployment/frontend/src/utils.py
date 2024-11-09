import json
import requests

from typing import Dict

from .constants import *

def send_request_to_backend(text: str) -> Dict[str, Dict]:
    response = {}

    for model in ENDPOINTS.keys():
        response[model] = requests.post(
            url=ENDPOINTS[model], json=[text]
        )

        response[model] = json.loads(response[model].text)[0]

    return response