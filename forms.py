from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import TimeField
from wtforms.fields.simple import EmailField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired


class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class CreateCafeForm(FlaskForm):
    name = StringField("Café Name", validators=[DataRequired()])
    city = SelectField("City", coerce=int, validators=[DataRequired()])
    website_url = StringField("Café Website URL", validators=[DataRequired()])
    opening_time = TimeField("Opening Time", validators=[DataRequired()])
    closing_time = TimeField("Closing Time", validators=[DataRequired()])
    address = StringField("Street, ZIP Code", validators=[DataRequired()])
    rating = StringField("Café Rating", validators=[DataRequired()])
    wifi = SelectField("Has Wifi", choices=[('yes', 'Yes'),('no', 'No')])
    power_outlet = SelectField("Power Outlet Available", choices=[('yes', 'Yes'), ('no', 'No')])
    image = FileField("Café Photo", validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField("Submit")

