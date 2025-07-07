from django.db import models
from django.conf import settings

class Camera(models.Model):
    DEVICE_TYPES = [
        ('tuya', 'Tuya Camera'),
        ('okam', 'O-KAM Pro Camera'),
        ('other', 'Andere'),
    ]

    BRANDS = [
        ('tuya', 'Tuya'),
        ('okam', 'O-KAM Pro'),
        ('unknown', 'Unbekannt'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES, default='tuya')
    brand = models.CharField(max_length=20, choices=BRANDS, default='tuya')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CameraType(models.Model):
    """
    Typen von Kameras wie Tuya, O-KAM Pro etc.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


