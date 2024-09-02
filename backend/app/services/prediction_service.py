from app import db, logger
import pandas as pd
import re
import joblib

from app.models.prediction import Prediction

# Load the saved model and vectorizer
model = joblib.load('app/assets/lr_model.pkl')
vectorizer = joblib.load('app/assets/vectorizer.pkl')


def predict(text):
    testing_news = {"text": [text]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test['text'] = new_def_test["text"].apply(preprocess_text)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorizer.transform(new_x_test)
    pred_lr = model.predict(new_xv_test)
    pred_proba = model.predict_proba(new_xv_test)

    result = check_output(pred_lr[0])
    confidence = max(pred_proba[0])
    confidence = round(confidence, 2)

    try:
        prediction = Prediction(news=text, prediction=result, confidence=confidence)

        db.session.add(prediction)
        db.session.commit()
    except Exception as e:
        logger.error(f"Error saving prediction to database: {e}")

    return result, confidence


def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove special characters and punctuation
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def check_output(n):
    if n == 1:
        return True
    return False
