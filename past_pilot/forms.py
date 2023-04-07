from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from flask_login import current_user
from past_pilot.models import User


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=16)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    key = StringField('Generated Secret Key', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken')
                                                
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use')
                                                        
    def validate_key(self, key):
        user = User.query.filter_by(key=key.data).first()
        if user:
            raise ValidationError('That key is already in use, please generate another one')
                                                        
                                                
class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class QuestionForm(FlaskForm):
    question = TextAreaField('Enter a question', validators=[DataRequired()])
    keys = StringField('Separate keys with a comma', validators=[DataRequired()])
    submit = SubmitField('Find')


class KeyForm(FlaskForm):
    keys = StringField('Separate keys with a comma', validators=[DataRequired()])
    submit = SubmitField('Access')