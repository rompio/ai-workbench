from django.conf import settings
from django.db import models
import sqlite3
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    name = models.CharField(max_length=100)
    instructions = models.TextField(blank=True, null=True)  # Neues Feld hinzugefügt
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    raw_food = models.ForeignKey('RawFoods', on_delete=models.CASCADE)  # ForeignKey hinzugefügt
    amount_in_grams = models.FloatField()

    def __str__(self):
        return f"{self.raw_food.name} - {self.amount_in_grams}g"

class Meal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="meals"
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class FoodEntry(models.Model):
    meal = models.ForeignKey(
        "Meal",
        on_delete=models.CASCADE,
        related_name="entries"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="food_entries"
    )
    raw_food_id = models.IntegerField()
    name = models.CharField(max_length=100)
    amount_in_grams = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)

    # Dynamisch generierte Nährstofffelder
    NUTRIENT_FIELDS = [
        "kcal", "Fett", "Eiweiß", "Kohlenhydrate", "Ballaststoffe", "Salz",
        "Cholesterin", "Vitamin A Retinoläquivalent", "Vitamin A Retinolaktivitätsäquivalent",
        "Retinol", "Beta-Carotin", "Vitamin B1 Thiamin", "Vitamin B2 Riboflavin",
        "Vitamin B3 Niacin, Nicotinsäure", "Vitamin B3 Niacinäquivalent",
        "Vitamin B5 Pantothensäure", "Vitamin B6 Pyridoxin", "Vitamin B7 Biotin (Vitamin H)",
        "Vitamin B9 gesamte Folsäure", "Vitamin B12 Cobalamin", "Vitamin C Ascorbinsäure",
        "Vitamin D Calciferole", "Vitamin E", "Vitamin K", "Natrium", "Kalium",
        "Calcium", "Magnesium", "Phosphor", "Schwefel", "Chlorid", "Eisen", "Zink",
        "Kupfer", "Mangan", "Fluorid", "Iodid", "Mannit", "Sorbit", "Xylit",
        "Glucose (Traubenzucker)", "Fructose (Fruchtzucker)", "Galactose (Schleimzucker)",
        "Monosaccharide (1 M)", "Saccharose (Rübenbenzucker)", "Maltose (Malzzucker)",
        "Lactose (Milchzucker)", "Disaccharide (2 M)", "Oligosaccharide, resorbierbar (3 - 9 M)",
        "Oligosaccharide, nicht resorbierbar", "Glykogen (tierische Stärke)", "Stärke",
        "Polysaccharide (> 9 M)", "Isoleucin", "Leucin", "Lysin", "Methionin", "Cystein",
        "Phenylalanin", "Tyrosin", "Threonin", "Tryptophan", "Valin", "Arginin", "Histidin",
        "Alanin", "Asparaginsäure", "Glutaminsäure", "Glycin", "Prolin", "Serin",
        "Harnsäure", "Purin", "Butansäure / Buttersäure", "Hexansäure / Capronsäure",
        "Octansäure / Caprylsäure", "Decansäure / Caprinsäure", "Dodecansäure / Laurinsäure",
        "Tetradecansäure / Myristinsäure", "Pentadecansäure", "Hexadecansäure / Palmitinsäure",
        "Heptadecansäure", "Octadecansäure / Stearinsäure", "Eicosansäure / Arachinsäure",
        "Decosansäure / Behensäure", "Tetracosansäure / Lignocerinsäure", "Tetradecensäure",
        "Pentadecensäure", "Hexadecensäure / Palmitoleinsäure", "Heptadecensäure", "Eicosensäure",
        "Hexadecadiensäure", "Hexadecatetraensäure", "Glycerin und Lipoide",
        "ALA - Linolensäure Omega 3", "Stearidonsäure Omega 3", "EPA - Eicosapentaensäure Omega 3",
        "Docosadiensäure", "Docosatriensäure", "Docosatetraensäure",
        "Docosapentaensäure Omega 3", "DHA - Docosahexaensäure Omega 3",
        "Octadecadiensäure / Linolsäure Omega 6", "Nonadecatriensäure",
        "Eicosadiensäure Omega 6", "Eicosatriensäure Omega 6",
        "Eicosatetraensäure / Arachidonsäure Omega 6", "Decosensäure / Erucasäure Omega 9",
        "Tetracosensäure / Nervonsäure Omega 9", "Poly-Pentosen", "Poly-Hexosen",
        "Cellulose", "Lignin", "Poly-Uronsäure"
    ]

    # Automatisch Nährstofffelder hinzufügen
    for nutrient in NUTRIENT_FIELDS:
        locals()[nutrient] = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} ({self.meal.name})"


