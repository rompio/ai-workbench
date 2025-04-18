from django.contrib.auth.models import AbstractUser
from django.db import models


class Tool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    is_verified = models.BooleanField(
        default=False
    )  # Für die Verwaltung der Verifizierung des Benutzers (z.B. E-Mail-Verifizierung)

    def __str__(self):
        return self.username
