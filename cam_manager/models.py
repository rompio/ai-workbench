# cam_manager/models.py

from django.db import models
from django.conf import settings

class CameraType(models.Model):
    """
    Typen von Kameras wie Tuya, O-KAM Pro etc.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Camera(models.Model):
    """
    Einzelne Kamera, die einem Benutzer gehört
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    camera_type = models.ForeignKey(CameraType, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    stream_url = models.URLField(blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Optional: Standort oder Beschreibung
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
