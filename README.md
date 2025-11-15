# 📈 Reddit Trend Predictor & Analyzer  

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Scikit-learn](https://img.shields.io/badge/ML-Scikit--learn-orange)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/WebApp-Streamlit-red)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red)]()

---

## 🧠 Overview  
The **Reddit Trend Predictor** is a machine learning project that predicts whether a Reddit post will trend based on its **title**, **description**, **sentiment**, and **time-based features**.  
It leverages the **Meta Reddit Corpus Dataset** from Kaggle and includes an interactive **Streamlit web app** for real-time predictions.

---

## 🚀 Features  
✅ Uses real Reddit posts and comments dataset  
💬 Sentiment analysis using **TextBlob**  
🧮 Text vectorization with **TF-IDF**  
🌲 Machine learning with **Random Forest Classifier**  
📊 Feature importance visualization (numeric + text features)  
💻 Interactive **Streamlit UI** for live post predictions  

---

## 📊 Dataset  
**Source:** [The Meta Corpus of Reddit Dataset (Kaggle)](https://www.kaggle.com/datasets/thedevastator/the-meta-corpus-of-datasets-the-reddit-dataset)  

**Files Used:**  
- `the-reddit-dataset-dataset-posts.csv`  
- `the-reddit-dataset-dataset-comments.csv`  

**Key Attributes:**  
- `title`, `selftext`, `created_utc`, `score`, `num_comments`, `sentiment`, `subreddit.name`  

---

## 🧩 Project Structure  

```bash
RedditTrendPredictor/
│
├── app/
│   └── app.py                        # Streamlit web app
│
├── models/
│   ├── trend_model.pkl               # Trained Random Forest model
│   ├── tfidf_vectorizer.pkl          # TF-IDF vectorizer
│   └── scaler.pkl                    # Feature scaler
│
├── notebooks/
│   └── reddit_trend_predictor.ipynb  # Full ML notebook
│
├── data/
│   ├── the-reddit-dataset-dataset-posts.csv
│   └── the-reddit-dataset-dataset-comments.csv
│
├── reports/
│   └── Reddit_Trend_Predictor_Report.docx
│
├── requirements.txt
└── README.md
