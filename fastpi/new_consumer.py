import json
from os import getenv
from typing import Any, Dict

import aio_pika
from db.models import Fare
from dotenv import load_dotenv
from fastapi import HTTPException
from utils import get_db


load_dotenv()


url = getenv("AMQP_URL")


class Callback:
    def __init__(self):
        self.db = next(get_db())

    def receive_message(self, msg):
        self.msg = msg
        print("Getting message from broker")
        print(" [x] Received" + str(self.msg))
        # time.sleep(5)
        print("Receiving finished")
        return

    def create_fare(self, data: Dict[str, Any]):
        self.receive_message(data)
        fare = Fare(
            id=data["id"],
            location=data["location"],
            price=data["price"],
            difficulty=data["difficulty"],
        )
        self.db.add(fare)
        self.db.commit()
        self.db.refresh(fare)

    def update_fare(self, data: Dict[str, Any]):
        fare = self.db.query(Fare).filter(Fare.id == data["id"]).first()
        fare.location = data["location"]
        fare.price = data["price"]
        fare.difficulty = data["difficulty"]
        self.db.commit()
        self.db.refresh(fare)

    def delete_fare(self, data: int):
        fare = self.db.query(Fare).filter(Fare.id == int(data)).first()
        self.db.delete(fare)
        self.db.commit()

    async def process_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                data = json.loads(message.body.decode("utf-8"))
                self.receive_message(data)

                handlers = {
                    "new_fare": self.create_fare,
                    "fare_updated": self.update_fare,
                    "fare_deleted": self.delete_fare,
                }

                handler = handlers.get(message.content_type)
                if handler:
                    handler(data)
                else:
                    raise HTTPException(status_code=200)
            finally:
                self.db.close()
