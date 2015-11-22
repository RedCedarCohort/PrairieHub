import requests
from flask import Blueprint, redirect, url_for, jsonify, current_app
from ..models import User

frontend = Blueprint('frontend', __name__)


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
