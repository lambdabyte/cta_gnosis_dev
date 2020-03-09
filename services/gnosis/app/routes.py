from app import app
from app import db
from app.models import User
from app.forms import RegistrationForm
from flask_restx import Resource
from flask import render_template, flash, redirect, url_for

@app.route('/index')
def index():
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
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }