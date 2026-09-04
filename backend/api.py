import os
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from textblob import TextBlob
from datetime import datetime
from scipy.sparse import hstack
import joblib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load model using relative paths (works on any machine) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

model = joblib.load(os.path.join(MODELS_DIR, "trend_model.pkl"))
vectorizer = joblib.load(os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl"))
scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))

DAY_MAP = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2,
    "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
}

# --- Time-based engagement multipliers (based on Reddit peak activity research) ---
# Hours are in 24h format (UTC). Reddit peaks ~14:00-17:00 UTC on weekdays.
HOUR_MULTIPLIER = {
    0: 0.88,  1: 0.85,  2: 0.83,  3: 0.82,  4: 0.83,
    5: 0.86,  6: 0.90,  7: 0.94,  8: 0.97,  9: 1.00,
    10: 1.03, 11: 1.06, 12: 1.08, 13: 1.10, 14: 1.12,
    15: 1.12, 16: 1.10, 17: 1.07, 18: 1.05, 19: 1.03,
    20: 1.01, 21: 0.98, 22: 0.95, 23: 0.91
}

# Weekdays (Mon-Thu) see 5-12% higher engagement than weekends on Reddit.
DAY_MULTIPLIER = {
    "Monday": 1.05, "Tuesday": 1.08, "Wednesday": 1.07,
    "Thursday": 1.06, "Friday": 1.02, "Saturday": 0.90, "Sunday": 0.88
}

# --- Request schema ---
class PredictRequest(BaseModel):
    title: str
    selftext: str
    hour: int
    dayofweek: str

# --- API endpoint ---
@app.post("/predict")
def predict(req: PredictRequest):
    text = (req.title + " " + req.selftext).lower()
    sentiment = TextBlob(text).sentiment.polarity

    numeric = pd.DataFrame([{
        "title_len": len(req.title),
        "selftext_len": len(req.selftext),
        "hour": req.hour,
        "dayofweek": DAY_MAP[req.dayofweek],
        "month": datetime.now().month,
        "sentiment": sentiment,
        "num_comments": 0,
        "avg_comment_sentiment": 0,
        "avg_comment_score": 0
    }])

    numeric = numeric[scaler.feature_names_in_]

    X_num = scaler.transform(numeric)
    X_text = vectorizer.transform([text])
    X = hstack([X_num, X_text])

    prob = model.predict_proba(X)[0][1] * 100

    # Apply time-aware engagement adjustment
    h_mult = HOUR_MULTIPLIER.get(req.hour, 1.0)
    d_mult = DAY_MULTIPLIER.get(req.dayofweek, 1.0)
    prob = prob * h_mult * d_mult
    prob = round(min(max(prob, 0.0), 100.0), 2)

    return {
        "trend_probability": prob,
        "label": (
            "High" if prob >= 70 else
            "Medium" if prob >= 40 else
            "Low"
        )
    }
