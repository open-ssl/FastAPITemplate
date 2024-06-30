#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  poetry run celery --app=src.tasks.tasks:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  poetry run celery --app=src.tasks.tasks:celery flower
 fi
