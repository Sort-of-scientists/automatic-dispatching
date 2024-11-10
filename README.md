# Решение команды "Своего рода ученые" для хакатона от Цифрового прорыва

## Варианты взаимодействия с решением
1. Удаленно. Наше решение развернуто на YandexCloud: http://51.250.78.146:8004/
2. Локально. Инструкция по установке:

   1. Убедитесь, что у вас установлен `docker` и `docker-compose`.
   2. Выполните команду `docker-compose up --build`
   3. Откройте в браузере UI http://0.0.0.0:8004

## Описание решения
Наше решение представляет собой две части - backend и frontend

### Backend методы
Cостоит из 5 микросервисов и одной MongoDB:
#### database
Первый микросервис, отвечающий за взаимодействие с MongoDB <br>
`port` - 8001

#### Вставка нового обращения в базу
**Method**: `POST` <br>
**Request body**: 
```
{
  "text": "string",
  "failure": "string",
  "failure_score": 0,
  "equipment": "string",
  "equipment_score": 0,
  "number": "string",
  "timestamp": "2024-11-10T03:54:37.906Z"
}
```
**Response**:
```
OK!
```
#### Получение всех серийных номеров
**Method**: `GET` <br>
**Response**:
```
["string"]
```

#### Получение обращения по серийному номеру
**Method**: `GET` <br>
**Query-params**:
- `number`: string <br>
**Response**:
```
{
  "text": "string",
  "failure": "string",
  "failure_score": 0,
  "equipment": "string",
  "equipment_score": 0,
  "number": "string",
  "timestamp": "2024-11-10T03:54:37.906Z"
}
```

#### Фильтрация обращений по Типу устройства и Точке отказа
**Method**: `GET` <br>
**Query-params**:
- `equipment`: string - Тип устройства
- `failure`: string - Точка отказа <br>
**Response**:
```
[
  {
    "text": "string",
    "failure": "string",
    "failure_score": 0,
    "equipment": "string",
    "equipment_score": 0,
    "number": "string",
    "timestamp": "2024-11-10T04:02:32.543Z"
  }
]
```

#### equipment, failure, numbers
Микросервисы для моделей прогноза оборудования, точки отказа и серийного номера соответсвенно.
`port` - 8001, 8002, 8003 соответсвенно

**Method**: `POST` <br>
**Request body**:
```
[
  "string"
]
```
**Response**:
```
[
  {
    "label": "string",
    "score": 0
  }
]
```

#### multilabel
Микросервис модели для мультиклассовой классификации

`port` - 8006

**Method**: `POST` <br>
**Request body**:
```
[
  "string"
]
```
**Response**:
```
[
  [
    {
      "label": "string",
      "score": 0
    }
  ]
]
```
