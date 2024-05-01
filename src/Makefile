YML_FILE = db/docker-compose.yml
start:
	docker-compose -f $(YML_FILE) up -d
stop:
	docker-compose -f $(YML_FILE) down --volumes
rebuild:
	docker-compose -f $(YML_FILE) up -d --build shop_db
