from django.urls import path
from . import views

app_name = "week_planner"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("create/", views.create_plan, name="create_plan"),
]
