from django.contrib.auth.models import AbstractUser
from django.db import models


class Tool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    JOB_TITLE_CHOICES = [
        ("Engineer", "Engineer"),
        ("Data Scientist", "Data Scientist"),
        ("Product Manager", "Product Manager"),
        # Add other job titles as necessary
    ]

    job_title = models.CharField(
        max_length=100, blank=True, null=True, choices=JOB_TITLE_CHOICES
    )
    tools = models.ManyToManyField(
        Tool, related_name="users_with_access", blank=True
    )
    role = models.CharField(
        max_length=50,
        choices=[("Admin", "Admin"), ("User", "User")],
        default="User",
    )
    is_verified = models.BooleanField(
        default=False
    )  # For handling email verification or admin approval

    def __str__(self):
        return self.username

    def has_tool_access(self, tool_name):
        """Check if the user has access to a specific tool."""
        return self.tools.filter(name=tool_name).exists()
