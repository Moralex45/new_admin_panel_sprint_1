import os
from dotenv import load_dotenv

load_dotenv()

dsl = {
    'dbname': os.getenv('POSTGRES_DB_NAME'),
    'user': os.getenv('POSTGRES_DB_USER'),
    'password': os.getenv('POSTGRES_DB_PASSWORD'),
    'host': os.getenv('POSTGRES_DB_HOST', '127.0.0.1'),
    'port': os.getenv('POSTGRES_DB_PORT', 5432),
}

SQLITE_DB_PATH = os.environ.get('SQLITE_DB_PATH')
