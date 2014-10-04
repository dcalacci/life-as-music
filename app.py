from flask import session

from flask import Flask, redirect, url_for, session, request, render_template, flash
from flask_oauth import OAuth

DEBUG = True

FACEBOOK_APP_ID = ' 527044020761840'
FACEBOOK_APP_SECRET = '1e58e176ee7c845698e37f2e40e1d696'

with open('static/keys.txt', 'rb') as f:
    TWITTER_KEY, TWITTER_SECRET = [key.strip() for key in f.readlines()]

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = 'dev key'
oauth = OAuth()


twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=TWITTER_KEY,
    consumer_secret=TWITTER_SECRET
)



@app.route('/')
def index():
    #return redirect(url_for('login'))
    return render_template('index.html')


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/login')
def login():
    print "logging in..."
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    console.log('response:', resp)
    if session.has_key('twitter_token'):
        del session['twitter_token']

    print "request: ", request
    next_url = request.args.get('next') or url_for('index')
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



# facebook



# facebook = oauth.remote_app('facebook',
#     base_url='https://graph.facebook.com/',
#     request_token_url=None,
#     access_token_url='/oauth/access_token',
#     authorize_url='https://www.facebook.com/dialog/oauth',
#     consumer_key=FACEBOOK_APP_ID,
#     consumer_secret=FACEBOOK_APP_SECRET,
#     request_token_params={'scope': 'email'}
# )


# @app.route('/login')
# def login():
#     return facebook.authorize(callback=url_for('facebook_authorized',
#         next=request.args.get('next') or request.referrer or None,
#         _external=True))





# @app.route('/login/authorized')
# @facebook.authorized_handler
# def facebook_authorized(resp):
#     if resp is None:
#         return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#     session['oauth_token'] = (resp['access_token'], '')
#     me = facebook.get('/me')
#     content = 'Logged in as id=%s name=%s redirect=%s' % \
#               (me.data['id'], me.data['name'], request.args.get('next'))
#     return render_template('index.html', content=content)


# @facebook.tokengetter
# def get_facebook_oauth_token():
#     return session.get('oauth_token')


if __name__ == '__main__':
    app.run()
