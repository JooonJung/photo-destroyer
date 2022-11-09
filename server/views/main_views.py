from flask import Blueprint, request, session, make_response
from models import User
from db import db
from views.Forms import RegisterForm, LoginForm

bp = Blueprint('main', __name__, url_prefix='/api/v1/')

@bp.route('/login', methods=('GET', 'POST'))
def logIn():
    if request.method == "POST":
        form = LoginForm(request.form)
        response = make_response('Response')
        try:
            if form.validate():
                session['email']=form.email.data
                user = User.query.filter(User.email == form.email.data).first()
                response.status = 200
                response = user.serializeWithoutPassword
                return response
            else:
                response.status = 404
                response = form.errors
                return response
        except:
            response.status = 404
            response = {"errror" : "wrong password"}
            return response
    else:
        response.status = 404
        return response
if __name__ == "__main__":
    bp.run(debug = True)

@bp.route('/signup', methods = ["GET", "POST"])
def signUp():
    form = RegisterForm(request.form)
    response = make_response('Response')

    if request.method == "POST": 
        if not form.validate():
            response.status = 404
            response = {"errors": form.errors}
            return response
        else:
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user = User(username, password, email)

            db.session.add(user)
            db.session.commit()
            response.status = 201
            return response
    else:
        response.status = 404
        return response
if __name__ == "__main__":
    bp.run(debug = True)

@bp.route('/logout', methods=["GET"])
def logOut():
    session.pop("email", None)
    response = make_response('Response')
    response.status = 200
    return response
if __name__ == "__main__":
    bp.run(debug = True)