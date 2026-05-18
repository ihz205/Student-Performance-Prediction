import streamlit as st
import pandas as pd
import sqlite3
import joblib

# Load model
model = joblib.load("model.pkl")

# Page title
st.title("🎓 Student Performance Prediction System")

st.write("Enter student details to predict final grade.")

# User inputs
age = st.slider("Age", 15, 22)

studytime = st.slider("Study Time", 1, 4)

failures = st.slider("Past Failures", 1, 4)

absences = st.slider("Absences", 0, 12)

G1 = st.slider("First Period Grade (G1)", 0, 20)

G2 = st.slider("Second Period Grade (G2)", 0, 20)

# Predict button
if st.button("Predict Performance"):

    # Create dataframe
    input_data = pd.DataFrame([{
        'age': age,
        'studytime': studytime,
        'failures': failures,
        'absences': absences,
        'G1': G1,
        'G2': G2
    }])

    # Prediction
    prediction = model.predict(input_data)[0]

    # Show result
    st.success(f"Predicted Final Grade (G3): {round(prediction, 2)}")

    # Save to database
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students (
        age,
        studytime,
        failures,
        absences,
        G1,
        G2,
        predicted_G3
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        age,
        studytime,
        failures,
        absences,
        G1,
        G2,
        float(prediction)
    ))

    conn.commit()
    conn.close()

    st.info("Student record saved to database.")

# Show records
if st.checkbox("Show Database Records"):

    conn = sqlite3.connect("students.db")

    df = pd.read_sql(
        "SELECT * FROM students",
        conn
    )

    st.dataframe(df)

    conn.close()