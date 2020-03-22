from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class RegistrationForm(FlaskForm):
    entered_username = StringField('Username', validators=[DataRequired()])
    entered_email = StringField('Email', validators=[DataRequired(), Email()])
    entered_password = PasswordField('Password', validators=[DataRequired()])
    entered_password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('entered_password')]
    )
    submit = SubmitField('Register')

    def validate_entered_username(self, entered_username):
        # query users in database to find match for entered username
        user = User.query.filter_by(username=entered_username.data).first()
        # if match found, then username is already taken
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_entered_email(self, entered_email):
        # query user in db based on email to find entered email
        user = User.query.filter_by(email=entered_email.data).first()
        # if match found, then email is already in use
        if user is not None:
            raise ValidationError('Please use another email address.')

    def validate_entered_password(self, entered_password):
        if len(entered_password.data) < 8 or any(str.isdigit(c) for c in entered_password.data) == False: 
            raise ValidationError('Password must be 8 characters and contain one number.')

class LoginForm(FlaskForm):
    entered_username = StringField('Username', validators=[DataRequired()])
    entered_password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')