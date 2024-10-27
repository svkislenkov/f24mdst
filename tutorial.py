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
    if scores['compound'] >= 0.05:      # TODO: tweak these values as necessary
        return 1  # Positive
    elif scores['compound'] <= -0.05:
        return 0  # Negative
    else:
        return 2  # Neutral

"""Now let's load our sample data from json back into a list -> dict format. And then we add labels to each post in our dataset based on our SIA."""

import json
with open('sample_data.json') as f:
    sample_data = json.load(f)

for post in sample_data:
    post['label'] = get_sentiment(post['text'])

"""Now that we have labeled data, we can split our data into test and training sets, and start training our model."""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
sample_data = pd.DataFrame(sample_data)

X_train, X_test, y_train, y_test = train_test_split(sample_data['text'], sample_data['label'], test_size=0.2, random_state=42)

"""We've split our data, the next step is to create a bag of words representation of our data. A bag of words representation disregards the ordering of sentences, and just turns the post into a list of the words that made up that post. Here's an example."""

vectorizer = CountVectorizer(stop_words='english')

example_sentences = ["hello here sentence banana", "different sentence orange"]

bag_of_words = vectorizer.fit_transform(example_sentences)

print("Feature Names:", vectorizer.get_feature_names_out())
print("Bag of Words Representation:\n", bag_of_words.toarray())

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
print(classification_report(y_test, y_pred, target_names=['Negative', 'Positive']))

"""That's pretty good accuracy, considering the size of our dataset. We expect that with a larger dataset(as you should be collecting) our accuracy will increase. The next step would be to take this model and apply it to more data, using it to classify new posts by sentiment.

Next let's try the Hidden Markov Model(HMM). First we need to group our bag of words by each post, since we are treating these as our sequences.
"""

vectorizer = CountVectorizer(max_features=10, min_df=1)
X_bow = vectorizer.fit_transform(sample_data['text']).toarray()
X_sequences = [X_bow[i] for i in range(len(X_bow))]

"""The next step is to pair our sequences with the length of the sequence. HMM is an unsupervised model, so we do not need to include the labels from our training set."""

from hmmlearn.hmm import MultinomialHMM
from sklearn.preprocessing import LabelEncoder
import numpy as np

X_train = np.concatenate([np.array(seq).reshape(-1, 1) for seq in X_sequences])
lengths = [len(seq) for seq in X_sequences]

model = MultinomialHMM(n_components=2, random_state=42)

model.fit(X_train, lengths)

"""Now let's test how our model performs on other sets of data."""

def predict_sentiment(text):
    text_bow = vectorizer.transform(text).toarray()

    altered_vec = np.concatenate([np.array(seq).reshape(-1, 1) for seq in text_bow])

    logprob, hidden_states = model.decode(altered_vec)
    return hidden_states

data = [
        "I love this product!",
        "This is the worst experience I've had.",
        "Absolutely fantastic! Highly recommend it.",
        "Not good, very disappointing.",
        "I feel great about this!", ]

predicted_sentiment = predict_sentiment(data)
print(predicted_sentiment)