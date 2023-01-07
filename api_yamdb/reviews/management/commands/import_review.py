import csv

from django.db import IntegrityError
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from reviews.models import Review, User, Title

from api_yamdb.settings import IMPORT_DATA_ADRESS


class Command(BaseCommand):
    help = 'Импортирует базу данных для модели Review из файла csv'

    def handle(self, *args, **options):

        with open(
            f'{IMPORT_DATA_ADRESS}/review.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:

                try:
                    review_id = row['id']

                    Review.objects.create(
                        id=row['id'],
                        title=get_object_or_404(
                            Title, id=row['title_id']
                        ),
                        text=row['text'],
                        author=get_object_or_404(
                            User, id=row['author']
                        ),
                        score=row['score'],
                        pub_date=row['pub_date']
                    )

                except IntegrityError as err:
                    self.stdout.write(
                        f'Рецензия с id {review_id} уже внесена в базу. '
                        f'Ошибка внесения - {err}'
                    )

                else:
                    self.stdout.write(
                        f'Рецензия с id {review_id} внесена в базу.'
                    )
