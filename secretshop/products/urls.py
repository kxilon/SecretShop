from django.contrib import admin
from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductList.as_view(), name='catalog'),
    path('product/<slug:product_slug>/', views.ShowProduct.as_view(), name='product'),
    path('category/<slug:category_slug>/', views.ProductCategory.as_view(), name='categories'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

]