from django.urls import path, include
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.shortcuts import render 
from . import views
from django.conf import settings

app_name = 'userprofile'

urlpatterns = [
    # Authentication
    path('sign-in/', views.SignInView.as_view(), name='sign_in'),
    path('logout/', views. LogoutView.as_view(), name='logout'),
    
    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

