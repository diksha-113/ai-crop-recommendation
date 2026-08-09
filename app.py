import streamlit as st
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# ============================================================
# 🌱 AI CROP RECOMMENDATION SYSTEM
# Spreadsheet-Based Smart Farming Simulator
# Class 10 School Project
# ============================================================

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="AI Crop Recommendation",
    page_icon="🌱",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("🌱 AI Crop Recommendation System")

st.subheader("📊 Spreadsheet-Based Smart Farming Simulator")

st.write(
    "Enter weather and soil information in the farm spreadsheet. "
    "The AI model will predict a suitable crop."
)

st.divider()

# ============================================================
# TRAINING DATA
# ============================================================

# Temperature, Rainfall, Soil pH

training_data = [

    # Rice
    [28, 1400, 6.5],
    [30, 1600, 6.2],
    [25, 1200, 6.8],

    # Wheat
    [20, 600, 6.5],
    [22, 700, 6.8],
    [18, 500, 6.7],

    # Maize
    [27, 800, 6.5],
    [30, 900, 6.8],
    [25, 700, 6.2],

    # Cotton
    [28, 700, 6.5],
    [30, 900, 7.0],
    [26, 600, 6.8],

    # Soybean
    [24, 600, 6.2],
    [26, 700, 6.5],
    [25, 550, 6.0],

    # Chickpea
    [22, 500, 6.5],
    [20, 450, 6.8],
    [24, 600, 7.0]
]

# Crop names for training data

crop_names = [
    "Rice",
    "Rice",
    "Rice",

    "Wheat",
    "Wheat",
    "Wheat",

    "Maize",
    "Maize",
    "Maize",

    "Cotton",
    "Cotton",
    "Cotton",

    "Soybean",
    "Soybean",
    "Soybean",

    "Chickpea",
    "Chickpea",
    "Chickpea"
]

# ============================================================
# TRAIN AI MODEL
# ============================================================

model = KNeighborsClassifier(n_neighbors=3)

model.fit(training_data, crop_names)

# ============================================================
# SPREADSHEET INPUT
# ============================================================

st.subheader("📋 Farm Data Spreadsheet")

st.write(
    "Enter the conditions for one or more farms. "
    "You can edit the values directly in the table."
)

# ============================================================
# EMPTY SPREADSHEET
# ============================================================

default_data = pd.DataFrame({
    "Farm": pd.Series([""], dtype="string"),
    "Temperature (°C)": pd.Series([None], dtype="float64"),
    "Rainfall (mm)": pd.Series([None], dtype="float64"),
    "Soil pH": pd.Series([None], dtype="float64")
})

# ============================================================
# DISPLAY EDITABLE SPREADSHEET
# ============================================================

farm_data = st.data_editor(
    default_data,
    num_rows="dynamic",
    width="stretch",
    hide_index=True
)

st.info(
    "💡 Enter the farm name, temperature, rainfall and soil pH. "
    "You can add more farms using the table."
)

# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🤖 ANALYZE FARM DATA",
    width="stretch"
):

    results = []

    # ========================================================
    # GO THROUGH EACH FARM
    # ========================================================

    for index, row in farm_data.iterrows():

        # Get farm name
        farm_name = row["Farm"]

        if pd.isna(farm_name) or str(farm_name).strip() == "":
            farm_name = f"Farm {index + 1}"

        # Get values from spreadsheet
        temperature = row["Temperature (°C)"]
        rainfall = row["Rainfall (mm)"]
        soil_ph = row["Soil pH"]

        # ====================================================
        # CHECK FOR EMPTY VALUES
        # ====================================================

        if (
            pd.isna(temperature)
            or pd.isna(rainfall)
            or pd.isna(soil_ph)
        ):

            results.append({
                "Farm": farm_name,
                "Recommended Crop": "Missing Data",
                "AI Confidence": "N/A",
                "Smart Farming Advice":
                    "⚠️ Please enter all temperature, rainfall and soil pH values."
            })

            continue

        # ====================================================
        # CONVERT VALUES TO NUMBERS
        # ====================================================

        try:

            temperature = float(temperature)
            rainfall = float(rainfall)
            soil_ph = float(soil_ph)

        except (ValueError, TypeError):

            results.append({
                "Farm": farm_name,
                "Recommended Crop": "Invalid Data",
                "AI Confidence": "N/A",
                "Smart Farming Advice":
                    "⚠️ Please enter numbers only."
            })

            continue

        # ====================================================
        # CHECK VALID RANGES
        # ====================================================

        if temperature < 0 or temperature > 60:

            results.append({
                "Farm": farm_name,
                "Recommended Crop": "Invalid Data",
                "AI Confidence": "N/A",
                "Smart Farming Advice":
                    "🌡 Temperature should be between 0°C and 60°C."
            })

            continue

        if rainfall < 0 or rainfall > 5000:

            results.append({
                "Farm": farm_name,
                "Recommended Crop": "Invalid Data",
                "AI Confidence": "N/A",
                "Smart Farming Advice":
                    "🌧 Rainfall should be between 0 and 5000 mm."
            })

            continue

        if soil_ph < 0 or soil_ph > 14:

            results.append({
                "Farm": farm_name,
                "Recommended Crop": "Invalid Data",
                "AI Confidence": "N/A",
                "Smart Farming Advice":
                    "🌱 Soil pH should be between 0 and 14."
            })

            continue

        # ====================================================
        # PREPARE DATA FOR AI
        # ====================================================

        input_data = [
            [temperature, rainfall, soil_ph]
        ]

        # ====================================================
        # AI PREDICTION
        # ====================================================

        prediction = model.predict(input_data)

        crop = prediction[0]

        # ====================================================
        # AI CONFIDENCE
        # ====================================================

        probabilities = model.predict_proba(input_data)

        confidence = max(probabilities[0]) * 100

        # ====================================================
        # SMART FARMING LOGIC
        # ====================================================

        if rainfall < 500:

            advice = (
                "💧 Low rainfall. "
                "Consider irrigation."
            )

        elif rainfall > 1500:

            advice = (
                "🌧 High rainfall. "
                "Check drainage to avoid waterlogging."
            )

        elif soil_ph < 5.5:

            advice = (
                "🌱 Soil is acidic. "
                "Consider appropriate soil treatment."
            )

        elif soil_ph > 7.5:

            advice = (
                "🌱 Soil is alkaline. "
                "Consider suitable soil management."
            )

        else:

            advice = (
                "✅ Conditions appear suitable "
                "for farming."
            )

        # ====================================================
        # SAVE RESULT
        # ====================================================

        results.append({
            "Farm": farm_name,
            "Recommended Crop": crop,
            "AI Confidence": f"{confidence:.1f}%",
            "Smart Farming Advice": advice
        })

    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    st.divider()

    st.subheader("🌾 AI Prediction Results")

    results_df = pd.DataFrame(results)

    st.dataframe(
        results_df,
        width="stretch",
        hide_index=True
    )

    # ========================================================
    # DOWNLOAD RESULTS
    # ========================================================

    csv_data = results_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Results as CSV",
        data=csv_data,
        file_name="crop_recommendation_results.csv",
        mime="text/csv",
        width="content"
    )

    # ========================================================
    # HOW AI WORKS
    # ========================================================

    st.divider()

    st.subheader("🧠 How the AI Works")

    st.write(
        """
        The system uses a **K-Nearest Neighbors (KNN)**
        machine-learning model.

        The model learns from previous farming examples
        containing:

        • Temperature

        • Rainfall

        • Soil pH

        When new farm conditions are entered, the AI
        compares them with previous examples and predicts
        a suitable crop.
        """
    )

    # ========================================================
    # SMART FARMING LOGIC
    # ========================================================

    st.subheader("🌱 Smart Farming Logic")

    st.write(
        """
        The application also checks the farm conditions
        and provides simple smart-farming suggestions.

        💧 Low rainfall → irrigation suggestion

        🌧 Very high rainfall → drainage suggestion

        🌱 Low soil pH → soil treatment suggestion

        🌱 High soil pH → soil management suggestion

        ✅ Suitable conditions → normal farming recommendation
        """
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🌱 AI Crop Recommendation System | "
    "Spreadsheet-Based Predictive Tool | "
    "Class 10 Project"
)

