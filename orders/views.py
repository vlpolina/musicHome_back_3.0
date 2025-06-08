from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from shop.models import Order, OrderItem, Cart, CartItem, Delivery
from .serializer import (
    CreateOrderSerializer,
    OrderDetailSerializer,
    OrderHistorySerializer,
)

# создание заказа и получение уведомления об этом на эл. почту
class CreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Создание заказа",
        operation_description="Для авторизованных пользователей. Создает заказ на основе выбранных товаров из корзины. Не выбранные товары остаются в корзине. Нельзя создать заказ с пустой корзиной. Также отправляет уведомление об оформлении заказа на почту",
        request_body=CreateOrderSerializer,
        responses={
            201: openapi.Response(description="Заказ успешно создан"),
            400: openapi.Response(description="Ошибка: пустая корзина или неверные данные"),
        }
    )
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        cart = Cart.objects.filter(client_id=user).first()
        if not cart:
            return Response({"error": "Корзина не найдена"}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({"error": "Корзина пуста"}, status=status.HTTP_400_BAD_REQUEST)

        address = serializer.validated_data["address"]
        delivery_id = serializer.validated_data["delivery_id"]
        items = serializer.validated_data["items"]

        delivery = Delivery.objects.get(pk=delivery_id)
        selected_ids = [item["product_id"] for item in items]
        selected_cart_items = cart_items.filter(product_id__in=selected_ids)

        if not selected_cart_items.exists():
            return Response({"error": "Выбранные товары не найдены в корзине"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            client_id=user,
            cart_id=cart,
            address=address,
            delivery_type=delivery
        )

        for item in items:
            product_id = item["product_id"]
            count = item["count"]
            try:
                cart_item = selected_cart_items.get(product_id=product_id)
            except CartItem.DoesNotExist:
                continue

            if count > cart_item.count:
                return Response({"error": f"Недостаточно товара: {cart_item.product.name}"}, status=status.HTTP_400_BAD_REQUEST)

            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                count=count,
                sum_cost=cart_item.product.price * count
            )

            if count == cart_item.count:
                cart_item.delete()
            else:
                cart_item.count -= count
                cart_item.sum_cost = cart_item.count * cart_item.product.price
                cart_item.save()

        # Отправка письма
        send_mail(
            subject="Оформление заказа",
            message=f"Ваш заказ №{order.order_id} успешно оформлен! Вы можете посмотреть детали или отменить его в личном кабинете!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True
        )

        return Response({"message": "Заказ успешно создан", "order_id": order.order_id}, status=201)


# отмена незавершенного заказа
class CancelView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(client_id=self.request.user)

    @swagger_auto_schema(
        operation_summary="Отмена заказа",
        operation_description="Для авторизованных пользователей. Позволяет отменить незавершённый заказ по его ID",
        responses={
            200: openapi.Response(description="Заказ успешно отменён"),
            400: openapi.Response(description="Заказ уже завершён, отмена невозможна"),
            404: openapi.Response(description="Заказ не найден"),
        }
    )
    def delete(self, request, pk):
        try:
            order = Order.objects.get(order_id=pk, client_id=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)

        if order.status or order.payment_status:
            return Response({"error": "Завершенный заказ нельзя отменить"}, status=status.HTTP_400_BAD_REQUEST)

        order.delete()
        return Response({"message": "Заказ отменен"}, status=status.HTTP_200_OK)


# просмотр истории заказов
class HistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderHistorySerializer

    @swagger_auto_schema(
        operation_summary="История заказов",
        operation_description="Для авторизованных пользователей. Возвращает список заказов пользователя с датой, адресом, типом доставки и общей суммой",
        responses={
            200: openapi.Response(description="Список заказов", schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT)
            )),
        }
    )
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(client_id=self.request.user)


# просмотр информации об одном заказе
class DetailsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderDetailSerializer
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_summary="Детали заказа",
        operation_description="Для авторизованных пользователей. Возвращает подробную информацию по заказу, включая товары, количество и стоимость",
        responses={
            200: openapi.Response(description="Подробности заказа", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
            )),
            404: openapi.Response(description="Заказ не найден"),
        }
    )
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(client_id=self.request.user)
