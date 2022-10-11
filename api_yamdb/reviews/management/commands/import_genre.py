import csv

from django.core.management.base import BaseCommand
from reviews.models import Genres

from api_yamdb.settings import IMPORT_DATA_ADRESS


class Command(BaseCommand):
    help = 'Импортирует базу данных для модели Genres из файла csv'

    def handle(self, *args, **options):

        with open(
            f'{IMPORT_DATA_ADRESS}/genre.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:
                genre = Genres()
                genre.id = row['id']
                genre.name = row['name']
                genre.slug = row['slug']

                if Genres.objects.filter(id=genre.id).exists():
                    self.stdout.write(
                        f'Жанр с id {genre.id} уже существует в базе.'
                    )

                elif Genres.objects.filter(name=genre.name).exists():
                    self.stdout.write(
                        f'Жанр c именем {genre.name}'
                        f' уже существует в базе.'
                    )

                elif Genres.objects.filter(slug=genre.slug).exists():
                    self.stdout.write(
                        f'Жанр со слагом {genre.slug}'
                        f' уже существует в базе.'
                    )

                else:
                    genre = Genres()
                    genre.id = row['id']
                    genre.name = row['name']
                    genre.slug = row['slug']
                    genre.save()

                    self.stdout.write(
                        f'Жанр {genre.name} внесен в базу.'
                    )
