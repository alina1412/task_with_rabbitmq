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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    """ping service for debug"""
    return {"success": "Yes"}


@app.get("/pingdb")
async def pingdb(session: AsyncSession = Depends(get_session)):
    """ping db for debug"""
    query = "SELECT 1"
    await session.execute(query).all()
    return {"success": "Yes"}


@app.on_event("startup")
async def app_startup():
    """run receive from rabbitmq"""
    asyncio.create_task(from_que_to_db())


if __name__ == "__main__":
    uvicorn.run("service.__main__:app", port=80, host="0.0.0.0", reload=True)
