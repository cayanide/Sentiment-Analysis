from flask import Flask, render_template, request
from scrape_reviews import scrape_reviews
from predict_sentiment import predict_sentiment, generate_summary

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment_data = None
    overall_rating = None
    ai_review = None

    if request.method == "POST":
        # Get the product URL from the form
        product_url = request.form["product_url"]

        # Scrape reviews for the product
        reviews = scrape_reviews(product_url)

        if reviews:
            # Get sentiment predictions
            sentiments = predict_sentiment(reviews)
            sentiment_data = zip(reviews, sentiments)

            # Generate AI-based review summary
            ai_review, overall_rating = generate_summary(reviews, sentiments)

            # Calculate the overall sentiment rating
            positive_reviews = sum(1 for sentiment in sentiments if sentiment == 'positive')
            negative_reviews = sum(1 for sentiment in sentiments if sentiment == 'negative')
            neutral_reviews = sum(1 for sentiment in sentiments if sentiment == 'neutral')

            # Create a simple rating based on the counts
            total_reviews = len(sentiments)
            if positive_reviews > negative_reviews and positive_reviews > neutral_reviews:
                overall_rating = "Positive"
            elif negative_reviews > positive_reviews and negative_reviews > neutral_reviews:
                overall_rating = "Negative"
            else:
                overall_rating = "Neutral"

    return render_template("index.html", sentiment_data=sentiment_data, overall_rating=overall_rating, ai_review=ai_review)


if __name__ == "__main__":
    app.run(debug=True)
