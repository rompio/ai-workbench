from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", include("home.urls")),  # Include home app URLs
    path("users/", include("users.urls")),
    path("job_hunter/", include("job_hunter.urls")),
]
