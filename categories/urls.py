from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'categories'

routerAdmin = routers.SimpleRouter()
routerAdmin.register(r'crud-categories', AdminCategorySet, basename='admin_crud_categories')

urlpatterns = [
    path('get-all/', CategoriesList.as_view(), name="get_all"),
    path('admin/', include(routerAdmin.urls), name="crud_categories"),
]