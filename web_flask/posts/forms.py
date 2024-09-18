from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange


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
