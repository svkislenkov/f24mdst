import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import sys
import numpy as np

def train_model():
    # Step 1: Load Data
    with open("tdata.json", "r") as file:
        data = json.load(file)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Step 2: Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()
    df['sentiment_score'] = df['cleaned_selftext'].apply(
        lambda x: analyzer.polarity_scores(x)['compound']
    )

    # Step 3: Prepare Features and Target
    features = df[['sentiment_score']]
    target = df['upvote_ratio']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Step 4: Train Model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Step 5: Evaluate Model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    
    return model, analyzer

def predict_opinion(user_text):
    try:
        # Train model and get analyzer
        model, analyzer = train_model()

        # Process User Input
        user_sentiment_score = analyzer.polarity_scores(user_text)['compound']
        user_features = pd.DataFrame({
            'sentiment_score': [user_sentiment_score],
        })

        # Predict upvote ratio and clip between 0 and 1
        predicted_ratio = model.predict(user_features)[0]
        predicted_ratio = np.clip(predicted_ratio, 0, 1)
        return predicted_ratio

    except Exception as e:
        print(f"Error in prediction process: {str(e)}")
        return 0.5

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_text = sys.argv[1]
        ratio = predict_opinion(user_text)
        print(f"Predicted Upvote/Downvote Ratio: {ratio}")
    else:
        print("No input text provided")

