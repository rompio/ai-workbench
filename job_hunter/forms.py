# job_hunter/forms.py
from django import forms
from .models import PInfo
from .models import Offer
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']  # Nur das Resume-Feld bearbeiten

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            "position",
            "company",
            "offer_text",
            "about_company",
            "url",
            "response",
            "status",
        ]


class PInfoForm(forms.ModelForm):
    class Meta:
        model = PInfo
        fields = ["first_name", "last_name", "email", "background"]
        widgets = {
            "background": forms.Textarea(attrs={"rows": 4}),
        }
