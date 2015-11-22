from flask import Blueprint, redirect, url_for

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    return redirect('/admin')
