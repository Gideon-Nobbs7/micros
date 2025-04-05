import logging
import time

import pika

# Set up logging to both console and file

def pdf_process_func(msg):
    print("PDF processing")
    print(" [x] Received: " + str(msg))
    time.sleep(5)
    print("PDF processing finished")


url = "amqps://jyzdcjde:XK-10u8Wiy8xM8gUWeNo_liUr0wSMsoe@rattlesnake.rmq.cloudamqp.com/jyzdcjde"
params = pika.URLParameters(url)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    pdf_process_func(body)

channel.basic_consume(
    queue='admin',
    on_message_callback=callback,
    auto_ack=True
)
print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()

connection.close()
