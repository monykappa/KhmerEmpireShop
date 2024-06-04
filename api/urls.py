from django.urls import path, include
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.shortcuts import render 
from . import views
from django.conf import settings


urlpatterns = [
    path('api/products/', views.LaptopSpecListAPI.as_view(), name='products-api'),
    path('api/products/<slug:slug>/', views.ProductDetailBySlugAPI.as_view(), name='product-detail-api'),

    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

