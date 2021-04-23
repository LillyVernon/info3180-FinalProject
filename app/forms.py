from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,validators,PasswordField,SelectField
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

class AddCarForm(FlaskForm):
    make=StringField('Make', validators=[InputRequired()])
    model=StringField('Model', validators=[InputRequired()])
    colour = StringField('Colour', validators=[InputRequired()])
    year = StringField('Year', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    car_type=SelectField('Car Type',choices=[('SUV', 'SUV'), ('Lexus','Lexus'), ('Lamborghini','Lamborghini')])
    transmis=SelectField('Transmission',choices=[('Automatic', 'Automatic'), ('Manual','Manual')])
    desc=TextAreaField('Description', validators=[InputRequired()])
    photo = FileField('Upload Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'Images only!'])])

class LoginForm(FlaskForm):
    username=StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', [validators.DataRequired()])




