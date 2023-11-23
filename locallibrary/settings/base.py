import dj_database_url
import os
from django.contrib.messages import constants
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = '...'
DEBUG = True

# ALLOWED_HOSTS = [".herokuapp.com", "127.0.0.1"]

DEFAULT_DOMAIN = "hung-library.herokuapp.com"


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # My apps
    "catalog.apps.CatalogConfig",
    "users.apps.UsersConfig",
    "api.apps.ApiConfig",
    # 3rd parties apps
    "rest_framework",
    "crispy_forms",
    "crispy_bootstrap4",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "locallibrary.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR/"templates",],
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

WSGI_APPLICATION = "locallibrary.wsgi.application"


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

PASSWORD_MIN_LENGTH = 8


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Bangkok"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR/"static_root"


# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# STORAGES = None

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR/"media_root"

LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/catalog/books/"
LOGOUT_REDIRECT_URL = "/catalog/books/"


# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES["default"].update(db_from_env)


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

MESSAGE_TAGS = {
    constants.ERROR: "danger",
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
