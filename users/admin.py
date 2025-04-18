# users/admin.py
from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    # Entferne job_title und role, da sie im Modell nicht mehr existieren
    list_display = ["username", "first_name", "last_name", "email"]


admin.site.register(CustomUser, CustomUserAdmin)
