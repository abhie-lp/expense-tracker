"""Settings file for heroku deployment"""

from .base import *
from os import environ

SECRET_KEY = environ.get("SECRET_KEY", "set a secret key in environment.")
DEBUG = environ.get("DEBUG", True) == "1"
ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "*").split()
AUTH_PASSWORD_VALIDATORS = []
