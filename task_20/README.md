# Инструкция

### 1. Создать и запустить базу данных
docker-compose up -d db

### Проверить, что бд запустилась
docker-compose ps
docker-compose logs db


### 2. Собрать образ MLflow
docker-compose build mlflow

### 3. Запустить MLflow сервер
docker-compose up -d mlflow

# Посмотреть логи
docker-compose logs -f mlflow

### 4. Открой http://localhost:5000

### 5. Создай эксперимент

    В интерфейсе MLflow нажми кнопку "Create Experiment"

    Копирни Experiment ID из адресной строки или из списка экспериментов


### 6. Как навеселился всласть:

### Останови и удалить контейнеры
docker-compose down

### Или останови, удали контейнеры и тома
docker-compose down -v

### Проверить, что контейнеры удалены
docker ps -a | grep mlflow

### Проверить, что тома удалены
docker volume ls | grep mlflow


## Скриншоты:

![task_18](https://github.com/MaxKots/HSE_DataOps/blob/main/task_19/.assets/1.jpg)
