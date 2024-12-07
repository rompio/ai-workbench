from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),  # Matches /admin/
    path(
        "", include("home.urls")
    ),  # Matches /home/ and forwards to home/urls.py
    path(
        "users/", include("users.urls")
    ),  # Matches /users/ and forwards to users/urls.py
    path("job_hunter/", include("job_hunter.urls")),  # Matches /job_hunter/
]
