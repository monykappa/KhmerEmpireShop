from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.contrib import admin
from django.conf import settings 
from django.conf.urls.static import static
from .views import ProductListView 

app_name = 'products'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),  
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

