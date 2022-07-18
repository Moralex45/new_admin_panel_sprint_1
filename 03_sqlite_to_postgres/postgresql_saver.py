from models import MAPPING, SQLiteData


class PostgresSaver:
    """
        Класс, импортирующий SQLite-данные в PostgreSQL.
    """

    def __init__(self, connection):
        self.connection = connection

    def _compose_insert_sql(self, table_name: str, columns: tuple) -> str:

        placeholders = ('%s',) * len(columns)
        sql = """
            INSERT INTO {table} ({columns})
            VALUES ({placeholders});
        """.format(
            table=table_name,
            columns=', '.join(columns),
            placeholders=', '.join(placeholders))
        return sql

    def save(self, obj: SQLiteData) -> None:

        obj_type = type(obj)

        msg = '"{type}" нет в MAPPING.'.format(type=obj_type)
        assert obj_type in MAPPING, msg
        destinations = MAPPING[obj_type]

        attribute_mapping = destinations['attribute_to_column']
        columns = []
        values = []
        for attr_name, col_name in attribute_mapping.items():
            value = getattr(obj, attr_name)
            if value:
                values.append(value)
                columns.append(col_name)

        table_name = destinations['destination_table']

        sql = self._compose_insert_sql(table_name, columns)
        with self.connection.cursor() as cursor:
            cursor.execute(sql, values)
