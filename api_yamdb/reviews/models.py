from django.conf import settings
from django.db import models

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

class Review(models.Model):
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='review'
    )
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, related_name='review'
    )
    score = models.CharField(
        max_length=2,
        choices=SCORE_CHOICES,
        default = '1',
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
