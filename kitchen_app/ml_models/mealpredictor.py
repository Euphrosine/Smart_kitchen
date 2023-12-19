import joblib
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

class MealPredictor:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.dataset = pd.read_csv(self.dataset_path)
        self.dataset = self.dataset.sample(frac=1).reset_index(drop=True)  # Shuffle the dataset
        self.dataset['ingredients'] = self.dataset['ingredients'].str.split(',')  # Split the ingredients into lists
        self.X = self.dataset[['ingredients']]
        self.y = self.dataset['meal']

    def predict(self, given_ingredients):
        # Convert given ingredients to a set for faster lookup
        given_ingredients_set = set(given_ingredients)

        # Filter out meals that don't contain any of the given ingredients
        filtered_dataset = self.dataset[
            self.dataset['ingredients'].apply(lambda x: any(ingredient in x for ingredient in given_ingredients_set))]

        # If all meals are filtered out, return an appropriate message
        if filtered_dataset.empty:
            return "No meals contain the given ingredients.", None

        # Otherwise, proceed with the similarity computation
        X_filtered = filtered_dataset[['ingredients']]
        y_filtered = filtered_dataset['meal']

        # Create a MultiLabelBinarizer object
        mlb = MultiLabelBinarizer()
        X_filtered_encoded = pd.DataFrame(mlb.fit_transform(X_filtered['ingredients']), columns=mlb.classes_)

        given_ingredients_encoded = mlb.transform([given_ingredients])
        similarity_scores = cosine_similarity(given_ingredients_encoded, X_filtered_encoded)

        # Get the indices of the top meals
        top_indices = similarity_scores[0].argsort()[::-1]

        # Select the top distinct meals
        top_meals = {}
        for index in top_indices:
            meal = y_filtered.iloc[index]
            ingredients = X_filtered.iloc[index].values[0]
            category = filtered_dataset['category'].iloc[index]
            if meal not in top_meals:
                top_meals[meal] = {'ingredients': ingredients, 'category': category}
            if len(top_meals) == 2:
                break

        return top_meals, X_filtered_encoded, given_ingredients_encoded, similarity_scores

    def plot(self, X_filtered_encoded, given_ingredients_encoded, top_2_meals, similarity_scores):
        # Apply PCA to reduce the dimensionality to 2
        pca = PCA(n_components=2)
        X_filtered_encoded_pca = pca.fit_transform(X_filtered_encoded)
        given_ingredients_encoded_pca = pca.transform(given_ingredients_encoded)

        # Create a scatter plot
        fig = go.Figure()

        # Add a scatter plot for the meals
        fig.add_trace(
            go.Scatter(x=X_filtered_encoded_pca[:, 0], y=X_filtered_encoded_pca[:, 1], mode='markers', name='Meals'))

        # Add a scatter plot for the given ingredients
        fig.add_trace(
            go.Scatter(x=given_ingredients_encoded_pca[:, 0], y=given_ingredients_encoded_pca[:, 1], mode='markers',
                       name='Given ingredients', marker=dict(size=15, color='red')))

        # Get the indices of the top 2 meals
        top_2_indices = similarity_scores[0].argsort()[-len(top_2_meals):][::-1]

        # Add a scatter plot for the first nearby meal
        fig.add_trace(
            go.Scatter(x=[X_filtered_encoded_pca[top_2_indices[0], 0]], y=[X_filtered_encoded_pca[top_2_indices[0], 1]],
                       mode='markers', name=f'First match meal: {top_2_meals[0]}', marker=dict(color='green')))

        # If there's a second meal, add a scatter plot for it
        if len(top_2_meals) > 1:
            fig.add_trace(go.Scatter(x=[X_filtered_encoded_pca[top_2_indices[1], 0]],
                                     y=[X_filtered_encoded_pca[top_2_indices[1], 1]], mode='markers',
                                     name=f'Second match meal: {top_2_meals[1]}', marker=dict(color='yellow')))

        # Show the plot
        fig.show()

if __name__ == "__main__":

    meal_predictor = MealPredictor('kitchenDataset.csv')
    # Save the model
    path = './models/meal_predictor.joblib'
    joblib.dump(meal_predictor, path)
    print(f"Model saved to {path}")

    given_ingredients = ['water', 'sugar', 'teabag']
    top_meals, X_filtered_encoded, given_ingredients_encoded, similarity_scores = meal_predictor.predict(
        given_ingredients)
    top_2_meals = list(top_meals.keys())
    top_2_categories = [top_meals[meal]['category'] for meal in top_2_meals]
    print("Top 2 meals:", top_meals)

    meal_predictor.plot(X_filtered_encoded, given_ingredients_encoded, top_2_meals, similarity_scores)