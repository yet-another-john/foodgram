from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from backend.constants import (MAX_LENGTH_OF_INGREDIENT,
                               MAX_LENGTH_OF_UNIT,
                               MAX_LENGTH_OF_TAG,
                               MAX_LENGTH_OF_TAG_SLUG,
                               MAX_LENGTH_OF_RECIPE)

from users.models import User

class Ingredient(models.Model):

    name = models.CharField('Ингредиент', max_length=MAX_LENGTH_OF_INGREDIENT,)
    measurement_unit = models.CharField('Единица измерения',
                                        max_length=MAX_LENGTH_OF_UNIT)

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
            ),
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField('Тег', max_length=MAX_LENGTH_OF_TAG)
    slug = models.CharField('Слаг', max_length=MAX_LENGTH_OF_TAG_SLUG)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиент',
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True, null=True,
        default=None,
        verbose_name='Изображение'
    )
    name = models.CharField('Название', max_length=MAX_LENGTH_OF_RECIPE)
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(1)],
    )

    author_id = models.PositiveSmallIntegerField('Время приготовления')

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ингредиент',
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество',
    )

    class Meta:
        default_related_name = 'recipe_ingredient'
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredient} {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_shopping_cart'
            )
        ]
