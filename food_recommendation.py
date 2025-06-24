import pandas as pd
import random

# Global course mapping
course_mapping = {
    'Breakfast': ['south indian breakfast', 'indian breakfast', 'north indian breakfast', 'world breakfast', 'brunch'],
    'Lunch': ['lunch', 'main course', 'one pot dish'],
    'Snack': ['snack', 'appetizer', 'side dish'],
    'Dinner': ['dinner', 'main course', 'one pot dish']
}

# ----------------------
# Utility Functions
# ----------------------

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25:
        return 'Normal'
    elif 25 <= bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'

def calculate_calorie_requirement(gender, weight_kg, height_cm, age, activity_level):
    if gender.lower() == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very active': 1.9
    }

    calories = bmr * activity_multipliers.get(activity_level.lower(), 1.2)
    return round(calories)

# ----------------------
# Recommendation Logic
# ----------------------

def recommend_meals_by_calories(df, total_calories, num_options=3, randomize=True):
   
    recommendations = []
    meal_ratios = {'Breakfast': 0.25, 'Lunch': 0.35, 'Snack': 0.15, 'Dinner': 0.25}
    meal_calories = {meal: int(total_calories * ratio) for meal, ratio in meal_ratios.items()}

    for meal, target_cal in meal_calories.items():
        course_variants = course_mapping.get(meal, [])
        subset = df[df['Course'].isin(course_variants)].copy()

        if not subset.empty:
            subset['Calorie_Diff'] = (subset['Calories'] - target_cal).abs()
            if randomize:
                closest_options = subset.sample(n=min(num_options, len(subset)))
            else:
                closest_options = subset.sort_values(by='Calorie_Diff').head(num_options)
            
            if not closest_options.empty:
                closest_options = closest_options.assign(Meal=meal)
                recommendations.append(closest_options)
        else:
            print(f"No dishes found for {meal}.")

    if recommendations:
        result = pd.concat(recommendations)
        return result[[
        'Meal', 'RecipeName', 'Ingredients', 'PrepTimeInMins', 'CookTimeInMins',
        'Servings', 'Cuisine', 'Course', 'Diet', 'Instructions', 'URL', 'Calories'
    ]].reset_index(drop=True).to_dict(orient='records')
    else:
        return []
# ----------------------
# Load dataset function
# ----------------------

def load_food_data(filepath="data/IndianFoodDataset_Cleaned.csv"):
    df = pd.read_csv(filepath)
    df['Course'] = df['Course'].astype(str).str.lower()
    return df
