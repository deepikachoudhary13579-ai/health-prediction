import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("health_prediction.pkl")

st.set_page_config(page_title="Health Lifestyle Predictor")

st.title("🏥 Health Lifestyle Predictor")

st.write("Enter your lifestyle details below")

# User Inputs
age = st.number_input("Age", min_value=1, max_value=100, value=25)

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

height = st.number_input(
    "Height (meters)",
    min_value=0.5,
    max_value=2.5,
    value=1.70
)

weight = st.number_input(
    "Weight (kg)",
    min_value=20.0,
    max_value=200.0,
    value=70.0
)

sleep = st.number_input(
    "Sleep Hours",
    min_value=0.0,
    max_value=24.0,
    value=8.0
)

exercise = st.number_input(
    "Exercise Days/Week",
    min_value=0,
    max_value=7,
    value=3
)

steps = st.number_input(
    "Daily Steps",
    min_value=0,
    value=8000
)

water = st.number_input(
    "Water Intake (Litres)",
    min_value=0.0,
    value=2.5
)

protein = st.number_input(
    "Protein Intake (grams)",
    min_value=0,
    value=60
)

junk = st.number_input(
    "Junk Food Frequency/Week",
    min_value=0,
    value=2
)

smoking = st.selectbox(
    "Smoking",
    ["No", "Yes"]
)

alcohol = st.selectbox(
    "Alcohol",
    ["No", "Yes"]
)

if st.button("Predict Health Status"):

    bmi = weight / (height ** 2)

    gender_value = 0 if gender == "Male" else 1
    smoking_value = 1 if smoking == "Yes" else 0
    alcohol_value = 1 if alcohol == "Yes" else 0

    user_data = np.array([[
        age,
        gender_value,
        bmi,
        sleep,
        exercise,
        steps,
        water,
        protein,
        junk,
        smoking_value,
        alcohol_value
    ]])

    prediction = model.predict(user_data)

    st.success(f"Predicted Health Status: {prediction[0]}")

    # Health Score
    score = 100

    if sleep < 7:
        score -= 10

    if exercise < 3:
        score -= 15

    if steps < 8000:
        score -= 10

    if water < 2:
        score -= 10

    if junk > 3:
        score -= 15

    if smoking_value == 1:
        score -= 20

    if alcohol_value == 1:
        score -= 10

    score = max(score, 0)

    st.subheader("Health Score")
    st.progress(score / 100)
    st.write(f"Score: {score}/100")

    st.subheader("Recommendations")

    recommendations = []

    if sleep < 7:
        recommendations.append("Sleep 7-9 hours daily")

    if exercise < 3:
        recommendations.append("Exercise more frequently")

    if water < 2:
        recommendations.append("Drink more water")

    if protein < 60:
        recommendations.append("Increase protein intake")

    if junk > 3:
        recommendations.append("Reduce junk food")

    if len(recommendations) == 0:
        st.success("Great lifestyle habits!")

    for rec in recommendations:
        st.write("✔", rec)

    st.subheader("Possible Risks")

    risks = []

    if bmi > 30:
        risks.append("Obesity")

    if smoking_value == 1:
        risks.append("Lung Disease")

    if junk > 4:
        risks.append("Diabetes")

    if sleep < 6:
        risks.append("Fatigue")

    if exercise == 0:
        risks.append("Heart Disease")

    if len(risks) == 0:
        st.success("No major risks detected")

    for risk in risks:
        st.write("⚠", risk)