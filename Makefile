all: build up

pull:
	docker-compose pull

push:
	docker-compose push

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	docker-compose run --rm --no-deps --volume=${PWD}/src:/src app bash -c '/wait && alembic upgrade head'

downgrade:
	docker-compose run --rm --no-deps --volume=${PWD}/src:/src app bash -c '/wait && alembic downgrade -1'

#createsuperuser:
#	docker-compose run app bash -c '/wait && python manage.py createsuperuser'

makemigrations:
	docker-compose run --rm --no-deps --volume=${PWD}/src:/src app bash -c '/wait && alembic revision --autogenerate -m $n'
	sudo chown -R ${USER} src/app/migrations/versions

psql:
	docker exec -it wal-g-PerFarm-db psql -U postgres

dev:
	docker-compose up

dev_test:
	docker-compose run --volume=${shell pwd}/src:/src app bash -c '/wait && pytest'

#shell:
#	docker-compose run app python manage.py shell

test:
	docker-compose run app pytest

precommit-install:
	pip install pre-commit
	pre-commit install

lint:
	pre-commit run --all-files

isort:
	docker-compose run --rm --no-deps app isort --check --diff .

flake8:
	docker-compose run --rm --no-deps app flake8 --config setup.cfg

black:
	docker-compose run --rm --no-deps app black --check --config pyproject.toml .

docker_lint:
	make isort
	make black
	make flake8

.PHONY: all build up down migrate makemigrations dev psql celery celerybeat dev_test update_or_create_user_groups update_roles vacation test debug dotenv precommit-install
