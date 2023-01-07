import csv

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from reviews.models import Comment, User, Review

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

                try:
                    comment_id = row['id']

                    Comment.objects.create(
                        id=row['id'],
                        review=get_object_or_404(
                            Review, id=row['review_id']
                        ),
                        text=row['text'],
                        author=get_object_or_404(
                            User, id=row['author']
                        )
                    )

                except IntegrityError as err:
                    self.stdout.write(
                        f'Комментарий c id {comment_id} уже внесен в базу. '
                        f'Ошибка внесения - {err}'
                    )

                else:
                    self.stdout.write(
                        f'Комментарий c id {comment_id} внесен в базу.'
                    )
