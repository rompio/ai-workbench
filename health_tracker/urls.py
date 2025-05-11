from django.urls import path, include

app_name = "health_tracker"

urlpatterns = [
    path("week-planner/", include("week_planner.urls", namespace="week_planner")),
    path("workout/", include("workout.urls", namespace="workout")),
    path("food/", include("food.urls", namespace="food")),
    path("profile/", include("users.urls", namespace="users")),
    path("ai-assistant/", include("ai_assistant.urls", namespace="ai_assistant")),
]
