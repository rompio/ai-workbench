from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("job_hunter.urls")),  # Link to the job_hunter app's URLs
]
