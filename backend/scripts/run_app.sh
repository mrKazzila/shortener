#!/bin/bash

# just for log
current_dir=$(pwd)
echo "Current dir: $current_dir"

# Check the value of the MODE variable and start the corresponding server
case "$MODE" in
    "DEV")
        echo "Running uvicorn in DEV mode"
        uvicorn app.main:app --reload --host 0.0.0.0 \
            --port 8000 --log-config ./app/settings/logger_config.yaml
        ;;
    "PROD")
        echo "Running gunicorn in PROD mode"
        gunicorn app.main:app --worker-class \
            uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
        ;;
    *)
        echo "Unknown mode: $MODE. Please set MODE to DEV or PROD."
        exit 1
        ;;
esac
