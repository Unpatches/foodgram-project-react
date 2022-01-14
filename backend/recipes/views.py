from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from api import filters, permissions, pagination
from .models import Favorite, Ingredient, ShoppingList, Recipe, Tag
from .serializers import (CreateRecipeSerializer, FavouriteSerializer,
                          IngredientSerializer, ShoppingListSerializer,
                          ReadyRecipeSerializer, TagSerializer)
from .file import send_file


class TagsViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None


class IngredientsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.RecipeFilter
    pagination_class = pagination.CustomPageNumberPaginator

    def get_serializer_class(self):
        return (
            ReadyRecipeSerializer if self.request.method == 'GET' else
            CreateRecipeSerializer
        )

    @action(
        detail=True,
        methods=['POST', ],
        permission_classes=[permissions.IsAuthorOrAdmin]
    )
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = FavouriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        get_object_or_404(
            Favorite,
            user=request.user,
            recipe=get_object_or_404(Recipe, id=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', ],
        permission_classes=[permissions.IsAuthorOrAdmin]
    )
    def shopping_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = ShoppingListSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        get_object_or_404(
            ShoppingList,
            user=request.user,
            recipe=get_object_or_404(Recipe, id=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated, ])
    def download_shopping_cart(self, request):
        return send_file(
            request, f'Список покупок: {request.user}.txt'
        )
