from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        unique=True,
        max_length=50,
    )
    color = models.CharField(
        verbose_name='Цвет тега',
        unique=True,
        max_length=50,
    )
    slug = models.SlugField(
        verbose_name='Ссылка на тег',
        unique=True,
        max_length=150,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Мера измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=50, verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение',
    )
    text = models.TextField(
        max_length=1000, verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientForRecipe',
        verbose_name='Ингредиенты',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Ошибка. Время не может быть меньше 1.'),
            validators.MaxValueValidator(
                6000, message='Ошибка. Недопустимое значение времени')
        ),
        verbose_name='Время приготовления'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientForRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_amounts',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_amounts',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Ошибка. Ингредиентов не может быть меньше 1.'),
            validators.MaxValueValidator(
                10000, message='Ошибка. Ингредиентов слишком много.')
        ),
        verbose_name='Количество ингредиентов',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient',
            )
        ]
        verbose_name = 'Ингредиенты'

    def __str__(self):
        return f'{self.ingredient}: {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorite',
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        related_name='is_favorited',
        on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
            )
        ]

    def __str__(self):
        return f'{self.recipe}: {self.user}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        related_name='purchase',
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE, )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.recipe}: {self.user}'
