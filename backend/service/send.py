#!/usr/bin/env python

import logging

import pika
from service.config import password, username

logger = logging.getLogger(__name__)

credentials = pika.PlainCredentials(username=username, password=password)

parameters = pika.ConnectionParameters(
    host="rabbitmq",
    credentials=credentials,
    virtual_host="amqp",
    port=5672,
)
queue_name = "task_queue"


def send_to_que(message: str = '{"check": "check"}') -> None:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
        ),
    )
    logger.info("Sent ")
    connection.close()


if __name__ == "__main__":
    send_to_que()
