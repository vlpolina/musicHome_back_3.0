from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from shop.models import Cart, CartItem, Product

# Получить корзину авторизованного пользователя
class GetView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получение корзины текущего пользователя",
        operation_description="Для авторизованных пользователей. Получает корзину текущего пользователя",
        responses={200: CartItemSerializer(many=True)}
    )
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(client_id=request.user)
        items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)


add_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['product_id'],
    properties={
        'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID товара'),
    },
)

# Добавить товар в корзину
class AddView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=add_request_schema,
        operation_summary="Добавление товара в корзину",
        operation_description="Для авторизованных пользователей. Добавляет товар в корзину. Если товар уже в корзине — увеличивает его количество на 1.",
        responses={
            200: openapi.Response(description="Товар добавлен"),
            400: "Ошибка (товар закончился или превышен лимит)",
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

        if product.amount < 1:
            return Response({"error": "Товар закончился на складе"}, status=status.HTTP_400_BAD_REQUEST)

        cart, created = Cart.objects.get_or_create(client_id=request.user)
        item = CartItem.objects.filter(cart=cart, product=product).first()
        if item:
            if item.count + 1 < product.amount:
                item.count += 1
                item.sum_cost = item.count * product.price
                item.save()
            else:
                return Response({"error": "Товар закончился на складе"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            CartItem.objects.create(cart=cart, product=product, count=1, sum_cost=product.price)

        return Response({"message": "Товар добавлен в корзину"}, status=status.HTTP_200_OK)


change_count_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['product_id', 'count'],
    properties={
        'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID товара'),
        'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Новое количество'),
    },
)

# Изменить количество товара в корзине
class ChangeCount(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=change_count_schema,
        operation_summary="Изменение количества товара в корзине",
        operation_description="Для авторизованных пользователей. Изменяет количество товара в корзине",
        responses={
            200: openapi.Response(description="Количество обновлено"),
            400: "Ошибка валидации",
            404: "Элемент не найден"
        }
    )
    def put(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "product_id обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        new_count = request.data.get('count')
        if not new_count:
            return Response({"error": "count обязателен"}, status=status.HTTP_400_BAD_REQUEST)
        new_count=int(new_count)
        if new_count < 1:
            return Response({"error": "Количество должно быть не меньше 1"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
            cart = Cart.objects.get(client_id=request.user)
            cart_item = CartItem.objects.get(cart=cart, product=product)
        except (Product.DoesNotExist, Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({"error": "Элемент корзины не найден"}, status=status.HTTP_404_NOT_FOUND)

        if new_count > product.amount:
            return Response({"error": "Недостаточно товара на складе"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.count = new_count
        cart_item.sum_cost = new_count * product.price
        cart_item.save()
        return Response({"message": "Количество товара в корзине обновлено"}, status=status.HTTP_200_OK)


# Удалить один товар
class DeleteOneView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Удаление товара из корзины",
        operation_description="Для авторизованных пользователей. Позволяет удалить один товар из корзины по ID CartItem",
        responses={
            200: openapi.Response(description="Удалено"),
            404: "Товар не найден в корзине"
        }
    )
    def delete(self, request, pk):
        try:
            cart = Cart.objects.get(client_id=request.user)
            cart_item = CartItem.objects.get(pk=pk, cart=cart)
            cart_item.delete()
            return Response({"message": "Товар удален из корзины"}, status=status.HTTP_200_OK)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({"error": "Товар не найден в корзине"}, status=status.HTTP_404_NOT_FOUND)


# Очистить корзину
class ResetView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Очистка корзины текущего пользователя",
        operation_description="Для авторизованных пользователей. Удаляет все товары из корзины текущего пользователя",
        responses={
            200: openapi.Response(description="Корзина очищена"),
            404: "Корзина не найдена"
        }
    )
    def delete(self, request):
        try:
            cart = Cart.objects.get(client_id=request.user)
            CartItem.objects.filter(cart=cart).delete()
            return Response({"message": "Корзина очищена"}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Корзина не найдена"}, status=status.HTTP_404_NOT_FOUND)