import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# -------------------------------
# Setup: Load + Train Functions
# -------------------------------
def load_and_prepare_sleep_data(csv_path="data/Sleep_health_and_lifestyle_dataset.csv"):
    df_sleep = pd.read_csv(csv_path)
    df_sleep = df_sleep.drop(columns=['Person ID', 'Gender', 'Occupation'])

    df_sleep[['Systolic_BP', 'Diastolic_BP']] = df_sleep['Blood Pressure'].str.split('/', expand=True).astype(float)
    df_sleep = df_sleep.drop(columns=['Blood Pressure'])

    non_numeric_cols = df_sleep.select_dtypes(include='object').columns
    df_sleep = df_sleep.drop(columns=non_numeric_cols)

    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_sleep)

    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(df_scaled)
    df_sleep['Cluster'] = clusters

    return df_sleep, scaler, kmeans


# -------------------------------
# Interpretations
# -------------------------------
def interpret_sleep_duration(val):
    if val < 6:
        return f"{val} hrs (⚠️ Short sleep — may affect focus/immunity)"
    elif val > 9:
        return f"{val} hrs (⚠️ Oversleeping — may cause fatigue)"
    else:
        return f"{val} hrs (✅ Healthy sleep range)"

def interpret_sleep_quality(val):
    if val < 5:
        return f"{val}/10 (⚠️ Poor quality — may affect energy)"
    elif val >= 8:
        return f"{val}/10 (✅ Excellent quality)"
    else:
        return f"{val}/10 (Moderate — can improve)"

def interpret_stress(val):
    if val > 7:
        return f"{val}/10 (⚠️ High stress)"
    elif val < 4:
        return f"{val}/10 (✅ Low stress)"
    else:
        return f"{val}/10 (Moderate)"

def interpret_steps(val):
    if val < 5000:
        return f"{val} steps (⚠️ Low activity)"
    elif val > 10000:
        return f"{val} steps (✅ Very active)"
    else:
        return f"{val} steps (Moderate)"

def interpret_activity(val):
    if val < 3:
        return f"{val}/10 (⚠️ Sedentary)"
    elif val > 7:
        return f"{val}/10 (✅ Very active)"
    else:
        return f"{val}/10 (Moderate)"

def interpret_hr(val):
    if val > 90:
        return f"{val} bpm (⚠️ High — reduce caffeine/stress)"
    elif val < 60:
        return f"{val} bpm (✅ Low — good fitness)"
    else:
        return f"{val} bpm (Normal)"


# -------------------------------
# Generate Insights
# -------------------------------
def generate_cluster_insights(df_original, scaler, kmeans_model, user_input):
    input_df = pd.DataFrame([user_input])
    input_scaled = scaler.transform(input_df)
    predicted_cluster = kmeans_model.predict(input_scaled)[0]
    cluster_data = df_original[df_original['Cluster'] == predicted_cluster]

    stats = {
        "Average Sleep Duration": round(cluster_data["Sleep Duration"].mean(), 1),
        "Average Sleep Quality": round(cluster_data["Quality of Sleep"].mean(), 1),
        "Average Stress Level": round(cluster_data["Stress Level"].mean(), 1),
        "Average Daily Steps": int(cluster_data["Daily Steps"].mean()),
        "Average Physical Activity": round(cluster_data["Physical Activity Level"].mean(), 1),
        "Average Heart Rate": int(cluster_data["Heart Rate"].mean()),
    }

    interpretations = {
        "Sleep Duration": interpret_sleep_duration(stats["Average Sleep Duration"]),
        "Sleep Quality": interpret_sleep_quality(stats["Average Sleep Quality"]),
        "Stress Level": interpret_stress(stats["Average Stress Level"]),
        "Daily Steps": interpret_steps(stats["Average Daily Steps"]),
        "Physical Activity Level": interpret_activity(stats["Average Physical Activity"]),
        "Heart Rate": interpret_hr(stats["Average Heart Rate"]),
    }

    suggestions = []
    if stats["Average Stress Level"] > 6:
        suggestions.append("Try mindfulness, journaling, or guided meditation.")
        suggestions.append("Maintain a consistent sleep schedule.")
    if stats["Average Stress Level"] < 4:
        suggestions.append("Great job keeping your stress in check!")

    if stats["Average Sleep Duration"] < 6.5:
        suggestions.append("Avoid screens before bed. Maintain consistent timing.")
    if stats["Average Sleep Duration"] > 9:
        suggestions.append("Oversleeping may signal fatigue or poor sleep quality.")

    if stats["Average Sleep Quality"] < 6:
        suggestions.append("Try ASMR or calming music. Avoid caffeine at night.")
    if stats["Average Sleep Quality"] >= 8:
        suggestions.append("Excellent quality! Maintain your bedtime routine.")

    if stats["Average Daily Steps"] < 6000:
        suggestions.append("Try post-meal walks to increase steps.")
    if stats["Average Daily Steps"] > 10000:
        suggestions.append("You're highly active! Stay hydrated and rest well.")

    if stats["Average Physical Activity"] < 4:
        suggestions.append("Add light activities like yoga or stretching.")
    if stats["Average Physical Activity"] > 6:
        suggestions.append("Ensure proper rest and recovery after workouts.")

    if stats["Average Heart Rate"] > 90:
        suggestions.append("Reduce stimulants and practice deep breathing.")
    if stats["Average Heart Rate"] < 60:
        suggestions.append("Low heart rate — great fitness level!")

    return {
        "cluster": int(predicted_cluster),
        "stats": stats,
        "interpretations": interpretations,
        "suggestions": suggestions
    }
