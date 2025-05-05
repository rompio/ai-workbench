from django.urls import path
from . import views

app_name = 'household_manager'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
