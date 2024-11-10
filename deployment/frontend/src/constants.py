ENDPOINTS = {
    "equipment": "http://equipment:8000/predict",
    "failure": "http://failure:8000/predict",
    "numbers": "http://numbers:8000/predict",

    "database": {
        "insert": "http://database:8000/insert",
        "numbers": "http://database:8000/numbers",
        "message": "http://database:8000/message",
        "filter": "http://database:8000/filter"
    }
}

THRESHOLDS = {
    "equipment": 0.8,
    "failure": 0.8,
    "numbers": 1.0,
}

ALERT_DELAY = 0.3

LABELS = {
    "equipment": ["Ноутбук", "СХД", "Сервер"],
    "failure": [
        'Блок питания', 
        'Материнская плата', 
        'Матрица', 
        'Вентилятор', 
        'Сервер', 
        'Wi-fi модуль', 
        'Диск', 
        'SFP модуль',
        'Оперативная память', 
        'Программное обеспечение', 
        'Клавиатура',
        'Корпус', 
        'Аккумулятор', 
        'Камера', 
        'Wi-fi антенна', 
        'Динамики',
        'Jack'
    ]
}