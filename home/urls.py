from django.urls import path
from . import views

app_name = "home"  # This is important for namespacing

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),  # Dashboard URL
]
