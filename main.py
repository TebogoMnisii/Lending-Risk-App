from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Allow CORS from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model, encoder, and features list
model = joblib.load("model.pkl")
ohe = joblib.load("encoder.pkl")
feature_cols = joblib.load("features.pkl")

class Applicant(BaseModel):
    employment_status: str
    monthly_income: float
    monthly_rent: float
    has_bank_account: int
    repaid_previous_loans: int
    last_loan_amount_repaid: float
    number_of_dependents: int
    business_years: float

@app.post("/predict")
async def predict(applicant: Applicant):
    data = applicant.dict()

    # Build DataFrame
    df = pd.DataFrame([{
        "income": data["monthly_income"],
        "rent": data["monthly_rent"],
        "dependents": data["number_of_dependents"],
        "repaid_previous_loans": data["repaid_previous_loans"],
        "loan_repayment_amount": data["last_loan_amount_repaid"],
        "business_years": data["business_years"],
        "has_bank_account": data["has_bank_account"],
        "employment_status": data["employment_status"],
    }])

    # Derived feature
    df["rent_to_income_ratio"] = df["rent"] / df["income"]

    # Encode employment_status
    employment_encoded = ohe.transform(df[["employment_status"]])
    df = df.drop("employment_status", axis=1).reset_index(drop=True)
    df_encoded = pd.concat([df, pd.DataFrame(employment_encoded, columns=ohe.get_feature_names_out())], axis=1)

    # Reorder columns to match training features
    df_encoded = df_encoded[feature_cols]

    # Predict
    prediction = model.predict(df_encoded)[0]
    confidence = model.predict_proba(df_encoded)[0][prediction]

    return {
        "prediction": "Not Likely to Default" if prediction == 0 else "Likely to Default",
        "confidence": round(confidence * 100, 1),
    }

