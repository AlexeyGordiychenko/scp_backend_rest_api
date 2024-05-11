run-dev:
	docker-compose -f docker-compose.yml --profile dev up -d

build-dev:
	docker-compose -f docker-compose.yml --profile dev up -d --build

stop-dev:
	docker-compose -f docker-compose.yml --profile dev down

restart-dev: stop-dev run-dev

clear-dev:
	docker-compose -f docker-compose.yml --profile dev down --volumes

generate-migration:
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

migrate:
	alembic upgrade head

rollback:
	alembic downgrade -1
