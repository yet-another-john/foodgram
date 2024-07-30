"""Serializers for project."""

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingList, ShortLink, Tag)
from foodgram.constants import BASE_USER_FIELDS_LIMIT
from users.models import Follow, User


class BaseUserSerializer(serializers.ModelSerializer):
    """Сериалайзация модели пользователей."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        """BaseUserSerializer."""

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_is_subscribed(self, obj):
        """Is user subscribed."""
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and Follow.objects.filter(
                user=request.user,
                author=obj,
            ).exists()
        )


class PutUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователей (аватар)."""

    avatar = Base64ImageField(allow_null=True)

    class Meta:
        """PutUserSerializer."""

        model = User
        fields = (
            'avatar',
        )

    def validate_avatar(self, data):
        """Функция валидации поля аватар."""
        if not data:
            raise serializers.ValidationError(
                'Аватар - это обязательное поле.'
            )
        return data


class FavoriteAndShoppingDataSerializer(serializers.ModelSerializer):
    """Сериалайзация модели пользователей (избранное, корзина)."""

    image = Base64ImageField()

    class Meta:
        """Favorite and cart serializer."""

        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class BaseFavoriteAndShoppingSerializer(serializers.ModelSerializer):
    """Cериализатор базовый (избранное, корзина)."""

    name_of_model = ''

    class Meta:
        """BaseSerializer."""

        model = None
        fields = (
            'user',
            'recipe',
        )
        read_only_fields = ('user',)

    def validate(self, data):
        """Валидация рецептов."""
        user = self.context.get('request').user
        recipe = data.get('recipe')
        if self.Meta.model.objects.filter(
            user=user,
            recipe=recipe,
        ).exists():
            raise ValidationError(
                f'Рецепт уже добавлен в {self.name_of_model}'
            )
        return data

    def to_representation(self, instance):
        """."""
        return FavoriteAndShoppingDataSerializer(
            instance.recipe,
            context=self.context,
        ).data


class FavoriteSerializer(BaseFavoriteAndShoppingSerializer):
    """Сериализатор для модели избранного."""

    name_of_model = 'избранное'

    class Meta(BaseFavoriteAndShoppingSerializer.Meta):
        """FavoriteSerializer."""

        model = Favorite


class ShoppingSerializer(BaseFavoriteAndShoppingSerializer):
    """Сериализатор для модели списка покупок."""

    name_of_model = 'список покупок'

    class Meta(BaseFavoriteAndShoppingSerializer.Meta):
        """Сериализатор для модели списка покупок."""

        model = ShoppingList


