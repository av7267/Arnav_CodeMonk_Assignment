from datetime import timedelta
from pathlib import Path

import environ


# Base project directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Environment variable configuration
env = environ.Env()

# Load local .env file if available
environ.Env.read_env(
    BASE_DIR / ".env"
)


# Security
SECRET_KEY = env(
    "SECRET_KEY",
    default="unsafe-secret-key",
)


# Installed applications
INSTALLED_APPS = [
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",

    # Local applications
    "apps.users",
    "apps.paragraphs",
]


# Middleware configuration
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


# Django template configuration
TEMPLATES = [
    {
        "BACKEND": (
            "django.template.backends.django.DjangoTemplates"
        ),
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                (
                    "django.template.context_processors.debug"
                ),
                (
                    "django.template.context_processors.request"
                ),
                (
                    "django.contrib.auth.context_processors.auth"
                ),
                (
                    "django.contrib.messages.context_processors.messages"
                ),
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# Password validation rules
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        )
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True


# Static files
STATIC_URL = "static/"


# Default primary key field type
DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)


# Custom user model
AUTH_USER_MODEL = "users.User"


# Django REST Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        (
            "rest_framework_simplejwt.authentication."
            "JWTAuthentication"
        ),
    ],

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],

    "DEFAULT_SCHEMA_CLASS": (
        "drf_spectacular.openapi.AutoSchema"
    ),
}


# JWT token configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=15
    ),

    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=7
    ),
}


# Swagger / OpenAPI configuration
SPECTACULAR_SETTINGS = {
    "TITLE": "Codemonk Backend API",
    "DESCRIPTION": (
        "Backend API for paragraph processing "
        "and word frequency search."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}


# Celery configuration
CELERY_BROKER_URL = env(
    "REDIS_URL",
    default="redis://redis:6379/0",
)

CELERY_RESULT_BACKEND = env(
    "REDIS_URL",
    default="redis://redis:6379/0",
)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"