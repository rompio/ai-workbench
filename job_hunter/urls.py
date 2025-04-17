from django.urls import path
from django.shortcuts import redirect
from .views import dashboard_view

app_name = "job_hunter"

urlpatterns = [
    path("", lambda request: redirect("job_hunter:dashboard")), 
    path("dashboard/", dashboard_view, name="dashboard"),
]
