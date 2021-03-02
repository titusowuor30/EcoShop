from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('become_vendor/', views.become_vendor, name='become_vendor'),
    path('vendor_admin/', views.vendor_admin, name='vendor_admin'),

    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:id>/', views.add_product, name='edit_product'),
    path('delete_product/<int:id>/', views.product_delete, name='delete_product'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='vendor/login.html'), name='login'),
]
