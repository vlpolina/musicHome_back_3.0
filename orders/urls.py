from django.urls import path

from .views import *

app_name = 'orders'

urlpatterns = [
    path('create/', CreateView.as_view(), name="create"),
    path('cancel/<int:pk>/', CancelView.as_view(), name="cancel"),
    path('view-history/', HistoryView.as_view(), name="view_history"),
    path('details/<int:pk>/', DetailsView.as_view(), name="details"),
]
