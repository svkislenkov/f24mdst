import praw
from praw.models import MoreComments
import json
import pprint

from keys import CLIENT_ID, CLIENT_SECRET

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent="My User",
)

submission_data = []
for submission in reddit.subreddit("AITAH").hot(limit=10):

    submission_data.append({
        "id": submission.id,
        "title": submission.title,
        "author": str(submission.author),  # Convert the Redditor object to string
        "selftext": submission.selftext,
        "score": submission.score,
        "ups?": submission.ups,
        "url": submission.url,
        "created_utc": submission.created_utc
    })
    with open('tdata.json', 'w') as json_file:
        json.dump(submission_data, json_file, indent=4)
