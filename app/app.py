import streamlit as st
import pandas as pd
import numpy as np
from textblob import TextBlob
import joblib

# ===============================
# 🔥 Reddit Trend Predictor App
# ===============================

st.set_page_config(page_title="Reddit Trend Predictor", layout="centered")

st.title("📈 Reddit Trend Predictor & Analyzer")
st.write("Enter a Reddit post title and description to predict whether it will trend.")

# --- Input Section ---
with st.form("trend_form"):
    title = st.text_input("Post Title", placeholder="Enter the Reddit post title...")
    selftext = st.text_area("Post Description", placeholder="Enter the post body text...")
    hour = st.slider("Hour of the Day", 0, 23, 12)
    dayofweek = st.selectbox(
        "Day of the Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    submitted = st.form_submit_button("Predict")

# --- Helper Functions ---
day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}

# def extract_features(title, selftext, hour, dayofweek):
#     sentiment = TextBlob(title + " " + selftext).sentiment.polarity
#     title_len = len(title)
#     selftext_len = len(selftext)

#     features = pd.DataFrame([
#         {
#             "title_len": title_len,
#             "selftext_len": selftext_len,
#             "hour": hour,
#             "dayofweek": day_map[dayofweek],
#             "month": 11,  # current month placeholder
#             "sentiment": sentiment,
#             "num_comments": 0,
#             "avg_comment_sentiment": 0,
#             "avg_comment_score": 0,
#         }
#     ])
#     return features

def extract_features(title, selftext, hour, dayofweek):
    sentiment = TextBlob(title + " " + selftext).sentiment.polarity
    text = (title + " " + selftext).lower()
    numeric = pd.DataFrame([{
        "title_len": len(title),
        "selftext_len": len(selftext),
        "hour": hour,
        "dayofweek": day_map[dayofweek],
        "month": 11,
        "sentiment": sentiment,
        "num_comments": 0,
        "avg_comment_sentiment": 0,
        "avg_comment_score": 0
    }])

    X_num_scaled = scaler.transform(numeric)
    X_text = vectorizer.transform([text])

    from scipy.sparse import hstack
    X_final = hstack([X_num_scaled, X_text])
    return X_final

# --- Load Model ---
@st.cache_resource
@st.cache_resource
def load_model():
    try:
        model = joblib.load("C:\\Users\\krish\\OneDrive\\Desktop\\RedditTrendPredictor\\models\\trend_model.pkl")
        vectorizer = joblib.load("C:\\Users\\krish\\OneDrive\\Desktop\\RedditTrendPredictor\\models\\tfidf_vectorizer.pkl")
        scaler = joblib.load("C:\\Users\\krish\\OneDrive\\Desktop\\RedditTrendPredictor\\models\\scaler.pkl")
        st.success("✅ Model and preprocessors loaded successfully.")
        return model, vectorizer, scaler
    except Exception as e:
        st.error(f"❌ Could not load model/vectorizer/scaler: {e}")
        return None, None, None


model, vectorizer, scaler = load_model()

# --- Prediction ---
if submitted:
    if not title.strip():
        st.warning("Please enter a post title.")
    elif model is None:
        st.error("Model not available. Train and save your model as 'trend_model.pkl'.")
    else:
        X = extract_features(title, selftext, hour, dayofweek)
        prob = model.predict_proba(X)[0][1]

        st.subheader("Prediction Result:")
        st.metric(label="Trend Probability", value=f"{prob*100:.2f}%")

        if prob >= 0.5:
            st.success("🔥 This post is likely to TREND!")
        else:
            st.info("💤 This post might not trend much.")

st.markdown("---")
st.caption("Model trained on Reddit posts with text, sentiment, and time-based features.")
