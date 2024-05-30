from django.urls import path, include
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.shortcuts import render 
from . import views
from django.conf import settings

app_name = 'orders'

urlpatterns = [
    path('add-to-cart/<slug:slug>/',views. AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('clear-cart/', views.ClearCartView.as_view(), name='clear_cart'),
    path('payment_complete/', views.PaymentCompleteView.as_view(), name='payment_complete'),
    
    path('order-history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('order-history/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    
    path('paypal/', include('paypal.standard.ipn.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

