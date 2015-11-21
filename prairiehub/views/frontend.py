from flask import Blueprint, render_template, g, redirect, url_for
from flask.ext.login import login_required
from ..models import User

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
@login_required
def index():
    return render_template('index.html')
