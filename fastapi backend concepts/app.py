from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import clean_data
import models
import Ensemble_models

# Initialize FastAPI app
app = FastAPI()

# Define the input schema using Pydantic
class UserInput(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    body_fat: float
    diastolic: int
    systolic: int
    gripForce: float
    sit_and_bend_forward_cm: float
    sit_ups_counts: int
    broad_jump_cm: int

# Define the mapping for class labels
class_mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}

@app.post("/predicat")
def predict_category(user_input: UserInput):
    # Convert input to DataFrame
    input_data = pd.DataFrame([{
        'age': user_input.age,
        'gender': user_input.gender,
        'height_cm': user_input.height_cm,
        'weight_kg': user_input.weight_kg,
        'body fat_%': user_input.body_fat,
        'diastolic': user_input.diastolic,
        'systolic': user_input.systolic,
        'gripForce': user_input.gripForce,
        'sit and bend forward_cm': user_input.sit_and_bend_forward_cm,
        'sit-ups counts': user_input.sit_ups_counts,
        'broad jump_cm': user_input.broad_jump_cm
    }])
    
    
@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}
    

    # Preprocess data
    scaled_data = clean_data.Normalize_newdata(input_data)
    encoded_data = clean_data.encoder_testdata(scaled_data)

    # Apply PCA
    pca_data = models.Pca_test(encoded_data)

    # Get the prediction from the ensemble model
    prediction = Ensemble_models.Ensemble_predication(encoded_data, pca_data)

    # Map the prediction to a label
    predicted_label = class_mapping[prediction[0]]

    # Return the result
    return {"predicted_class": predicted_label}

# Run the app using uvicorn
# Command: uvicorn app:app --reload
