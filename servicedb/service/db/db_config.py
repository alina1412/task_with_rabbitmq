from os import environ

from dotenv import load_dotenv

load_dotenv(verbose=True)


class DBConfig:
    DATABASE_NAME: str = environ.get("DATABASE_NAME")
    DATABASE_USERNAME: str = environ.get("DATABASE_USERNAME")
    DATABASE_PASSWORD: str = environ.get("DATABASE_PASSWORD")
    POSTGRES_PORT: int = environ.get("POSTGRES_PORT")

    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", default="localhost")

    assert DATABASE_PASSWORD
