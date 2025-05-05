from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("users/", include("users.urls")),
    path("job_hunter/", include("job_hunter.urls")),
    path('health-tracker/', include('health_tracker.urls')),
    path('movie-rater/', include('movie_rater.urls')),
    path('household-manager/', include('household_manager.urls')),
]
