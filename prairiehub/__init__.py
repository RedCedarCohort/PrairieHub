import json
import requests
import models
import views
import flask.ext.restless

from flask import Flask, Blueprint
from flask.ext.superadmin import Admin
from .extensions import db


def create_app(config_file=None, config_path=None):
    app = Flask(__name__)
    app.config.update(
        DEBUG=True,
        SECRET_KEY="\xe9\xd7\xa2\xfa\x96\xdf\xd4\x99\xea\x15\x18\xba\xcb\xfb%\xf5\xa6\xb1\xe2~\xb1<\xfd\x8f",
        SQLALCHEMY_DATABASE_URI="mysql://vagrant:vagrant@localhost/phub",
        SQLALCHEMY_ECHO=False,
        DEBUG_TB_ENABLED=True,
        DEBUG_TB_HOSTS=[],
        DEBUG_TB_INTERCEPT_REDIRECTS=False,
        DEBUG_TB_PROFILER_ENABLED=False,
    )

    app.register_blueprint(views.frontend)

    db.app = app
    db.init_app(app)

    if app.debug and ('SECRET_KEY' in app.config):
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)

    load_admin(app)
    load_api(app)

    @app.after_request
    def post_processor(response):
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    return app


def load_admin(app):
    admin = Admin(app, 'Prairie Hub Admin')
    admin.register(models.User, session=db.session)
    admin.register(models.Tribe, session=db.session)
    admin.register(models.Photo, session=db.session)
    admin.register(models.Press, session=db.session)
    admin.register(models.Testimonial, session=db.session)


def load_api(app):
    manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

    manager.create_api(models.User, methods=['GET'], exclude_columns=[
        'password', 'photos.owner', 'tribes.cost_in_pennies', 'tribes.facebook_app_id',
        'tribes.header_image_url', 'tribes.meetup_group_urlname', 'tribes.purpose',
        'tribes.twitter_handle', 'tribes.registered_on', 'tribes.website_url',
        'tribes.youtube_channel_name', 'featured_video_embed_url'])

    manager.create_api(models.Tribe, methods=['GET', 'POST', 'PUT'], exclude_columns=[
        'members.password', 'members.registered_on', 'photos.tribe_id', 'press.tribe_id', 'testimonials.tribe_id'])

    manager.create_api(models.Photo, methods=['GET', 'POST', 'PUT', 'DELETE'], exclude_columns=['tribe'])
    manager.create_api(models.Press, methods=['GET', 'POST', 'PUT', 'DELETE'], exclude_columns=['tribe'])
    manager.create_api(models.Testimonial, methods=['GET', 'POST', 'PUT', 'DELETE'], exclude_columns=['tribe'])
