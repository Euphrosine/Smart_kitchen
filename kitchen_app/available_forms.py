# forms.py

from django import forms
from .models import Category

class ChooseCategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    available_ingredients = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter available ingredients, separated by commas'}))
