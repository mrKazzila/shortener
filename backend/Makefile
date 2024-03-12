# ===== Base variables =====
PROJECT_NAME = shortener_url
DC = docker-compose

DC_FILE = docker-compose.yaml
ENV_FILE = env/.env

# ===== Docker automation =====
up:
	@echo "Run the bli db Docker container ..."
	${DC} --env-file ${ENV_FILE} -p ${PROJECT_NAME} -f ${DC_FILE} up -d --build
	@echo "Success up!"

down:
	@echo "Stop the bli db Docker container ..."
	${DC} --env-file ${ENV_FILE} -p ${PROJECT_NAME} -f ${DC_FILE} down
	@echo "Success down!"


# ===== Setup automation =====
poetry_setup:
	echo "Run poetry setup ..."
	poetry config virtualenvs.in-project true
	poetry shell
	poetry install
	echo "Poetry setup done!"

# ===== Linters & Formatter automation =====
lint:
	echo "Start linters ..."
	-black app/ --quiet
	-ruff check app/ --silent --fix
	-isort app
	echo "Linters done!"
