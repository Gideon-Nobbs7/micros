import json
import os

import pika
from dotenv import load_dotenv

load_dotenv()

def publish_to_queue(method, body):
    url = os.getenv("AMQP_URL")
    params = pika.URLParameters(url)
    params.socket_timeout = 2

    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue='main')

        properties = pika.BasicProperties(content_type=method)
        channel.basic_publish(
            exchange='',
            routing_key='main',
            body=json.dumps(body),
            properties=properties
        )
        print("[x] Message sent to broker/consumer")
    finally:
        connection.close()
