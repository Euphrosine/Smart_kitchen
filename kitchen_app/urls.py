from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CategoryListAPIView,IngredientListByCategoryAPIView

urlpatterns = [
    path('api/', views.api_view, name='api_view'),
    path('', views.display_view, name='display_view'),
    
    # kitchen mgmt
    # path('meal-suggestion/', views.meal_suggestion, name='meal_suggestion'),
    path('api/categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('api/ingredients/<int:category_id>/', IngredientListByCategoryAPIView.as_view(), name='ingredient-list-by-category'),
    path('kitchen/', views.stockmanagement, name='stockmanagement'),
    path('predict-meal/', views.predict_meal, name='predict_meal'),
    
    path('lamp/toggle/', views.lamp_toggle, name='lamp_toggle'),
    path('fan/toggle/', views.fan_toggle, name='fan_toggle'),
    path('lamp/status/', views.get_lamp_status, name='get_lamp_status'),
    path('fan/status/', views.get_fan_status, name='get_fan_status'),
    path('lamp/toggle/template/', views.lamp_toggle_view, name='lamp_toggle_view'),
    path('fan/toggle/template/', views.fan_toggle_view, name='fan_toggle_view'),
]