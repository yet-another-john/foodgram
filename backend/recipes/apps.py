"""Apps."""

from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """Приложение рецепты."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
