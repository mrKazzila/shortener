#!/bin/bash

sleep 5
echo "Running alembic migration ..."
alembic_result=$(alembic upgrade head)

# Check the result of Alembic execution
# shellcheck disable=SC2181
if [ $? -eq 0 ]; then
    echo "Migration completed successfully."
else
    echo "Migration failed with error: $alembic_result"
    exit 1
fi
