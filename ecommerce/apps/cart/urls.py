from django.urls import path

from . import views
from apps.customer import views as customer_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.cart_detail, name='cart'),
    path('success/', views.success, name='success'),
    path('problem/', views.problem, name='problem'),
    path('customer-login/',customer_views.LoginView.as_view(),name='customer_login'),
]