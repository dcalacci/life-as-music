from flask import session
import pickle

def tw_get_timeline(token=None):
    resp = twitter.get("statuses/user_timeline.json")
    if resp.status == 200:
      tweets = resp.data
      user = session['twitter_user']
      pickle.dump( tweets, open( user + "_timeline.p", "wb" ) )
    else:
      return str(resp.status)
    return str(resp.data)
