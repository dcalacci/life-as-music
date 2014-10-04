from flask import Flask, session, redirect, request, flash
from flask import session
from flask_oauth import OAuth
import pickle

app = Flask(__name__)
app.debug = True
app.secret_key = 'super-secret-text'

oauth = OAuth()

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='fYssQs123qUPugFWPONOlGiE7',
    consumer_secret='VREY11ztVX4y6chAeD0CNie4zTKG5W4IEZy2X8GeMdzzSe000X'
)

@app.route('/login')
def login():
  return twitter.authorize(callback='/oauth-authorized')


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or '/'
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)

@app.route("/timeline")
def get_timeline(token=None):
    resp = twitter.get("statuses/user_timeline.json")
    if resp.status == 200:
      tweets = resp.data
      user = session['twitter_user']
      pickle.dump( tweets, open( user + "_timeline.p", "wb" ) )
    else:
      return str(resp.status)
    return str(resp.data)

@app.route("/test")
@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

@app.route("/")
def hello():
  return "Hello World!"

if __name__ == "__main__":
  app.run()
