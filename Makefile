start:
	uvicorn src.main:app --reload

black:
	black migrations src

migrate:
	sh ./scripts/migrate_db.sh "$(text)"

upgrade:
	#sh ./scripts/upgrade_db.sh "$(hash)"
	alembic upgrade head