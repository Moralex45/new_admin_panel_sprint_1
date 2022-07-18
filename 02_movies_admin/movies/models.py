import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """Модель. Атрибуты создания и редактирования"""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """UUID основной ключ"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Жанр фильма."""

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    """Фильм или телешоу."""

    MIN_RATING = 0
    MAX_RATING = 100

    class Filmwork_types(models.TextChoices):
        MOVIE = 'MV', ('Movie')
        TV_SHOW = 'TV', ('TV Show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[
            MinValueValidator(MIN_RATING),
            MaxValueValidator(MAX_RATING)
        ]
    )
    type = models.CharField(
        _('type'),
        max_length=2,
        choices=Filmwork_types.choices
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = _('film work')
        verbose_name_plural = _('film works')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    """Связь между фильмами и жанрами (Много ко многим)."""

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class Person(UUIDMixin, TimeStampedMixin):
    """"""

    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        db_table = 'content\".\"person'
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"

    def __str__(self):
        return self.role
