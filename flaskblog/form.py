from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        print(user)
        if user:
            raise ValidationError('Username is taken. Please choose another one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class TranslationForm(FlaskForm):
    language = SelectField('Language', choices=[('finnish', 'Finnish to English'), ('english', 'English to Finnish')], validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()], default='')
    submit = SubmitField('Translate')
