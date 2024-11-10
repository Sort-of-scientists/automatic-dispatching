from fastapi import FastAPI, Query
from typing import List, Optional

from pydantic import BaseModel

from pymongo import MongoClient


client = MongoClient("mongodb://mongodb:27017/")

database = client["database"]
collection = database["messages"]


class Message(BaseModel):
    text: str
    failure: str
    equipment: str
    number: str


app = FastAPI()


@app.get("/")
def read_root():
    return {}


@app.post("/insert")
def insert_messages(message: Message):
    collection.insert_one(document=message.model_dump())
    
    return "OK!"


@app.get("/numbers")
def get_all_numbers() -> List[str]:
    curs = collection.find({})

    return [item["number"] for item in curs]


@app.get("/message")
def get_message_by_number(number: str) -> Message:
    curs = collection.find({"number": number})

    return Message(**[item for item in curs][0])


@app.get("/filter", response_model=List[Message])
def get_messages(equipment: Optional[str] = Query(None), failure: Optional[str] = Query(None)) -> List[Message]:
    query = {}
    if equipment:
        query["equipment"] = equipment
    if failure:
        query["failure"] = failure

    cursor = collection.find(query)
    
    results = [Message(**doc) for doc in cursor]
    return results

    