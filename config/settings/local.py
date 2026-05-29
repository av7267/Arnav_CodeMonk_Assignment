from .base import *


# Enable debug mode for local development
DEBUG = env.bool(
    "DEBUG",
    default=True,
)


# Allowed hosts for local environment
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[
        "localhost",
        "127.0.0.1",
    ],
)


# Database configuration
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="sqlite:///db.sqlite3",
    )
}