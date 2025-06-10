from .base import *

DEBUG = env("DEBUG")
SECRET_KEY = "5fb5d249130b849e89b4170dc884d8222905f58f7fca8defe838b6295559"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
    },
    "sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "locallibrary001.sqlite3",
    },
}
