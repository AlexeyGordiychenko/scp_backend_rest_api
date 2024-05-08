run-dev:
	docker-compose -f docker-compose.yml --profile dev up -d

build-dev:
	docker-compose -f docker-compose.yml --profile dev up -d --build

stop-dev:
	docker-compose -f docker-compose.yml --profile dev down

restart-dev: stop-dev run-dev

clear-dev:
	docker-compose -f docker-compose.yml --profile dev down --volumes