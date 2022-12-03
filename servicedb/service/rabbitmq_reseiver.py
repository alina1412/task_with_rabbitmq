#!/usr/bin/env python
import json
import logging

import aio_pika
import databases
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from service.config import password, username  # isort: skip
from service.db.db_settings import async_database_uri  # isort: skip
from service.models import user_data  # isort: skip

logger = logging.getLogger(__name__)


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


async def rabbitmq_fetching(channel_pool) -> None:
    """consume messages from rabbitmq and send it to db"""
    async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
        await channel.set_qos(10)

        queue = await channel.declare_queue(
            QUEUE,
            durable=True,
            auto_delete=False,
        )

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                body = message.body.decode("utf-8")
                body = json.loads(body)
                print(body)
                await process_message(body)
                await message.ack()
                print("consumed")
                logger.info("consumed")


async def from_que_to_db(loop) -> None:
    """create connection to rabbitmq, start process of receiving and sending data to db"""

    async def get_connection() -> AbstractRobustConnection:
        return await aio_pika.connect_robust(
            host="rabbitmq", login=username, password=password, port=5672, loop=loop
        )

    connection_pool: Pool = Pool(get_connection, max_size=2, loop=loop)

    async def get_channel() -> aio_pika.Channel:
        async with connection_pool.acquire() as connection:
            return await connection.channel()

    channel_pool: Pool = Pool(get_channel, max_size=10, loop=loop)

    try:
        await rabbitmq_fetching(channel_pool)
    except KeyboardInterrupt:
        channel_pool.close()
        connection_pool.close()
        logger.info("closed connection")
