from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from .serializer import *


# получение способов доставки товаров для заказа
class DeliveriesList(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


# CRUD для администратора
class AdminDeliverySet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = AdminDeliverySerializer
    lookup_field = 'delivery_id'
    permission_classes = (IsAdminUser, )