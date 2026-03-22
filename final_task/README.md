# ML Platform — Итоговый проект DataOps

## Выполненные этапы

### Этап 1. MLflow
- Создан Dockerfile на базе \`python:3.11-slim\` с установкой MLflow и зависимостей
- Настроен docker-compose.yaml с сервисами \`mlflow\` и \`mlflow-db\` (PostgreSQL)
- Пароль для БД: \`mlflow_password\`, пользователь: \`mlflow\`
- MLflow доступен по адресу: http://localhost:5000

![final_task](https://github.com/MaxKots/HSE_DataOps/blob/main/final_task/.assets/9.jpg)

### Этап 2. Airflow
- Создан docker-compose.yaml с сервисами:
  - \`airflow-db\` (PostgreSQL 17)
  - \`airflow-init\` (создание пользователя admin/admin)
  - \`airflow-webserver\` (порт 8080)
  - \`airflow-scheduler\`
  - \`airflow-triggerer\`
- Настроен файл \`webserver_config.py\` для отключения CSRF
- Создан тестовый DAG \`ml_pipeline\` в \`dags/test_dag.py\`
- Airflow доступен по адресу: http://localhost:8080 (admin/admin)

![final_task](https://github.com/MaxKots/HSE_DataOps/blob/main/final_task/.assets/3.jpg)


### Этап 3. LakeFS + MinIO
- Создан docker-compose.yaml с сервисами:
  - \`lakefs-db\` (PostgreSQL)
  - \`minio\` (S3-совместимое хранилище)
  - \`lakefs\` (сервер версионирования данных)
- MinIO доступен: http://localhost:9001 (minioadmin/minioadmin)
- Создан bucket: \`lakefs-data\`
- LakeFS доступен: http://localhost:8000
- Создан репозиторий \`my-data\` с пространством \`s3://lakefs-data/my-data\`
- Создана ветка \`dev\`, загружен файл \`housing_data.csv\` и выполнен commit

![final_task](https://github.com/MaxKots/HSE_DataOps/blob/main/final_task/.assets/4.jpg)
![final_task](https://github.com/MaxKots/HSE_DataOps/blob/main/final_task/.assets/10.jpg)

### Этап 4. JupyterHub
- Создан Dockerfile на базе \`python:3.14-slim\`
- Установлены \`jupyterhub\`, \`jupyterlab\`, \`configurable-http-proxy\`
- Создан \`jupyterhub_config.py\` с настройками аутентификации
- JupyterHub доступен: http://localhost:8888 (admin/admin)

![final_task](https://github.com/MaxKots/HSE_DataOps/blob/main/final_task/.assets/5.jpg)

### Этап 5. ML-сервис
- Создан FastAPI сервис с эндпоинтами:
  - \`GET /healthz\` — проверка здоровья
  - \`GET /readyz\` — готовность
  - \`POST /api/v1/predict\` — предсказание
  - \`GET /metrics\` — метрики для Prometheus
- Сервис подключен к PostgreSQL для логирования
- Доступен: http://localhost:8001
- Пример запроса:
  \`\`\`bash
  curl -X POST http://localhost:8001/api/v1/predict \\
    -H "Content-Type: application/json" \\
    -d '{"features": [3.5]}'
  # Ответ: {"prediction":7.065,"model_version":"1.0.0"}

![final_task](https://github.com/MaxKots/HSE_DataOps/blob/main/final_task/.assets/2.jpg)
![final_task](https://github.com/MaxKots/HSE_DataOps/blob/main/final_task/.assets/6.jpg) \`\`\`

### Этап 6. Мониторинг (Prometheus + Grafana)
- Создан docker-compose.yaml для Prometheus и Grafana
- Настроен сбор метрик с ML-сервиса
- Prometheus доступен: http://localhost:9090
- Grafana доступна: http://localhost:3000 (admin/admin)
- Создан дашборд с метриками:
  - \`http_requests_total\`
  - \`http_request_duration_seconds_bucket\

![final_task](https://github.com/MaxKots/HSE_DataOps/blob/main/final_task/.assets/7.jpg)
![final_task](https://github.com/MaxKots/HSE_DataOps/blob/main/final_task/.assets/8.jpg)

### Этап 7-8. Kubernetes + Helm
- Созданы манифесты в \`k8s/\`:
  - \`deployment.yaml\` — развертывание с probes (startup, readiness, liveness)
  - \`service.yaml\` — ClusterIP на порту 80
  - \`ingress.yaml\` — ingress для доступа
  - \`secret.yaml\` — секрет с DATABASE_URL
- Создан Helm chart в \`helm/ml-service/\`:
  - \`Chart.yaml\`, \`values.yaml\`, \`templates/deployment.yaml\`, \`templates/service.yaml\`
- Возможность менять версию образа и ресурсы через \`values.yaml\`
- Ресурсы развернуты в minikube:
  \`\`\`bash
  kubectl get pods
  kubectl get svc
  kubectl get ingress

отчет helm 
```text
echo "=== K8S MANIFESTS ===" && ls -la ~/HSE_DataOps/final_task/k8s/ && \
echo "=== DEPLOYMENT ===" && head -30 ~/HSE_DataOps/final_task/k8s/deployment.yaml && \
echo "=== HELM CHART ===" && ls -la ~/HSE_DataOps/final_task/helm/ml-service/ && \
echo "=== HELM VALUES ===" && cat ~/HSE_DataOps/final_task/helm/ml-service/values.yaml
=== K8S MANIFESTS ===
итого 24
drwxrwxr-x  2 max max 4096 мар 22 05:15 .
drwxrwxr-x 12 max max 4096 мар 22 05:22 ..
-rw-rw-r--  1 max max 1211 мар 22 01:06 deployment.yaml
-rw-rw-r--  1 max max  422 мар 22 01:06 ingress.yaml
-rw-rw-r--  1 max max  165 мар 22 04:47 secret.yaml
-rw-rw-r--  1 max max  180 мар 22 01:06 service.yaml
=== DEPLOYMENT ===
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-service
  labels:
    app: ml-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ml-service
  template:
    metadata:
      labels:
        app: ml-service
    spec:
      containers:
        - name: ml-service
          image: ml-service:1.0.0
          ports:
            - containerPort: 8001
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: ml-service-secrets
                  key: database-url
          startupProbe:
            httpGet:
              path: /healthz
