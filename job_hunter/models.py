from django.conf import settings
from django.db import models
from users.models import CustomUser


class PInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    background = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Offer(models.Model):
    STATUS_CHOICES = [
        (1, 'Open'),
        (2, 'Applied'),
        (3, 'Rejected'),
        (4, 'Accepted'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    offer = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    response = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.position} at {self.company}"

class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    resume = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application by {self.user} for {self.offer}"

class ChatLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_input = models.TextField()
    assistant_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatLog for {self.user} at {self.created_at}"
