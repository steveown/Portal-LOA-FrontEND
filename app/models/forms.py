from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField("username", validators=[DataRequired()])
	password = PasswordField("password", validators=[DataRequired()])
	remember_me = BooleanField("remember_me")

class RegisterForm(FlaskForm):
	nome = StringField("email", validators=[DataRequired()])
	sobrenome = StringField("email", validators=[DataRequired()])
	email = StringField("email", validators=[DataRequired()])
	password = StringField("password", validators=[DataRequired()])
	confirmpassword = StringField("confirmpassword", validators=[DataRequired()])