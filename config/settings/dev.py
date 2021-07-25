"""Settings file for local development"""

from .base import *
from decouple import config

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG") == "1"
ALLOWED_HOSTS = config("ALLOWED_HOSTS").split()
AUTH_PASSWORD_VALIDATORS = []
