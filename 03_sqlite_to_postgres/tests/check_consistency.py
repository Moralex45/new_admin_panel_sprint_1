import sys
import sqlite3
from contextlib import closing
import psycopg2
from psycopg2.extras import DictCursor

import settings
from models import MAPPING, TABLE_MATCHING, SQLiteData
from psycopg2.extensions import connection as pg_connection
from psycopg2.extras import RealDictRow
from sqlite_loader import SQLiteLoader

sys.path.append("..")


def compare_content(
        sqlite_obj: SQLiteData, pg_row: RealDictRow,
        attribute_mapping: dict) -> None:
    """
        Сравнить содержимое SQLite-объекта с строкой из PostgreSQL.
    """

    table_name = TABLE_MATCHING[type(sqlite_obj)]
    for attr, column in attribute_mapping.items():
        sqlite_value = getattr(sqlite_obj, attr, None)
        pg_value = pg_row[column]
        msg = (
            'Значение в SQLite "{table_name}.{attr}" не равно '
            'значению в PostgreSQL "{table_name}.{column}": '
            '{sqlite_value} != {pg_value}. '
            'Смотри {table_name}.id = {id}.'
        ).format(
            table_name=table_name,
            attr=attr,
            column=column,
            sqlite_value=sqlite_value,
            pg_value=pg_value,
            id=sqlite_obj.id,
        )

        assert sqlite_value == pg_value, msg


def get_sqlite_table_size(
        table_name: str, connection: sqlite3.Connection) -> int:
    """
        Посчитать число строк в таблице SQLite.
    """

    sql = 'SELECT count(*) FROM {table};'.format(table=table_name)
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        return tuple(cursor.fetchone())[0]


def get_pg_table_size(table_name: str, connection: pg_connection) -> int:
    """
        Посчитать число строк в таблице PostgreSQL.
    """
    sql = 'SELECT count(*) FROM {table};'.format(table=table_name)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count']


def check_consistency(
        sqlite_conn: sqlite3.Connection, pg_conn: pg_connection):
    """
        Сравнить таблицы SQLite и PostgreSQL размерами и построчно.
    """

    tables = TABLE_MATCHING.values()
    # Сравнить размеры таблиц.
    for table_name in tables:
        sqlite_table_size = get_sqlite_table_size(table_name, sqlite_conn)
        pg_table_size = get_pg_table_size(table_name, pg_conn)
        msg = 'Размеры таблиц "{table}" не равны'.format(table=table_name)
        assert sqlite_table_size == pg_table_size, msg

    # Сравнить содержимое таблиц.
    sqlite_loader = SQLiteLoader(sqlite_conn)
    for source, table_name in TABLE_MATCHING.items():
        for obj in sqlite_loader.load(source):
            sql = 'SELECT * FROM {table} WHERE id=%s;'.format(table=table_name)
            values = (obj.id,)
            with pg_conn.cursor() as cursor:
                cursor.execute(sql, values)
                row = cursor.fetchone()
                attribute_mapping = MAPPING[source][
                    'attribute_to_column']
                compare_content(obj, row, attribute_mapping)


if __name__ == '__main__':
    with sqlite3.connect(
            settings.SQLITE_DB_PATH
        ) as sqlite_conn, \
            psycopg2.connect(
                **settings.dsl,
                cursor_factory=DictCursor) as pg_conn:
        check_consistency(sqlite_conn, pg_conn)
