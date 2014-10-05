from sentiment import classifier
from flask import session
import pickle

def process_tweet(tweet):
    tweet = tweet.replace('/', '').split()
    return [w.lower() for w in tweet]

def tw_get_text(tweets):
    texts = [tweet['text'] for tweet in tweets]
    return map(process_tweet, texts)

def get_sent(tweets):
    tweets = tw_get_text(tweets)
    sents = map(classifier.pos_neg_classify_sentence, tweets)
    return {'pos': [t['pos'] for t in sents],
            'neg': [t['neg'] for t in sents]}


def tw_get_timeline(twitter, token=None):
    resp = twitter.get("statuses/user_timeline.json?count=3400")
    if resp.status == 200:
      tweets = resp.data
      user = session['twitter_user']
      pickle.dump( tweets, open( user + "_timeline.p", "wb" ) )
    else:
      return str(resp.status)
    return str(resp.data)
