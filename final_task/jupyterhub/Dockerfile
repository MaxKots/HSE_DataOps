FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm && \
    npm install -g configurable-http-proxy && \
    pip install --no-cache-dir jupyterhub jupyterlab notebook && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -m admin && echo "admin:admin" | chpasswd

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

WORKDIR /srv/jupyterhub
EXPOSE 8888

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]