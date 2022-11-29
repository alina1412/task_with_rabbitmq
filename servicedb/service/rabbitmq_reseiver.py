#!/usr/bin/env python
import json
import logging

import databases
import pika

from service.config import password, username
from service.db.db_settings import async_database_uri
from service.models import user_data

logger = logging.getLogger(__name__)


credentials = pika.PlainCredentials(username=username, password=password)

parameters = pika.ConnectionParameters(
    host="rabbitmq",
    # host="localhost",
    credentials=credentials,
    virtual_host="amqp",
    port=5672,
)
queue_name = "task_queue"


async def prepare_dict(message) -> dict:
    """the phone has to be validated as digits before"""
    data = {}
    for key in ("name", "surname", "patronymic", "phone", "text"):
        val = message.get(key, None)
        if val == "":
            val = None
        data[key] = val
    data["phone"] = int(data["phone"])
    print(data)
    return data


async def insert_to_db(data: dict) -> None:
    try:
        database = databases.Database(async_database_uri())
        await database.connect()
        query = user_data.insert()
        await database.execute_many(query=query, values=[data])
        await database.disconnect()
        logger.info("inserted into db")
    except Exception as exc:
        logger.error(exc)
        logger.error("NOT inserted into db")


async def process_message(message):
    data = await prepare_dict(message)
    await insert_to_db(data)


async def rabbitmq_fetching(channel):
    try:
        for method_frame, properties, body in channel.consume(queue_name):
            message = body.decode("utf-8")
            message = json.loads(message)
            print(message)
            await process_message(message)
            # Acknowledge the message:
            channel.basic_ack(method_frame.delivery_tag)
            print("consumed")
            logger.info("consumed")
    except Exception as exc:
        # channel.close()
        # connection.close()
        raise exc


async def from_que_to_db() -> None:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    print(channel.is_open)
    logger.info(channel.is_open)

    while True:
        await rabbitmq_fetching(channel)
