#!/bin/bash

if [ "$1" = "" ]; then
    echo "Please fill argument 'hash'='REVISION UPGRADE COMMIT HASH' for command. Now it is empty!"
else
    echo "Start to upgrade database"
    alembic upgrade $1
fi