class RawFoods(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=False)
    NUTRIENT_FIELDS = [
        "kcal", "Fett", "Eiweiß", "Kohlenhydrate", "Ballaststoffe", "Salz",
        "Cholesterin", "Vitamin A Retinoläquivalent", "Vitamin A Retinolaktivitätsäquivalent",
        "Retinol", "Beta-Carotin", "Vitamin B1 Thiamin", "Vitamin B2 Riboflavin",
        "Vitamin B3 Niacin, Nicotinsäure", "Vitamin B3 Niacinäquivalent",
        "Vitamin B5 Pantothensäure", "Vitamin B6 Pyridoxin", "Vitamin B7 Biotin (Vitamin H)",
        "Vitamin B9 gesamte Folsäure", "Vitamin B12 Cobalamin", "Vitamin C Ascorbinsäure",
        "Vitamin D Calciferole", "Vitamin E", "Vitamin K", "Natrium", "Kalium",
        "Calcium", "Magnesium", "Phosphor", "Schwefel", "Chlorid", "Eisen", "Zink",
        "Kupfer", "Mangan", "Fluorid", "Iodid", "Mannit", "Sorbit", "Xylit",
        "Glucose (Traubenzucker)", "Fructose (Fruchtzucker)", "Galactose (Schleimzucker)",
        "Monosaccharide (1 M)", "Saccharose (Rübenbenzucker)", "Maltose (Malzzucker)",
        "Lactose (Milchzucker)", "Disaccharide (2 M)", "Oligosaccharide, resorbierbar (3 - 9 M)",
        "Oligosaccharide, nicht resorbierbar", "Glykogen (tierische Stärke)", "Stärke",
        "Polysaccharide (> 9 M)", "Isoleucin", "Leucin", "Lysin", "Methionin", "Cystein",
        "Phenylalanin", "Tyrosin", "Threonin", "Tryptophan", "Valin", "Arginin", "Histidin",
        "Alanin", "Asparaginsäure", "Glutaminsäure", "Glycin", "Prolin", "Serin",
        "Harnsäure", "Purin", "Butansäure / Buttersäure", "Hexansäure / Capronsäure",
        "Octansäure / Caprylsäure", "Decansäure / Caprinsäure", "Dodecansäure / Laurinsäure",
        "Tetradecansäure / Myristinsäure", "Pentadecansäure", "Hexadecansäure / Palmitinsäure",
        "Heptadecansäure", "Octadecansäure / Stearinsäure", "Eicosansäure / Arachinsäure",
        "Decosansäure / Behensäure", "Tetracosansäure / Lignocerinsäure", "Tetradecensäure",
        "Pentadecensäure", "Hexadecensäure / Palmitoleinsäure", "Heptadecensäure", "Eicosensäure",
        "Hexadecadiensäure", "Hexadecatetraensäure", "Glycerin und Lipoide",
        "ALA - Linolensäure Omega 3", "Stearidonsäure Omega 3", "EPA - Eicosapentaensäure Omega 3",
        "Docosadiensäure", "Docosatriensäure", "Docosatetraensäure",
        "Docosapentaensäure Omega 3", "DHA - Docosahexaensäure Omega 3",
        "Octadecadiensäure / Linolsäure Omega 6", "Nonadecatriensäure",
        "Eicosadiensäure Omega 6", "Eicosatriensäure Omega 6",
        "Eicosatetraensäure / Arachidonsäure Omega 6", "Decosensäure / Erucasäure Omega 9",
        "Tetracosensäure / Nervonsäure Omega 9", "Poly-Pentosen", "Poly-Hexosen",
        "Cellulose", "Lignin", "Poly-Uronsäure"
    ]
    # Automatisch Nährstofffelder hinzufügen
    for nutrient in NUTRIENT_FIELDS:
        locals()[nutrient] = models.FloatField(default=0)