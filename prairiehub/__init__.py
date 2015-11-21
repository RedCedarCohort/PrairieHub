import json
import requests
import models

from flask import Flask, Blueprint, g, request
from flask.ext.superadmin import Admin, model

from views.frontend import frontend
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

    load_blueprints(app)
    load_extensions(app)
    load_custom_template_filters(app)
    load_template_context_processors(app)
    load_request_preprocessors(app)

    return app


def load_blueprints(app):
    app.register_blueprint(frontend)


def load_extensions(app):
    db.init_app(app)

    if app.debug and ('SECRET_KEY' in app.config):
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)

    admin = Admin(app, 'Prairie Huby Admin')
    admin.register(models.users.User, session=db.session)


def load_custom_template_filters(app):
    @app.template_filter('max')
    def max_filter(collection):
        return max(collection)

    @app.template_filter('min')
    def min_filter(collection):
        return min(collection)

    @app.template_filter('to_json')
    def to_json_filter(data):
        return json.dumps(data)


# Add context processors to make variables or functions available to all templates by default
def load_template_context_processors(app):
    @app.context_processor
    def context_processor():
        def is_list(lst):
            return isinstance(lst, list)

        def is_dict(d):
            return isinstance(d, dict)

        def is_bool(b):
            return isinstance(b, bool)

        return {
            'is_bool': is_bool,
            'is_list': is_list,
            'is_dict': is_dict,
        }


# Add preprocessors to perform universal setup before a request is run
def load_request_preprocessors(app):
    @app.before_request
    def stub():
        pass
