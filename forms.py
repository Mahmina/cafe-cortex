from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")