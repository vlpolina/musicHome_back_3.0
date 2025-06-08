from django.urls import path

from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'accounts'

urlpatterns = [
    path('signup/', RegisterUser.as_view(), name='registrate'),
    path('token/forgot-password/', EmailForPassword.as_view(), name='forgot_password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('check-admin/', CheckAdminView.as_view(), name='check_admin'),
    path('user/', UserView.as_view(), name='user'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
