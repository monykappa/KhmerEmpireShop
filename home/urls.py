from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.contrib import admin
from django.conf import settings 
from django.conf.urls.static import static
from home import views



app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('base/', BaseView.as_view(), name='base'),
    path('', HomeAuth.as_view(), name='home_auth'),
    
    path('products/', ProductListView.as_view(), name='product_list'),  
    path('products/<slug:slug>/', product_detail, name='product_detail'),
    
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment_complete/', views.payment_complete, name='payment_complete'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('order-history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('order-history/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    
    
    # authentication
    path('sign-in/', SignInView.as_view(), name='sign_in'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
