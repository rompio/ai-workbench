from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tool


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        "username",
        "email",
        "job_title",
        "role",
        "is_verified",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + (
        (
            "Zusätzliche Felder",
            {
                "fields": (
                    "job_title",
                    "tools",
                    "role",
                    "is_verified",
                ),
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Zusätzliche Felder",
            {
                "fields": (
                    "job_title",
                    "tools",
                    "role",
                    "is_verified",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tool)
