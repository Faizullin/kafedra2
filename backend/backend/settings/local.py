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
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE += 'debug_toolbar.middleware.DebugToolbarMiddleware',
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

# if DEBUG:
#     CORS_ALLOW_ALL_ORIGINS = True
#     CORS_ALLOW_CREDENTIALS = True
