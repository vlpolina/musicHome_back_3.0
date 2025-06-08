from django.urls import path

from .views import *

app_name = 'feedbacks'

urlpatterns = [
    path('add/', AddView.as_view(), name="add"),
    path('update/', UpdateView.as_view(), name="update"),
    path('delete/<int:pk>/', DeleteView.as_view(), name="delete"),
    path('admin-answer/', AnswerByAdminView.as_view(), name="admin_answer"),
    path('get/<int:pk>/', GetView.as_view(), name="get"),
    path('block-by-admin/', BlockByAdminView.as_view(), name="admin_block"),
]
