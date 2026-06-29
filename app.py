import streamlit as st
from datetime import date

st.set_page_config(page_title="Your Plate, Perfected", page_icon="🍽️", layout="wide")

st.title("Your Plate, Perfected")
st.subheader("Daily Meal Builder + History")

st.divider()

# ==================== 1. CALCULEAZĂ ȚINTELE ====================
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 15, 80, 25)
    weight = st.number_input("Weight (kg)", 40.0, 200.0, 80.0)
    height = st.number_input("Height (cm)", 140.0, 220.0, 180.0)

with col2:
    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"])
    goal = st.selectbox("Goal", ["Fat Loss", "Maintenance", "Muscle Gain"])

if st.button("Calculate Targets"):
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
    mult = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55,
            "Very Active": 1.725, "Extra Active": 1.9}
    tdee = bmr * mult[activity]

    if goal == "Fat Loss":
        cal = tdee * 0.8
    elif goal == "Muscle Gain":
        cal = tdee * 1.1
    else:
        cal = tdee

    st.session_state.targets = {
        "calories": round(cal),
        "protein": round(weight * 2.2),
        "carbs": round((cal * 0.4) / 4),
        "fats": round((cal * 0.25) / 9)
    }
    st.session_state.meals = []
    st.success("Targets calculated!")

# ==================== 2. DACĂ AVEM ȚINTE ====================
if "targets" in st.session_state:

    st.divider()
    st.subheader("Your Daily Targets")

    t = st.session_state.targets
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Calories", t["calories"])
    col2.metric("Protein", f"{t['protein']} g")
    col3.metric("Carbs", f"{t['carbs']} g")
    col4.metric("Fats", f"{t['fats']} g")

    # ==================== 3. TOATE REȚETELE ====================
    all_recipes = {
        "Breakfast": [
            {"name": "Classic Tomato & Pepper Omelette with Toast", "cal": 375, "pro": 47, "car": 34, "fat": 12},
            {"name": "Protein Berry Oats with Toast", "cal": 410, "pro": 46, "car": 38, "fat": 9},
            {"name": "Scrambled Eggs with Smoked Salmon", "cal": 410, "pro": 47, "car": 8, "fat": 20},
            {"name": "Protein French Toast", "cal": 400, "pro": 45, "car": 38, "fat": 11},
            {"name": "Overnight Protein Oats", "cal": 420, "pro": 45, "car": 42, "fat": 10},
        ],
        "Lunch": [
            {"name": "Grilled Chicken Breast Classic", "cal": 475, "pro": 52, "car": 38, "fat": 12},
            {"name": "Turkey Rice Bowl", "cal": 465, "pro": 49, "car": 38, "fat": 11},
            {"name": "Lean Beef with Sweet Potato", "cal": 485, "pro": 48, "car": 42, "fat": 14},
            {"name": "Lean Beef Stir-Fry", "cal": 455, "pro": 48, "car": 35, "fat": 14},
        ],
        "Dinner": [
            {"name": "Baked White Fish with Potatoes", "cal": 430, "pro": 46, "car": 32, "fat": 12},
            {"name": "Grilled Chicken with Sweet Potato", "cal": 420, "pro": 48, "car": 32, "fat": 10},
            {"name": "Lean Beef with Salad & Potatoes", "cal": 430, "pro": 46, "car": 28, "fat": 14},
        ],
        "Snacks": [
            {"name": "Classic Whey Shake", "cal": 280, "pro": 42, "car": 28, "fat": 3},
            {"name": "Protein Pancakes", "cal": 295, "pro": 38, "car": 28, "fat": 6},
            {"name": "Greek Yogurt with Dark Chocolate", "cal": 260, "pro": 28, "car": 22, "fat": 9},
            {"name": "Chocolate Protein Mousse", "cal": 260, "pro": 40, "car": 18, "fat": 7},
        ]
    }

    # ==================== 4. ADAUGĂ MESE ====================
    st.divider()
    st.subheader("Add Meals")

    cat = st.selectbox("Category", list(all_recipes.keys()))
    meal_list = [r["name"] for r in all_recipes[cat]]
    chosen = st.selectbox("Choose a meal", meal_list)

    if st.button("Add Meal"):
        for r in all_recipes[cat]:
            if r["name"] == chosen:
                if "meals" not in st.session_state:
                    st.session_state.meals = []
                st.session_state.meals.append(r)
                st.success(f"Added: {chosen}")
                break

    # ==================== 5. TOTAL CURENT ====================
    if "meals" in st.session_state and st.session_state.meals:
        st.divider()
        st.subheader("Today's Intake So Far")

        total_cal = sum(m["cal"] for m in st.session_state.meals)
        total_pro = sum(m["pro"] for m in st.session_state.meals)
        total_car = sum(m["car"] for m in st.session_state.meals)
        total_fat = sum(m["fat"] for m in st.session_state.meals)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Calories", f"{total_cal} / {st.session_state.targets['calories']}")
        col2.metric("Protein", f"{total_pro} / {st.session_state.targets['protein']} g")
        col3.metric("Carbs", f"{total_car} / {st.session_state.targets['carbs']} g")
        col4.metric("Fats", f"{total_fat} / {st.session_state.targets['fats']} g")

        st.write("**Meals added today:**")
        for m in st.session_state.meals:
            st.write(f"- {m['name']} ({m['cal']} kcal | {m['pro']}g P)")

    # ==================== 6. ISTORIC ZILNIC (SIMPLU) ====================
    st.divider()
    st.subheader("Daily History")

    if st.button("Save Today"):
        if "history" not in st.session_state:
            st.session_state.history = {}

        today = str(date.today())
        total_cal = sum(m["cal"] for m in st.session_state.get("meals", []))
        st.session_state.history[today] = total_cal
        st.success(f"Saved {today} — {total_cal} kcal")

    if "history" in st.session_state and st.session_state.history:
        st.write("**Previous days:**")
        for day, cal in st.session_state.history.items():
            st.write(f"- {day}: **{cal} kcal**")
