from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasksite.models import User
from flasksite.scrape import entries_list


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose a different one.')


class Top10Form(FlaskForm):
    position_1 = StringField('1.', validators=[DataRequired(), Length(min=2, max=20)])
    position_2 = StringField('2.', validators=[DataRequired(), Length(min=2, max=20)])
    position_3 = StringField('3.', validators=[DataRequired(), Length(min=2, max=20)])
    position_4 = StringField('4.', validators=[DataRequired(), Length(min=2, max=20)])
    position_5 = StringField('5.', validators=[DataRequired(), Length(min=2, max=20)])
    position_6 = StringField('6.', validators=[DataRequired(), Length(min=2, max=20)])
    position_7 = StringField('7.', validators=[DataRequired(), Length(min=2, max=20)])
    position_8 = StringField('8.', validators=[DataRequired(), Length(min=2, max=20)])
    position_9 = StringField('9.', validators=[DataRequired(), Length(min=2, max=20)])
    position_10 = StringField('10.', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit selection')
