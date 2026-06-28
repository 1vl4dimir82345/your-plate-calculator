import streamlit as st

st.set_page_config(page_title="Your Plate, Perfected", page_icon="🍽️")

st.title("Your Plate, Perfected")
st.subheader("Nutrition Calculator")

st.write("Enter your details below to get your personalized macros.")

# INPUTS
age = st.number_input("Age (years)", min_value=15, max_value=80, value=25)
weight = st.number_input("Weight (kg)", min_value=40.0, max_value=200.0, value=80.0)
height = st.number_input("Height (cm)", min_value=140.0, max_value=220.0, value=180.0)

activity_level = st.selectbox(
    "Activity Level",
    ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"]
)

goal = st.selectbox(
    "Goal",
    ["Fat Loss", "Maintenance", "Muscle Gain"]
)

# CALCULATIONS
bmr = 10 * weight + 6.25 * height - 5 * age + 5

activity_multipliers = {
    "Sedentary": 1.2,
    "Lightly Active": 1.375,
    "Moderately Active": 1.55,
    "Very Active": 1.725,
    "Extra Active": 1.9
}

tdee = bmr * activity_multipliers[activity_level]

if goal == "Fat Loss":
    daily_calories = tdee * 0.8
elif goal == "Muscle Gain":
    daily_calories = tdee * 1.1
else:
    daily_calories = tdee

protein = weight * 2.2
fats = (daily_calories * 0.25) / 9
carbs = (daily_calories * 0.4) / 4

# RESULTS
st.divider()
st.subheader("Your Results")

col1, col2, col3 = st.columns(3)
col1.metric("Daily Calories", f"{daily_calories:.0f} kcal")
col2.metric("Protein", f"{protein:.0f} g")
col3.metric("Carbs", f"{carbs:.0f} g")

st.metric("Fats", f"{fats:.0f} g")

st.caption("Note: This calculator uses the Mifflin-St Jeor formula (optimized for men).")