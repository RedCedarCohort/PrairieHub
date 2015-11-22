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
        return '<User %r>' % (self.email,)
