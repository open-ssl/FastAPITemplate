#!/bin/bash

if [ "$1" = "" ]; then
    echo "Please fill argument 'text'='REVISION COMMIT MESSAGE' for command. Now it is empty!"
else
    echo "Start to create revision"
    alembic revision --autogenerate -m "$1"
fi
