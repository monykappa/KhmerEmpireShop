from django.shortcuts import render
from .models import *
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductListView(LoginRequiredMixin, ListView):
    model = LaptopSpec
    template_name = 'products/products.html'
    context_object_name = 'laptop_specs'
    