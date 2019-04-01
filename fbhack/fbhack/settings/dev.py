from .base import *
from .credentials import DB_PASSWORD

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': DB_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': ' 5432',
    }
}
