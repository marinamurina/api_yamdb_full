import csv

from django.db import IntegrityError
from django.core.management.base import BaseCommand
from reviews.models import User

from api_yamdb.settings import IMPORT_DATA_ADRESS


class Command(BaseCommand):
    help = 'Импортирует базу данных для модели User из файла csv'

    def handle(self, *args, **options):

        with open(
            f'{IMPORT_DATA_ADRESS}/users.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:

                try:
                    user_id = row['id']

                    User.objects.create(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        confirmation_code=row['confirmation_code'],
                    )

                except IntegrityError as err:
                    self.stdout.write(
                        f'Юзер с id {user_id} уже внесен в базу. '
                        f'Ошибка внесения - {err}'
                    )

                else:
                    self.stdout.write(
                        f'Юзер с id {user_id} внесен в базу.'
                    )
