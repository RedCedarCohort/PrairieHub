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

    return app


def load_admin(app):
    admin = Admin(app, 'Prairie Hub Admin')
    admin.register(models.User, session=db.session)
    admin.register(models.Tribe, session=db.session)


def load_api(app):
    manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
    manager.create_api(models.User, methods=['GET'], exclude_columns=['password'])
    manager.create_api(models.Tribe, methods=['GET', 'POST'])
