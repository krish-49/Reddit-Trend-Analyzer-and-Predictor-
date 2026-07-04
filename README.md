# 📈 Reddit Trend Predictor & Analyzer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Scikit-learn](https://img.shields.io/badge/ML-Scikit--learn-orange)](https://scikit-learn.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React-blue)](https://reactjs.org/)
[![Streamlit](https://img.shields.io/badge/WebApp-Streamlit-red)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 🧠 Overview
The **Reddit Trend Predictor** is a data science project that predicts whether a Reddit post is likely to trend based on its **title**, **description**, **sentiment**, and **time-based features**.

It uses the **Meta Reddit Corpus Dataset** from Kaggle and includes:
- A **FastAPI** backend for real-time predictions
- A **React** frontend with a speedometer result display
- A **Streamlit** app as an alternative standalone UI

---

## ✅ Features
- 💬 Sentiment analysis using **TextBlob**
- 🧮 Text vectorization with **TF-IDF**
- 🌲 Machine learning with **Random Forest Classifier**
- 📊 Feature importance (numeric + text features)
- ⚡ REST API via **FastAPI**
- 💻 Interactive **React UI** with live predictions

---

## 📁 Project Structure

```bash
RedditTrendPredictor/
│
├── app/
│   └── app.py                    # Streamlit standalone app
│
├── backend/
│   ├── api.py                    # FastAPI prediction endpoint
│   └── main.py                   # Notebook-based API runner
│
├── frontend/
│   └── src/
│       ├── App.jsx               # Main React UI
│       └── Speedometer.jsx       # Gauge chart component
│
├── models/
│   ├── trend_model.pkl           # Trained Random Forest model
│   ├── tfidf_vectorizer.pkl      # TF-IDF vectorizer
│   └── scaler.pkl                # Feature scaler
│
├── notebook/
│   └── notebookb09ce3759c.ipynb  # Full ML training notebook
│
├── data/
│   ├── the-reddit-dataset-dataset-posts.csv
│   └── the-reddit-dataset-dataset-comments.csv
│
├── .env.example                  # Template for environment variables
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/RedditTrendPredictor.git
cd RedditTrendPredictor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
# Then open .env and fill in your Reddit API credentials
```

### 4. Run the FastAPI backend
```bash
cd backend
uvicorn api:app --reload
```

### 5. Run the React frontend
```bash
cd frontend
npm install
npm start
```

### OR run the Streamlit app
```bash
streamlit run app/app.py
```

---

## 📦 Dataset
**Source:** [The Meta Corpus of Reddit Dataset (Kaggle)](https://www.kaggle.com/datasets/thedevastator/the-meta-corpus-of-datasets-the-reddit-dataset)

**Files Used:**
- `the-reddit-dataset-dataset-posts.csv`
- `the-reddit-dataset-dataset-comments.csv`

---

## 🔑 Environment Variables
Copy `.env.example` to `.env` and fill in your values. Never commit `.env` to GitHub.

| Variable | Description |
|---|---|
| `REDDIT_CLIENT_ID` | Your Reddit app's client ID |
| `REDDIT_CLIENT_SECRET` | Your Reddit app's client secret |
| `REDDIT_USER_AGENT` | A descriptive name for your app |
