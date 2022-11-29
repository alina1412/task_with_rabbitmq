"""сервис записи в базу данных: servicedb/"""

import asyncio
import logging

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service.db.db_settings import get_session
from service.rabbitmq_reseiver import from_que_to_db
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


app = FastAPI()


origins = [
    # "http://localhost",
    # "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return {"success": "Yes"}


@app.get("/pingdb")
async def pingdb(session: AsyncSession = Depends(get_session)):
    # query = """SELECT id, name, surname, patronymic, phone, "text" FROM user_data;"""
    query = "SELECT 1"
    results = (await session.execute(query)).all()
    res = list(results)
    print(res)
    logger.info(res)
    return {"success": "1"}


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(from_que_to_db())
    await task


if __name__ == "__main__":
    uvicorn.run("service.__main__:app", port=80, host="0.0.0.0", reload=True)
