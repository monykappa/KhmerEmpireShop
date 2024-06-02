from django import forms
from products.models import *


class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False) 

    class Meta:
        model = Product
        exclude = ['slug']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['cpu'] = forms.ModelChoiceField(
            queryset=CpuSpec.objects.all(), 
            required=False, 
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['gpu'] = forms.ModelMultipleChoiceField(
            queryset=GpuSpec.objects.all(), 
            required=False, 
            widget=forms.SelectMultiple(attrs={'class': 'form-control'})
        )
        self.fields['memory'] = forms.ModelChoiceField(
            queryset=MemorySpec.objects.all(), 
            required=False, 
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['storage'] = forms.ModelChoiceField(
            queryset=StorageSpec.objects.all(), 
            required=False, 
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['display'] = forms.ModelChoiceField(
            queryset=DisplaySpec.objects.all(), 
            required=False, 
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['port'] = forms.ModelMultipleChoiceField(
            queryset=PortSpec.objects.all(), 
            required=False, 
            widget=forms.SelectMultiple(attrs={'class': 'form-control'})
        )
        self.fields['wireless_connectivity'] = forms.ModelMultipleChoiceField(
            queryset=WirelessConnectivity.objects.all(), 
            required=False, 
            widget=forms.SelectMultiple(attrs={'class': 'form-control'})
        )
        self.fields['webcam'] = forms.ModelChoiceField(
            queryset=WebcamSpec.objects.all(), 
            required=False, 
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['battery'] = forms.ModelChoiceField(
            queryset=BatterySpec.objects.all(), 
            required=False, 
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['operating_system'] = forms.ModelChoiceField(
            queryset=OperatingSystem.objects.all(), 
            required=False, 
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    def save(self, commit=True):
        instance = super(ProductForm, self).save(commit=False)
        image = self.cleaned_data.get('image')
        if image:
            product_image = ProductImage(product=instance, image=image)
            if commit:
                product_image.save()
        if commit:
            instance.save()
        return instance