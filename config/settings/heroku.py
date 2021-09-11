"""Settings file for heroku deployment"""

from .base import *
from os import environ

SECRET_KEY = environ.get("SECRET_KEY", "set a secret key in environment.")
DEBUG = environ.get("DEBUG", True) == "1"
ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "*").split()
AUTH_PASSWORD_VALIDATORS = []
DATABASES["default"] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': environ.get("PG_NAME"),
    'USER': environ.get("PG_USER"),
    'PASSWORD': environ.get("PG_PASSWORD"),
    'HOST': environ.get("PG_HOST"),
    'PORT': environ.get("PG_PORT"),
}

REST_FRAMEWORK.update({
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
})
