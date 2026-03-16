# Инструкция

## 1. виртуальное окружение и зависимости
make dev.install
source .venv/bin/activate

## 2. Поднятие PostgreSQL в Docker
make db.up

## 3. выполнение миграций
make db.migrate

## 4. Откат последней миграции
make db.rollback

## 5. выполнение снова
make db.migrate

## 6. Проверка результата через psql
make db.psql


## Скриншоты:

![task_18](https://github.com/MaxKots/HSE_DataOps/tree/main/task_18/.assets/1.jpg)

![task_18](https://github.com/MaxKots/HSE_DataOps/tree/main/task_18/.assets/2.jpg)

![task_18](https://github.com/MaxKots/HSE_DataOps/tree/main/task_18/.assets/3.jpg)


