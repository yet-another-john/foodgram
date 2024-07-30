"""App user."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """User config class."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
