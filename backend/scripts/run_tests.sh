#!/bin/bash

echo "Running pytest tests ..."
coverage run --source app -m pytest

# Check the result of the tests
pytest_result=$?
if [ $pytest_result -eq 0 ]; then
    echo "Tests passed successfully."
else
    echo "Tests failed with error code: $pytest_result"
    exit $pytest_result
fi

# Generate a coverage report and display a success message
coverage html
echo "Coverage report generated successfully."
