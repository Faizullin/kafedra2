from .base import *

if DEBUG and DATABASES is None:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# if DEBUG:
#     MIDDLEWARE.append(
#         "backend.delay_middleware.DelayMiddleware"
#     )
#     DEV_REQUEST_DELAY = env.float('DEV_REQUEST_DELAY', 0.5)

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = [
        "127.0.0.1",
    ]


    def show_toolbar(request):
        return True


    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
        'RESULTS_CACHE_SIZE': 100,
        'SQL_WARNING_THRESHOLD': 2000
    }

# if DEBUG:
#     CORS_ALLOW_ALL_ORIGINS = True
#     CORS_ALLOW_CREDENTIALS = True


if DEBUG:
    INSTALLED_APPS.append('django_filters')
    INSTALLED_APPS.append('rest_framework')
    INSTALLED_APPS.remove('django.contrib.staticfiles')
