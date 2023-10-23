# ===== Base variables =====
DC = docker-compose
DC_FILE = infra/docker/docker-compose.yaml
ENV_FILE = env/.env
PROJECT_NAME = shortener_project

# ===== Setup automation =====
poetry_setup:
	echo "Run poetry setup ..."
	poetry config virtualenvs.in-project true
	poetry shell
	poetry install


# ===== Local docker automation =====
docker_run:
	${DC} --env-file ${ENV_FILE} -p ${PROJECT_NAME} -f ${DC_FILE} up -d --build

docker_stop:
	${DC} -f ${DC_FILE} down -v


# ===== Tests automation =====
test_coverage:
	echo "Run pytest with coverage ..."
	coverage run -m pytest
	coverage html


# ===== Linters & Formatter automation =====
lint:
	echo "Start linters ..."
	-black app/ --quiet
	-ruff check app/ --silent --fix
	-isort app
	echo "Linters done!"
