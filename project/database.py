import os

from django.conf import settings


engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
}


def config():
    service_name = os.getenv('DATABASE_SERVICE_NAME', '').upper().replace('-', '_')
    if service_name:
        engine = engines.get(os.getenv('DATABASE_ENGINE'), engines['postgresql'])
    else:
        engine = engines['postgresql']
    name = os.getenv('DATABASE_NAME')
    if not name and engine == engines['sqlite']:
        name = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    return {
        'ENGINE': engine,
        'NAME': 'default',
        'USER': 'django',
        'PASSWORD': 'pxviFo8wxSTGstTq',
        'PORT': '5432',
        'HOST': '10.137.255.43',
        'TEST': {
            'NAME': 'test_yourmum',
        }
    }
