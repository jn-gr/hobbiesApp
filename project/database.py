import os

from django.conf import settings


engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
}


def config():
    service_name = 'hobbiesapp'
    if service_name:
        engine = engines.get(os.getenv('DATABASE_ENGINE'), engines['postgresql'])
    else:
        engine = engines['postgresql']
    name = os.getenv('DATABASE_NAME')
    if not name and engine == engines['sqlite']:
        name = os.path.join(settings.BASE_DIR, 'db.sqlite3')

    return {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME', 'postgres'),
        'USER': os.getenv('DATABASE_USER', 'django'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'asseater1'), 
        'HOST': os.getenv('DATABASE_HOST', 'postgresql')
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
