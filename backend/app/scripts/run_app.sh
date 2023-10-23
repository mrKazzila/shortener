#!/bin/bash

current_dir=$(pwd)
echo "Current dir: $current_dir"
echo "Run gunicorn"

gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
