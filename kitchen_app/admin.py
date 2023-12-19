from django.contrib import admin
from .models import KitchenData,Category,Ingredient,Meal

# Register your models here.
admin.site.register(KitchenData)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Meal)