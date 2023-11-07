#!/bin/bash
sleep 5

echo "Run alembic migration ..."

alembic_result=$(alembic upgrade head)
echo "Migration result: $alembic_result"
