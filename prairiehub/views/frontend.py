import requests
from flask import Blueprint, redirect, url_for, jsonify, current_app, request
from ..models import User

frontend = Blueprint('frontend', __name__)


MEETUP_API_KEY = '2b793857386a66497a38128078367373'
MEETUP_OAUTH_API_KEY = '1amnk6p2leb2s5h6opdjej8flu'
MEETUP_OAUTH_API_SECRET = '9he0flqup6bhsamq191bdkq59b'
REDIRECT_URI = 'http://localhost:5000/meetup/callback'


@frontend.route('/')
def index():
    return redirect('/admin')


@frontend.route('/login/facebook/<access_token>')
def facebook_login(access_token):
    r = requests.get('https://graph.facebook.com/v2.5/me?fields=id&access_token=' + access_token)
    try:
        user_id = User.query.filter_by(facebook_id=r.json()['id']).first().id
    except:
        user_id = None

    return jsonify({
        'id': user_id
    })


@frontend.route('/login/custom/<email>/<password>')
def custom_login(email, password):
    try:
        user_id = User.query.filter_by(email=email, password=password).first().id
    except:
        user_id = None

    return jsonify({
        'id': user_id
    })


# https://secure.meetup.com/oauth2/authorize?client_id=1amnk6p2leb2s5h6opdjej8flu&response_type=code&redirect_uri=http://localhost:5000/meetup/callback
@frontend.route('/meetup')
def homepage():
    url_params = {
        'client_id': MEETUP_OAUTH_API_KEY,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
    }

    return '<a href="%s">Authenticate with Meetup</a>' % ('https://secure.meetup.com/oauth2/authorize?' +
                                                          '&'.join((k + '=' + v) for k, v in url_params.iteritems()))


@frontend.route('/meetup/callback')
def callback():
    r = requests.post('https://secure.meetup.com/oauth2/access', data={
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'client_id': MEETUP_OAUTH_API_KEY,
        'client_secret': MEETUP_OAUTH_API_SECRET,
        'code': request.args['code']
    })

    return str(r.json())


# Step 1

# https://secure.meetup.com/oauth2/access
#client_id=1amnk6p2leb2s5h6opdjej8flu
#&client_secret=9he0flqup6bhsamq191bdkq59b
#&grant_type=authorization_code
#&redirect_uri=http://localhost:5000/meetup/callback
#&code=7b44b1588add1696a9cc2cdf60aa7589

# Step 2 (POST)
# https://secure.meetup.com/oauth2/access

# with the body of the request being (line breaks are for readability)
# client_id=YOUR_CONSUMER_KEY
# &client_secret=YOUR_CONSUMER_SECRET
# &grant_type=authorization_code
# &redirect_uri=SAME_REDIRECT_URI_USED_FOR_PREVIOUS_STEP
# &code=CODE_YOU_RECEIVED_FROM_THE_AUTHORIZATION_RESPONSE

# ask: 7b44b1588add1696a9cc2cdf60aa7589
# token: ba63681fd3433605611b44c4ae579c90

# >>> data = {
# ... 'client_id': '1amnk6p2leb2s5h6opdjej8flu',
# ... 'client_secret': '9he0flqup6bhsamq191bdkq59b',
# ... 'grant_type': 'authorization_code',
# ... 'redirect_uri': 'http://localhost:5000/meetup/callback',
# ... 'code': '7b44b1588add1696a9cc2cdf60aa7589'}
# >>> r = requests.post("https://secure.meetup.com/oauth2/access", data=data)
# >>> r.json()
# {u'access_token': u'ba63681fd3433605611b44c4ae579c90', u'token_type': u'bearer', u'expires_in': 3600, u'refresh_token': u'2509ed947ed6da6d55c6187944f955eb'}

######

# With normal user API key:
# >>> rr = requests.get('https://api.meetup.com/2/groups?photo-host=public&groupnum=9362332&group_id=9362332&page=20&key=2b793857386a66497a38128078367373')
