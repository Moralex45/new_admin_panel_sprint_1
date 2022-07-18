import sqlite3
from contextlib import closing

from models import TABLE_MATCHING


class SQLiteLoader:
    """
        Класс получающий данные из SQLite по batch_size за раз.
    """

    def __init__(self, connection):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row

    def load(self, sqlite_data_class: type, batch_size=10):
        table_name = TABLE_MATCHING[sqlite_data_class]
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(f'SELECT * FROM {table_name};')
            while data := cursor.fetchmany(batch_size):
                for row in data:
                    row_dict = dict(zip(row.keys(), tuple(row)))
                    obj = sqlite_data_class(**row_dict)
                    yield obj
