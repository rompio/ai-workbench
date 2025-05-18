from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localdate
from datetime import timedelta, datetime
from django.http import JsonResponse
from django.db.models import Q
from .models import Meal, FoodEntry, Recipe, Ingredient, RawFoods
from .forms import AddFoodForm, RecipeForm, IngredientForm
from django.forms import inlineformset_factory
from django.db.models import Sum


@login_required
def daily_nutrient_overview(request, date):
    # if not request.user.is_pro:
    #     return render(request, 'users/pro_required.html')
    # Umwandlung des Datums, falls es als String übergeben wird
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d").date()

    # Holen aller Mahlzeiten des Benutzers für das angegebene Datum
    meals = Meal.objects.filter(user=request.user)

    # Initialisieren der Gesamtnährstoffe
    total_nutrients = {nutrient: 0 for nutrient in FoodEntry.NUTRIENT_FIELDS}

    # Sammeln aller FoodEntry-Einträge für das Datum
    entries = FoodEntry.objects.filter(meal__in=meals, date=date)

    # Nährstoffe summieren
    for entry in entries:
        for nutrient in FoodEntry.NUTRIENT_FIELDS:
            total_nutrients[nutrient] += getattr(entry, nutrient)

    return render(request, 'food/nutrient_overview.html', {
        'meal': None,  # Keine spezifische Mahlzeit
        'entries': entries,
        'date': date,
        'total_nutrients': total_nutrients,
    })



@login_required
def nutrient_overview(request, meal_id, date):
    # if not request.user.is_pro:
    #     return render(request, 'users/pro_required.html')
    # Umwandlung des Datums, falls es als String übergeben wird
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d").date()

    # Holen der Meal-Instanz für das angegebene Datum und den Benutzer
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)

    # Alle FoodEntry-Einträge für das angegebene Datum und die Mahlzeit des Benutzers
    entries = FoodEntry.objects.filter(meal=meal, date=date)

    # Nährstoffe berechnen
    total_nutrients = {nutrient: 0 for nutrient in FoodEntry.NUTRIENT_FIELDS}

    for entry in entries:
        for nutrient in FoodEntry.NUTRIENT_FIELDS:
            total_nutrients[nutrient] += getattr(entry, nutrient)

    return render(request, 'food/nutrient_overview.html', {
        'meal': meal,
        'entries': entries,
        'date': date,
        'total_nutrients': total_nutrients,  # Gesamtnährstoffe für den Tag
    })

from django.db import IntegrityError

def calculate_and_save_recipe_nutrients(recipe):
    # Dictionary zum Speichern der Gesamt-Nährstoffwerte
    nutrient_totals = {field: 0 for field in RawFoods.NUTRIENT_FIELDS}
    
    # Gesamtgewicht des Rezepts in Gramm
    total_weight = sum(ingredient.amount_in_grams for ingredient in recipe.ingredients.all())

    # Berechne die Nährwerte für jede Zutat und addiere sie
    for ingredient in recipe.ingredients.all():
        raw_food = ingredient.raw_food
        for nutrient in RawFoods.NUTRIENT_FIELDS:
            # Holen des Nährwerts pro 100g der Zutat
            nutrient_value_per_100g = getattr(raw_food, nutrient, 0)
            # Berechnung des Nährwerts für die gegebene Menge der Zutat
            nutrient_totals[nutrient] += (ingredient.amount_in_grams / 100) * nutrient_value_per_100g

    # Jetzt den Gesamtwert auf 100g des gesamten Rezepts skalieren
    if total_weight > 0:
        for nutrient in nutrient_totals:
            nutrient_totals[nutrient] = nutrient_totals[nutrient] * 100 / total_weight

    # Finde die höchste ID in der RawFoods-Tabelle
    try:
        last_id = RawFoods.objects.latest('id').id
    except RawFoods.DoesNotExist:
        last_id = 0  # Falls es keine Einträge gibt, starte bei ID 1

    # Rezept als neuen `RawFoods`-Eintrag speichern (automatisch mit ID+1)
    recipe_raw_food = RawFoods.objects.create(
        id=last_id + 1,  # Setze die ID auf die letzte ID plus 1
        name=f"Recipe: {recipe.name}",
        **nutrient_totals
    )
    
    return recipe_raw_food




def create_recipe_view(request):
    # Lade alle Rezepte aus der Datenbank
    food_recipes = Recipe.objects.all()  # Alle Rezepte aus der Datenbank
    return render(request, 'create_recipe.html', {'food_recipes': food_recipes})

@login_required
def recipe_detail(request, recipe_id):
    # Hole das Rezept anhand der Rezept-ID
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Hole alle Zutaten des Rezepts (falls vorhanden)
    ingredients = Ingredient.objects.filter(recipe=recipe)

    return render(request, 'food/recipe_detail.html', {
        'recipe': recipe,
        'ingredients': ingredients,
    })

