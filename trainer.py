from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Get text, upvote/downvote ratio from posts
import json
with open('tdata.json') as f:
    reddit_data = json.load(f)

X_text = []
X_sentiment = []
y_updown = []

for post in reddit_data:
    text = post['cleaned_title'] + " " + post['cleaned_selftext']
    # Get sentiment from posts
    X_text.append(text)
    sent = ((analyzer.polarity_scores(text)['compound'] + 1) / 2)
    X_sentiment.append(sent)
    y_updown.append(post['upvote_ratio'])

# Combine text, upvote/downvote, and sentiment into model

# Train model
    
# Text vectorization
tfidf = TfidfVectorizer(max_features=5000)
X_text_vec = tfidf.fit_transform(X_text).toarray()

# Combine text features and sentiment
X = np.hstack((X_text_vec, np.array(X_sentiment).reshape(-1, 1)))
y = np.array(y_updown)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluation
score = model.score(X_test, y_test)
print(f"Model R^2 score: {score}")

# Prompt for user input

user_text = input(f"Enter your unpopular opinion: ")
# Calculate sentiment based on user input
user_sentiment = ((analyzer.polarity_scores(user_text)['compound'] + 1) / 2)

# Preprocess text
user_text_vec = tfidf.transform([user_text]).toarray()
user_input = np.hstack((user_text_vec, [[user_sentiment]]))

# Predict ratio
predicted_ratio = model.predict(user_input)
print(f"Predicted Upvote/Downvote Ratio: {predicted_ratio[0]:.2f}")
# Throw sentiment and user input into model

# Output predicted up/down ratio

