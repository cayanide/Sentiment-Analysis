import joblib
import pandas as pd
from scrape_reviews import scrape_reviews
from nltk.corpus import stopwords
from collections import Counter

# Load the model and vectorizer
NB_model = joblib.load('NB_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Preprocess the text (same as before)
def preprocess_text(text):
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

# Predict sentiment for reviews
def predict_sentiment(reviews):
    if not reviews:  # Handle the case when there are no reviews
        print("No reviews to analyze.")
        return []

    processed_reviews = [preprocess_text(review) for review in reviews]
    reviews_TFIDF = vectorizer.transform(processed_reviews)
    predictions = NB_model.predict(reviews_TFIDF)
    return predictions

# Generate a summary based on customer reviews and predicted sentiments
def generate_summary(reviews, sentiments):
    sentiment_count = Counter(sentiments)
    total_reviews = len(sentiments)

    # Sentiment breakdown
    positive_count = sentiment_count.get('positive', 0)
    neutral_count = sentiment_count.get('neutral', 0)
    negative_count = sentiment_count.get('negative', 0)

    # Overall sentiment
    if positive_count > negative_count and positive_count > neutral_count:
        overall_rating = "Positive"
    elif negative_count > positive_count and negative_count > neutral_count:
        overall_rating = "Negative"
    else:
        overall_rating = "Neutral"

    # AI-Generated Review
    review_text = (
        f"The product has received {total_reviews} reviews. "
        f"{positive_count} reviews were positive, {neutral_count} were neutral, "
        f"and {negative_count} were negative. Overall, customer sentiment is {overall_rating.lower()}.\n\n"
    )

    # Additional insights from customer feedback
    if overall_rating == "Positive":
        review_text += "Customers frequently praised the product for its quality, performance, and value for money."
    elif overall_rating == "Negative":
        review_text += "Common complaints included issues with durability, functionality, and overall experience."
    else:
        review_text += "Reviews were mixed, with some users satisfied and others highlighting areas for improvement."

    return review_text, overall_rating
