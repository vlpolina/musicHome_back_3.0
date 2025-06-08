from django.urls import path, include

from .views import *
from rest_framework import routers

app_name = 'catalog'

routerAdmin = routers.SimpleRouter()
routerAdmin.register(r'crud-products', AdminProductsSet, basename='admin_crud_products')

urlpatterns = [
    path('get-all/', ProductsList.as_view(), name="all_products"),
    path('filter-by-brand/<int:brand_id>/', CatalogOneBrandList.as_view(), name="filter_by_brand"),
    path('filter-by-category/<int:cat_id>/', CatalogOneCatList.as_view(), name="filter_by_category"),
    path('<slug:slug>/', ProductDetailView.as_view(), name="product"),
    path('admin/', include(routerAdmin.urls), name="crud_product"),
]
