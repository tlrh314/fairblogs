import os
import sys

import environ

env = environ.Env()
env.read_env(str((environ.Path(__file__) - 1).path(".env")))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Use the 'apps' folder for our project apps
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

INSTALLED_APPS = [
    # Filebrowser should be listed before django.contrib.admin
    "dal",
    "dal_select2",
    "tinymce",
    "filebrowser",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.forms",
    "django.contrib.syndication",
    "myuser",
    "blog",
    "pages",
    "search",
    # "bootstrap",
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

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates")
        ],  # Additional directory for base templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "context_processors.base",
                "context_processors.contactinfo",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

BASE_URL = env("BASE_URL")
SITE_ID = env("SITE_ID", default=1)

SECRET_KEY = env("SECRET_KEY")
DEBUG = TEMPLATE_DEBUG = TEMPLATES[0]["OPTIONS"]["debug"] = env("DEBUG", default=False)
ROOT_URLCONF = "settings.urls"
WSGI_APPLICATION = "settings.wsgi.application"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "testserver",
    "fairblogs.nl",
    "www.fairblogs.nl",
]


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "myuser.Blogger"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = env("LANGUAGE_CODE")

TIME_ZONE = env("TIME_ZONE")

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATABASES = {
    "default": env.db("DATABASE_URL"),
}

CACHES = {"default": env.cache()}


EMAIL_CONFIG = env.email_url("EMAIL_URL", default="consolemail://")
vars().update(EMAIL_CONFIG)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = env("SERVER_EMAIL")

from settings.logsetup import *  # noqa E402 F403 F401

SENTRY_DSN_API = env("SENTRY_DSN_API", default="")
DJANGO_ENVIRONMENT = env("DJANGO_ENVIRONMENT")
import sentry_sdk  # noqa E402
from sentry_sdk.integrations.django import DjangoIntegration  # noqa E402

sentry_sdk.init(
    dsn=SENTRY_DSN_API,
    integrations=[DjangoIntegration()],
    environment=DJANGO_ENVIRONMENT,
)

if DEBUG:
    INSTALLED_APPS += [
        "django_extensions",
    ]

DEBUG_TOOLBAR_ON = env("DEBUG_TOOLBAR_ON", default=False)
if DEBUG_TOOLBAR_ON:
    print("WARNING: the debug_toolbar is on. This can be extremely slow")

    def show_toolbar(request):
        return True

    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE

    INTERNAL_IPS = ["127.0.0.1", "localhost"]

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
        "JQUERY_URL": "/static/js/jquery.min.js",
    }
