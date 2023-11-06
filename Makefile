# ===== Base variables =====
PROJECT_NAME = shortener_project
DC = docker-compose

BACK_DC_FILE = infra/backend/docker-compose.yaml
BACK_ENV_FILE = backend/env/.env

TEST_BACK_DC_FILE = infra/backend/docker-compose-tests.yaml
TEST_BACK_ENV_FILE = backend/env/.env-test

FRONT_DC_FILE = infra/frontend/docker-compose.yaml
FRONT_ENV_FILE = frontend/.env

METRICS_DC_FILE = infra/metrics/docker-compose.yaml

# ===== Backend automation =====
docker_run_back:
	@echo "Run the backend Docker container..."
	${DC} --env-file ${BACK_ENV_FILE} -p ${PROJECT_NAME} -f ${BACK_DC_FILE} up -d --build

docker_stop_back:
	@echo "Stopping backend Docker containers..."
	${DC} -f ${BACK_DC_FILE} down

docker_run_tests_back:
	@echo "Run the tests for backend Docker container..."
	${DC} --env-file ${TEST_BACK_ENV_FILE} -p ${PROJECT_NAME} -f ${TEST_BACK_DC_FILE} up -d --build
	sleep 4
	@while ! docker inspect -f '{{.State.Status}}' TEST-shortener-api | grep -q 'exited'; do \
			echo "Waiting for TEST-shortener-api container to exit..."; \
			sleep 1; \
		done
		@echo "Container TEST-shortener-api exited, stopping and removing all containers..."
		${DC} --env-file ${TEST_BACK_ENV_FILE} -p ${PROJECT_NAME} -f ${TEST_BACK_DC_FILE} down


# ===== Frontend automation =====
docker_run_front:
	@echo "Run the frontend Docker container..."
	${DC} --env-file ${FRONT_ENV_FILE} -p ${PROJECT_NAME} -f ${FRONT_DC_FILE} up -d --build

docker_stop_front:
	@echo "Stopping frontend Docker container..."
	${DC} -f ${FRONT_DC_FILE} down


# ===== Metrics automation =====
docker_run_metrics:
	@echo "Run the metrics Docker container..."
	${DC} -p ${PROJECT_NAME} -f ${METRICS_DC_FILE} up -d --build


# ===== All services =====
docker_setup_all: docker_run_back docker_run_front docker_run_metrics

docker_stop_all: docker_stop_back docker_stop_front
