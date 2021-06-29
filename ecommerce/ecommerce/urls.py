from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendors/',include('apps.vendor.urls')),
    path('cart/',include('apps.cart.urls')),
    path('customer/',include('apps.customer.urls')),
    path('', include('apps.sendemail.urls')),
    path('', include('apps.core.urls')),
    path('',include('apps.product.urls')),


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)