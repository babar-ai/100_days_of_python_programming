import streamlit as st
import pandas as pd
import clean_data
import models
import Ensemble_models

# New data dictionary
new_data = {
    'age': 27,
    'gender': 'M',
    'height_cm': 172.3,
    'weight_kg': 75.24,
    'body fat_%': 21.3,
    'diastolic': 80,
    'systolic': 130,
    'gripForce': 54.9,
    'sit and bend forward_cm': 18.4,
    'sit-ups counts': 60,
    'broad jump_cm': 217
}

# Streamlit sidebar input for new data
st.sidebar.header("Input your data")

# Collecting input data via the sidebar
age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=27)
gender = st.sidebar.selectbox("Gender", options=['M', 'F'], index=0)
height = st.sidebar.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=172.3)
weight = st.sidebar.number_input("Weight (kg)", min_value=20.0, max_value=200.0, value=75.24)
body_fat = st.sidebar.number_input("Body Fat (%)", min_value=0.0, max_value=50.0, value=21.3)
diastolic = st.sidebar.number_input("Diastolic", min_value=40, max_value=150, value=80)
systolic = st.sidebar.number_input("Systolic", min_value=80, max_value=180, value=130)
gripForce = st.sidebar.number_input("Grip Force", min_value=0.0, max_value=100.0, value=54.9)
sit_bend_forward = st.sidebar.number_input("Sit and Bend Forward (cm)", min_value=0.0, max_value=100.0, value=18.4)
sit_ups = st.sidebar.number_input("Sit-ups Count", min_value=0, max_value=100, value=60)
broad_jump = st.sidebar.number_input("Broad Jump (cm)", min_value=0.0, max_value=300.0, value=217)

# Create a DataFrame from user input
new_data = {
    'age': age,
    'gender': gender,
    'height_cm': height,
    'weight_kg': weight,
    'body fat_%': body_fat,
    'diastolic': diastolic,
    'systolic': systolic,
    'gripForce': gripForce,
    'sit and bend forward_cm': sit_bend_forward,
    'sit-ups counts': sit_ups,
    'broad jump_cm': broad_jump
}

newdata_frame = pd.DataFrame([new_data])

# Normalize the new data
newdata_scaled = clean_data.Normalize_newdata(newdata_frame)

# OneHot Encoding the gender column
newdata_encoded = clean_data.encoder_testdata(newdata_scaled)

# Apply PCA
new_data_pca = models.Pca_test(newdata_encoded)

# Ensemble prediction model
ensemble_model = Ensemble_models.Ensemble_predication(newdata_encoded, new_data_pca)

# Mapping numerical classes to labels
class_mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
predicted_label = class_mapping[ensemble_model[0]]

# Display predicted label
st.write(f'The predicted class is {predicted_label}')
