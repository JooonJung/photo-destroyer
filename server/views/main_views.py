from flask import Blueprint, request, session, make_response
from models import User
from db import db
from Forms import RegisterForm, LoginForm

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


@bp.route('/signup/emailAuth', methods = ["POST"])
def emailAuth():
    if request.method == "POST":
        pass


@bp.route('/signup', methods = ["POST"])
def signup():
    if 'user_id' in session:
        return make_response({"errors" : "session already exists"}, 401)

    form = RegisterForm(request.form)
    if request.method == "POST": 
        if not form.validate():
            return make_response({"errors": form.errors}, 401)
        else:
            user = User(form.username.data, form.password.data, form.email.data)
            db.session.add(user)
            db.session.commit()

            return make_response({"success": "user created"}, 201)


@bp.route('/logout', methods=["GET"])
def logOut():
    if 'user_id' not in session:
        return make_response({"errors" : "first, login to logout"}, 401)
    session.pop("user_id", None)
    return make_response({"success" : "logged out"}, 200)


if __name__ == "__main__":
    bp.run(debug = True)