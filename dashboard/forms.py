from django import forms
from products.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['slug']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['cpu'] = forms.ModelChoiceField(queryset=CpuSpec.objects.all(), required=False)
        self.fields['gpu'] = forms.ModelMultipleChoiceField(queryset=GpuSpec.objects.all(), required=False)
        self.fields['memory'] = forms.ModelChoiceField(queryset=MemorySpec.objects.all(), required=False)
        self.fields['storage'] = forms.ModelChoiceField(queryset=StorageSpec.objects.all(), required=False)
        self.fields['display'] = forms.ModelChoiceField(queryset=DisplaySpec.objects.all(), required=False)
        self.fields['port'] = forms.ModelMultipleChoiceField(queryset=PortSpec.objects.all(), required=False)
        self.fields['wireless_connectivity'] = forms.ModelMultipleChoiceField(queryset=WirelessConnectivity.objects.all(), required=False)
        self.fields['webcam'] = forms.ModelChoiceField(queryset=WebcamSpec.objects.all(), required=False)
        self.fields['battery'] = forms.ModelChoiceField(queryset=BatterySpec.objects.all(), required=False)
        self.fields['operating_system'] = forms.ModelChoiceField(queryset=OperatingSystem.objects.all(), required=False)