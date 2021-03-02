from django.urls import path
from . import views


urlpatterns = [
   path('',views.show_cart,name='cart'),
   path('checkout/',views.cart_detail,name='checkout'),
   path('success/', views.success, name='success'),

]
