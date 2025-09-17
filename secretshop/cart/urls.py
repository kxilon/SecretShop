from django.contrib.auth.urls import urlpatterns
from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    path('detail/', views.CartDetail.as_view(), name='cart_detail'),
    path('add/', views.CartAdd.as_view(), name='cart_add'),
    path('change/', views.CartChange.as_view(), name='cart_change'),
    path("checkout/", views.checkout_notify, name="checkout_notify"),
]