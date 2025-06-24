from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask import session, redirect, url_for, flash


# Import your custom modules
from food_recommendation import load_food_data, calculate_bmi, calculate_calorie_requirement, recommend_meals_by_calories
df=load_food_data()
from fitness_recommendation import load_exercise_data,recommend_exercises_by_bmi
df_fit=load_exercise_data()
from sleep_recommendation import load_and_prepare_sleep_data, generate_cluster_insights
df_sleep, scaler, kmeans = load_and_prepare_sleep_data()



app = Flask(__name__)
import os
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'fallback-dev-key')

# -------------------------
# Database Setup (SQLite)
# -------------------------
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

# -------------------------
# Routes
# -------------------------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Signup successful. Please login.", "success")
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash("Username already exists.", "danger")
            return redirect('/signup')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    next_page=request.args.get('next') 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(next_page or '/') 
        else:
            flash("Invalid credentials", "danger")
    
    return render_template('login.html',next=next_page)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

# ------------------------
# Module Pages
# ------------------------
@app.route('/food', methods=['GET', 'POST'])
def food():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        gender = request.form['gender']
        age = int(request.form['age'])
        activity_level = request.form['activity_level']

        bmi = calculate_bmi(weight, height)
        calories = calculate_calorie_requirement(gender, weight, height, age, activity_level)
        recommendations = recommend_meals_by_calories(df, calories)
        
        session['food_inputs'] = {
            'weight': weight, 'height': height, 'gender': gender,
            'age': age, 'activity_level': activity_level
        }

        return render_template('food_result.html', bmi=bmi, calories=calories, meals=recommendations)

    return render_template('food_form.html')


@app.route('/food/refresh')
def food_refresh():
    inputs = session.get('food_inputs')
    if not inputs:
        return redirect('/food')

    bmi = calculate_bmi(inputs['weight'], inputs['height'])
    calories = calculate_calorie_requirement(inputs['gender'], inputs['weight'], inputs['height'], inputs['age'], inputs['activity_level'])
    recommendations = recommend_meals_by_calories(df, calories, randomize=True)

    return render_template('food_result.html', bmi=bmi, calories=calories, meals=recommendations)


@app.route('/fitness', methods=['GET', 'POST'])
def fitness():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
    
        bmi = calculate_bmi(weight, height)
        exercises_df = recommend_exercises_by_bmi(df_fit, bmi, n=5, randomize=True)
        exercises = exercises_df.to_dict(orient='records')

        return render_template('fitness_result.html', exercises=exercises, bmi=bmi)

    return render_template('fitness_form.html')


@app.route('/sleep', methods=['GET', 'POST'])
def sleep():
    if request.method == 'POST':
        def safe_float(value, default):
            try:
                return float(value)
            except:
                return default

        def safe_int(value, default):
            try:
                return int(value)
            except:
                return default

        user_input = {
            "Age": safe_int(request.form.get('age', ''), 25),
            "Sleep Duration": safe_float(request.form.get('sleep_duration', ''), 7),
            "Quality of Sleep": safe_float(request.form.get('sleep_quality', ''), 6),
            "Physical Activity Level": safe_float(request.form.get('activity_level', ''), 5),
            "Stress Level": safe_float(request.form.get('stress_level', ''), 5),
            "Heart Rate": safe_float(request.form.get('heart_rate', ''), 75),
            "Daily Steps": safe_int(request.form.get('daily_steps', ''), 6000),
            "Systolic_BP": safe_float(request.form.get('systolic', ''), 120),
            "Diastolic_BP": safe_float(request.form.get('diastolic', ''), 80)
        }

        result = generate_cluster_insights(df_sleep, scaler, kmeans, user_input)
        return render_template('sleep_result.html', result=result)

    return render_template('sleep_form.html')



# ------------------------
# Run the Flask app
# ------------------------
if __name__ == '__main__':
    app.run(debug=True)
