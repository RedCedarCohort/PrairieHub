from flask import Blueprint, render_template, g, redirect, url_for

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    return "Hello World!"