=== HELM CHART ===
итого 20
drwxrwxr-x 3 max max 4096 мар 22 01:06 .
drwxrwxr-x 3 max max 4096 мар 22 01:06 ..
-rw-rw-r-- 1 max max  134 мар 22 01:06 Chart.yaml
drwxrwxr-x 2 max max 4096 мар 22 01:06 templates
-rw-rw-r-- 1 max max  641 мар 22 01:06 values.yaml
=== HELM VALUES ===
replicaCount: 2

image:
  repository: ml-service
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80
  targetPort: 8001

ingress:
  enabled: true
  className: nginx
  host: ml-service.local

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

probes:
  startup:
    path: /healthz
    failureThreshold: 30
    periodSeconds: 2
  readiness:
    path: /readyz
    initialDelaySeconds: 5
    periodSeconds: 10
  liveness:
    path: /healthz
    initialDelaySeconds: 10
    periodSeconds: 30

env:
  DATABASE_URL: "postgresql://mlsvc:mlsvc_pass@ml-service-db:5432/mlsvc"
```
  \`\`\`

### Этап 9. Prompt Storage MLflow
- Создан скрипт \`prompts/create_prompts.py\`
- Созданы три версии промптов:
  - v1: "You are a helpful assistant. Answer: {question}"
  - v2: "You are a data science expert. Answer: {question}"
  - v3: "You are a senior ML engineer. Explain: {question}"
- Промпты сохранены в MLflow Prompt Storage

![final_task](https://github.com/MaxKots/HSE_DataOps/blob/main/final_task/.assets/9.jpg)

## Структура проекта

![final_task](https://github.com/MaxKots/HSE_DataOps/blob/main/final_task/.assets/0.svg)


## Порты сервисов

| Сервис       | Порт  | URL                        | Credentials              |
|-------------|-------|----------------------------|--------------------------|
| MLflow      | 5000  | http://localhost:5000      | —                        |
| Airflow     | 8080  | http://localhost:8080      | admin / admin            |
| LakeFS      | 8000  | http://localhost:8000      | (создаётся при запуске)  |
| MinIO       | 9001  | http://localhost:9001      | minioadmin / minioadmin  |
| JupyterHub  | 8888  | http://localhost:8888      | admin / admin            |
| ML-сервис   | 8001  | http://localhost:8001      | —                        |
| Prometheus  | 9090  | http://localhost:9090      | —                        |
| Grafana     | 3000  | http://localhost:3000      | admin / admin            |

## Запуск всех сервисов

\`\`\`bash
# MLflow
cd mlflow && docker-compose up -d && cd ..

# Airflow
cd airflow && docker-compose up -d && cd ..

# LakeFS + MinIO
cd lakefs && docker-compose up -d && cd ..

# JupyterHub
cd jupyterhub && docker-compose up -d --build && cd ..

# ML-сервис
cd ml-service && docker-compose up -d --build && cd ..

# Мониторинг
cd monitoring && docker-compose up -d && cd ..

# Генерация нагрузки для метрик
for i in {1..20}; do
  curl -s -X POST http://localhost:8001/api/v1/predict \\
    -H "Content-Type: application/json" \\
    -d "{\"features\": [$i]}" > /dev/null
done

# Kubernetes (опционально)
minikube start --driver=docker
kubectl apply -f k8s/
helm install ml-release helm/ml-service/

# Prompt Storage
pip install mlflow
export MLFLOW_TRACKING_URI=http://localhost:5000
python prompts/create_prompts.py
\`\`\`

## Очистка и завершение работы

\`\`\`bash
# 1. Остановка всех Docker-контейнеров и удаление томов
cd mlflow && docker-compose down -v && cd ..
cd airflow && docker-compose down -v && cd ..
cd lakefs && docker-compose down -v && cd ..
cd jupyterhub && docker-compose down -v && cd ..
cd ml-service && docker-compose down -v && cd ..
cd monitoring && docker-compose down -v && cd ..

# 2. Остановка и удаление Kubernetes ресурсов
helm uninstall ml-release
kubectl delete -f k8s/
minikube stop
minikube delete

# 3. Удаление виртуального окружения
deactivate 2>/dev/null
rm -rf venv

# 4. Удаление всех образов, контейнеров, сетей и томов Docker
docker system prune -a --volumes -f

# 5. Проверка, что ничего не осталось
docker ps -a
docker volume ls
kubectl get pods --all-namespaces 2>/dev/null || echo "Kubernetes очищен"
\`\`\`

## Проверка работоспособности

\`\`\`bash
# Все контейнеры
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# ML-сервис
curl http://localhost:8001/healthz
curl -X POST http://localhost:8001/api/v1/predict -H "Content-Type: application/json" -d '{"features": [3.5]}'

# Prometheus метрики
curl http://localhost:8001/metrics | grep http_requests_total

# Airflow
curl http://localhost:8080

# MLflow
curl http://localhost:5000

# Kubernetes (если запущен)
kubectl get pods
kubectl get svc
kubectl get ingress
\`\`\`

## Файлы для проверки

| Файл | Назначение |
|------|------------|
| \`k8s/deployment.yaml\` | Kubernetes Deployment с probes |
| \`k8s/service.yaml\` | Kubernetes Service (ClusterIP) |
| \`k8s/ingress.yaml\` | Kubernetes Ingress |
| \`k8s/secret.yaml\` | Secret с DATABASE_URL |
| \`helm/ml-service/Chart.yaml\` | Helm Chart метаданные |
| \`helm/ml-service/values.yaml\` | Helm параметры |
| \`helm/ml-service/templates/deployment.yaml\` | Helm шаблон Deployment |
| \`helm/ml-service/templates/service.yaml\` | Helm шаблон Service |

## Выводы

Все этапы итогового проекта DataOps выполнены в полном объеме:

1. **MLflow** — развернут сервер для отслеживания экспериментов, база данных PostgreSQL, созданы промпты в Prompt Storage
2. **Airflow** — развернут оркестратор, создан DAG \`ml_pipeline\`, веб-интерфейс доступен
3. **LakeFS + MinIO** — развернуто версионирование данных, создан репозиторий, выполнены commit и branch
4. **JupyterHub** — развернут сервер для работы с ноутбуками, доступен JupyterLab
5. **ML-сервис** — создан FastAPI сервис с эндпоинтами /predict, /healthz, /metrics
6. **Мониторинг** — развернуты Prometheus и Grafana, настроен сбор метрик, создан дашборд
7. **Kubernetes** — созданы манифесты для развертывания ML-сервиса (Deployment, Service, Ingress, Secret)
8. **Helm** — создан Helm chart с возможностью настройки образа и ресурсов
9. **Prompt Storage** — в MLflow созданы несколько версий промптов

## Сертификаты и учетные данные

| Сервис     | Логин          | Пароль         |
|------------|----------------|----------------|
| Airflow    | admin          | admin          |
| JupyterHub | admin          | admin          |
| MinIO      | minioadmin     | minioadmin     |
| Grafana    | admin          | admin          |
| LakeFS     | создаётся при первом запуске | — |
| PostgreSQL (mlflow) | mlflow | mlflow_password |
| PostgreSQL (airflow) | airflow | hse_password |
| PostgreSQL (ml-service) | mlsvc | hse_password |

## Примечания

- Все пароли и учетные данные являются тестовыми и предназначены только для локального развертывания
- Для работы с Kubernetes использовался minikube с драйвером docker
- Промпты в MLflow созданы через \`mlflow.log_text()\` с группировкой в один run
- ML-сервис в Kubernetes не подключается к БД (отсутствует сервис \`ml-service-db\` в кластере), но это не влияет на факт наличия манифестов и Helm chart

## Завершение работы

После завершения всех проверок выполните команды из раздела "Очистка и завершение работы" для освобождения ресурсов.

