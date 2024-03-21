#!/bin/bash

current_dir=$(pwd)
echo "Current dir: $current_dir"

if [ "$MODE" == "DEV" ]; then
    echo "Running uvicorn in DEV mode"
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-config ./app/settings/logger_config.yaml

elif [ "$MODE" == "PROD" ]; then
    echo "Running gunicorn in PROD mode"
    gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

else
    echo "Unknown mode: $MODE. Please set MODE to DEV or PROD."
fi
