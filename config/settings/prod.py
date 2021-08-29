"""Settings for production environment"""

from .base import *
from decouple import config

DEBUG = False
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = [config("ALLOWED_HOST")]

DATABASES["default"] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': config("PG_NAME"),
    'USER': config("PG_USER"),
    'PASSWORD': config("PG_PASSWORD"),
    'HOST': config("PG_HOST"),
    'PORT': config("PG_PORT"),
}
