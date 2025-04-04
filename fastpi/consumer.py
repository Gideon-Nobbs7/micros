import pika, time, json, aio_pika, os
from db.models import Fare
from utils import get_db
from dotenv import load_dotenv
from pathlib import Path
# from decouple import config

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

load_dotenv()


url = os.getenv("AMQP_URL")


if url is None:
    url = os.environ.get("AMQP_URL")


def receiving_msg(msg):
    print("Getting message from broker")
    print(" [x] Received" + str(msg))
    # time.sleep(5)
    print("Receiving finished")
    return



async def callback(message: aio_pika.IncomingMessage):
    db = next(get_db())
    async with message.process():
        try:
            data = json.loads(message.body.decode("utf-8"))
            print("First data:", type(data))
            receiving_msg(data)

            if message.content_type == "new_fare":
                fare = Fare(
                    id=data['id'], 
                    location=data['location'], 
                    price=data['price'], 
                    difficulty=data['difficulty']
                )
                print(f"Type>>> {type(fare.id)}")
                db.add(fare)
                db.commit()
                db.refresh(fare)
            
            elif message.content_type == "fare_updated":
                fare = db.query(Fare).filter(Fare.id == data['id']).first()
                print(type(fare.id))
                fare.location = data['location']
                fare.price = data['price']
                fare.difficulty = data['difficulty']
                db.commit()
                db.refresh(fare)
            
            elif message.content_type == "fare_deleted":
                fare = db.query(Fare).filter(Fare.id == int(data)).first()
                if fare:
                    print(type(fare.id))
                    db.delete(fare)
                    db.commit()
                else:
                    print(f"Fare with ID {data['id']} does not exist")
        finally:
            db.close()




