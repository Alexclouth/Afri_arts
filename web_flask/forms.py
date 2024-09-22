from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField, FloatField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from web_flask.models import User
from flask_login import current_user

class Signup(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    is_artist = RadioField('Choose your Profile-Type', choices=[('member', 'Member'), ('artist', 'Artist')], validators=[DataRequired()])
    first_name = StringField('First Name', validators=[Length(max=128)])
    last_name = StringField('Last Name', validators=[Length(max=128)])
    city = StringField('City', validators=[Length(max=128)])
    country = StringField('Country', validators=[Length(max=128)])
    bio = TextAreaField('Bio', validators=[Length(max=1024)])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a anoter username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class Signin(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'webp'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description', validators=[Length(max=1024)])
    image = FileField('Choose a picture', validators=[FileAllowed(['jpg', 'png', 'webp'])])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    # Dropdown for art_type with predefined choices
    art_type = SelectField('Art Type', choices=[
        ('painting', 'Painting'),
        ('sculpture', 'Sculpture'),
        ('photography', 'Photography'),
        ('digital_art', 'Digital Art'),
        ('mixed_media', 'Mixed Media')
    ], validators=[DataRequired()])
    style = SelectField('Style', choices=[
        ('abstract', 'Abstract'),
        ('realism', 'Realism'),
        ('surrealism', 'Surrealism'),
        ('pop_art', 'Pop Art'),
        ('contemporary', 'Contemporary')
    ], validators=[DataRequired()])
    submit = SubmitField('Post')
    update = SubmitField('Update Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
