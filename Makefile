include .env

check: black test

start:
	uvicorn src.main:app --reload

black:
	black migrations src tests

celery:
	celery -A src.tasks.tasks:celery worker --loglevel=INFO

celery-web:
	celery -A src.tasks.tasks:celery flower

redis:
	redis-cli --pass ${REDIS_PASS}

migrate:
	sh ./scripts/migrate_db.sh "$(text)"

upgrade:
	#sh ./scripts/upgrade_db.sh "$(hash)"
	alembic upgrade head

test:
	pytest -v -s tests

rebuild:
	docker compose build && docker compose up