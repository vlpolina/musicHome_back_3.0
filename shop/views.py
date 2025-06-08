from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# получение всех опубликованных товаров + статус корзина / избранное
class ProductsList(generics.ListAPIView):
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductCatalogSerializer

    @swagger_auto_schema(
        operation_summary="Получение всех опубликованных товаров для каталога",
        operation_description="Для всех пользователей. Возвращает массив всех опубликованных товаров. Если запрос выполняет авторизованный пользователь, то также возвращает статусы товаров из каталога для данного пользователя - добавлены ли товары в корзину и избранное",
        responses={
            200: ProductCatalogSerializer,
        }
    )
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# получение товаров одной категории + статус корзина / избранное
class CatalogOneCatList(generics.ListAPIView):
    serializer_class = ProductCatalogSerializer

    @swagger_auto_schema(operation_summary="Получение товаров одной категории",
                         operation_description="Для всех пользователей. Фильтрация опубликованных товаров по категории товара. Если запрос выполняет авторизованный пользователь, то также возвращает статусы товаров из каталога для данного пользователя - добавлены ли товары в корзину и избранное")
    def get_queryset(self):
        cat_id = self.kwargs['cat_id']
        queryset = Product.objects.filter(cat=cat_id, is_published=True)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# получение товаров одного бренда + статус корзина / избранное
class CatalogOneBrandList(generics.ListAPIView):
    serializer_class = ProductCatalogSerializer

    @swagger_auto_schema(operation_summary="Получение товаров одного бренда",
                         operation_description="Для всех пользователей. Фильтрация опубликованных товаров по выбранному бренду. Если запрос выполняет авторизованный пользователь, то также возвращает статусы товаров из каталога для данного пользователя - добавлены ли товары в корзину и избранное")
    def get_queryset(self):
        brand_id = self.kwargs['brand_id']
        queryset = Product.objects.filter(brand_name=brand_id, is_published=True)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# получение 1 товара + статус корзина / избранное
class ProductDetailView(APIView):
    @swagger_auto_schema(operation_summary="Получение одного товара",
                         operation_description="Для всех пользователей. Получение подробной информации о товаре. Если запрос выполняет авторизованный пользователь, то также возвращает статусы товара для данного пользователя - добавлен ли он в корзину и избранное",
                         responses={200: ProductSerializer})
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug, is_published=True)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)


# CRUD для администратора
class AdminProductsSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = AdminProductsSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminUser, )