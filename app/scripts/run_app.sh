#!/bin/bash

current_dir=$(pwd)
echo "Current dir: $current_dir"

alembic_result=$(alembic upgrade head)
echo "Migration result: $alembic_result"


gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
