import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from kitchen_app.models import Category, Ingredient, Meal
from tqdm import tqdm

# Replace 'path/to/kitchen_app/ml_models/kitchenDataset.csv' with the actual path to your CSV file
csv_file_path = 'kitchen_app\ml_models\kitchenDataset.csv'

# Open the CSV file and read the data
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row

    categories_set = set()  # Use a set to store distinct categories

    for row in tqdm(reader, desc="Collecting Categories"):
        ingredients_str, meal_name, category_name = row
        ingredients_list = ingredients_str.split(',')

        try:
            # Collect distinct categories
            categories_set.add(category_name)
        except Exception as e:
            print(f"Error processing category: {e}")

    # Insert distinct categories into the database
    created_categories = []
    for category_name in tqdm(categories_set, desc="Inserting Categories"):
        try:
            # Get or create Category instance
            category, created = Category.objects.get_or_create(name=category_name)
            created_categories.append(category)
            if not created:
                # Category already exists, skip this row
                print(f"Category {category} exists")
                continue
        except Exception as e:
            print(f"Error processing category: {e}")

    # Reset the file pointer to the beginning of the file
    file.seek(0)
    next(reader)  # Skip the header row again

        # Process the data to associate ingredients and meals with categories
   # Process the data to associate ingredients and meals with categories
    for row in tqdm(reader,desc="Processing Rows"):
        ingredients_str, meal_name, category_name = row
        ingredients_list = ingredients_str.split(',')

        try:
            # Get or create Category instance
            category, created = Category.objects.get_or_create(name=category_name)

            # Get existing ingredients for the category
            existing_ingredients = Ingredient.objects.filter(category=category)

            # Get or create Ingredient instances, avoiding duplicates
            ingredients = [existing_ingredients.get_or_create(name=ingredient,category=category)[0] for ingredient in ingredients_list]

            # Get or create Meal instance
            meal, meal_created = Meal.objects.get_or_create(name=meal_name, category=category)

            # Check if the combination of ingredients already exists for the meal
            existing_ingredient_names = meal.ingredients.values_list('name', flat=True)
            new_ingredient_names = set(ingredients_list)

            # Calculate the set of new ingredients to be added
            ingredients_to_add = new_ingredient_names - set(existing_ingredient_names)

            # Add new ingredients to the meal
            for ingredient_name in ingredients_to_add:
                ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name, category=category)
                meal.ingredients.add(ingredient)

            # Save the changes
            meal.save()

        except Exception as e:
            print(f"Error processing row: {e}")

    print("Data inserted successfully.")