def create_recipe(request):
    food_recipes = Recipe.objects.all()  # Alle Rezepte aus der Datenbank

    if request.method == 'POST':
        name = request.POST.get('recipe_name')
        instructions = request.POST.get('instructions')

        if name and instructions:
            recipe = Recipe.objects.create(user=request.user, name=name, instructions=instructions)
            return redirect('food:add_ingredients', recipe_id=recipe.id)

    return render(request, 'food/create_recipe.html', {'food_recipes': food_recipes})


@login_required
def add_ingredients(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "POST":
        ingredient_id = request.POST.get("ingredient_id")
        amount_in_grams = request.POST.get("ingredient_amount")

        # Validierung
        if not ingredient_id or not amount_in_grams:
            return render(request, 'food/add_ingredients.html', {
                'recipe': recipe,
                'error': "Both ingredient and amount are required."
            })

        try:
            # ID in ein RawFoods-Objekt umwandeln
            raw_food = RawFoods.objects.get(id=ingredient_id)
        except RawFoods.DoesNotExist:
            return render(request, 'food/add_ingredients.html', {
                'recipe': recipe,
                'error': "The selected ingredient does not exist."
            })

        # Neue Zutat hinzufügen
        Ingredient.objects.create(
            recipe=recipe,
            raw_food=raw_food,
            amount_in_grams=float(amount_in_grams)
        )

        # Alten Eintrag in RawFoods löschen (falls vorhanden)
        RawFoods.objects.filter(name=f"Recipe: {recipe.name}").delete()

        # Berechnung der neuen Nährwerte und Speichern als neuen RawFoods-Eintrag
        calculate_and_save_recipe_nutrients(recipe)

        return redirect('food:recipe_detail', recipe_id=recipe.id)

    return render(request, 'food/add_ingredients.html', {
        'recipe': recipe
    })



@login_required
def meal_list(request):
    date = localdate()
    return redirect('food:meal_list_by_date', date=date)


@login_required
def meal_list_by_date(request, date):
    try:
        # `date` von String in ein Datum umwandeln
        date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        # Fallback auf das aktuelle Datum, wenn die Umwandlung fehlschlägt
        date = localdate()

    # Abrufen der Mahlzeiten für den Benutzer
    meals = Meal.objects.filter(user=request.user)

    # Kalorienberechnungen
    meals_data = []
    total_kcal = 0
    for meal in meals:
        entries = FoodEntry.objects.filter(meal=meal, date=date)
        kcal_sum = entries.aggregate(total_kcal=Sum('kcal'))['total_kcal'] or 0  # Summe der Kalorien
        meals_data.append({
            'meal': meal,
            'entries': entries,
            'kcal_sum': kcal_sum,
        })
        total_kcal += kcal_sum

    # `calorie_target` des Nutzers abrufen
    calorie_target = request.user.calorie_target

    context = {
        'meals': meals_data,
        'date': date,
        'prev_date': date - timedelta(days=1),
        'next_date': date + timedelta(days=1),
        'total_kcal': total_kcal,
        'calorie_target': calorie_target,  # Hinzufügen zum Kontext
    }

    return render(request, 'food/meal_list.html', context)


from food.models import RawFoods  # Importiere das Modell RawFood

@login_required
def meal_detail(request, meal_id, date):
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d").date()

    meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    entries = FoodEntry.objects.filter(meal=meal, date=date)

    if request.method == "POST":
        food_name = request.POST.get("food-search")
        quantity_in_grams = float(request.POST.get("quantity_in_grams", 0))

        # Suche nach dem Lebensmittel in der 'RawFood'-Tabelle
        selected_food = RawFoods.objects.filter(name__iexact=food_name).first()

        if selected_food:
            food_data = {
                "id": selected_food.id,
                "name": selected_food.name,
                # Die Nährstofffelder werden dynamisch aus dem Modell abgerufen
                **{nutrient: getattr(selected_food, nutrient) for nutrient in FoodEntry.NUTRIENT_FIELDS}
            }
            FoodEntry.objects.create(
                meal=meal,
                user=request.user,
                raw_food_id=food_data["id"],
                name=food_data["name"],
                amount_in_grams=quantity_in_grams,
                date=date,
                **{nutrient: (food_data[nutrient] * quantity_in_grams) / 100 for nutrient in FoodEntry.NUTRIENT_FIELDS}
            )
        return redirect('food:detail', meal_id=meal.id, date=date)

    return render(request, 'food/meal_detail.html', {
        'meal': meal,
        'entries': entries,
        'date': date,
    })


@login_required
def search_food(request):
    query = request.GET.get('q', '').strip()
    results = []
    
    if query:
        # Suche nach dem Lebensmittel in der 'RawFood'-Tabelle basierend auf dem Namen
        raw_foods = RawFoods.objects.filter(name__icontains=query)  # Case-insensitive Suche
        
        results = [
            {"id": food.id, "name": food.name}
            for food in raw_foods
        ]

    return JsonResponse({"results": results})
