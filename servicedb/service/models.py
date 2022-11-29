from sqlalchemy import BigInteger, Column, MetaData, String, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

metadata = MetaData()
DeclarativeBase = declarative_base(metadata=metadata)


user_data = Table(
    "user_data",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("patronymic", String, nullable=True),
    Column("phone", BigInteger(), nullable=False),
    Column("text", Text, nullable=True),
)