class FollowRepresentationSerializer(BaseUserSerializer):
    """Сериализатор для рецептов."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='recipes.count')

    class Meta(BaseUserSerializer.Meta):
        """FollowRepresentationSerializer."""

        model = User
        fields = (
            BaseUserSerializer.Meta.fields[:BASE_USER_FIELDS_LIMIT] + (
                'recipes',
                'recipes_count',
                'avatar',
            )
        )

    def get_recipes(self, obj):
        """Получение рецептов."""
        request = self.context.get('request')
        queryset = obj.recipes.all()
        limit = request.query_params.get('recipes_limit')
        if limit:
            try:
                queryset = queryset[:int(limit)]
            except (TypeError, ValueError):
                pass
        return FavoriteAndShoppingDataSerializer(
            queryset,
            many=True,
        ).data


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели подписок."""

    class Meta:
        """FollowSerializer."""

        model = Follow
        fields = (
            'author',
            'user',
        )
        validators = [
            UniqueTogetherValidator(
                fields=('author', 'user'),
                queryset=model.objects.all(),
                message='Вы уже подписаны на автора.',
            )
        ]

    def validate_author(self, data):
        """Валидация автора."""
        if self.context.get('request').user == data:
            raise ValidationError(
                'Подписаться на себя нельзя.'
            )
        return data

    def to_representation(self, instance):
        """."""
        return FollowRepresentationSerializer(
            instance.author,
            context=self.context,
        ).data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        """TagSerializer."""

        model = Tag
        fields = (
            'id',
            'name',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        """IngredientSerializer."""

        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиентов в рецепте."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.ReadOnlyField()

    class Meta:
        """IngredientInRecipeSerializer."""

        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class CreateIngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания ингредиента в рецепте."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
    )

    class Meta:
        """CreateIngredientInRecipeSerializer."""

        model = IngredientInRecipe
        fields = (
            'id',
            'amount',
        )


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = BaseUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredients_in_recipe',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        """RecipeGetSerializer."""

        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def _get_item(self, obj, model):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and model.objects.filter(
                user=request.user,
                recipe=obj,
            ).exists()
        )

    def get_is_favorited(self, obj):
        """Избранное."""
        return self._get_item(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        """Покупки."""
        return self._get_item(obj, ShoppingList)


class RecipeCUDSerializer(serializers.ModelSerializer):
    """Сериализатор для создания, удаления и редактирования рецептов."""

    ingredients = CreateIngredientInRecipeSerializer(
        many=True,
        source='ingredients_in_recipe'
    )
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )

    @staticmethod
    def _set_ingredients_and_tags(ingredients, tags, recipe):
        recipe.tags.set(tags)
        ingredients_in_recipe = []
        for ingredient in ingredients:
            ingredients_in_recipe.append(
                IngredientInRecipe(
                    recipe=recipe,
                    ingredient=ingredient.get('ingredient'),
                    amount=ingredient.get('amount'),
                )
            )
        IngredientInRecipe.objects.bulk_create(ingredients_in_recipe)

    def validate(self, data):
        """Валидация тэгов."""
        tags = data.get('tags', [])
        if not tags:
            raise ValidationError(
                'Добавьте тэг к рецепту.'
            )

        if len(tags) != len(set(tags)):
            raise ValidationError(
                'Нельзя добавлять одинаковые тэги.'
            )

        ingredients = data.get('ingredients_in_recipe', [])
        if not ingredients:
            raise ValidationError('Не добавлен ингредиент(ы).')

        unique_ingredients = set()
        for ingredient in ingredients:
            unique_ingredient = ingredient.get('ingredient')
            unique_ingredients.add(unique_ingredient)

        if len(ingredients) != len(unique_ingredients):
            raise ValidationError(
                'Нельзя добавлять одинаковые ингредиенты в рецепт.'
            )

        return data

    def validate_image(self, data):
        """Валидация изображения."""
        if not data:
            raise serializers.ValidationError(
                'Изображение - это обязательное поле.'
            )
        return data

    def create(self, validated_data):
        """Создание рецепта."""
        ingredients = validated_data.pop('ingredients_in_recipe', [])
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(
            author=self.context.get('request').user, **validated_data,
        )
        self._set_ingredients_and_tags(
            ingredients,
            tags,
            recipe,
        )
        return recipe

    def update(self, instance, validated_data):
        """Обновление рецепта."""
        ingredients = validated_data.pop('ingredients_in_recipe', [])
        tags = validated_data.pop('tags', [])
        instance.ingredients.clear()
        instance.tags.clear()
        self._set_ingredients_and_tags(
            ingredients,
            tags,
            instance,
        )
        return super().update(instance, validated_data)

    class Meta:
        """RecipeCUDSerializer."""

        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def to_representation(self, instance):
        """."""
        return RecipeGetSerializer(instance, context=self.context).data


class ShortLinkSerializer(serializers.ModelSerializer):
    """Сериализатор для модели коротких ссылок."""

    class Meta:
        """ShortLinkSerializer."""

        model = ShortLink
        fields = '__all__'

    def create(self, validated_data):
        """Создание коротких ссылок."""
        full_url = validated_data['full_url']
        short_url, _ = ShortLink.objects.get_or_create(
            full_url=full_url,
        )
        return short_url

    def to_representation(self, instance):
        """."""
        return {'short-link': instance}
