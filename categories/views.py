from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from .serializer import *
from django.db import models


# получение категорий товаров для фильтра
class CategoriesList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# CRUD для администратора
class AdminCategorySet(viewsets.ModelViewSet):
    serializer_class = AdminCategorySerializer
    lookup_field = 'category_id'
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        return Category.objects.annotate(product_count=models.Count('product'))