from django.db import models
from django.conf import settings


SCORE_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
)

# Models for Categories, Genres, Title


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
    )

    slug = models.SlugField(unique=True)


class Genres(models.Model):
    name = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    year = models.IntegerField()

    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )

    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        blank=True
    )


class Review(models.Model):
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='review'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review'
    )
    score = models.CharField(
        max_length=2,
        choices=SCORE_CHOICES,
        default='1',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text[:settings.FIRST_SYMBOLS_NUMBER]


class Comment(models.Model):
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='comment'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comment'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text[:settings.FIRST_SYMBOLS_NUMBER]
