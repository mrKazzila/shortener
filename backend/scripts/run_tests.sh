#!/bin/bash

echo "Run pytest tests ..."
coverage run --source app -m pytest && coverage html
