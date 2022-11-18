from wtforms import StringField, PasswordField, EmailField, Form, FieldList
from wtforms.validators import DataRequired, Length, EqualTo, Email, StopValidation, ValidationError, URL
from models import User
from werkzeug.security import check_password_hash
from flask import session


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


class AccountForm(Form):
    def compareUsername(self, field):
        user = User.query.filter_by(id=session['user_id']).first()
        if user.username == field.data:
            raise StopValidation(message='same username')

    username = StringField('username', validators=[
        DataRequired("missing username"),
        Length(min=2, max=25),
        compareUsername,
        ]
    )


class PasswordChangeForm(Form):
    class NotEqualTo(EqualTo):
        def __init__(self, fieldname, message=None):
            super().__init__(fieldname, message)

        def __call__(self, form, field):
            try:
                other = form[self.fieldname]
            except KeyError as exc:
                raise ValidationError(
                    field.gettext("Invalid field name '%s'.") % self.fieldname
            ) from exc
            if field.data != other.data:
                return

            d = {
                "other_label": hasattr(other, "label")
                and other.label.text
                or self.fieldname,
                "other_name": self.fieldname,
            }
            message = self.message
            if message is None:
                message = field.gettext("Field must not be equal to %(other_name)s.")

            raise ValidationError(message % d)

    oldPassword = PasswordField('oldPassword', validators=[
            DataRequired("missing old password")
        ]
    )
    newPassword = PasswordField('newPassword', validators=[
            DataRequired("missing new password"),
            NotEqualTo('oldPassword', 'password has not changed'),
            EqualTo('newPasswordConfirm', 'wrong password confirmation'),
        ]
    )
    newPasswordConfirm = PasswordField('newPasswordConfirm', validators=[
            DataRequired("missing new password confirmation"),
        ]
    )


class EmailForm(Form):
    email = EmailField('email', validators=[
        DataRequired(message="missing email"), 
        Email(),
        ]
    )


class PhotoCreateForm(Form):
    def brandValidate(self, field):
        if field.data not in ["lifeFourCuts", "selpix", "photoSignature", "photoism", "haruFilm"]:
            raise StopValidation(message='brand not available')


    QRcodeUrl = StringField('QRcodeUrl', validators=[
        DataRequired(message="missing QRcode URL"),
        URL(),
        ]
    )
    brand = StringField('QRcodeUrl', validators=[
        DataRequired(message="missing brand"),
        brandValidate,
        ]
    )