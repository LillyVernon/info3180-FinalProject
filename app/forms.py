from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,validators,PasswordField
from wtforms.validators import DataRequired, InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class RegisterForm(FlaskForm):

    username=StringField('Username', validators=[InputRequired()])
    fullname=StringField('Fullname', validators=[InputRequired()])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])
    location=StringField('Location', validators=[InputRequired()])
    biography= TextAreaField('Biography', validators=[InputRequired()])
    photo = FileField('Upload Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'Images only!'])])