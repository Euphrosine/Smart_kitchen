import joblib
from mealpredictor import MealPredictor
import warnings

warnings.filterwarnings('ignore')

if __name__ == "__main__":
    # Load the trained model
    model_path = 'models/meal_predictor.joblib'
    try:
        meal_predictor = joblib.load(model_path)
        print("Loaded model from:", model_path)
    except Exception as e:
        (
            print(f"Error loading model: {e}"))
        exit()

    user_ingredients_input = input("Enter ingredients separated by comma: ")
    user_ingredients = [ingredient.strip() for ingredient in user_ingredients_input.split(',')]
    top_meals, X_filtered_encoded, given_ingredients_encoded, similarity_scores = meal_predictor.predict(
        user_ingredients)
    top_2_meals = list(top_meals.keys())
    top_2_categories = [top_meals[meal]['category'] for meal in top_2_meals]
    print("Top 2 meals:", top_meals)

    meal_predictor.plot(X_filtered_encoded, given_ingredients_encoded, top_2_meals, similarity_scores)
