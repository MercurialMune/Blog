from . import auth
from flask_login import login_required, current_user, login_user, logout_user
from .. models import User
from flask import render_template, redirect, request, url_for, abort, flash
from .. import db
from .forms import LoginForm, RegisterForm


@auth.route('/register/', methods= ['GET', 'POST'])
def register():
    form = RegisterForm()
    title = 'Add Account'
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('/auth/register.html', register_form = form, title = title)


@auth.route('/login/', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    title = 'Blog Login'
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data)
            return redirect(request.args.get("next") or url_for('main.index'))
        flash('Invalid login credentials')
    return render_template('/auth/login.html', login_form=login_form, title=title)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))