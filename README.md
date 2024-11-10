# Решение команды "Своего рода ученые" для хакатона от Цифрового прорыва

## Варианты взаимодействия с решением
1. Удаленно. Наше решение развернуто на YandexCloud: http://51.250.78.146:8004/
2. Локально. Инструкция по установке:

   1. Убедитесь, что у вас установлен `docker` и `docker-compose`.
   2. Перейдите в папку deployments/: `cd deployments`
   3. Выполните команду `docker-compose up --build`
   4. Откройте в браузере UI http://0.0.0.0:8004

## Описание решения
Наше решение представляет собой две части - backend и frontend. Чтобы посмотреть тренировочный код, перейдите на ветку dev.

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
## Выгрузка артефактов
В нашем проекте мы использовали DVC для контроля версий данных и моделей. По этой причине в репозитории не лежат ни сами модели, ни сами данные. Если вам потребуется выгрузить модели, то воспользуйтесь этой инструкцией:

1. Установить DVC:
```
pip install dvc
pip install dvc-s3
```
3. Склонировать репозиторий:
```git clone https://github.com/vkimbris/automatic-dispatching.git```
4. Внутри репозитория настроить подключение к S3:
```
dvc remote modify --local storage access_key_id <access_key_id>
dvc remote modify --local storage secret_access_key <secret_access_key>
```
4. Выгрузить данные и модели
dvc pull

P.S для получения ```<access_key_id>``` и ```<secret_access_key>``` обратитесь к: tg - @kimbrisvv, @kkk145, @ospvval, @smaslennikova
