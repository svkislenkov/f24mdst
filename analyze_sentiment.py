# -*- coding: utf-8 -*-
"""tutorial.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LwQ-43n5n3iMCBog-Pm4aHUktW8YaW3l

When traning a model, we need a group of pre labeled data, from which our model can derive it's pattern. Because our reddit posts are not labeled for sentiment analysis to start, we will use a Sentiment Intensity Analyzer(SIA) to label our data for us initially.

Run "pip install vaderSentiment"
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

"""Here we create an instance of an analyzer. Then we define a function which, given a piece of text, will call our analyzer on it and label it with etierh positive(1), negative(0), or netural(2)."""

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    print(scores['compound'], ":")
    if scores['compound'] >= 0.3:      # TODO: tweak these values as necessary
        return 1  # Positive
    elif scores['compound'] <= -0.3:
        return 0  # Negative
    else:
        return 2  # Neutral

"""Now let's load our sample data from json back into a list -> dict format. And then we add labels to each post in our dataset based on our SIA."""

import json
with open('tdata.json') as f:
    reddit_data = json.load(f)

for post in reddit_data:
    text = post['cleaned_title'] + " " + post['cleaned_selftext']
    post['label'] = get_sentiment(text)
    print(post['original_title'] + " (link: ", post["url"], ")\n" + post['original_selftext'][:200] + "...\n")

"""Now that we have labeled data, we can split our data into test and training sets, and start training our model."""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
reddit_data = pd.DataFrame(reddit_data)

X_train, X_test, y_train, y_test = train_test_split(reddit_data['cleaned_selftext'], reddit_data['label'], test_size=0.2, random_state=42)

vectorizer = CountVectorizer(stop_words='english')

"""The top array is the array of feature words found in the sentences. The bottom arrays each showcase how many of the feature words appear within each sentence. Let's now apply this to our training and test data."""

X_train_bow = vectorizer.fit_transform(X_train)
X_test_bow = vectorizer.transform(X_test)

"""Next we create an instance of a naive bayes model, and we train the model on our bag of words and our labels for the corresponding posts."""

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

nb = MultinomialNB()
nb.fit(X_train_bow, y_train)

"""Now we use our trained model to predict the results of our test data."""

y_pred = nb.predict(X_test_bow)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
print(classification_report(y_test, y_pred, target_names=['Negative', 'Positive', 'Neutral']))
