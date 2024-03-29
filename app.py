from flask import Flask, session, redirect, request, flash, render_template, session, jsonify
from flask_oauth import OAuth
import requests
import pickle
import manage_data

app = Flask(__name__)
app.debug = True
app.secret_key = 'super-secret-text'

oauth = OAuth()

jawbone = oauth.remote_app('jawbone',
    base_url="https://jawbone.com/",
    request_token_url=None,
    access_token_url="/auth/oauth2/token",
    authorize_url="https://jawbone.com/auth/oauth2/auth",
    consumer_key="VeXxXXfkIFo",
    consumer_secret="04e5713a9dea0eaa24d8322ece2037dcb842da66",
    request_token_params={
      "scope":"basic_read move_read location_read friends_read mood_read sleep_read meal_read weight_read generic_event_read",
      "response_type":"code"
    }
)

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='fYssQs123qUPugFWPONOlGiE7',
    consumer_secret='VREY11ztVX4y6chAeD0CNie4zTKG5W4IEZy2X8GeMdzzSe000X'
)




@app.route('/uplogin')
def uplogin():
  return jawbone.authorize(callback="http://localtest.com/up-authorized")


@app.route("/up-authorized")
def up_authorized():
  code = request.args.get('code')

  print ">>>authorizing..."

  next_url = "/"

  token_url = "https://jawbone.com/auth/oauth2/token"

  payload = {
      "client_id":jawbone.consumer_key,
      "client_secret":jawbone.consumer_secret,
      "grant_type":"authorization_code",
      "code":code
  }

  r = requests.get(token_url, params=payload)

  session['jawbone_token'] = (
      r.json()['access_token']
  )

  flash('You were signed in')
  return redirect(next_url)


@app.route("/jbtoken")
@jawbone.tokengetter
def get_jawbone_token(token=None):
  return session.get('jawbone_token')


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
    manage_data.tw_get_timeline(twitter, token)


@app.route("/twtoken")
@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route("/jb_data")
def jb_data(token=None):
    token = get_jawbone_token()
    print "token:", token
    return jsonify({'distances': manage_data.get_steps(jawbone, token)})

@app.route('/all_data')
def get_all_data(token=None):
    jb_token = get_jawbone_token()
    tw_token = get_twitter_token()
    res ={'jb_distances': [],
          'bpm': [],
          'attention': [],
          'sentiment': []}
    res['jb_distances'] = manage_data.get_steps(jawbone, jb_token)
    _tweets = manage_data.tw_get_timeline(twitter, tw_token)
    res.update({'bpm': manage_data.tweets_to_bpm(_tweets),
                'attention': manage_data.get_attention(_tweets),
                'sentiment': manage_data.get_sent(_tweets)})
    return jsonify(res)


# idol route
# @app.route('/get_sent')
# def sent():
#     return manage_data.idol_sentiment("I'm angry.")


@app.route('/')
def index():
    #return redirect(url_for('login'))
    return render_template('index.html')

if __name__ == "__main__":
  app.run()
