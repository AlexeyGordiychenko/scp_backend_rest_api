run-dev:
	docker compose --profile dev up -d

run-dev-postgres:
	docker compose --profile dev up -d postgres-dev

build-dev:
	docker compose --profile dev build

build-test:
	docker compose --profile test build

stop-dev:
	docker compose --profile dev down

restart-dev: stop-dev run-dev

clear-dev:
	docker compose --profile dev down --volumes

run-test:
	docker compose run --rm -T app-test || true
	$(MAKE) check-test
	$(MAKE) stop-test

stop-test:
	docker compose --profile test down

check-test:
	docker compose exec postgres-test psql -U postgres -c "SELECT * FROM client;SELECT * FROM supplier;SELECT * FROM product;SELECT * FROM address;SELECT id, product_id, extension FROM image;"

generate-migration:
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

migrate:
	alembic upgrade head

rollback:
	alembic downgrade -1
