FROM python:3.10-slim AS builder

WORKDIR /api

RUN pip install --no-cache-dir poetry
COPY pyproject.toml .
RUN poetry install --no-cache

COPY . .

RUN chmod a+x deployment/*.sh

CMD ["poetry", "run", "gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "src.main:app" ]
