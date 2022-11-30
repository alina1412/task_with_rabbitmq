### Task with rabbitmq

in the process

## Description
Project provides take feedback from users (frontend form), process it and save to database.

Create 5 docker containers.

> Frontend -> Backend -> Rabbitmq -> Saving-to-db-service -> db

 Frontend gets feedback from users, sends it to backend, which validates it and sends to rabbitmq. Next service retrieves it from rabbitmq and sends data to db.

## How to run locally
if running first time
- create virtual environment (poetry install)
- run `make build` command from Makefile
- run `make db-migrate` after all containers started (rabbitmq starts for quite long)
- check rabbitmq locally by http://localhost:15672 with username and password from .env
- check frontend locally by http://localhost:8080/
- check db by connecting to it with data from .env



## Tools used
- rabbitmq
- tornado
- fastapi
- docker-compose
- postgres db
- alembic
- poetry
- pydantic
- javascript, html
- asyncio
