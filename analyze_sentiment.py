from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to get sentiment label
def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    if scores['compound'] >= 0.3:
        return 1  # Positive
    elif scores['compound'] <= -0.3:
        return 0  # Negative
    else:
        return 2  # Neutral

# Load sample data from JSON file
with open('tdata.json') as f:
    reddit_data = json.load(f)

# Array to hold the objects for the new JSON file
output_data = []

# Process each post
for post in reddit_data:
    text = post['cleaned_title'] + " " + post['cleaned_selftext']
    post['label'] = get_sentiment(text)
    
    # Create and add an object to the output array as per the TODO
    output_data.append({
        "url": post["url"],
        "text": post.get('original_selftext', ''),  # Use .get to avoid KeyError if 'original_selftext' is missing
        "sentiment": post["label"],
        "upvote_ratio": post["upvote_ratio"]
    })

# Save the array of objects to a new JSON file
with open('labeled_data.json', 'w') as outfile:
    json.dump(output_data, outfile, indent=4)

# Continue with data processing and model training
reddit_data = pd.DataFrame(reddit_data)
X_train, X_test, y_train, y_test = train_test_split(
    reddit_data['cleaned_selftext'], 
    reddit_data['label'], 
    test_size=0.2, 
    random_state=42
)

vectorizer = CountVectorizer(stop_words='english')

# Transform text data to bag-of-words representation
X_train_bow = vectorizer.fit_transform(X_train)
X_test_bow = vectorizer.transform(X_test)

# Train a Naive Bayes classifier
nb = MultinomialNB()
nb.fit(X_train_bow, y_train)

# Test the model
y_pred = nb.predict(X_test_bow)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
print(classification_report(y_test, y_pred, target_names=['Negative', 'Positive', 'Neutral']))
