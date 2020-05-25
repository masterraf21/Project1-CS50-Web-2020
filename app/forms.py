from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.getUser_username(username)
        if user is not None:
            raise ValidationError('Please use different username')


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[('0.0', '0.0'), ('0.5', '0.5'), (
        '1.0', '1.0'), ('1.5', '1.5'), ('2.0', '2.0'), ('2.5', '2.5'), ('3.0', '3.0'), ('3.5', '3.5'), ('4.0', '4.0'), ('4.5', '4.5'), ('5.0', '5.0')])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[
                         DataRequired(), Length(min=0, max=20)])
    stype = SelectField('Type', choices=[(
        'title', 'Title'), ('isbn', 'ISBN'), ('author', 'Author')])
    submit = SubmitField('Submit')
