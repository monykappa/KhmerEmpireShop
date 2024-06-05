# import
from venv import logger
from rest_framework import generics
from products.models import LaptopSpec
from .serializers import LaptopSpecSerializer
from rest_framework.generics import RetrieveAPIView
from orders.models import *
from products.models import *
from userprofile.models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



class LaptopSpecListAPI(generics.ListAPIView):
    queryset = LaptopSpec.objects.all()
    serializer_class = LaptopSpecSerializer

class ProductDetailBySlugAPI(RetrieveAPIView):
    queryset = LaptopSpec.objects.all()
    serializer_class = LaptopSpecSerializer
    lookup_field = 'slug'