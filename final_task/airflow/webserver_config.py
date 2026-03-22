from flask_appbuilder.security.manager import AUTH_DB
import os

# Отключаем CSRF полностью
WTF_CSRF_ENABLED = False
WTF_CSRF_CHECK_DEFAULT = False
CSRF_ENABLED = False

# Настройки аутентификации
AUTH_TYPE = AUTH_DB
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Admin"

# Отключаем защиту сессии
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = False

# Секретный ключ
SECRET_KEY = os.urandom(24)
