from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from backend.constants import (MAX_LENGTH_OF_FIRST_NAME,
                               MAX_LENGTH_OF_LAST_NAME,
                               MAX_LENGTH_OF_PASS)


class User(AbstractUser):

    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(RegexValidator(r'^[\w.@+-]+\Z'),),
    )
    first_name = models.CharField(max_length=MAX_LENGTH_OF_FIRST_NAME)
    last_name = models.CharField(max_length=MAX_LENGTH_OF_LAST_NAME)
    password = models.CharField(max_length=MAX_LENGTH_OF_PASS)
    avatar = models.ImageField(
        upload_to='users/images/',
        null=True,
        default=None
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "password", ]

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='follower',
        verbose_name='подписчик',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='author',
        verbose_name='автор',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'author'],
                name='unique_following'
            )
        ]

    def __str__(self):
        return f'{self.follower} - {self.author}'
