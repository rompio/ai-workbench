from django.db import models
from users.models import CustomUser


class PInfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    background = models.TextField(blank=True, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Offer(models.Model):
    POSITION_CHOICES = [
        ('Software Engineer', 'Software Engineer'),
        ('Data Scientist', 'Data Scientist'),
        ('Product Manager', 'Product Manager'),
        # Add other positions as necessary
    ]
    
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)
    company = models.CharField(max_length=200)
    offer = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    status = models.IntegerField(default=0)  # You could make this a choice field if needed
    response = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='offers')

    def __str__(self):
        return f"{self.position} at {self.company}"
    

class Application(models.Model):
    resume = models.TextField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return f"Application by {self.user.username} for {self.offer.position}"
    

class ChatLog(models.Model):
    user_input = models.TextField()
    assistant_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_logs')

    def __str__(self):
        return f"Chat with {self.user.username} at {self.created_at}"