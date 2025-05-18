from django import forms
from .models import Recipe, Ingredient, FoodEntry


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'instructions']  # instructions hinzugefügt



class IngredientForm(forms.ModelForm):
    raw_food = forms.ModelChoiceField(
        queryset=FoodEntry.objects.all(),
        label="Zutat",
        widget=forms.Select
    )

    class Meta:
        model = Ingredient
        fields = ['raw_food', 'amount_in_grams']


class SearchForm(forms.Form):
    search_term = forms.CharField(label="Search for food", max_length=100)


class AddFoodForm(forms.Form):
    food_item = forms.ChoiceField(choices=[], required=True)
    quantity_in_grams = forms.IntegerField(min_value=1, required=True)

    def __init__(self, *args, **kwargs):
        raw_foods = kwargs.pop('raw_foods', [])
        super().__init__(*args, **kwargs)
        self.fields['food_item'].choices = [(food[0], food[1]) for food in raw_foods]  # food[0] -> id, food[1] -> name
