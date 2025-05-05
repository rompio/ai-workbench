from django.urls import path
from . import views

app_name = 'health_tracker'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
