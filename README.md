### Task with rabbitmq


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

<img src="https://user-images.githubusercontent.com/8655093/204727512-c9aabd8b-af6c-4a4c-a422-efca3961d6a9.jpg" height="250"> </img>
<img src="https://user-images.githubusercontent.com/8655093/204727517-77437070-42cc-4b1d-bd0c-164f27badbe2.jpg" height="250"> </img>
<img src="https://user-images.githubusercontent.com/8655093/204727518-3c500b06-ea9d-4798-a17d-838a126836ef.jpg" height="250"> </img>
<img src="https://user-images.githubusercontent.com/8655093/204727520-d8979105-80c6-45e2-985c-962125f6dd34.jpg" height="250"> </img>


