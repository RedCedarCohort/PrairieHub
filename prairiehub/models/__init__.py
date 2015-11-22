from flask.ext.superadmin import model
from datetime import datetime
from flask import current_app
from ..extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, index=True)
    facebook_id = db.Column(db.String(128), index=True)
    password = db.Column(db.String(16))
    registered_on = db.Column(db.DateTime)

    def __init__(self, email='', password='', facebook_id=''):
        self.facebook_id = facebook_id
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.email


class Tribe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    logo_url = db.Column(db.String(512))
    purpose = db.Column(db.String(2048))
    meetup_group_urlname = db.Column(db.String(32))
    facebook_app_id = db.Column(db.String(64))
    twitter_handle = db.Column(db.String(64))
    registered_on = db.Column(db.DateTime)

    def __init__(self, name='', logo_url='', purpose='', meetup_group_urlname='',
                 facebook_app_id='', twitter_handle=''):
        self.name = name
        self.logo_url = logo_url
        self.purpose = purpose
        self.meetup_group_urlname = meetup_group_urlname
        self.facebook_app_id = facebook_app_id
        self.twitter_handle = twitter_handle

        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return '<Tribe %r>' % self.name
