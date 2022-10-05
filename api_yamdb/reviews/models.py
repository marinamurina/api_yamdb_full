from django.db import models

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
