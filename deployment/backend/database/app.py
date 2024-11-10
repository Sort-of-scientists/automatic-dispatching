from fastapi import FastAPI, Query
from typing import List, Optional

from pydantic import BaseModel, Field

from pymongo import MongoClient
from datetime import datetime


client = MongoClient("mongodb://mongodb:27017/")

database = client["database"]
collection = database["messages"]


class Message(BaseModel):
    text: str
    failure: str
    failure_score: float
    equipment: str
    equipment_score: float
    number: str
    timestamp: datetime = Field(default_factory=datetime.now)


app = FastAPI()


@app.get("/")
def read_root():
    return {}


@app.post("/insert")
def insert_messages(message: Message):
    collection.insert_one(document=message.model_dump() | {"timestamp": datetime.now()})
    
    return "OK!"


@app.get("/numbers")
def get_all_numbers() -> List[str]:
    curs = collection.find({})

    return [item["number"] for item in curs]


@app.get("/message")
def get_message_by_number(number: str) -> Message:
    curs = collection.find({"number": number})
    elem = [item for item in curs][0]

    return Message(
        text=elem["text"],
        failure=elem["failure"],
        failure_score=elem["failure_score"],
        equipment=elem["equipment"],
        equipment_score=elem["equipment_score"],
        number=elem["number"],
    )


@app.get("/filter", response_model=List[Message])
def get_messages(equipment: Optional[str] = Query(None), failure: Optional[str] = Query(None)) -> List[Message]:
    query = {}
    if equipment:
        query["equipment"] = equipment
    if failure:
        query["failure"] = failure

    cursor = collection.find(query).sort({ "timestamp": -1 })
    
    results = [
        Message(
            text=elem["text"],
            failure=elem["failure"],
            failure_score=elem["failure_score"],
            equipment=elem["equipment"],
            equipment_score=elem["equipment_score"],
            number=elem["number"],
        )

        for elem in cursor
    ]

    return results

    