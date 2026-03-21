import streamlit as st
import sqlite3
import bcrypt

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Diet Planner",
    page_icon="🥗",
    layout="wide"
)

# ================= LOAD MODEL =================
@st.cache_resource
def load_predict():
    from predict import predict_diet
    return predict_diet

predict_diet = load_predict()

# ================= STYLING =================
st.markdown("""
<style>

/* 🌄 BACKGROUND IMAGE */
[data-testid="stAppViewContainer"] {
    background: url("https://img.pikbest.com/wp/202343/healthy-nutrition-close-up-of-concept-on-white-textured-background_9988050.jpg!bw700") no-repeat center center fixed;
     background-size: cover;      /* 🔥 key fix */
    background-attachment: fixed;
    min-height: 100vh;
}

/* 🌫️ DARK OVERLAY */
[data-testid="stAppViewContainer"]::before {
    content: "";
  
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.6);
    z-index: -1;
}


/* 🔥 SIDEBAR TRANSPARENT */
[data-testid="stSidebar"] {
    background: transparent !important;
}
header[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0.0) !important;
}

/* 🔥 LABELS */
label {
    color: black !important;
    font-weight: 600 !important;
}

/* 🔥 INPUT FIELDS */
input, textarea {
    color: black !important;
    background-color: #f0f0f0 !important;
}

/* Selectbox */
div[data-baseweb="select"] {
    color: black !important;
}

/* 🔥 BUTTONS */
.stButton button {
    background-color: #00f5d4 !important;
    color: black !important;
    font-weight: bold;
    border-radius: 10px;
}

.stButton button:hover {
    background-color: #00c9a7 !important;
}

/* 🔥 RADIO TEXT */
div[role="radiogroup"] label {
    color: white !important;
}

/* CARDS */
.card {
    background: rgba(255,255,255,0.15);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
    color: white;
}

.card h3 {
    color: black;
}

/* METRIC */
.metric-card {
    background: rgba(255,255,255,0.2);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

.metric-title {
    color: black;
}

.metric-value {
    color: black;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* 🔥 CARD TEXT → BLACK */
.card {
    color: #000000 !important;
}

/* Paragraph text */
.card p {
    color: #000000 !important;
    font-weight: 500;
}

/* Headings */
.card h3 {
    color: #000000 !important;
}

/* Weekly plan text */
.card b {
    color: #000000 !important;
}

/* Metric titles */
.metric-title {
    color: #333 !important;
}

/* Optional: darker card for contrast */
.card {
    background: rgba(255, 255, 255, 0.85);
}

</style>
""", unsafe_allow_html=True)

# ================= DATABASE =================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= HEADER =================
st.markdown("# 🧠 AI Diet Recommendation System")
st.markdown("### Personalized diet plans powered by AI 🚀")

# ================= MENU =================
menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# ================= REGISTER =================
if choice == "Register":
    st.subheader("📝 Register")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not name or not email or not password:
            st.warning("All fields required")
        else:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            try:
                c.execute(
                    "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                    (name, email, hashed_pw)
                )
                conn.commit()
                st.success("Registered successfully ✅")
            except sqlite3.IntegrityError:
                st.error("Email already exists ❌")

# ================= LOGIN =================
elif choice == "Login":
    st.subheader("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = c.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if user and bcrypt.checkpw(password.encode(), user[3]):
            st.session_state.user = user[1]
            st.success("Login successful 🎉")
        else:
            st.error("Invalid credentials ❌")

# ================= HOME =================
if st.session_state.user:

    st.subheader(f"🏠 Welcome, {st.session_state.user}")
    st.markdown("### Enter Your Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120)

    with col2:
        bmi = st.number_input("BMI", min_value=10.0, max_value=50.0)

    with col3:
        gender = st.selectbox("Gender", ["Male", "Female"])

    # ================= USER INPUT =================
    diseases = st.multiselect(
        "Select Diseases",
        [
            "None", "Diabetes", "Hypertension", "Heart Disease",
            "Obesity", "Thyroid", "PCOS", "Anemia",
            "Kidney Disease", "Liver Disease", "Asthma",
            "Arthritis", "Cholesterol", "Depression",
            "Vitamin Deficiency", "Digestive Issues",
            "Allergy", "Migraine"
        ]
    )

    if "None" in diseases:
        diseases = []

    activity = st.selectbox("Activity Level", ["Low", "Moderate", "High"])

    include_foods = st.text_input("Foods to include (optional)")
    exclude_foods = st.text_input("Foods to avoid (optional)")

    action = st.radio("Plan Type", ["Normal", "Personalized", "Premium"])

    if st.button("Get Diet Plan"):

        if action == "Personalized":
            personalized = "yes"
        elif action == "Premium":
            personalized = "premium"
        else:
            personalized = None

        diet, guide = predict_diet(
            age, bmi, diseases, activity, gender,
            personalized, include_foods, exclude_foods
        )

        st.success("✅ Diet Plan Generated")

        # -------- DIET --------
        st.markdown(f"""
        <div class="card">
            <h3>🍽️ Recommended Diet</h3>
            <p><b>{diet}</b></p>
        </div>
        """, unsafe_allow_html=True)

        # -------- METRICS --------
        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(f"<div class='metric-card'><div class='metric-title'>Calories</div><div class='metric-value'>{guide['calories']}</div></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-card'><div class='metric-title'>Protein</div><div class='metric-value'>{guide['protein']}</div></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric-card'><div class='metric-title'>Carbs</div><div class='metric-value'>{guide['carbohydrates']}</div></div>", unsafe_allow_html=True)
        col4.markdown(f"<div class='metric-card'><div class='metric-title'>Fat</div><div class='metric-value'>{guide['fat']}</div></div>", unsafe_allow_html=True)

        # -------- FOODS --------
        st.markdown(f"""
        <div class="card">
            <h3>🥦 Recommended Foods</h3>
            <p>{", ".join(guide["recommended_foods"])}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h3>🚫 Foods to Avoid</h3>
            <p>{", ".join(guide["foods_to_avoid"])}</p>
        </div>
        """, unsafe_allow_html=True)

        # -------- WEEKLY --------
        if "weekly_plan" in guide:
            weekly_html = ""
            for day, meal in guide["weekly_plan"].items():
                weekly_html += f"<p><b>{day}:</b> {meal}</p>"

            st.markdown(f"""
            <div class="card">
                <h3>📅 Weekly Plan</h3>
                {weekly_html}
            </div>
            """, unsafe_allow_html=True)

        # -------- PREMIUM --------
        if "meal_plan" in guide:
            meal_html = ""
            for day, meals in guide["meal_plan"].items():
                meal_html += f"<p><b>{day}</b><br>"
                meal_html += f"🍳 Breakfast: {meals['Breakfast']}<br>"
                meal_html += f"🍛 Lunch: {meals['Lunch']}<br>"
                meal_html += f"🌙 Dinner: {meals['Dinner']}</p>"

            st.markdown(f"""
            <div class="card">
                <h3>🍽️ Meal-to-Meal Plan</h3>
                {meal_html}
            </div>
            """, unsafe_allow_html=True)

        # -------- EXERCISE --------
        if "exercise_plan" in guide:
            st.markdown(f"""
            <div class="card">
                <h3>🏋️ Exercise Plan</h3>
                <p>{", ".join(guide["exercise_plan"])}</p>
            </div>
            """, unsafe_allow_html=True)

        # -------- NOTE --------
        if "note" in guide:
            st.markdown(f"""
            <div class="card">
                <h3>🤖 AI Note</h3>
                <p>{guide["note"]}</p>
            </div>
            """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()