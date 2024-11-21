#!/usr/bin/env python
import json
import logging

import aio_pika
import databases
from aio_pika.abc import AbstractChannel, AbstractQueue

from service.config import password, username  # isort: skip
from service.db.db_settings import async_database_uri  # isort: skip
from service.models import user_data  # isort: skip

logger = logging.getLogger(__name__)


QUEUE = "task_queue"


def prepare_dict(message) -> dict:
    """The phone has to be validated as digits before"""
    data = {}
    for key in ("name", "surname", "patronymic", "phone", "text"):
        val = message.get(key, None)
        val = val if val else None
        data[key] = val
    data["phone"] = int(data["phone"])
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


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process(ignore_processed=True):
        encoded = message.body.decode("utf-8")
        encoded = json.loads(encoded)
        data = prepare_dict(encoded)
        await insert_to_db(data)
        await message.ack()
        # print("consumed")
        logger.info("consumed")


async def rabbitmq_fetching(channel: AbstractChannel) -> None:
    """Consume messages from rabbitmq and send it to db"""
    queue: AbstractQueue = await channel.declare_queue(
        QUEUE,
        durable=True,
        auto_delete=False,
    )
    await queue.consume(callback=process_message, no_ack=False)


async def from_que_to_db(loop) -> None:
    """Create connection to rabbitmq, start process
    of receiving and sending data to db
    """
    connection = await aio_pika.connect_robust(
        host="rabbitmq", login=username, password=password, port=5672, loop=loop
    )
    channel = await connection.channel()
    await channel.set_qos(1)
    try:
        await rabbitmq_fetching(channel)
    except KeyboardInterrupt:
        connection.close()
        logger.info("closed connection")
