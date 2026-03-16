FROM python:3.14-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Установка configurable-http-proxy через npm
RUN npm install -g configurable-http-proxy

# Установка JupyterHub и сопутствующих пакетов
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Создание директории для конфигурации
RUN mkdir -p /etc/jupyterhub

# Копирование конфигурации
COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py

# Рабочая директория
WORKDIR /srv/jupyterhub

# Запуск JupyterHub
CMD ["jupyterhub", "-f", "/etc/jupyterhub/jupyterhub_config.py"]
