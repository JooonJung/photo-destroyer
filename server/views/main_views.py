from flask import Blueprint, request, session, make_response, Flask, url_for, render_template
from models import User
from db import db
from Forms import RegisterForm, LoginForm, EmailForm
import string, random
from werkzeug.security import generate_password_hash
import datetime
from views.token import generate_confirmation_token, confirm_token, send_email

bp = Blueprint('main', __name__, url_prefix='/api/v1/')

@bp.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        if 'user_id' in session:
            return make_response({"errors" : "session already exists"}, 401)

        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter(User.email==form.email.data).first()
            if not user:
                return make_response({"errors": "no matching user"}, 401)
            if not user.verify_password(form.password.data):
                return make_response({"errors" : "password wrong."}, 401)
            session['user_id']=user.id
            resp = make_response({"success": user.serializeWithoutPassword}, 200)
            resp.set_cookie('user_id', f'{user.id}')
            return resp
        else:
            return make_response(form.errors, 401)

@bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        return make_response({"error": 'The confirmation link is invalid or has expired.'}, 401)
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return make_response({"success": 'Account already confirmed. Please login.'}, 200)
    else:
        user.confirmed = True
        user.confirmAt = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return make_response({"success" : "email confirmed"} , 200)

@bp.route('/signup', methods = ["POST"])
def signup():
    if 'user_id' in session:
        return make_response({"errors" : "session already exists"}, 401)

    form = RegisterForm(request.form)
    if request.method == "POST": 
        if not form.validate():
            return make_response({"errors": form.errors}, 401)
        else:
            user = User(form.username.data, form.password.data, form.email.data, confirmed=False)
            db.session.add(user)
            db.session.commit()

            token = generate_confirmation_token(user.email)
            confirm_url = url_for('main.confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            print("before")
            send_email(user.email, subject, html)
            print("after")

            return make_response({"success": "user created"}, 201)


@bp.route('/logout', methods=["GET"])
def logOut():
    if 'user_id' not in session:
        return make_response({"errors" : "first, login to logout"}, 401)
    session.pop("user_id", None)
    return make_response({"success" : "logged out"}, 200)


@bp.route('/resetPassword', methods = ["POST"])
def resetPassword():
    if request.method == "POST":
        form = EmailForm(request.form)
        if not form.validate():
            return make_response({"errors": form.errors}, 401)
        user = User.query.filter(User.email==form.email.data).first()
        if not user:
            return make_response({"errors": "no matching user"}, 401)

        ## 1. 랜덤 key 발급 후 이메일 전송
        ### write code here...

        ## 2. 랜덤 key 기반 본인 인증 과정
        ### write code here...

        ## 3. 본인 인증이 되면 랜덤 password 발급 후 password update
        randomPassword = "".join([random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10)])
        print(randomPassword) # 일단 테스트할 때 필요해서 비번 출력, 이메일 구현되면 삭제
        user.password = generate_password_hash(randomPassword)
        user.updatedAt = datetime.datetime.now()
        db.session.commit()

        ## 4. password 이메일로 보내주기
        ### write code here...

        return make_response({"success" : {"password": ["reset password"]}}, 200)


if __name__ == "__main__":
    bp.run(debug = True)