from django.urls import path

from .views import *

app_name = 'favourites'

urlpatterns = [
    path('get/', GetView.as_view(), name="get"),
    path('add/', AddView.as_view(), name="add"),
    path('delete/<int:pk>/', DeleteOneView.as_view(), name="delete"),
    path('reset/', ResetView.as_view(), name="reset"),
]
