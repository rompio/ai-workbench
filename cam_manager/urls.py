from django.urls import path
from . import views

app_name = 'cam_manager'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_camera, name='add_camera'),
]
