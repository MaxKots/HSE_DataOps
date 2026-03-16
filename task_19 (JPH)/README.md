# Инструкция

### 1. Собрать образ
docker-compose build

### 2. Запустить JupyterHub
docker-compose up -d

### 3. Посмотреть логи
docker-compose logs -f

### 4. Открыть браузер и перейти на http://localhost:8000. Все проверить и порадоваться

### 5. Остановить и удалить контейнеры, сети, тома
docker-compose down -v --remove-orphans

### 6. Удалить оставшиеся контейнеры
docker rm -f lakefs_postgres lakefs_minio lakefs_server jupyterhub_server 2>/dev/null


## Скриншоты:

![task_18](https://github.com/MaxKots/HSE_DataOps/blob/main/task_19/.assets/1.jpg)


