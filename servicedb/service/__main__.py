"""fastapi service to write to db: servicedb/"""

import asyncio
import logging

import uvicorn
from fastapi import Depends, FastAPI, Query
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from service.db.db_settings import get_session  # isort: skip
from service.rabbitmq_reseiver import from_que_to_db  # isort: skip
from service.models import user_data  # isort: skip

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
    (await session.execute(query)).all()
    return {"success": "Yes"}


@app.get("/getdata")
async def get_data(
    perpage: int = Query(10, description="results per page"),
    offset: int = Query(0, description="skip first N results"),
    session: AsyncSession = Depends(get_session),
):
    """get data from db with pagination"""
    query = (
        select(
            [
                user_data.c.name,
                user_data.c.surname,
                user_data.c.patronymic,
                user_data.c.phone,
                user_data.c.text,
            ]
        )
        .order_by("id")
        .limit(perpage)
        .offset(offset)
    )
    res = (await session.execute(query)).fetchall()
    answer = []
    for feedback in list(res):
        answer.append(
            {
                "name": feedback[0],
                "surname": feedback[1],
                "patronymic": feedback[2],
                "phone": feedback[3],
                "text": feedback[4],
            }
        )
    return JSONResponse(content=jsonable_encoder(answer))


@app.on_event("startup")
async def app_startup():
    """run receive from rabbitmq"""
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(from_que_to_db(loop))


if __name__ == "__main__":
    uvicorn.run("service.__main__:app", port=80, host="0.0.0.0", reload=True)
