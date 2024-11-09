ENDPOINTS = {
    "equipment": "http://equipment:8000/predict",
    "failure": "http://failure:8000/predict",
    "numbers": "http://numbers:8000/predict",
}

THRESHOLDS = {
    "equipment": 0.8,
    "failure": 0.8,
    "numbers": 1.0,
}

ALERT_DELAY = 1.2