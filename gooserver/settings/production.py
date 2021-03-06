# vim: tabstop=4 shiftwidth=4 softtabstop=4
from defaults import *

DEBUG = False

DATABASES = {
    'default': {
# Testing environment
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'goo-server',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Set server contact url (to inform goo-pilot.py)
# Production environment
BASE_URL = 'https://submit.grid.unesp.br'

WSGI_APPLICATION = 'gooserver.wsgi-production.application'
