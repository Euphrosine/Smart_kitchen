# from django import forms
# from .models import IngredientQuantity

# class ChooseCategoryForm(forms.Form):
#     category = forms.ChoiceField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')])

# class ChooseQuantityForm(forms.ModelForm):
#     class Meta:
#         model = IngredientQuantity
#         fields = ['quantity']

#     def __init__(self, *args, **kwargs):
#         ingredients_quantities = kwargs.pop('ingredients_quantities', None)
#         super(ChooseQuantityForm, self).__init__(*args, **kwargs)

#         for ingredient_quantity in ingredients_quantities:
#             self.fields[f'ingredient_{ingredient_quantity.ingredient.id}'] = forms.IntegerField(
#                 label=ingredient_quantity.ingredient.name,
#                 initial=ingredient_quantity.quantity
#             )

#     def save(self):
#         for field_name, value in self.cleaned_data.items():
#             if field_name.startswith('ingredient_'):
#                 ingredient_id = int(field_name.split('_')[1])
#                 ingredient_quantity = IngredientQuantity.objects.get(ingredient__id=ingredient_id)
#                 ingredient_quantity.quantity = value
#                 ingredient_quantity.save()
from django import forms
from .models import Category

class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
