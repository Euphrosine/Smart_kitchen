from  kitchen_app.ml_models.mealpredictor import MealPredictor  # Import your MealPredictor class
import joblib
import warnings
warnings.filterwarnings('ignore')

# def return_model():
# Load the trained model
model_path = 'kitchen_app/ml_models/models/meal_predictor.joblib'
try:
    meal_predictor = joblib.load(model_path)
    print("Loaded model from:", model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    exit()
