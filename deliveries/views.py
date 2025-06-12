from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from .serializer import *
from rest_framework.views import APIView
from django.db.models import Count, Avg, Sum
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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


# Статистика использования способов доставки (только для админов)
class DeliveryStatsView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Статистика использования способов доставки",
        responses={200: DeliveryStatsSerializer(many=True)},
    )
    def get(self, request):
        stats = Delivery.objects.annotate(
            total_orders=Count('order'),
            avg_time=Avg('delivery_time'),
            total_revenue=Sum('order__orderitem__sum_cost')
        ).values('delivery_id', 'type', 'total_orders', 'avg_time', 'total_revenue')

        serializer = DeliveryStatsSerializer(stats, many=True)
        return Response(serializer.data)


# Фильтрация способов доставки по стоимости и времени
class FilteredDeliveriesView(generics.ListAPIView):
    serializer_class = DeliverySerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('max_cost', openapi.IN_QUERY, description="Максимальная стоимость доставки",
                              type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_time', openapi.IN_QUERY, description="Максимальное время доставки (часы)",
                              type=openapi.TYPE_INTEGER),
        ],
        operation_summary="Фильтрация способов доставки по стоимости и времени",
        responses={200: DeliverySerializer(many=True)},
    )
    def get_queryset(self):
        qs = Delivery.objects.all()
        max_cost = self.request.query_params.get('max_cost')
        max_time = self.request.query_params.get('max_time')
        if max_cost is not None:
            try:
                max_cost = float(max_cost)
                qs = qs.filter(cost__lte=max_cost)
            except ValueError:
                pass
        if max_time is not None:
            try:
                max_time = int(max_time)
                qs = qs.filter(delivery_time__lte=max_time)
            except ValueError:
                pass
        return qs