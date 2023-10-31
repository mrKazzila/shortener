# ===== Base variables =====
PROJECT_NAME = shortener_project
DC = docker-compose

BACK_DC_FILE = infra/backend/docker-compose.yaml
BACK_ENV_FILE = backend/env/.env

FRONT_DC_FILE = infra/frontend/docker-compose.yaml
FRONT_ENV_FILE = frontend/.env

# ===== Local docker automation =====
docker_run_back:
	${DC} --env-file ${BACK_ENV_FILE} -p ${PROJECT_NAME} -f ${BACK_DC_FILE} up -d --build

docker_stop_back:
	${DC} -f ${BACK_DC_FILE} down -v


# ===== Local docker automation =====
docker_run_front:
	${DC} --env-file ${FRONT_ENV_FILE} -p ${PROJECT_NAME} -f ${FRONT_DC_FILE} up -d --build

docker_stop_front:
	${DC} -f ${FRONT_DC_FILE} down -v


# ===== All services =====
docker_setup_all: docker_run_back docker_run_front

docker_stop_all: docker_stop_back docker_stop_front
