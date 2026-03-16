.PHONY: build up down logs clean

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "JupyterHub доступен по адресу: http://localhost:8000"

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f

restart: down up
