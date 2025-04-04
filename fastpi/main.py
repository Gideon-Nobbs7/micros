from typing import List

import requests
import uvicorn
from .db import models
from .db.databaseConnect import engine
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .utils import get_db


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


# Response model
class FareSchema(BaseModel):
    id: int
    location: str
    price: int
    difficulty: str


class FarePlayerSchema(BaseModel):
    id: int
    user_id: int


# @app.on_event("startup")
# async def startup():
#     loop = asyncio.get_event_loop()
#     connection = await aio_pika.connect(url, loop=loop)
#     channel = await connection.channel()
#     queue = await channel.declare_queue("main")

#     async def process_message(message: aio_pika.IncomingMessage):
#         callback_handler = Callback()
#         await callback_handler.process_message(message)
#     await queue.consume(process_message)


@app.get("/")
async def start():
    return "Server is running"


@app.post("/api/products/{id}/like")
async def like(id: int):
    req = requests.get("http://localhost/api/user")
    return req


@app.get("/api/products", response_model=List[FareSchema])
async def index(db: Session = Depends(get_db)):
    fares = db.query(models.Fare).all()
    return fares


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
