import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import joblib

# Sample realistic data
data = {
    "income": [2000, 3000, 1500, 2500, 4000],
    "rent": [600, 800, 500, 700, 1000],
    "employment_status": ["Employed", "Self-Employed", "Unemployed", "Student", "Employed"],
    "dependents": [0, 1, 2, 0, 1],
    "repaid_previous_loans": [1, 0, 1, 0, 1],
    "loan_repayment_amount": [500, 0, 300, 0, 700],
    "default": [0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

# Create rent_to_income_ratio feature
df["rent_to_income_ratio"] = df["rent"] / df["income"]

X = df.drop("default", axis=1)
y = df["default"]

# OneHotEncoder for categorical features
ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
X_encoded = ohe.fit_transform(X[["employment_status"]])

X_remaining = X.drop("employment_status", axis=1).reset_index(drop=True)
X_final = pd.concat([X_remaining, pd.DataFrame(X_encoded, columns=ohe.get_feature_names_out())], axis=1)

# Train/test split (for demonstration, we train on all data)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_final, y)

# Save the model, encoder, and feature columns
joblib.dump(model, "model.pkl")
joblib.dump(ohe, "encoder.pkl")
joblib.dump(X_final.columns.tolist(), "features.pkl")

print("Model, encoder, and features saved.")
