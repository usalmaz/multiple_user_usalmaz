from .settings import *

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'locator',
        'USER': 'scott',
        'PASSWORD': 'Acts2:38-39',
        'HOST': 'localhost',
        'PORT': '',
    }
}
