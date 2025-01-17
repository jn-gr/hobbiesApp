import os
from django.conf import settings

engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
}

# Required environment variables
REQUIRED_ENV_VARS = ["DATABASE_NAME", "DATABASE_USER", "DATABASE_PASSWORD", "DATABASE_ENGINE", "DATABASE_SERVICE_NAME"]

def config():
    # Check for missing environment variables
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

    service_name = os.getenv('DATABASE_SERVICE_NAME').upper().replace('-', '_')
    engine = engines.get(os.getenv('DATABASE_ENGINE'), engines['postgresql'])

    name = os.getenv('DATABASE_NAME')
    if not name and engine == engines['sqlite']:
        name = os.path.join(settings.BASE_DIR, 'db.sqlite3')

    return {
        'ENGINE': engine,
        'NAME': name,
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv(f'{service_name}_SERVICE_HOST'),
        'PORT': os.getenv(f'{service_name}_SERVICE_PORT'),
    }
