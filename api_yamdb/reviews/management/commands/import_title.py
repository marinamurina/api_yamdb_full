import csv

from django.db import IntegrityError
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from reviews.models import Categories, Title

from api_yamdb.settings import IMPORT_DATA_ADRESS


class Command(BaseCommand):
    help = 'Импортирует базу данных для модели Title из файла csv'

    def handle(self, *args, **options):

        with open(
            f'{IMPORT_DATA_ADRESS}/titles.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:

                try:
                    title_name = row['name']

                    Title.objects.create(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category=get_object_or_404(
                            Categories, id=row['category']
                        )
                    )

                except IntegrityError as err:
                    self.stdout.write(
                        f'Произведение "{title_name}" уже внесено в базу. '
                        f'Ошибка внесения - {err}'
                    )

                else:
                    self.stdout.write(
                        f'Произведение "{title_name}" внесено в базу.'
                    )
