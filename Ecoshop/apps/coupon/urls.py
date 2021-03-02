from django.urls import path
from . import views


urlpatterns = [
    path('apply-coupon/', views.CuponApply, name='apply-coupon')

]
