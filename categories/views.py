from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from .serializer import *


# получение категорий товаров для фильтра
class CategoriesList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# CRUD для администратора
class AdminCategorySet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = AdminCategorySerializer
    lookup_field = 'category_id'
    permission_classes = (IsAdminUser, )