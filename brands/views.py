from rest_framework import generics, viewsets
from .serializer import *
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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