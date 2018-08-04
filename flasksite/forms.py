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
    position_1 = SelectField('1.', choices=entries_list, validators=[DataRequired(), Length(min=2, max=20)])
    position_2 = SelectField('2.', choices=entries_list, validators=[DataRequired(), Length(min=2, max=20)])
    position_3 = SelectField('3.', choices=entries_list, validators=[DataRequired(), Length(min=2, max=20)])
    position_4 = SelectField('4.', choices=entries_list, validators=[DataRequired(), Length(min=2, max=20)])
    position_5 = SelectField('5.', choices=entries_list, validators=[DataRequired(), Length(min=2, max=20)])
    position_6 = SelectField('6.', choices=entries_list, validators=[DataRequired(), Length(min=2, max=20)])
    position_7 = SelectField('7.', choices=entries_list, validators=[DataRequired(), Length(min=2, max=20)])
    position_8 = SelectField('8.', choices=entries_list, validators=[DataRequired(), Length(min=2, max=20)])
    position_9 = SelectField('9.', choices=entries_list, validators=[DataRequired(), Length(min=2, max=20)])
    position_10 = SelectField('10.', choices=entries_list, validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit selection')
