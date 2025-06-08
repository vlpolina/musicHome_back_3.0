from django.urls import path

from .views import *

app_name = 'cart'

urlpatterns = [
    path('get/', GetView.as_view(), name="get"),
    path('add/', AddView.as_view(), name="add"),
    path('change-count/', ChangeCount.as_view(), name="change_count"),
    path('delete/<int:pk>/', DeleteOneView.as_view(), name="delete"),
    path('reset/', ResetView.as_view(), name="reset"),
]
