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
    # heaklth_tracker apps:
    path("week-planner/", include("week_planner.urls", namespace="week_planner")),
    path("ai_assistant/", include("ai_assistant.urls", namespace="ai_assistant")),
    path("food/", include("food.urls", namespace="food")),
    path("workout/", include("workout.urls", namespace="workout")),
    path('cam-manager/', include('cam_manager.urls')),
]
