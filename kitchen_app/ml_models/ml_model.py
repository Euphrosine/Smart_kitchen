# kitchen_app/ml_models/ml_model.py

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

def predict_meal(selected_category):
    model_path = 'trained_kitchen_model_decision_tree.joblib'

    # Load the model and label encoder
    clf, label_encoder_meal = joblib.load(model_path)

    # Encode the user input category
    try:
        user_input_category_encoded = label_encoder_meal.transform([selected_category])
    except ValueError as e:
        # Handle the case where the label is unseen
        print(f"Error: {e}")
        return "Unknown Meal"

    # Make prediction using the trained model
    prediction_encoded = clf.predict(user_input_category_encoded.reshape(-1, 1))

    # Decode the predicted meal using the inverse of label encoding
    predicted_meal = label_encoder_meal.inverse_transform(prediction_encoded)

    return predicted_meal[0]
