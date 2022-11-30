#!/usr/bin/env python
import asyncio
import json
import logging

import databases
import pika

from service.config import password, username  # isort: skip
from service.db.db_settings import async_database_uri  # isort: skip
from service.models import user_data  # isort: skip

logger = logging.getLogger(__name__)


credentials = pika.PlainCredentials(username=username, password=password)

parameters = pika.ConnectionParameters(
    host="rabbitmq",
    # host="localhost",
    credentials=credentials,
    # virtual_host="amqp",
    port=5672,
)
QUEUE = "task_queue"


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


async def process_message(message) -> None:
    data = await prepare_dict(message)
    await insert_to_db(data)


async def rabbitmq_fetching(channel) -> None:
    """getting one message from queue rabbitmq and sending it to db"""
    method_frame, header_frame, body = channel.basic_get(queue=QUEUE)
    if not method_frame:
        return
    body = body.decode("utf-8")
    body = json.loads(body)
    print(body)
    await process_message(body)
    channel.basic_ack(method_frame.delivery_tag)
    print("consumed")
    logger.info("consumed")


async def from_que_to_db() -> None:
    """create connection to rabbitmq, start process of receiving and sending data to db"""
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)
    print(channel.is_open)
    logger.info(channel.is_open)

    while True:
        try:
            await rabbitmq_fetching(channel)
            await asyncio.sleep(0.5)
        except KeyboardInterrupt:
            channel.close()
            connection.close()
            logger.info("closed connection")
