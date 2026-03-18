import random

# ================= MEAL PLAN =================
def generate_meal_plan(guide):
    foods = guide.get("recommended_foods", [])

    if not foods:
        foods = ["Rice", "Fruits", "Vegetables"]

    def meal():
        return random.choice(foods)

    return {
        "Monday": f"{meal()} + {meal()} + {meal()}",
        "Tuesday": f"{meal()} + {meal()} + {meal()}",
        "Wednesday": f"{meal()} + {meal()} + {meal()}",
        "Thursday": f"{meal()} + {meal()} + {meal()}",
        "Friday": f"{meal()} + {meal()} + {meal()}",
        "Saturday": f"{meal()} + {meal()} + {meal()}",
        "Sunday": f"{meal()} + {meal()} + {meal()}"
    }


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

    # -------- DIET LOGIC --------
    if bmi > 25:
        diet = "Low Carb Diet"
    elif "Hypertension" in diseases or "BP" in diseases:
        diet = "Low Sodium Diet"
    elif "Diabetes" in diseases:
        diet = "Low Sugar Diet"
    else:
        diet = "Balanced Diet"

    # -------- GUIDE --------
    guide = {
        "calories": "2000 kcal",
        "protein": "70g",
        "carbohydrates": "250g",
        "fat": "60g",
        "vitamins": "A, B, C",
        "recommended_foods": ["Rice", "Fruits", "Vegetables", "Eggs"],
        "foods_to_avoid": ["Junk food", "Sugar"]
    }

    # -------- APPLY INCLUDE / EXCLUDE --------
    if include_list:
        guide["recommended_foods"].extend(include_list)

    if exclude_list:
        guide["foods_to_avoid"].extend(exclude_list)

        guide["recommended_foods"] = [
            food for food in guide["recommended_foods"]
            if food not in exclude_list
        ]

    # -------- PERSONALIZED PLAN --------
    if personalized == "yes":
        guide["weekly_plan"] = generate_meal_plan(guide)
        guide["note"] = "🤖 AI Personalized Plan"

    return diet, guide