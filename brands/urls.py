from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'brands'

routerAdmin = routers.SimpleRouter()
routerAdmin.register(r'crud-brands', AdminBrandSet, basename='admin_crud_brand')

urlpatterns = [
    path('get-all/', BrandsList.as_view(), name="brands_list"),
    path('admin/', include(routerAdmin.urls), name="crud_brands"),
    path('admin/stats/', BrandStatsView.as_view(), name="brand_stats")
]
