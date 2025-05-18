from django.db import models
from django.conf import settings

class WeekPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WeekPlan {self.id} for {self.user.username} ({self.created_at.strftime('%Y-%m-%d')})"
