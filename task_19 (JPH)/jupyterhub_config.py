# jupyterhub_config.py
import os

# Настройки прокси
c.JupyterHub.bind_url = 'http://:8000'

# Используем dummy аутентификатор для простоты (любой логин/пароль работает)
c.JupyterHub.authenticator_class = 'dummy'

# Используем простой spawner (запускает сервер в том же контейнере)
c.JupyterHub.spawner_class = 'simple'

# Настройки администратора
admin_user = os.environ.get('JUPYTERHUB_ADMIN', 'admin')
c.Authenticator.admin_users = {admin_user}

# Разрешаем всем пользователям (включая не-админов)
c.Authenticator.allow_all = True

# База данных (SQLite для простоты)
c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'

# Разрешаем пользователям создавать свои сервера
c.JupyterHub.allow_named_servers = True

# Таймауты
c.JupyterHub.tornado_settings = {
    'headers': {
        'X-Frame-Options': 'DENY',
    },
}

# Настройки логов
c.JupyterHub.log_level = 'INFO'

# Криптографический ключ из .env
c.JupyterHub.crypt_key = os.environ.get('JUPYTERHUB_CRYPT_KEY')
