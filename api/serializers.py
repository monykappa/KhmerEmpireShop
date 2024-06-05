from rest_framework import serializers
from products.models import *


class CpuBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CpuBrand
        fields = ['name']

class GpuBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpuBrand
        fields = ['name']

class CpuSpecSerializer(serializers.ModelSerializer):
    cpu_brand = CpuBrandSerializer()

    class Meta:
        model = CpuSpec
        fields = ['model', 'cpu_brand', 'cores', 'threads', 'cpu_detail']

class GpuSpecSerializer(serializers.ModelSerializer):
    gpu_brand = GpuBrandSerializer()

    class Meta:
        model = GpuSpec
        fields = ['model', 'gpu_brand', 'vram', 'vram_type', 'gpu_detail']

class MemorySpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemorySpec
        fields = ['capacity', 'type', 'speed', 'memory_brand']

class StorageSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageSpec
        fields = ['type', 'capacity', 'capacity_type', 'interface', 'read_speed', 'write_speed', 'form_factor', 'storage_brand']

class DisplaySpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplaySpec
        fields = ['display', 'display_detail']

class PortSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortSpec
        fields = ['port']

class WirelessConnectivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WirelessConnectivity
        fields = ['wireless_connectivity']

class WebcamSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebcamSpec
        fields = ['webcam', 'webcam_detail']

class BatterySpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatterySpec
        fields = ['battery', 'battery_detail']

class OperatingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingSystem
        fields = ['operating_system', 'operating_system_detail']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    brand = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    color = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['name', 'model', 'brand', 'description', 'price', 'category', 'color', 'year', 'warranty_months', 'warranty_years', 'images']

class LaptopSpecSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    cpu = CpuSpecSerializer()
    gpu = GpuSpecSerializer(many=True)
    memory = MemorySpecSerializer()
    storage = StorageSpecSerializer()
    display = DisplaySpecSerializer()
    port = PortSpecSerializer(many=True)
    wireless_connectivity = WirelessConnectivitySerializer(many=True)
    webcam = WebcamSpecSerializer()
    battery = BatterySpecSerializer()
    operating_system = OperatingSystemSerializer()

    class Meta:
        model = LaptopSpec
        fields = '__all__'
