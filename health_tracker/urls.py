from django.urls import path, include
from . import views

app_name = "health_tracker"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("week-planner/", include("week_planner.urls", namespace="week_planner")),
    path("workout/", include("workout.urls", namespace="workout")),
    path("food/", include("food.urls", namespace="food_list")),
    path("profile/", include("users.urls", namespace="users")),
    path("ai-assistant/", include("ai_assistant.urls", namespace="ai_assistant")),
]
