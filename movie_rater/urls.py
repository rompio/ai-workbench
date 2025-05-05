from django.urls import path
from . import views

app_name = 'movie_rater'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
