import uuid
from datetime import datetime
from dataclasses import dataclass, field, fields


from dateutil.parser import parse


class SQLiteData:
    """
        Базовый класс для объектного представления таблиц SQLite.
        Представление Datetime
    """

    def __post_init__(self):
        for own_field in fields(type(self)):
            if own_field.type == datetime:
                value = getattr(self, own_field.name)
                if isinstance(value, str):
                    setattr(self, own_field.name, parse(value))


@dataclass
class Genre(SQLiteData):
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())


@dataclass
class FilmWork(SQLiteData):
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime
    rating: float
    type: str
    file_path: str = ''
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())


@dataclass
class Person(SQLiteData):
    id: uuid.UUID
    full_name: str
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())


@dataclass
class GenreFilmWork(SQLiteData):
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime = field(default=datetime.now())


@dataclass
class PersonFilmWork(SQLiteData):
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime = field(default=datetime.now())


TABLE_MATCHING = {
    Genre: 'genre',
    FilmWork: 'film_work',
    Person: 'person',
    GenreFilmWork: 'genre_film_work',
    PersonFilmWork: 'person_film_work',
}

MAPPING = {
    Person: {
        'destination_table': 'person',
        'attribute_to_column': {
             'id': 'id',
             'full_name': 'full_name',
             'created_at': 'created',
             'updated_at': 'modified',
        },
    },
    FilmWork: {
        'destination_table': 'film_work',
        'attribute_to_column': {
            'id': 'id',
            'title': 'title',
            'description': 'description',
            'rating': 'rating',
            'type': 'type',
            'creation_date': 'creation_date',
            'created_at': 'created',
            'updated_at': 'modified',
        },
    },
    Genre: {
        'destination_table': 'genre',
        'attribute_to_column': {
             'id': 'id',
             'name': 'name',
             'description': 'description',
             'created_at': 'created',
             'updated_at': 'modified',
        },
    },
    GenreFilmWork: {
        'destination_table': 'genre_film_work',
        'attribute_to_column': {
             'id': 'id',
             'genre_id': 'genre_id',
             'film_work_id': 'film_work_id',
             'created_at': 'created',
        },
    },
    PersonFilmWork: {
        'destination_table': 'person_film_work',
        'attribute_to_column': {
             'id': 'id',
             'person_id': 'person_id',
             'role': 'role',
             'film_work_id': 'film_work_id',
             'created_at': 'created',
        },
    },
}
