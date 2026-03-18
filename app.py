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
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

.card h3 {
    color: #00f5d4;
}

.metric-card {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

.metric-title {
    color: #bbb;
    font-size: 14px;
}

.metric-value {
    font-size: 22px;
    font-weight: bold;
    color: #00f5d4;
}
</style>
""", unsafe_allow_html=True)

# ================= DATABASE =================
conn = sqlite3.connect("../users.db", check_same_thread=False)
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
    st.markdown("## 📝 Register")

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
    st.markdown("## 🔐 Login")

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
    st.markdown(f"## 🏠 Welcome, {st.session_state.user}")

    st.markdown("### Enter Your Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120)

    with col2:
        bmi = st.number_input("BMI", min_value=10.0, max_value=50.0)

    with col3:
        gender = st.selectbox("Gender", ["Male", "Female"])

    diseases = st.multiselect(
        "Select Diseases",
        ["None", "Diabetes", "Heart Disease", "BP", "Obesity"]
    )

    activity = st.selectbox(
        "Activity Level",
        ["Low", "Moderate", "High"]
    )

    include_foods = st.text_input("Foods to include (optional)")
    exclude_foods = st.text_input("Foods to avoid (optional)")

    action = st.radio("Plan Type", ["Normal", "Personalized"])

    if st.button("Get Diet Plan"):
        try:
            personalized = "yes" if action == "Personalized" else None

            diet, guide = predict_diet(
                age, bmi, diseases, activity, gender,
                personalized, include_foods, exclude_foods
            )

            st.success("✅ Diet Plan Generated")

            # ================= CARD UI =================
            st.markdown("## 🥗 Your AI Diet Plan")

            # Diet Card
            st.markdown(f"""
            <div class="card">
                <h3>🍽️ Recommended Diet</h3>
                <p><b>{diet}</b></p>
            </div>
            """, unsafe_allow_html=True)

            # Metrics
            col1, col2, col3, col4 = st.columns(4)

            col1.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Calories</div>
                <div class="metric-value">{guide['calories']}</div>
            </div>
            """, unsafe_allow_html=True)

            col2.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Protein</div>
                <div class="metric-value">{guide['protein']}</div>
            </div>
            """, unsafe_allow_html=True)

            col3.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Carbs</div>
                <div class="metric-value">{guide['carbohydrates']}</div>
            </div>
            """, unsafe_allow_html=True)

            col4.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Fat</div>
                <div class="metric-value">{guide['fat']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Recommended Foods
            st.markdown(f"""
            <div class="card">
                <h3>🥦 Recommended Foods</h3>
                <p>{", ".join(guide["recommended_foods"])}</p>
            </div>
            """, unsafe_allow_html=True)

            # Avoid Foods
            st.markdown(f"""
            <div class="card">
                <h3>🚫 Foods to Avoid</h3>
                <p>{", ".join(guide["foods_to_avoid"])}</p>
            </div>
            """, unsafe_allow_html=True)

            # Weekly Plan
            if "weekly_plan" in guide:
                weekly_html = ""
                for day, meal in guide["weekly_plan"].items():
                    weekly_html += f"<p><b>{day}:</b> {meal}</p>"

                st.markdown(f"""
                <div class="card">
                    <h3>📅 Weekly Meal Plan</h3>
                    {weekly_html}
                </div>
                """, unsafe_allow_html=True)

            # Note



        except Exception as e:
            st.error(f"Error: {e}")

    # LOGOUT
    if st.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()