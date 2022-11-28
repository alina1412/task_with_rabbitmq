from sqlalchemy import Column, Integer, MetaData, String, Text
from sqlalchemy.orm import declarative_base

metadata = MetaData()
DeclarativeBase = declarative_base(metadata=metadata)


class UserData(DeclarativeBase):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    phone = Column(Integer, nullable=False)
    text = Column(Text, nullable=True)
