import csv

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.shortcuts import get_object_or_404
from reviews.models import Review, User

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
                review = Review()
                review.id = row['id']
                review.title_id = row['title_id']
                review.author = get_object_or_404(User, id=row['author'])

                criterion1 = Q(title_id=review.title_id)
                criterion2 = Q(author=review.author)

                if Review.objects.filter(id=review.id).exists():
                    self.stdout.write(
                        f'Рецензия с id {review.id}'
                        f' уже существует в базе.'
                    )

                elif Review.objects.filter(
                    criterion1 & criterion2
                ).exists():
                    self.stdout.write(
                        f'Рецензия юзера {review.author.username}'
                        f' на произведение {review.title.name}'
                        f' уже существует в базе.'
                    )

                else:
                    review = Review()
                    review.id = row['id']
                    review.title_id = row['title_id']
                    review.text = row['text']
                    review.author = get_object_or_404(
                        User, id=row['author']
                    )
                    review.score = row['score']
                    review.pub_date = row['pub_date']
                    review.save()

                    self.stdout.write(
                        f'Рецензия с id {review.id} внесена в базу.'
                    )
