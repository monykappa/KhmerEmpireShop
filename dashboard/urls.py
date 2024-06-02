from django.urls import path, include
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.shortcuts import render 
from . import views
from django.conf import settings

app_name = 'dashboard'

urlpatterns = [
    # path('base/', views.base, name='base'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/sign_in/', views.DashboardSignInView.as_view(), name='sign_in'),
    path('dashboard/logout/', views.DashboardLogoutView.as_view(), name='logout'),
    
    
    path('dashboard/order/', views.OrderHistoryView.as_view(), name='order'),
    
    path('dashboard/products/', views.ProductListView.as_view(), name='product_list'),
    path('dashboard/products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    path('dashboard/order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

