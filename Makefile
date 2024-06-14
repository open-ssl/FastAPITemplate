start:
	uvicorn src.app.main:app --reload

black:
	black auth config migrations src/app

migrate:
	sh ./scripts/migrate_db.sh "$(text)"

upgrade:
	#sh ./scripts/upgrade_db.sh "$(hash)"
	alembic upgrade head