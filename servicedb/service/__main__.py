"""сервис записи в базу данных: servicedb/"""

import logging

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from service.db.db_settings import get_session

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


if __name__ == "__main__":
    uvicorn.run("service.__main__:app", port=80, host="0.0.0.0", reload=True)
