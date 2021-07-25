"""Settings for production environment"""

from .base import *
from decouple import config

DEBUG = False
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = [config("ALLOWED_HOST")]
