from django import forms
from .models import Camera

class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['name', 'ip_address', 'stream_url', 'device_type', 'brand']  # 👈 stream_url ist dabei
