from .base import *
from .credentials import SECRET_KEY, DB_PASSWORD

# Set true for this fancy Django default homepage
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '/cloudsql/facebook-hack-2019:us-east1:fbhack-db',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': DB_PASSWORD,
    }
}

ALLOWED_HOSTS = ['facebook-hack-2019.appspot.com', 'fbhack.wkulikowski.com']
