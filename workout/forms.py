from django import forms

class WorkoutAktivitätForm(forms.Form):
    aktivität = forms.CharField(max_length=100)
    dauer = forms.IntegerField(min_value=0)
    distanz = forms.FloatField(min_value=0)
    puls = forms.IntegerField(min_value=0)
    max_puls = forms.IntegerField(min_value=0)
    höhenmeter = forms.FloatField(min_value=0)