from django.contrib import admin
from django.urls import path, include
from onlineShop import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic import RedirectView



schema_view = get_schema_view(
   openapi.Info(
      title="Документация API",
      default_version='v1',
      description="API для веб-приложения Интернет-магазин музыкальных инструментов",
      contact=openapi.Contact(email="vlasova2002polina18@gmail.ru"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('brands/', include('brands.urls', namespace='brands')),
    path('catalog/', include('shop.urls', namespace='catalog')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('categories/', include('categories.urls', namespace='categories')),
    path('deliveries/', include('deliveries.urls', namespace='deliveries')),
    path('favourites/', include('favourites.urls', namespace='favourites')),
    path('feedbacks/', include('feedbacks.urls', namespace='feedbacks')),
    path('orders/', include('orders.urls', namespace='orders')),
    # swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)