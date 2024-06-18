include .env

start:
	uvicorn src.main:app --reload

black:
	black migrations src

redis:
	redis-cli --pass ${REDIS_PASS}

migrate:
	sh ./scripts/migrate_db.sh "$(text)"

upgrade:
	#sh ./scripts/upgrade_db.sh "$(hash)"
	alembic upgrade head