# cam_manager/urls.py

from django.urls import path
from . import views

app_name = 'cam_manager'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]
