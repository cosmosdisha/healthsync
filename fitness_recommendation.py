import json
import pandas as pd
import random

# -----------------------------
# Load Fitness Dataset Function
# -----------------------------
def load_exercise_data(filepath="data/exercises.json"):
    with open(filepath, "r") as f:
        data = json.load(f)
    df_fit = pd.json_normalize(data)
    if 'instructions' in df_fit.columns:
        df_fit['instructions'] = df_fit['instructions'].apply(
            lambda x: ' '.join(x) if isinstance(x, list) else str(x)
        )
    return df_fit

# -----------------------------
# Map BMI to Fitness Level
# -----------------------------
def map_bmi_to_level(bmi):
    if bmi < 18.5:
        return "beginner"
    elif 18.5 <= bmi < 25:
        return "intermediate"
    else:
        return "expert"

# -----------------------------
# Main Recommendation Function
# -----------------------------
def recommend_exercises_by_bmi(df_fit, bmi, n=5,randomize=True):
    level = map_bmi_to_level(bmi)
    recommended = df_fit[df_fit['level'].str.lower() == level.lower()]
    if recommended.empty:
        return pd.DataFrame(columns=['name', 'level', 'equipment', 'primaryMuscles', 'instructions', 'category'])
    
    if randomize:
        return recommended.sample(n=min(n, len(recommended)), random_state=random.randint(1, 10000)).reset_index(drop=True)
    else:
        return recommended.head(n).reset_index(drop=True)
    