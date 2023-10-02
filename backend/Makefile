poetry_setup:
	poetry config virtualenvs.in-project true
	poetry shell
	poetry install

fastapi_run:
	alembic upgrade head
	uvicorn app.main:app --reload

tests_coverage:
	coverage run -m pytest
	coverage html

docker_run:
	docker-compose -f infra/docker/docker-compose.yaml up -d --build

docker_stop:
	docker-compose -f docker-compose.yaml down -v

run_formatters:
	black app/ --quiet
	ruff check app/ --silent --fix
	isort app/
