prepare_env:
	touch env/.env && echo \
"\
# ===== BASE SETTINGS =====\n\
BASE_URL=http://localhost:8000\n\n\
# ===== DATABASE SETTINGS =====\n\
DATABASE_ENGINE=postgresql+asyncpg\n\
DATABASE_HOST=${DB_HOST}\n\
DATABASE_PORT=${DB_PORT}\n\
DATABASE_NAME=${DB_NAME}\n\
DATABASE_USER=${DB_USER}\n\
DATABASE_PASSWORD=${DB_PASSWORD}\
" > env/.env

	touch env/.env.db && echo \
"\
POSTGRES_DB=${DB_NAME}\n\
POSTGRES_USER=${DB_USER}\n\
POSTGRES_PASSWORD=${DB_PASSWORD}\
" > env/.env.db

poetry_setup:
	poetry config virtualenvs.in-project true
	poetry shell
	poetry install

fastapi_run:
	alembic upgrade head
	uvicorn app.main:app --reload

#run_linters:
#	pre-commit install
#	pre-commit run --all-files

tests_coverage:
	coverage run -m pytest
	coverage html

docker_run:
	docker-compose -f docker-compose.yaml up -d --build

docker_stop:
	docker-compose -f docker-compose.yaml down -v
