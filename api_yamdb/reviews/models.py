from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории', max_length=256, unique=True)
    slug = models.SlugField(
        verbose_name='Идентификатор категории', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256, unique=True)
    slug = models.SlugField(
        verbose_name='Идентификатор жанра',
        max_length=50, unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256)

    year = models.IntegerField(
        verbose_name='Год создания',
        validators=[validate_year])

    description = models.TextField(
        verbose_name='Описание',
        null=True, blank=True)

    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр',
        related_name="titles",)

    category = models.ForeignKey(
        Category, blank=True,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles', null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['category', 'name']

    def __str__(self):
        return f'Title {self.name}, genre {self.genre}, {self.year}'


class GenreTitle(models.Model):
    """Модель создания связи между произведениями и их жанрами."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_genre_for_a_title'
            )
        ]

    def __str__(self):
        return f'GenreTitle {self.pk}, title {self.title},' \
               f'genre {self.genre}.'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',)

    text = models.TextField(
        verbose_name='Текст',)

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',)

    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        default=1,
        validators=[
            MinValueValidator(1, 'Оценка должна быть больше 1.'),
            MaxValueValidator(10, 'Оценка должна быть меньше 10.'),
        ],

    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Комментарий',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст коментария',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['review', 'author']

    def __str__(self):
        return self.text[:10]
