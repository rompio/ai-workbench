from django.contrib import admin
from .models import Meal, FoodEntry

# Meal im Admin registrieren
admin.site.register(Meal)

# FoodEntry im Admin registrieren
class FoodEntryAdmin(admin.ModelAdmin):
    list_display = ('meal', 'name', 'kcal', 'Fett', 'Eiweiß', 'Kohlenhydrate', 'amount_in_grams')
    search_fields = ('name',)
    list_filter = ('meal',)

admin.site.register(FoodEntry, FoodEntryAdmin)
