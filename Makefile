build:
	docker-compose up --build

db-migrate:
	poetry run alembic -c alembic.ini upgrade head


# Dev
lint:
	poetry run isort backend servicedb
	poetry run black backend servicedb
	poetry run pylint backend servicedb

req:
	poetry export -f requirements.txt --without-hashes --without dev --output requirements.txt

# run in rabbitmq docker
status:
	rabbitmqctl cluster_status