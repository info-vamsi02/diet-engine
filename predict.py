import random

# ================= CALCULATIONS =================
def calculate_calories(age, bmi, gender, activity):
    base = 1800

    if gender == "Male":
        base += 200
    else:
        base -= 100

    if activity == "Low":
        base += 0
    elif activity == "Moderate":
        base += 300
    else:
        base += 500

    if bmi > 25:
        base -= 300
    elif bmi < 18:
        base += 300

    return base


def calculate_macros(calories, bmi):
    if bmi > 25:
        protein_ratio = 0.30
        carbs_ratio = 0.40
        fat_ratio = 0.30
    elif bmi < 18:
        protein_ratio = 0.25
        carbs_ratio = 0.55
        fat_ratio = 0.20
    else:
        protein_ratio = 0.25
        carbs_ratio = 0.50
        fat_ratio = 0.25

    protein = int((calories * protein_ratio) / 4)
    carbs = int((calories * carbs_ratio) / 4)
    fat = int((calories * fat_ratio) / 9)

    return protein, carbs, fat


# ================= DISEASE LOGIC =================
def adjust_for_diseases(diseases, calories):
    avoid = []
    recommend = []

    if "Diabetes" in diseases:
        avoid += ["Sugar", "White Rice", "Sweets"]
        recommend += ["Oats", "Brown Rice", "Millets"]

    if "Hypertension" in diseases or "BP" in diseases:
        avoid += ["Salt", "Pickles", "Processed Food"]
        recommend += ["Banana", "Leafy Vegetables"]

    if "Heart Disease" in diseases:
        avoid += ["Fried Food", "Red Meat"]
        recommend += ["Nuts", "Olive Oil", "Fish"]

    if "Obesity" in diseases:
        calories -= 300
        recommend += ["Salads", "Low Fat Food"]

    if "Thyroid" in diseases:
        avoid += ["Soy", "Processed Food"]
        recommend += ["Eggs", "Iodine-rich foods"]

    if "PCOS" in diseases:
        avoid += ["Sugar", "Refined Carbs"]
        recommend += ["Seeds", "High Protein Foods"]

    if "Anemia" in diseases:
        recommend += ["Spinach", "Dates", "Iron-rich foods"]

    if "Kidney Disease" in diseases:
        avoid += ["Salt", "High Protein"]
        recommend += ["Low Sodium Foods"]

    if "Liver Disease" in diseases:
        avoid += ["Alcohol", "Fried Food"]
        recommend += ["Fruits", "Vegetables"]

    if "Asthma" in diseases:
        avoid += ["Cold Drinks"]
        recommend += ["Warm Fluids", "Ginger"]

    if "Arthritis" in diseases:
        avoid += ["Sugar"]
        recommend += ["Omega-3", "Fish"]

    if "Cholesterol" in diseases:
        avoid += ["Butter", "Fried Food"]
        recommend += ["Oats", "Nuts"]

    if "Depression" in diseases:
        recommend += ["Dark Chocolate", "Banana"]

    if "Vitamin Deficiency" in diseases:
        recommend += ["Fruits", "Vegetables"]

    if "Digestive Issues" in diseases:
        avoid += ["Spicy Food"]
        recommend += ["Curd", "Fiber Foods"]

    if "Allergy" in diseases:
        avoid += ["Peanuts", "Dairy"]

    if "Migraine" in diseases:
        avoid += ["Caffeine"]
        recommend += ["Magnesium Foods"]

    return calories, list(set(avoid)), list(set(recommend))


# ================= MEAL PLAN =================
def generate_meal_plan(guide):
    foods = list(set(guide.get("recommended_foods", [])))

    if len(foods) < 3:
        foods += ["Rice", "Fruits", "Vegetables"]

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    plan = {}
    for day in days:
        selected = random.sample(foods, min(3, len(foods)))
        plan[day] = " + ".join(selected)

    return plan


