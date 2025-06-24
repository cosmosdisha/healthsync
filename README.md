# 🌿 HealthSync – Your Personalized Wellness Companion

Have you ever wanted to lose weight or improve your health, only to get lost in endless Google searches and conflicting advice,  Overwhelming information, Zero personalization?

Yeah, we’ve been there.

**HealthSync** simplifies that journey by giving you personalized recommendations for:
- 🍽️ **Healthy Meals**
- 🏋️ **Fitness Routines**
- 😴 **Sleep Insights**

All based on your **demographics**, **body metrics**, and **lifestyle patterns** — because wellness should be *personal*. No fluff. Just what you need.

---
### 🚀 Enjoy the service on this hosted website
https://healthsync-zt3g.onrender.com

## 🚀 Features

It focus on **three core wellness pillars**:

### 🍲 Smart Meal Recommendations
You input your age, BMI, and daily calorie goals — It returns meal options categorized as Breakfast, Lunch, Snacks, and Dinner. Each suggestion includes:
- Calorie count
- Ingredients list
- Prep & Cook time
- Serving size
- Cooking instructions
- 📺 YouTube tutorial links

✅ You can also click “Refresh Suggestions” to get a new set of meals!

---

### 🏃 Fitness Guidance
Based on your BMI, we recommend:
- Exercises suited for your fitness level (beginner/intermediate/advanced)
- Primary muscles targeted
- Equipment needed
- Step-by-step instructions for each move

All of this is dynamically fetched and randomized so every visit feels fresh.

---

### 😴 Sleep Pattern Clustering
It applies unsupervised learning (K-Means clustering) on sleep-related data like:
- Age  
- Sleep Duration  
- Physical Activity  
- Stress Level  
- Blood Pressure  
- Heart Rate  

You get **cluster-based insights** into your wellness category and actionable suggestions for improving sleep hygiene.

---

## 🛠 Tech Stack

| Layer         | Tools/Frameworks                         |
|---------------|------------------------------------------|
| 🖼 Frontend    | HTML, Tailwind CSS, Jinja2               |
| ⚙️ Backend     | Python, Flask                            |
| 🧠 ML Models   | scikit-learn (KMeans), pandas, numpy     |
| 🔒 Auth & DB   | Flask-Login, SQLite                      |
| 📦 Others      | JSON, CSV, Git                           |

---

## ⚙️ Backend Logic

- **ML Model**: A trained KMeans model segments users into wellness clusters.
- **Meal Recommender**: Uses total calorie target to pick recipes from categorized dishes.
- **Fitness Recommender**: Maps BMI to difficulty levels and picks exercises from JSON data.
- **User Auth**: Optional login/signup using Flask-Login + SQLite (can be expanded to store history or preferences).
- **Forms & Routing**: Each module form posts to its route, which handles input parsing, computes logic, and renders personalized results.

---

## 🧬 Datasets Used

| Module     | Dataset Type          | Description                                   |
|------------|------------------------|-----------------------------------------------|
| Food       | CSV Recipes Dataset     | Includes nutrition facts and cooking steps    |
| Fitness    | JSON Exercise Data      | Mapped to levels, categories, equipment       |
| Sleep      | Custom/Synthetic CSV    | Built for clustering and behavioral analysis  |

---
### 📁 Clone the Repository

```bash
git clone https://github.com/cosmosdisha/healthsync
```

### 📦 Create a Virtual Environment

```bash
python -m venv healthenv
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```
### 🚀 Run the App Locally

```bash
python app.py
```
