include .env
export

MIGRATIONS_DIR = ./migrations
DB_URI = postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(POSTGRES_HOST):$(POSTGRES_PORT)/$(POSTGRES_DB)

.PHONY: dev.install db.migration.new db.migrate db.rollback db.up db.down db.psql

dev.install:
	python3 -m venv .venv || true
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "Зависимости установлены. Активируйте: source .venv/bin/activate"

db.migration.new:
	yoyo new --database "$(DB_URI)" -m "$(name)" $(MIGRATIONS_DIR)

db.migrate:
	yoyo apply --database "$(DB_URI)" $(MIGRATIONS_DIR) --batch

db.rollback:
	yoyo rollback --database "$(DB_URI)" $(MIGRATIONS_DIR) --batch

db.up:
	docker-compose up -d db
	@echo "Ожидание готовности PostgreSQL..."
	@until docker-compose exec db pg_isready -U $(POSTGRES_USER) -d $(POSTGRES_DB) > /dev/null 2>&1; do sleep 1; done
	@echo "PostgreSQL готов."

db.down:
	docker-compose down

db.psql:
	docker-compose exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)
