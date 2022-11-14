from itsdangerous import URLSafeTimedSerializer
import config
from flask import Flask, current_app
from flask_mail import Message, Mail

def generate_confirmation_token(email):
    app = Flask(__name__)
    app.secret_key = "12345678910"
    app.config.from_object(config)
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    app = Flask(__name__)
    app.config.from_object(config)
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def send_email(to, subject, template):
    app = current_app
    mail = Mail(app)
    app.config.from_object(config)
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_USERNAME']
    )
    mail.send(msg)


