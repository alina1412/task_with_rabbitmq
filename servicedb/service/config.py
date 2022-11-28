from os import environ

from dotenv import find_dotenv, load_dotenv

path = find_dotenv()
load_dotenv(path, verbose=True)


username = environ.get("RABBITMQ_USERNAME")
password = environ.get("RABBITMQ_PASSWORD")
