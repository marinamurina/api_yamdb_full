import csv

from django.db import IntegrityError
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

                try:
                    title_genre_id = row['id']
                    title_id = row['title_id']
                    genre_id = row['genre_id']
                    title = Title.objects.get(id=title_id)
                    genre = Genres.objects.get(id=genre_id)

                    TitleGenres.objects.create(
                        id=title_genre_id,
                        title=title,
                        genre=genre,
                    )

                except IntegrityError as err:
                    self.stdout.write(
                        f'Связь "{title.name}" '
                        f'c "{genre.name}" уже внесена в базу. '
                        f'Ошибка внесения - {err}'
                    )

                except (Title.DoesNotExist, Genres.DoesNotExist):
                    self.stdout.write(
                        f'Произведения с id {title_id} '
                        f'или жанра с id {genre_id} нет в базе. '
                        f'Необходимо сначала добавить их в базу.'
                    )

                else:
                    self.stdout.write(
                        f'Связь "{title.name}" '
                        f'c "{genre.name}" внесена в базу.'
                    )
