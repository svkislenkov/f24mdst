# graphing tool
import matplotlib.pyplot as plt
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

import json

def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    return scores['compound']

with open('tdata.json') as f:
    reddit_data = json.load(f)

sentiment = []
updownratio = []

for post in reddit_data:
    if post['score'] == 0 and post['num_comments'] > 20:
        text = post['cleaned_title'] + " " + post['cleaned_selftext']
        sentiment.append(get_sentiment(text))
        updownratio.append(post['upvote_ratio'])
    if post['score'] > 100:
        text = post['cleaned_title'] + " " + post['cleaned_selftext']
        sentiment.append(get_sentiment(text))
        updownratio.append(post['upvote_ratio'])

#x_transformed = np.log(np.abs(sentiment) + 1) * np.sign(sentiment)
#y_transformed = np.log(np.abs(updownratio) + 1) * np.sign(updownratio)

x_transformed = np.sign(sentiment) * np.power(np.abs(sentiment), 2)
y_transformed = np.sign(updownratio) * np.power(np.abs(updownratio), 2)

# Vertical lon
plt.axvline(x=0.0, color='red', linestyle='--', label='x = 0')
# Add horizontal dividing lines at specific y-values
plt.axhline(y=0.5, color='red', linestyle='--', label='y = 0.5')

plt.scatter(sentiment, updownratio, color='blue', label='Sentiment vs. Ratio')

plt.xlabel('Sentiment Score')
plt.ylabel('Upvote/Downvote Ratio')

# Add a title
plt.title('Scatter Plot of Upvote/Downvote Ratio vs. Sentiment')

plt.show()