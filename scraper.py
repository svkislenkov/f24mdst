import praw
from praw.models import MoreComments
import json
import pprint
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

print(os.getenv("CLIENT_ID"))
print(os.getenv("CLIENT_SECRET"))

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
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
