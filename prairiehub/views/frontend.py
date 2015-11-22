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
        user = User.query.filter_by(facebook_id=r.json()['id']).first()
        ret = {
            'id': user.id,
            'pwd': '',
            'email': user.email,
        }
    except:
        ret = {
            'id': None,
            'pwd': None,
            'email': None,
        }

    return jsonify(ret)


@frontend.route('/login/custom/<email>/<password>')
def custom_login(email, password):
    try:
        user = User.query.filter_by(email=email, password=password).first()
        ret = {
            'id': user.id,
            'pwd': '',
            'email': user.email,
        }
    except:
        ret = {
            'id': None,
            'pwd': None,
            'email': None,
        }

    return jsonify(ret)
