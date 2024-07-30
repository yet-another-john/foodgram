"""Data import script."""

import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Класс команды."""

    help = 'Импорт в базу данных.'

    def handle(self, *args, **options):
        """Обработчик."""
        self.import_ingredients()

    def import_ingredients(self):
        """Функция загрузки данных."""
        file_path = 'data/ingredients.csv'

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)

            for row in reader:
                ingredient = Ingredient.objects.create(
                    name=row[0],
                    measurement_unit=row[1]
                )
                ingredient.save()
