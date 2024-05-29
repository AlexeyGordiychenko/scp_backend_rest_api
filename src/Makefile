define COMPOSE_CMD
	cat docker-compose-base.yml docker-compose-$1.yml | docker-compose -f -
endef

COMPOSE_CMD_DEV := $(call COMPOSE_CMD,dev)
COMPOSE_CMD_TEST := $(call COMPOSE_CMD,test)

run-dev:
	$(COMPOSE_CMD_DEV) --profile dev up -d

run-dev-postgres:
	$(COMPOSE_CMD_DEV) --profile dev up -d postgres-dev

build-dev:
	$(COMPOSE_CMD_DEV) --profile dev up -d --build

stop-dev:
	$(COMPOSE_CMD_DEV) down

restart-dev: stop-dev run-dev

clear-dev:
	$(COMPOSE_CMD_DEV) --profile dev down --volumes

run-test:
	$(COMPOSE_CMD_TEST) run --rm app-test
	$(COMPOSE_CMD_TEST) down

generate-migration:
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

migrate:
	alembic upgrade head

rollback:
	alembic downgrade -1
