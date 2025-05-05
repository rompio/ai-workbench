from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class Tool(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    is_pro = models.BooleanField(default=False)
    tools = models.ManyToManyField(Tool, blank=True)
