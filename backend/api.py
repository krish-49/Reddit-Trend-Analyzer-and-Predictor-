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


# ---------------- Load model ----------------
MODEL_DIR = "../models"

model = joblib.load("C:\\Users\\krish\\OneDrive\\Desktop\\RedditTrendPredictor\\models\\trend_model.pkl")
vectorizer = joblib.load("C:\\Users\\krish\\OneDrive\\Desktop\\RedditTrendPredictor\\models\\tfidf_vectorizer.pkl")
scaler = joblib.load("C:\\Users\\krish\\OneDrive\\Desktop\\RedditTrendPredictor\\models\\scaler.pkl")

DAY_MAP = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2,
    "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
}

# ---------------- Request schema ----------------
class PredictRequest(BaseModel):
    title: str
    selftext: str
    hour: int
    dayofweek: str

# ---------------- API endpoint ----------------
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

    # Ensure training feature order
    numeric = numeric[scaler.feature_names_in_]

    X_num = scaler.transform(numeric)
    X_text = vectorizer.transform([text])
    X = hstack([X_num, X_text])

    prob = model.predict_proba(X)[0][1] * 100

    return {
        "trend_probability": round(prob, 2),
        "label": (
            "High" if prob >= 70 else
            "Medium" if prob >= 40 else
            "Low"
        )
    }
