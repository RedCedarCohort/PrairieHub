from flask import Blueprint, render_template, g, redirect, url_for
from ..models.users import User

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    return "Hello %s!" % User.query.first().first_name