# ================= PREMIUM MEAL PLAN =================
def generate_meal_to_meal_plan():
    breakfast = [
        "Oats + Fruits", "Boiled Eggs + Toast",
        "Idli + Sambar", "Poha", "Smoothie"
    ]

    lunch = [
        "Rice + Dal + Veg", "Chapati + Curry",
        "Paneer + Roti", "Vegetable Khichdi"
    ]

    dinner = [
        "Soup + Salad", "Light Khichdi",
        "Chapati + Veg", "Eggs + Veg"
    ]

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    plan = {}
    for day in days:
        plan[day] = {
            "Breakfast": random.choice(breakfast),
            "Lunch": random.choice(lunch),
            "Dinner": random.choice(dinner)
        }

    return plan


# ================= EXERCISE =================
def suggest_exercise(bmi, diseases, activity):
    exercises = []

    if bmi > 25:
        exercises += ["Walking 30 min", "Cycling", "Jogging"]

    if bmi < 18:
        exercises += ["Light Yoga", "Stretching"]

    if "Diabetes" in diseases:
        exercises += ["Brisk Walking", "Yoga"]

    if "Heart Disease" in diseases:
        exercises += ["Light Walking", "Breathing Exercises"]

    if "Hypertension" in diseases or "BP" in diseases:
        exercises += ["Meditation", "Yoga"]

    if "Arthritis" in diseases:
        exercises += ["Low Impact Exercise"]

    if "Depression" in diseases:
        exercises += ["Yoga", "Walking"]

    if "Asthma" in diseases:
        exercises += ["Breathing Exercises"]

    if activity == "High":
        exercises += ["Gym Workout", "HIIT"]

    if not exercises:
        exercises = ["General Fitness"]

    return list(set(exercises))


# ================= MAIN FUNCTION =================
def predict_diet(age, bmi, diseases, activity, gender,
                 personalized=None, include_foods=None, exclude_foods=None):

    # -------- SAFE INPUT --------
    try:
        bmi = float(bmi or 0)
    except:
        bmi = 0

    diseases = diseases or []
    include_foods = include_foods or ""
    exclude_foods = exclude_foods or ""

    include_list = [f.strip() for f in include_foods.split(",") if f.strip()]
    exclude_list = [f.strip() for f in exclude_foods.split(",") if f.strip()]

    # -------- DIET TYPE --------
    if bmi > 25:
        diet = "Low Carb Diet"
    elif "Hypertension" in diseases or "BP" in diseases:
        diet = "Low Sodium Diet"
    elif "Diabetes" in diseases:
        diet = "Low Sugar Diet"
    else:
        diet = "Balanced Diet"

    # -------- CALCULATIONS --------
    calories = calculate_calories(age, bmi, gender, activity)
    calories, avoid_extra, recommend_extra = adjust_for_diseases(diseases, calories)
    protein, carbs, fat = calculate_macros(calories, bmi)

    # -------- GUIDE --------
    guide = {
        "calories": f"{calories} kcal",
        "protein": f"{protein}g",
        "carbohydrates": f"{carbs}g",
        "fat": f"{fat}g",
        "vitamins": random.choice(["A, B, C", "B12, D", "Iron, Calcium"]),
        "recommended_foods": ["Rice", "Fruits", "Vegetables", "Eggs"] + recommend_extra,
        "foods_to_avoid": ["Junk Food"] + avoid_extra
    }

    # -------- INCLUDE / EXCLUDE --------
    if include_list:
        guide["recommended_foods"].extend(include_list)

    if exclude_list:
        guide["foods_to_avoid"].extend(exclude_list)
        guide["recommended_foods"] = [
            f for f in guide["recommended_foods"] if f not in exclude_list
        ]

    # -------- PERSONALIZED --------
    if personalized == "yes":
        guide["weekly_plan"] = generate_meal_plan(guide)
        guide["note"] = "🤖 AI Personalized Plan"

    # -------- PREMIUM --------
    if personalized == "premium":
        guide["meal_plan"] = generate_meal_to_meal_plan()
        guide["exercise_plan"] = suggest_exercise(bmi, diseases, activity)
        guide["note"] = "🌟 Premium AI Plan (Meal + Exercise)"

    return diet, guide