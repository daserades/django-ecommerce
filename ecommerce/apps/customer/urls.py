from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('customer-login/',views.LoginView.as_view(),name='customer_login'),
    path('customer-logout/',views.LogoutView.as_view(),name='customer_logout'),
    path('customer-profile/',views.customer_profile,name='customer_profile'),
    path('customer-control/',views.customer_control,name='customer_control'),
    path('password-update/',views.password_update,name='password_update'),
    path('password-success/',views.password_success,name='password_success'),
    path('edit-customer/',views.edit_customer, name='edit_customer'),
    path('<int:customer_id>/', views.orders, name='customer'),
]