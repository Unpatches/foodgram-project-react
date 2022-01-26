from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientForRecipe, Recipe,
                     ShoppingList, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '- пусто -'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '- пусто -'


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientForRecipe
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('name', 'author', 'is_favorited')
    search_fields = ('name', 'tags', 'author')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '- пусто -'

    def is_favorited(self, obj):
        return obj.is_favorited.all().count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('recipe', )
    empty_value_display = '- пусто -'


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('recipe', )
    empty_value_display = '- пусто -'
