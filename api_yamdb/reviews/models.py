from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser
)
from django.utils.translation import gettext_lazy as _
from django.db import models


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


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя',
        max_length=max([len(value) for role, value in ROLES]),
        choices=ROLES, default=USER,
    )
    email = models.EmailField('Почта пользователя', unique=True)
    confirmation_code = models.CharField(
        'Токен подтверждения', max_length=50, blank=True
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    def __str__(self):
        return self.username


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
        User, on_delete=models.CASCADE,
        related_name='review'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='review'
    )
    score = models.CharField(
        max_length=2,
        choices=SCORE_CHOICES,
        default='1',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text[:settings.FIRST_SYMBOLS_NUMBER]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comment'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comment'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text[:settings.FIRST_SYMBOLS_NUMBER]
