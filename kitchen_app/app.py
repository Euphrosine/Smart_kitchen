import pandas as pd
import joblib

# Load the trained Decision Tree model
try:
    decision_tree_model, label_encoder = joblib.load('ml_models/trained_kitchen_model_decision_tree.joblib')
except Exception as model_load_error:
    print(f"Error loading the model: {model_load_error}")
    decision_tree_model, label_encoder = None, None

if decision_tree_model is not None:
    # Get user input for category
    category_input = input("Enter category (e.g., breakfast, lunch, dinner): ")

    # Check if the category is valid
    if category_input.lower() in label_encoder.classes_:
        # Encode the category
        category_encoded = label_encoder.transform([category_input.lower()])[0]

        # Create a DataFrame with the encoded category
        user_input_df = pd.DataFrame([[category_encoded]], columns=['category_encoded'])

        # Make predictions using the trained model
        predicted_meals = decision_tree_model.predict(user_input_df)

        # Decode the predicted meals using the inverse of label encoding
        predicted_meals = label_encoder.inverse_transform(predicted_meals)

        # Print the predicted meals
        print("Predicted Meals:")
        for idx, meal in enumerate(predicted_meals):
            print(f"{idx + 1}. {meal}")

        # Get user selection
        user_choice = int(input("Select a meal (1-{}): ".format(len(predicted_meals))))

        # Check if the user choice is valid
        if 1 <= user_choice <= len(predicted_meals):
            selected_meal = predicted_meals[user_choice - 1]

            # Get the recommended ingredients for the selected meal from the dataset
            dataset_path = 'ml_models/kitchenDataset.csv'
            dataset = pd.read_csv(dataset_path)
            
            recommended_ingredients = dataset[dataset['meal'] == selected_meal]['ingredients'].iloc[0].split(',')

            # Print the results
            print(f"\nSelected Meal: {selected_meal}")
            print(f"Recommended Ingredients: {', '.join(recommended_ingredients)}")
        else:
            print("Invalid selection. Please choose a number between 1 and {}.".format(len(predicted_meals)))
    else:
        print("Invalid category. Please enter a valid category.")
else:
    print("Machine learning model not available. Unable to make predictions.")
