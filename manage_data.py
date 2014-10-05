from sentiment import classifier
from flask import session
import pickle
<<<<<<< HEAD

def norm(v):
    m = max(v)
    return [item/float(m) for item in v]


# sentiment
def process_tweet(tweet):
    tweet = tweet.replace('/', '').split()
    return [w.lower() for w in tweet]

def tw_get_text(tweets):
    texts = [tweet['text'] for tweet in tweets]
    return map(process_tweet, texts)

def get_sent(tweets):
    tweets = tw_get_text(tweets)
=======
import requests
import collections
import json
import pandas as pd
import numpy as np


def norm(v, r=[0,1]):
    m = max(v)
    diff = r[1] - r[0]
    return [r[0] + (diff*(item/float(m))) for item in v]

# sentiment
def _process_tweet(tweet):
    tweet = tweet.replace('/', '').split()
    return [w.lower() for w in tweet]

def _tw_get_text(tweets):
    texts = [tweet['text'] for tweet in tweets]
    return map(_process_tweet, texts)

def get_sent(tweets):
    tweets = _tw_get_text(tweets)
>>>>>>> 36a503cf8ab9f757d5034f4d3557891fa26ff9c8
    sents = map(classifier.pos_neg_classify_sentence, tweets)
    return {'pos': norm([t['pos'] for t in sents]),
            'neg': norm([t['neg'] for t in sents])}

<<<<<<< HEAD
# attention
def get_attention(tweets):
    get_atten = lambda (t): t['retweet_count'] + t['favorite_count']
    return norm(map(get_atten, tweets))


# tweet rate -> bpm
def avg_tweet_rate(tweets):
    dates = [t['created_at'] for t in tweets]
    dates =[pd.to_datetime(s) for s in avg_tweet_rate(d)]
    return dict(collections.Counter(dates))

def tweet_rate_to_bpm(tweets):
    dates = avg_tweet_rate(tweets)
    freq = dict(collections.Counter(dates))
    return np.mean(norm(freq.values(), r=[80,240]))
=======
# # IDOL
# IDOL_KEY = open('static/keys.txt', 'rb').readlines()[0].strip()

# def idol_sentiment(text):
#     sent_endpoint = 'https://api.idolondemand.com/1/api/sync/analyzesentiment/v1'
#     payload = {'text': text, 'apikey': IDOL_KEY}
#     res = requests.get(sent_endpoint, params=payload)
#     return json.loads(res.content)['aggregate']['score']

# def get_sent(tweets):
#     tweets = _tw_get_text(tweets)
#     sents = map(idol_sentiment, tweets)
#     return " ".join(sents)


# def sentiment_idol_action(text):
#     return {'name': 'analyzesentiment',
#             'version': 'v1',
#             'params': {'text': text,
#                        'apikey': IDOL_KEY}
#             }

# def build_idol_actions(tweets):
#     texts = tw_get_text(tweets)
#     return map(sentiment_idol_action, texts)

# def send_jobs(actions):
#     jobs_endpoint = 'https://api.idolondemand.com/1/job'
#     return requests.post(jobs_endpoint, data={'actions': actions}, params=IDOL_KEY).content

# attention
def get_attention(tweets):
    """Normalized measure of retweets/favorites for each tweet
    """
    get_atten = lambda (t): t['retweet_count'] + t['favorite_count']
    return norm(map(get_atten, tweets))

# tweet rate -> bpm
def _avg_tweet_rate(tweets):
    dates = [t['created_at'] for t in tweets]
    dates =[pd.to_datetime(s).date() for s in dates]
    return dict(collections.Counter(dates))

def tweets_to_bpm(tweets):
    """ Returns a float in the range [80, 240]
    """
    dates = _avg_tweet_rate(tweets)
    freq = dict(collections.Counter(dates))
    print "converting tweet frequency to bpm..."
    bpm = np.mean(norm(freq.values(), r=[80,240]))
>>>>>>> 36a503cf8ab9f757d5034f4d3557891fa26ff9c8


def tw_get_timeline(twitter, token=None):
    resp = twitter.get("statuses/user_timeline.json?count=3400")
    if resp.status == 200:
      tweets = resp.data
      user = session['twitter_user']
<<<<<<< HEAD
      pickle.dump( tweets, open( user + "_timeline.p", "wb" ) )
    else:
      return str(resp.status)
    return str(resp.data)

# avg tweets/day
# sentiment
=======
#      pickle.dump( tweets, open( user + "_timeline.p", "wb" ) )
    else:
      return str(resp.status)
    return resp.data

# jawbone

def get_ticks(token, xid):
    "normalized ticks for a move!"
    headers = {'Authorization': 'Bearer ' + str(token)}
    res = requests.get('https://jawbone.com/nudge/api/v.1.1/moves/' + xid + '/ticks',
                       headers=headers)
    return [t['distance'] for t in json.loads(res.content)['data']['items']]

def jb_get_moves(jawbone, token=None):
    headers = {'Authorization': 'Bearer ' + str(token)}
    payload = {'start_time': 1380974114}

    res = requests.get('https://jawbone.com/nudge/api/v.1.1/users/@me/moves',
                       headers=headers,
                       params=payload)
    return json.loads(res.content)['data']['items']

def get_steps(jawbone, token=None):
    moves = jb_get_moves(jawbone, token)
    distances = []
    for move in moves:
        distances.extend(get_ticks(token, move['xid']))
    print "length of distances: ", len(distances)
    return norm(distances)
>>>>>>> 36a503cf8ab9f757d5034f4d3557891fa26ff9c8
