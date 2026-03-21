# ML Platform — Итоговый проект DataOps

Полный цикл сборки и развёртывания ML-сервиса: от поднятия ключевых компонентов (MLflow, Airflow, LakeFS, JupyterHub) и регистрации артефактов до подготовки сервиса к деплою в Kubernetes с использованием Helm Charts.

## Структура проекта


![final_task](https://github.com/MaxKots/HSE_DataOps/blob/main/final_task/.assets/1.svg)


## Требования

- Docker и Docker Compose
- Python 3.11+
- (опционально) kubectl, Helm, minikube для этапов 7-8

## Порты сервисов

| Сервис       | Порт  | URL                        |
|-------------|-------|----------------------------|
| MLflow      | 5000  | http://localhost:5000      |
| Airflow     | 8080  | http://localhost:8080      |
| LakeFS      | 8000  | http://localhost:8000      |
| MinIO       | 9001  | http://localhost:9001      |
| JupyterHub  | 8888  | http://localhost:8888      |
| ML-сервис   | 8001  | http://localhost:8001      |
| Prometheus  | 9090  | http://localhost:9090      |
| Grafana     | 3000  | http://localhost:3000      |

## Запуск

### Подготовка

```bash
cd ~/ml-platform

docker --version
docker-compose --version
```

### Этап 1. MLflow

```bash
docker-compose up -d
# Жди ~30 сек
# Открывай http://localhost:5000
# Создай эксперимент: кнопка \"+\" слева
```

### Этап 2. Airflow

```bash
cd airflow
docker-compose up -d
# Первый запуск долгий — init делает миграции и создаёт пользователя
# Жди ~1-2 мин
# Открывай http://localhost:8080
# Логин: admin / admin
# DAG \"ml_pipeline\" появится в списке
cd ..
```

### Этап 3. LakeFS + MinIO

```bash
cd lakefs
docker-compose up -d
# Жди ~30 сек

# 1. MinIO: http://localhost:9001 (minioadmin / minioadmin)
#    Buckets → Create Bucket → имя: lakefs-data

# 2. LakeFS: http://localhost:8000
#    Первый вход — создаст admin-ключи, СОХРАНИТЕ ИХ
#    Create Repository:
#      Name: my-data
#      Storage Namespace: s3://lakefs-data/my-data
#    Создать ветку: dev
#    Upload файл → Commit
cd ..
```

### Этап 4. JupyterHub

```bash
cd jupyterhub
docker-compose up -d --build
# Жди ~1 мин (сборка образа)
# Открывай http://localhost:8888
# Логин: admin / admin
# Запустится JupyterLab
cd ..
```

### Этап 5. ML-сервис

```bash
cd ml-service
docker-compose up -d --build
# Жди ~30 сек

# Проверь здоровье
curl http://localhost:8001/healthz

# Сделай предсказание
curl -X POST http://localhost:8001/api/v1/predict \\
  -H \"Content-Type: application/json\" \\
  -d '{\"features\": [3.5]}'

# Ожидаемый ответ: {\"prediction\":7.03,\"model_version\":\"1.0.0\"}
cd ..
```

### Этап 6. Мониторинг

```bash
cd monitoring
docker-compose up -d

# Сгенери нагрузку чтобы появились метрики
for i in (seq 1 20); do
  curl -s -X POST http://localhost:8001/api/v1/predict \\
    -H \"Content-Type: application/json\" \\
    -d '{\"features\": ['\"i\"']}' > /dev/null
done

# Prometheus: http://localhost:9090
#   Targets → ml-service должен быть UP
#   Попробовать запрос: http_requests_total

# Grafana: http://localhost:3000 (admin / admin)
#   Datasource Prometheus уже подключен
#   Dashboards → New Dashboard → Add visualization
#   Метрики:
#     http_requests_total
#     http_request_duration_seconds_bucket
cd ..
```

### Этап 7-8. Kubernetes + Helm

```bash
# Запуск minikube
minikube start

# Вариант A: через манифесты
kubectl apply -f k8s/

# Вариант B: через Helm
helm install ml-release helm/ml-service/

# Проверка
kubectl get pods
kubectl get svc
kubectl get ingress

# Обновление образа через Helm
helm upgrade ml-release helm/ml-service/ --set image.tag=2.0.0

# Изменение ресурсов через Helm
helm upgrade ml-release helm/ml-service/ \\
  --set resources.requests.cpu=200m \\
  --set resources.limits.memory=1Gi
```

### Этап 9. Промпты MLflow

```bash
# MLflow должен быть запущен (этап 1)
pip install mlflow
export MLFLOW_TRACKING_URI=http://localhost:5000
python prompts/create_prompts.py
```
# Проверь в UI: http://localhost:5000 → раздел Prompt Storage


## Проверка что всё работает

```bash
docker ps --format \"table {{.Names}}\t{{.Status}}\t{{.Ports}}\"
```

Ожидаемый вывод:


NAMES              STATUS          PORTS
mlflow             Up              0.0.0.0:5000->5000/tcp
mlflow-db          Up (healthy)    0.0.0.0:5433->5432/tcp
airflow-webserver  Up              0.0.0.0:8080->8080/tcp
airflow-scheduler  Up
airflow-triggerer  Up
airflow-db         Up (healthy)
lakefs             Up              0.0.0.0:8000->8000/tcp
lakefs-minio       Up              0.0.0.0:9000-9001->9000-9001/tcp
lakefs-db          Up (healthy)
jupyterhub         Up              0.0.0.0:8888->8888/tcp
ml-service         Up              0.0.0.0:8001->8001/tcp
ml-service-db      Up (healthy)
prometheus         Up              0.0.0.0:9090->9090/tcp
grafana            Up              0.0.0.0:3000->3000/tcp


## Очистка и завершение работы

```bash
# Остановка всех сервисов и удаление контейнеров, сетей, томов

cd ~/ml-platform && docker-compose down -v
cd airflow && docker-compose down -v && cd ..
cd lakefs && docker-compose down -v && cd ..
cd jupyterhub && docker-compose down -v && cd ..
cd ml-service && docker-compose down -v && cd ..
cd monitoring && docker-compose down -v && cd ..

# Kubernetes (если применяли)
kubectl delete -f k8s/
# или
helm uninstall ml-release

# Удаление всех образов и кэша Docker
docker system prune -a --volumes -f
```

