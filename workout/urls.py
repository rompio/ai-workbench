from django.urls import path
from . import views
from django.urls import path, include
from django.urls import path
from . import views
app_name = "workout"

urlpatterns = [
    path('overview/', views.overview_view, name='overview'),
    path('add_activityA', views.add_activity, name="add_activity"),
]
