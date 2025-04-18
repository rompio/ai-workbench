from django.urls import path
from django.shortcuts import redirect
from .views import (
    dashboard_view,
    personal_data_view,
    offers_view,
    ai_assistant_view,
    search_view,
)

app_name = "job_hunter"

urlpatterns = [
    path("", lambda request: redirect("job_hunter:dashboard")), 
    path("dashboard/", dashboard_view, name="dashboard"),
    path("personal-data/", personal_data_view, name="personal_data"),
    path("offers/", offers_view, name="offers"),
    path("ai-assistant/", ai_assistant_view, name="ai_assistant"),
    path("search/", search_view, name="search"),
]
