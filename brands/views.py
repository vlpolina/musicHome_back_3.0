from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Avg, Prefetch
from shop.models import Brand, Product



# получить список брендов для фильтра
class BrandsList(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


# CRUD для администратора
class AdminBrandSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = AdminBrandSerializer
    lookup_field = 'brand_id'
    permission_classes = (IsAdminUser, )



class BrandStatsView(APIView):
    permission_classes = (IsAdminUser, )

    @swagger_auto_schema(
        operation_summary="Статистика по брендам",
        operation_description="""
            Возвращает список брендов с их статистикой:
            - количество товаров;
            - список категорий, в которых представлены товары бренда;
            - средняя цена товаров бренда.
            
            Только для администратора.
        """,
        responses={
            200: BrandStatsSerializer(many=True),
            403: "Нет доступа (только для администратора)"
        },
    )
    def get(self, request):
        stats = []

        brands = Brand.objects.prefetch_related(
            Prefetch('product_set', queryset=Product.objects.select_related('cat'))
        )

        for brand in brands:
            products = brand.product_set.all()
            total_products = products.count()

            if total_products == 0:
                continue

            categories = list(set(p.cat.name for p in products))
            avg_price = round(products.aggregate(Avg('price'))['price__avg'], 2)

            stats.append({
                'brand_id': brand.brand_id,
                'name': brand.name,
                'total_products': total_products,
                'categories': categories,
                'average_price': avg_price,
            })

        serializer = BrandStatsSerializer(stats, many=True)
        return Response(serializer.data)