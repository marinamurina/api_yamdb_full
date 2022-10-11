import csv

from django.core.management.base import BaseCommand
from reviews.models import Genres, Title, TitleGenres

from api_yamdb.settings import IMPORT_DATA_ADRESS


class Command(BaseCommand):
    help = 'Импортирует базу данных для связей Genres-Title из файла csv'

    def handle(self, *args, **options):

        with open(
            f'{IMPORT_DATA_ADRESS}/genre_title.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:
                genre = Genres()
                title = Title()
                title_genre = TitleGenres()
                title_genre.id = row['id']
                title.id = row['title_id']
                genre.id = row['genre_id']

                if TitleGenres.objects.filter(id=title_genre.id).exists():
                    self.stdout.write(
                        f'Связь {title.name} - {genre.name}'
                        f'уже существует в базе.'
                    )

                elif TitleGenres.objects.filter(
                    title=title.id, genre=genre.id
                ).exists():
                    self.stdout.write(
                        f'Связь {title.name} - {genre.name}'
                        f'уже существует в базе.'
                    )

                else:
                    genre = Genres()
                    title = Title()
                    title_genre = TitleGenres()
                    title_genre.id = row['id']
                    title.id = row['title_id']
                    genre.id = row['genre_id']
                    genre.save()

                    self.stdout.write(
                        f'Связь "{title.name} - {genre.name}" внесена в базу.'
                    )
