import sqlite3
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

import logzero
from logzero import logger

import settings
from sqlite_loader import SQLiteLoader
from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from postgresql_saver import PostgresSaver

logzero.logfile("sqlite_to_postgres.log")


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""

    loader = SQLiteLoader(sqlite_conn)
    saver = PostgresSaver(pg_conn)
    sources = (FilmWork, Person, PersonFilmWork, Genre, GenreFilmWork)

    for source in sources:
        for obj in loader.load(source):
            try:
                saver.save(obj)
            except Exception as e:
                logger.error(f"Failed to save {type(obj)} id={obj.id}.")
                logger.error(e)
            else:
                logger.info(f"Imported {type(obj)} id={obj.id}")
    logger.info("Импорт завершен")


if __name__ == '__main__':
    with sqlite3.connect(settings.SQLITE_DB_PATH) as sqlite_conn:
        with psycopg2.connect(
            **settings.dsl,
            cursor_factory=DictCursor
        ) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
