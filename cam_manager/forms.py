from django import forms
from .models import Camera

class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['name', 'ip_address', 'device_type', 'brand']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'device_type': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
        }
