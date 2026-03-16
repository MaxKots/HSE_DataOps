# переменные окружения из .env

include .env
export

# Переменные
MIGRATIONS_DIR = ./migrations
DB_URI = postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(POSTGRES_HOST):$(POSTGRES_PORT)/$(POSTGRES_DB)

# Зависимости
.PHONY: dev.install
dev.install:
	python -m venv .venv || true
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "✅  Зависимости установлены. Активируйте окружение: source .venv/bin/activate"

# Миграции

# Создание новой миграции.
# Использование: make db.migration.new name="users: create table"
.PHONY: db.migration.new
db.migration.new:
	yoyo new --database "$(DB_URI)" --sql -m "$(name)" $(MIGRATIONS_DIR)

# Применение всех неприменённых миграций
.PHONY: db.migrate
db.migrate:
	yoyo apply --database "$(DB_URI)" $(MIGRATIONS_DIR) --batch

# Откат последней применённой миграции
.PHONY: db.rollback
db.rollback:
	yoyo rollback --database "$(DB_URI)" $(MIGRATIONS_DIR) --batch

# Поднять БД
.PHONY: db.up
db.up:
	docker compose up -d db
	@echo "Ожидание готовности PostgreSQL"
	@until docker compose exec db pg_isready -U $(POSTGRES_USER) -d $(POSTGRES_DB) > /dev/null 2>&1; do \
		sleep 1; \
	done
	@echo "PostgreSQL готов к работе."

# Остановить БД
.PHONY: db.down
db.down:
	docker compose down

# Подключение psql-клиентом
.PHONY: db.psql
db.psql:
	docker compose exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)]
sources = ./migrations
; Строка подключения берётся из переменной окружения или подставляется через Makefile
database = %(DATABASE_URL)s
batch_mode = on
verbosity = 3