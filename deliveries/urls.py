from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'deliveries'

routerAdmin = routers.SimpleRouter()
routerAdmin.register(r'crud-deliveries', AdminDeliverySet, basename='admin_crud_deliveries')

urlpatterns = [
    path('get-all/', DeliveriesList.as_view(), name="get_all"),
    path('admin/', include(routerAdmin.urls), name="crud_deliveries"),
]