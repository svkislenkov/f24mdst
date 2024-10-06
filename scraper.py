import praw
from praw.models import MoreComments
import json
import pprint
import os
from dotenv import load_dotenv, dotenv_values
import nltk
from nltk.corpus import stopwords
import re



load_dotenv()

# print(os.getenv("CLIENT_ID"))
# print(os.getenv("CLIENT_SECRET"))

def expand_contractions(text):
    def replace(match):
        return CONTRADICTIONS[match.group(0)]
    return contractions_re.sub(replace, text)

def clean_text(text):
    text = text.lower()
    text = expand_contractions(text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = ' '.join([word for word in text.split() if word.lower() not in STOPWORDS])
    stop_words = r'\b(?:a|an|the|is|it|of|and|to|in)\b'
    text = re.sub(stop_words, '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent="My User",
)

# nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

CONTRADICTIONS = {
    "aren't": "are not",
    "can't": "cannot",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "I'd": "I would",
    "I'll": "I will",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it's": "it is",
    "let's": "let us",
    "mightn't": "might not",
    "mustn't": "must not",
    "shan't": "shall not",
    "she'd": "she would",
    "she'll": "she will",
    "she's": "she is",
    "shouldn't": "should not",
    "that's": "that is",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "we'd": "we would",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what's": "what is",
    "won't": "will not",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have"
}

contractions_re = re.compile('(%s)' % '|'.join(CONTRADICTIONS.keys()))

def expand_contractions(text):
    def replace(match):
        return CONTRADICTIONS[match.group(0)]
    return contractions_re.sub(replace, text)

def clean_text(text):
    
    text = text.lower()
    text = expand_contractions(text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = ' '.join([word for word in text.split() if word.lower() not in STOPWORDS])
    stop_words = r'\b(?:a|an|the|is|it|of|and|to|in)\b'
    text = re.sub(stop_words, '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

f = open("id.txt", "r")
seen_ids = set(f.read().splitlines())

submission_data = []
for submission in reddit.subreddit("AITAH").hot(limit=10):
    # print("test")
    cleaned_title = clean_text(submission.title)
    cleaned_selftext = clean_text(submission.selftext)
    
    if submission.id in seen_ids:
        continue
    else:
        seen_ids.add(submission.id)
        with open("id.txt", "a") as f:
            f.write(submission.id + "\n")

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


if os.path.exists('tdata.json'):
    with open('tdata.json', 'r') as json_file:
        try:
            existing_posts = json.load(json_file)
        except:
            existing_posts = []
else:
    existing_posts = []

# for post in existing_posts:
#     print(post.title)

existing_posts.extend(submission_data)            
    
with open('tdata.json', 'w') as json_file:
    json.dump(existing_posts, json_file, indent=4)


