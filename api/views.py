# import
from rest_framework import generics
from products.models import LaptopSpec
from .serializers import LaptopSpecSerializer
from rest_framework.generics import RetrieveAPIView


class LaptopSpecListAPI(generics.ListAPIView):
    queryset = LaptopSpec.objects.all()
    serializer_class = LaptopSpecSerializer

class ProductDetailBySlugAPI(RetrieveAPIView):
    queryset = LaptopSpec.objects.all()
    serializer_class = LaptopSpecSerializer
    lookup_field = 'slug'