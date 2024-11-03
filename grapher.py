# graphing tool
import matplotlib.pyplot as plt
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
    text = post['cleaned_title'] + " " + post['cleaned_selftext']
    sentiment.append(get_sentiment(text))
    updownratio.append(post['upvote_ratio'])


plt.scatter(sentiment, updownratio, color='blue', label='Sentiment vs. Ratio')

plt.xlabel('Upvote/Downvote Ratio')
plt.ylabel('Sentiment Score')

# Add a title
plt.title('Scatter Plot of Upvote/Downvote Ratio vs. Sentiment')

plt.show()