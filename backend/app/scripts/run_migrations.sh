#!/bin/bash

echo "Run alembic migration ..."

alembic_result=$(alembic upgrade head)
echo "Migration result: $alembic_result"
