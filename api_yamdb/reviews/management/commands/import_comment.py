import csv

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.shortcuts import get_object_or_404
from reviews.models import Comment, User

from api_yamdb.settings import IMPORT_DATA_ADRESS


class Command(BaseCommand):
    help = 'Импортирует базу данных для модели Comment из файла csv'

    def handle(self, *args, **options):

        with open(
            f'{IMPORT_DATA_ADRESS}/comments.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:
                comment = Comment()
                comment.id = row['id']
                comment.review_id = row['review_id']
                comment.text = row['text']
                comment.author = get_object_or_404(User, id=row['author'])

                criterion1 = Q(review_id=comment.review_id)
                criterion2 = Q(author=comment.author)
                criterion2 = Q(text=comment.text)

                if Comment.objects.filter(id=comment.id).exists():
                    self.stdout.write(
                        f'Комментарий с id {comment.id}'
                        f' уже существует в базе.'
                    )

                elif Comment.objects.filter(
                    criterion1 & criterion2 & criterion2
                ).exists():
                    self.stdout.write(
                        f'Комментарий юзера {comment.author.username}'
                        f' на рецензию id {comment.review.id}'
                        f' c текстом "{comment.text}" уже существует в базе.'
                    )

                else:
                    comment = Comment()
                    comment.id = row['id']
                    comment.review_id = row['review_id']
                    comment.text = row['text']
                    comment.author = get_object_or_404(User, id=row['author'])
                    comment.pub_date = row['pub_date']
                    comment.save()

                    self.stdout.write(
                        f'Комментарий с id {comment.id} внесен в базу.'
                    )
