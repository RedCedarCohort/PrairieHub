from flask.ext.superadmin import model
from datetime import datetime
from flask import current_app
from ..extensions import db


user_tribes = db.Table('user_tribes',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('tribe_id', db.Integer, db.ForeignKey('tribe.id')))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, index=True)
    facebook_id = db.Column(db.String(128), index=True)
    password = db.Column(db.String(16))
    registered_on = db.Column(db.DateTime)

    tribes = db.relationship('Tribe', secondary=user_tribes,
                             backref=db.backref('members', lazy='dynamic'))

    def __init__(self):
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return '<User %d|%r>' % (self.id, self.email)


class Tribe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    logo_url = db.Column(db.String(512))
    header_image_url = db.Column(db.String(512))
    featured_video_embed_url = db.Column(db.String(512))
    purpose = db.Column(db.String(2048))
    website_url = db.Column(db.String(512))
    youtube_channel_name = db.Column(db.String(32))
    meetup_group_urlname = db.Column(db.String(32))
    facebook_app_id = db.Column(db.String(64))
    twitter_handle = db.Column(db.String(64))
    cost_in_pennies = db.Column(db.Integer)
    registered_on = db.Column(db.DateTime)

    def __init__(self):
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return '<Tribe %d|%r>' % (self.id, self.name)


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tribe_id = db.Column(db.Integer, db.ForeignKey('tribe.id'))
    url = db.Column(db.String(512))

    tribe = db.relationship('Tribe', backref=db.backref('photos', lazy='dynamic'))

    def __repr__(self):
        return '<Photo %d|%r>' % (self.id, self.url)


class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tribe_id = db.Column(db.Integer, db.ForeignKey('tribe.id'))
    endorser_name = db.Column(db.String(64))
    testimonial_text = db.Column(db.String(512))
    picture_url = db.Column(db.String(512))

    tribe = db.relationship('Tribe', backref=db.backref('testimonials', lazy='dynamic'))

    def __repr__(self):
        return '<Testimonial %d|%r|%r|%d>' % (self.id, self.testimonial_text, self.endorser_name, self.tribe_id)
