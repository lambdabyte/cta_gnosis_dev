from app import app
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm
from flask_restx import Resource
from flask_login import current_user, login_user
from flask import render_template, flash, redirect, url_for


@app.route('/index')
def home():
    user = {'username': 'John Doe'} 
    return render_template('index.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.entered_username.data, email=form.entered_email.data)
        user.set_password(form.entered_password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # get the Login Form from forms file
    form = LoginForm()
    valid_user = 1;
    # use all validators defined in Login Form
    if form.validate_on_submit():
        # get User from database based on entered user in form
        user = User.query.filter_by(username=form.entered_username.data).first()
        # if user does not exist, or wrong password
        if user is None or not user.check_password(form.entered_password.data):
            valid_user = 0;
        else:
            login_user(user, remember=form.remember_me.data)       
            return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form, valid_user=valid_user)

class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }