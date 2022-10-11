import csv

from django.core.management.base import BaseCommand
from django.db.models import Q
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
                title = Title()
                title.id = row['id']
                title.name = row['name']
                title.year = row['year']
                title.category = get_object_or_404(
                    Categories, id=row['category']
                )

                criterion1 = Q(name=title.name)
                criterion2 = Q(category=title.category)
                criterion3 = Q(year=title.year)

                if Title.objects.filter(id=title.id).exists():
                    self.stdout.write(
                        f'Произведение с id {title.id}'
                        f' уже существует в базе.'
                    )

                elif Title.objects.filter(
                    criterion1 & criterion2 & criterion3
                ).exists():
                    self.stdout.write(
                        f'Произведение {title.name} {title.year} года'
                        f' уже существует в этой категории.'
                    )

                else:
                    title = Title()
                    title.id = row['id']
                    title.name = row['name']
                    title.year = row['year']
                    title.category = get_object_or_404(
                        Categories, id=row['category']
                    )
                    title.save()

                    self.stdout.write(
                        f'Произведение {title.name} внесено в базу.'
                    )
