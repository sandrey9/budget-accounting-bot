import os

from yoyo import get_backend
from yoyo import read_migrations


def migration():
    backend = get_backend(os.getenv('POSTGRES_DSN'))
    migrations = read_migrations('./migrations')

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
