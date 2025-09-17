"""
Django settings for core project.

Configurado con buenas prácticas para desarrollo:
- Variables en .env (SECRET_KEY, DEBUG, ALLOWED_HOSTS, DATABASE_URL)
- DRF + JWT (autenticación)
- CORS (habilitado en dev)
- OpenAPI/Swagger con drf-spectacular
- Idioma español (Colombia) y zona horaria Bogotá
"""

from pathlib import Path
import os
import environ

# -----------------------------------
# Paths
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------
# Variables de entorno (.env en la raíz del proyecto)
# -----------------------------------
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# -----------------------------------
# Seguridad / Debug / Hosts
# -----------------------------------
DEBUG = env("DEBUG", default=True)
SECRET_KEY = env("SECRET_KEY", default="!!-SOLO_DESARROLLO-CAMBIA-ESTO-EN-PRODUCCION-!!")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

# -----------------------------------
# Aplicaciones
# -----------------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceros
    "rest_framework",
    "corsheaders",
    "drf_spectacular",

    # Apps propias (las irás agregando)
    # "organizations",
    # "users",
    # "devices",
    # "playlists",
    # "mediafiles",
    # "delivery",
]

# -----------------------------------
# Middlewares
# -----------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS siempre arriba
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------------
# URLs / WSGI
# -----------------------------------
ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# -----------------------------------
# Base de datos
# - En dev: SQLite por simplicidad
# - En prod: define DATABASE_URL en .env (PostgreSQL recomendado)
# -----------------------------------
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}

# -----------------------------------
# Validadores de contraseña
# -----------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------
# Internacionalización
# -----------------------------------
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# -----------------------------------
# Archivos estáticos y media
# -----------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # para collectstatic en despliegue

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------
# DRF + JWT + OpenAPI
# -----------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Cartelera API",
    "DESCRIPTION": "API para administración de dispositivos, playlists y distribución de contenidos.",
    "VERSION": "0.1.0",
}

# -----------------------------------
# CORS (en dev permitir todo; en prod limitar dominios)
# -----------------------------------
CORS_ALLOW_ALL_ORIGINS = True
# Para producción, usa algo como:
# CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=["https://panel.tu-dominio.com"])
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = list(default_headers) + ["tu-header-personalizado"]
# CORS_ALLOW_METHODS = list(default_methods) + ["PUT", "DELETE"]    
# CORS_EXPOSE_HEADERS = ["Content-Disposition"]
# CORS_PREFLIGHT_MAX_AGE = 86400  # 24 horas
# CORS_REPLACE_HTTPS_REFERER = True
# CORS_URLS_REGEX = r"^/api/.*$"  # Solo para rutas que empiecen con /api/
# CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", default=["https://panel.tu-dominio.com"])
# CORS_ORIGIN_REGEX_WHITELIST = [r"^https://\w+\.tu-dominio\.com$"]
# CORS_ORIGIN_ALLOW_ALL = False
# CORS_ALLOW_METHODS = [
#     "GET",
#     "POST",           
#     "PUT",
#     "PATCH",
#     "DELETE",
#     "OPTIONS",
# ]
# CORS_ALLOW_HEADERS = [    
#     "accept",
