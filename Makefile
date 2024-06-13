start:
	uvicorn src.app.main:app --reload

black:
	black src/app
