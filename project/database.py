import os

from django.conf import settings
import dj_database_url


engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
}


def config():
    # Use SQLite for tests
    if settings.TEST:
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    
    if os.getenv('DATABASE_URL'):
        return dj_database_url.config()
    
    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hobbiesapp',
        'USER': 'hobbiesapp_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
