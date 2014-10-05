from sentiment import classifier
from flask import session
import pickle

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
    sents = map(classifier.pos_neg_classify_sentence, tweets)
    return {'pos': norm([t['pos'] for t in sents]),
            'neg': norm([t['neg'] for t in sents])}

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


def tw_get_timeline(twitter, token=None):
    resp = twitter.get("statuses/user_timeline.json?count=3400")
    if resp.status == 200:
      tweets = resp.data
      user = session['twitter_user']
      pickle.dump( tweets, open( user + "_timeline.p", "wb" ) )
    else:
      return str(resp.status)
    return str(resp.data)

# avg tweets/day
# sentiment
