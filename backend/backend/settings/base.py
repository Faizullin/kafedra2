from datetime import timedelta

import environ
import os
from celery.schedules import crontab
from django.utils.translation import gettext_lazy as _

root = environ.Path(__file__) - 3
BASE_DIR = root()
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env.bool('DEBUG', True)
USE_HTTPS = env.bool('USE_HTTPS', False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
FRONTEND_APP_BASE_URL = env.str('FRONTEND_APP_BASE_URL', 'http://localhost:5173')
SITE_COMMAND = env.str('SITE_COMMAND', None)
EMAIL_SERVICE_NAME = env.str("EMAIL_SERVICE_NAME", None)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', None)

# Application definition

DJANGO_APPS = [
    "modeltranslation",  # Translation
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms"
]

# Third party apps
THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    "rest_framework",
    "django_filters",
]

# Custom apps
PROJECT_APPS = [
    "apps.accounts",
    "apps.courses",
    "apps.results",
    "apps.search",
    "apps.quiz",
    "apps.payments",
    "apps.attachments",
    "apps.activities",
    "apps.assignments",
    "apps.posts",
    "apps.reviews",
    "apps.pages",
    "apps.my_dashboard",
]

# Combine all apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "backend.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # 'django.template.context_processors.i18n',
                # 'django.template.context_processors.media',
                # 'django.template.context_processors.static',
                # 'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

ASGI_APPLICATION = "backend.asgi.application"

DATABASES = None
if env.str("DB_USER", None) is not None and env.str("DB_PASSWORD", None) is not None:
    DATABASES = {
        'default': {
            'ENGINE': env.str('DB_ENGINE'),
            'NAME': env.str('DB_NAME'),
            'USER': env.str('DB_USER'),
            'PASSWORD': env.str('DB_PASSWORD'),
            'HOST': env.str('DB_HOST'),
            'PORT': env.str('DB_PORT'),
        }
    }

# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

gettext = lambda s: s

LANGUAGES = (
    ("en", gettext("English")),
    ("fr", gettext("French")),
    ("es", gettext("Spanish")),
    ("ru", gettext("Russia")),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

public_root = root.path('public/')
MEDIA_ROOT = public_root('media')
MEDIA_URL = env.str('MEDIA_URL', default='media/')
# STATIC_ROOT = public_root('static')
STATIC_URL = env.str('STATIC_URL', default='static/')

# print(str(public_root('static')))
# STATICFILES_DIRS = [
#     str(public_root('static')),
#     # "/var/www/static/",
# ]
STATICFILES_DIRS = (str(public_root('static')),)

# -----------------------------------
# E-mail configuration


if EMAIL_SERVICE_NAME == "GMAIL_OAUTH":
    EMAIL_SEND_FROM_NAME = env.str("EMAIL_SEND_FROM_NAME", None)
    EMAIL_BACKEND = 'gmailapi_backend.mail.GmailBackend'
    GMAIL_API_CLIENT_ID = env.str("GMAIL_API_CLIENT_ID")
    GMAIL_API_CLIENT_SECRET = env.str("GMAIL_API_CLIENT_SECRET")
    GMAIL_API_REFRESH_TOKEN = env.str("GMAIL_API_REFRESH_TOKEN")
elif env.str("EMAIL_HOST_USER", None) is not None:
    EMAIL_SEND_FROM_NAME = env.str("EMAIL_SEND_FROM_NAME")
    EMAIL_HOST = env.str("EMAIL_HOST")
    EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = env.str("EMAIL_PORT")
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True

# -----------------------------------
# crispy config

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

AUTH_USER_MODEL = 'accounts.CustomUser'
# LOGOUT_REDIRECT_URL = FRONTEND_APP_BASE_URL + "/"
# LOGIN_URL = FRONTEND_APP_BASE_URL + "/auth/login"

# # -----------------------------------
# # DRF setup
#
# REST_FRAMEWORK = {
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework.permissions.IsAuthenticated",
#     ],
#     "DEFAULT_AUTHENTICATION_CLASSES": [
#         "rest_framework.authentication.SessionAuthentication",
#         "rest_framework.authentication.BasicAuthentication",
#     ],
# }

# -----------------------------------
# Strip payment config

STRIPE_SECRET_KEY = env.str("STRIPE_SECRET_KEY", default="")
STRIPE_PUBLISHABLE_KEY = env.str("STRIPE_PUBLISHABLE_KEY", default="")


STUDENT_ID_PREFIX = env.str("STUDENT_ID_PREFIX", "ugr")
LECTURER_ID_PREFIX = env.str("LECTURER_ID_PREFIX", "lec")




# if USE_HTTPS:
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#     SECURE_SSL_REDIRECT = True
# else:
#     SECURE_SSL_REDIRECT = False
#     SESSION_COOKIE_SECURE = False

# CELERY SETTINGS

CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', None)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
# CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', None)

# CELERY_BEAT_SCHEDULE = {
#     "check_booking_payments": {
#         "task": "bookings.tasks.check_booking_payments",
#         "schedule": crontab(minute='*/10'),  # Run every 10 minutes ('*/10')
#     }
# }

# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': CELERY_BROKER_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

X_FRAME_OPTIONS = "SAMEORIGIN"

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'