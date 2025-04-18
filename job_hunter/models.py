from django.conf import settings
from django.db import models
from users.models import CustomUser
from django.utils import timezone
from django.contrib.auth.models import User

class PInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pinfo")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    background = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

class Offer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    offer_text = models.TextField()
    about_company = models.TextField()
    url = models.URLField()
    response = models.BooleanField(default=False)  # True or False
    status_choices = [
        (0, 'None'),
        (1, 'Open'),
        (2, 'Applied'),
        (3, 'Rejected'),
        (4, 'Accepted')
    ]
    status = models.IntegerField(choices=status_choices, default=0)

    def __str__(self):
        return f"{self.position} at {self.company}"
    
class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE, related_name='applications')
    resume = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Application by {self.user.username} for {self.offer.position}"

class ChatLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_logs')
    user_input = models.TextField()
    assistant_response = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ChatLog ({self.user.username}) @ {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

class Tool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name