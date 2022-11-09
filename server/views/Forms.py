from wtforms import StringField, PasswordField, EmailField, Form
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from models import User
from werkzeug.security import check_password_hash



class RegisterForm(Form):
    def ValidateUsername(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email already in use.')
    
    username = StringField('username', validators=[DataRequired("missing username"), Length(min=2, max=25)])
    email = EmailField('email', validators=[DataRequired(message="missing email"), Email(), ValidateUsername])
    password = PasswordField('password', validators=[
        DataRequired("missing password"), EqualTo('password_2', '비밀번호가 일치하지 않습니다')])
    password_2 = PasswordField('password_2', validators=[DataRequired("missing password_2")])


class LoginForm(Form):
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message
            
        def __call__(self, form, field):
            email = form['email'].data
            password = field.data
            
            usertable = User.query.filter(User.email == email).first()
            if not check_password_hash(usertable.password,  password):
                raise ValueError('비밀번호 틀림')
                
    email = StringField('email', validators=[DataRequired("missing email")])
    password = PasswordField('password', validators=[DataRequired("missing password"), UserPassword("wrong password")])