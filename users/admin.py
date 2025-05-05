from django.contrib import admin
from .models import CustomUser, Tool


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email"]
    filter_horizontal = ["tools"] 


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tool)
