from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Meal

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_meals(sender, instance, created, **kwargs):
    if created:  # Nur bei neu erstellten Benutzern
        default_meals = ["Breakfast", "Lunch", "Dinner", "Snack"]
        for meal_name in default_meals:
            Meal.objects.create(user=instance, name=meal_name)
