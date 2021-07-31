"""Settings file for local development"""

from .base import *
from decouple import config

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG") == "1"
INSTALLED_APPS += [
    "debug_toolbar",
]
ALLOWED_HOSTS = config("ALLOWED_HOSTS").split()
AUTH_PASSWORD_VALIDATORS = []
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ("127.0.0.1", "localhost")
