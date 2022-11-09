from wtforms import StringField, PasswordField, EmailField, Form
from wtforms.validators import DataRequired, Length, EqualTo, Email, StopValidation
from models import User
from werkzeug.security import check_password_hash


class RegisterForm(Form):
    def ValidateEmail(self, field):
        if User.query.filter_by(email=field.data).first():
            raise StopValidation(message='email already in use.')
    
    username = StringField('username', validators=[
        DataRequired(message="missing username"), 
        Length(min=2, max=25),
        ])
    email = EmailField('email', validators=[
        DataRequired(message="missing email"), 
        Email(),
        ValidateEmail,
        ])
    password = PasswordField('password', validators=[
        DataRequired("missing password"), 
        EqualTo('passwordConfirm', 'wrong password confirmation'),
        ])
    passwordConfirm = PasswordField('passwordConfirm', validators=[DataRequired("missing passwordConfirm")])


class LoginForm(Form):
    email = StringField('email', validators=[DataRequired("missing email")])
    password = PasswordField('password', validators=[DataRequired("missing password")])