import csv

from django.core.management.base import BaseCommand
from reviews.models import Categories

from api_yamdb.settings import IMPORT_DATA_ADRESS


class Command(BaseCommand):
    help = 'Импортирует базу данных для модели Categories из файла csv'

    def handle(self, *args, **options):

        with open(
            f'{IMPORT_DATA_ADRESS}/category.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:
                category = Categories()
                category.id = row['id']
                category.name = row['name']
                category.slug = row['slug']

                if Categories.objects.filter(id=category.id).exists():
                    self.stdout.write(
                        f'Категория с id {category.id}'
                        f'уже существует в базе.'
                    )

                elif Categories.objects.filter(name=category.name).exists():
                    self.stdout.write(
                        f'Категория с именем {category.name}'
                        f'уже существует в базе.'
                    )

                elif Categories.objects.filter(slug=category.slug).exists():
                    self.stdout.write(
                        f'Категория со слагом {category.slug}'
                        f'уже существует в базе.'
                    )

                else:
                    category = Categories()
                    category.id = row['id']
                    category.name = row['name']
                    category.slug = row['slug']
                    category.save()

                    self.stdout.write(
                        f'Категория {category.name} внесена в базу.'
                    )
