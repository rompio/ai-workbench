from django.urls import path
from . import views

app_name = 'food'

urlpatterns = [
    path('', views.meal_list, name='overview'),
    path('meal/<int:meal_id>/<str:date>/', views.meal_detail, name='detail'),
    path('search_food/', views.search_food, name='search_food'),
    path('create-recipe/', views.create_recipe, name='create_recipe'),
    path('add-ingredients/<int:recipe_id>/', views.add_ingredients, name='add_ingredients'),
    path('day/<str:date>/', views.meal_list_by_date, name='meal_list_by_date'),
    path('meal/<int:meal_id>/<str:date>/nutrient_overview/', views.nutrient_overview, name='nutrient_overview'),
    path('daily-nutrient-overview/<str:date>/', views.daily_nutrient_overview, name='daily_nutrient_overview'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),

]
