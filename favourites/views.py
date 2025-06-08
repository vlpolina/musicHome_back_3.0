from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from shop.models import Favourite, FavouriteItem, Product

# Получить избранное авторизованного пользователя
class GetView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получение избранного текущего пользователя",
        operation_description="Для авторизованных пользователей. Получает избранное текущего пользователя",
        responses={200: FavouriteItemSerializer(many=True)}
    )
    def get(self, request):
        favourite, _ = Favourite.objects.get_or_create(client_id=request.user)
        items = FavouriteItem.objects.filter(favourite=favourite)
        serializer = FavouriteItemSerializer(items, many=True)
        return Response(serializer.data)


add_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['product_id'],
    properties={
        'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID товара'),
    },
)

# Добавить товар в избранное
class AddView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=add_request_schema,
        operation_summary="Добавление товара в избранное",
        operation_description="Для авторизованных пользователей. Позволяет добавить товар в избранное. Если товар уже в избранном - вернуть сообщение об этом",
        responses={
            200: openapi.Response(description="Товар добавлен"),
            404: "Товар не найден"
        }
    )
    def post(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "product_id обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id, is_published=True)
        except Product.DoesNotExist:
            return Response({"error": "Товар не найден или не опубликован"}, status=status.HTTP_404_NOT_FOUND)

        favourite, created = Favourite.objects.get_or_create(client_id=request.user)
        item = FavouriteItem.objects.filter(favourite=favourite, product=product).first()
        if item:
            return Response({"message": "Товар уже был добавлен в избранное"}, status=status.HTTP_200_OK)
        else:
            FavouriteItem.objects.create(favourite=favourite, product=product)

        return Response({"message": "Товар добавлен в избранное"}, status=status.HTTP_200_OK)


# Удалить один товар
class DeleteOneView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Удаление товара из избранного",
        operation_description="Для авторизованных пользователей. Позволяет удалить один товар из избранного по ID FavouriteItem",
        responses={
            200: openapi.Response(description="Удалено"),
            404: "Товар не найден в избранном"
        }
    )
    def delete(self, request, pk):
        try:
            favourite = Favourite.objects.get(client_id=request.user)
            favourite_item = FavouriteItem.objects.get(pk=pk, favourite=favourite)
            favourite_item.delete()
            return Response({"message": "Товар удален из избранного"}, status=status.HTTP_200_OK)
        except (Favourite.DoesNotExist, FavouriteItem.DoesNotExist):
            return Response({"error": "Товар не найден в избранном"}, status=status.HTTP_404_NOT_FOUND)


# Очистить избранное
class ResetView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Очистка избранного",
        operation_description="Для авторизованных пользователей. Удаляет все избранные товары текущего пользователя",
        responses={
            200: openapi.Response(description="Избранные очищены"),
            404: "Избранные не найдены"
        }
    )
    def delete(self, request):
        try:
            favourite = Favourite.objects.get(client_id=request.user)
            FavouriteItem.objects.filter(favourite=favourite).delete()
            return Response({"message": "Избранные очищены"}, status=status.HTTP_200_OK)
        except Favourite.DoesNotExist:
            return Response({"error": "Избранные не найдены"}, status=status.HTTP_404_NOT_FOUND)