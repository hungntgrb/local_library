import dj_database_url
import os
from django.contrib.messages import constants

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = os.environ["DJANGO_SK1"]
DEBUG = os.environ["DJANGO_DEBUG1"] == "True"


ALLOWED_HOSTS = ["herokuapp.com", "127.0.0.1"]

DEFAULT_DOMAIN = f"http://polar-lake-80686.herokuapp.com"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # My apps
    "catalog",
    "users.apps.UsersConfig",
    "api.apps.ApiConfig",
    # 3rd parties apps
    "rest_framework",
    "crispy_forms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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
        "DIRS": [os.path.join(BASE_DIR, "templates"),],
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


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Bangkok"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/catalog/books/"
LOGOUT_REDIRECT_URL = "/catalog/books/"

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)

# Simplified statis files to serve
# https://warehouse.python.org/project/whitenoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CRISPY_TEMPLATE_PACK = "bootstrap4"

MESSAGE_TAGS = {
    constants.ERROR: "danger",
}

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = os.environ.get("EMAIL_USER1")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASS1")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
