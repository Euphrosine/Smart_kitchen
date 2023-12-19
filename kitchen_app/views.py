from django.shortcuts import render,redirect
from django.http import JsonResponse
import joblib
from .models import KitchenData,Lamp,Fan
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator  

from rest_framework import generics
from .models import Category,Ingredient
from .serializers import CategorySerializer,IngredientSerializer

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from load_model import meal_predictor



# Create your views here.
# http://127.0.0.1:8000/chart_data_api/?temperature=15&gas_level=16&humidity=18&flame=1
model_path = 'kitchen_app/ml_models/models/meal_predictor.joblib'
try:
    meal_predictor = joblib.load(model_path)
    print("Loaded model from:", model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Toggle view for Lamp
@require_POST
def lamp_toggle(request):
    status = request.GET.get('status')
    if status is not None and status in ['0', '1']:
        lamp = get_object_or_404(Lamp, pk=1)
        lamp.status = int(status)
        lamp.save()
        return JsonResponse({'status': lamp.status})
    else:
        return JsonResponse({'error': 'Invalid status value'})

# Toggle view for Fan
@require_POST
def fan_toggle(request):
    status = request.GET.get('status')
    if status is not None and status in ['0', '1']:
        fan = get_object_or_404(Fan, pk=1)
        fan.status = int(status)
        fan.save()
        return JsonResponse({'status': fan.status})
    else:
        return JsonResponse({'error': 'Invalid status value'})

# Get latest status view for Lamp
@require_GET
def get_lamp_status(request):
    lamp = get_object_or_404(Lamp, pk=1)
    return JsonResponse({'status': lamp.status})

# Get latest status view for Fan
@require_GET
def get_fan_status(request):
    fan = get_object_or_404(Fan, pk=1)
    return JsonResponse({'status': fan.status})

# View for lamp toggle template
def lamp_toggle_view(request):
    lamp = get_object_or_404(Lamp, pk=1)
    return render(request, 'kitchen_app/lamp_toggle.html', {'lamp_status': lamp.status})

# View for fan toggle template
def fan_toggle_view(request):
    fan = get_object_or_404(Fan, pk=1)
    return render(request, 'kitchen_app/fan_toggle.html', {'fan_status': fan.status})


def api_view(request): #chart_data_view
    temperature = request.GET.get('temperature', None)
    gas_level = request.GET.get('gas_level', None)
    humidity = request.GET.get('humidity', None)
    flame = request.GET.get('flame', None)
    

    # Create a dictionary to store the data you want to save
    data_to_save = {
        'datetime': timezone.now(),
        'temperature': temperature,
        'gas_level': gas_level,
        'humidity' : humidity,
        'flame': flame,
        
        # 'lamp': lamp,
        # 'fan': fan,
        # 'switch1' :switch1,
        # 'switch2':switch2,
    }

    # Remove None values from the dictionary
    data_to_save = {k: v for k, v in data_to_save.items() if v is not None}

    # Create a new entry in the database using the data
    KitchenData.objects.create(**data_to_save)

    return JsonResponse({"message": "Data saved successfully"})

# display chart,table and cards

def display_view(request):
    kitchen_data = KitchenData.objects.all()

    # Create a dictionary to store the data with boolean values represented as "ON" or "OFF"
    formatted_data = []

    for data in kitchen_data:
        formatted_data.append({
            'datetime': data.datetime,
            'temperature': data.temperature,
            'gas_level': data.gas_level,
            'humidity' : data.humidity,
            'flame': "ON" if data.flame else "OFF",
            
            # 'lamp': "ON" if data.lamp else "OFF",
            # 'fan': "ON" if data.fan else "OFF",
            # 'switch1': "ON" if data.switch1 else "OFF",
            # 'switch2': "ON" if data.switch2 else "OFF",
        })

    return render(request, 'kitchen_app/dashboard_view.html', {'kitchen_data': formatted_data})

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
   
    
class IngredientListByCategoryAPIView(generics.ListAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Ingredient.objects.filter(category__id=category_id)

def stockmanagement(request):
    return render(request, 'kitchen_app/stock_management.html')



@csrf_exempt
def predict_meal(request):
    if request.method == 'POST':
        try:
            # Get user input from the request
            user_ingredients_input = request.POST.get('ingredients', '')
            user_ingredients = [ingredient.strip() for ingredient in user_ingredients_input.split(',')]

            # Make predictions using the model
            top_meals, _, _, _ = meal_predictor.predict(user_ingredients)
            top_2_meals = list(top_meals.keys())

            # Prepare the response
            response = {
                'top_meals': top_meals,
                'top_2_meals': top_2_meals
            }

            return JsonResponse(response)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
