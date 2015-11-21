from flask import current_app
from ..extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))

    def __repr__(self):
        return '<User %d|%s|%s|%s>' % (self.id, self.email, self.first_name, self.last_name)
