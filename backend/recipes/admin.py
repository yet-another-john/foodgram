# isort: skip_file
"""Admin."""

from django.contrib import admin

from foodgram.constants import EMPTY_VALUE, MIN_VALUE_OF_INGREDIENTS
from .models import (Favorite, Ingredient, IngredientInRecipe,
                     Recipe, ShoppingList, ShortLink, Tag)
from .mixins import AdminMixin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Администрирование для модели тэгов."""

    list_display = (
        'id',
        'name',
        'slug',
    )
    list_filter = (
        'name',
        'slug',
    )
    empty_value_display = EMPTY_VALUE


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Администрирование для модели ингредиентов."""

    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
    empty_value_display = EMPTY_VALUE


class IngredientInLine(admin.TabularInline):
    """IngredientInLine."""

    model = IngredientInRecipe
    extra = 5
    min_num = MIN_VALUE_OF_INGREDIENTS


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Администрирование для модели рецептов."""

    list_display = (
        'id',
        'name',
        'author',
        'text',
        'cooking_time',
        'image',
        'amount_of_favorites',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    search_fields = (
        'name',
        'author',
    )
    empty_value_display = EMPTY_VALUE
    inlines = (IngredientInLine,)

    @admin.display(description='Количество в избранном')
    def amount_of_favorites(self, obj):
        """Количество в избранном."""
        return obj.favorites.count()


@admin.register(Favorite)
class FavoriteAdmin(AdminMixin):
    """Администрирование для модели избранного."""

    pass


@admin.register(ShoppingList)
class ShoppingListAdmin(AdminMixin):
    """Администрование для модели списка покупок."""

    pass


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    """Администрирование для модели коротких ссылок."""

    list_display = (
        'full_url',
        'short_url',
    )
    search_fields = ('full_url', 'short_url')
