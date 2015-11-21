from flask import Blueprint, session, request, flash, url_for, redirect, render_template, abort, g
from flask.ext.login import login_user, logout_user, current_user
from flask.ext.superadmin import model

from ..extensions import db
from ..models import User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['email'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    registered_user = User.query.filter_by(email=request.form['email'], password=request.form['password']).first()

    if registered_user is None:
        flash('E-mail or Password is invalid', 'error')
        return redirect(url_for('.login'))

    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('frontend.index'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('frontend.index'))


class UserModel(model.ModelAdmin):
    session = db.session

    def is_accessible(self):
        return current_user.is_authenticated
