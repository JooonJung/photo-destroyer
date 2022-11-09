from db import db 
from models import User
from flask import Blueprint, make_response, request, session
from werkzeug.security import generate_password_hash
import datetime

bp = Blueprint('account', __name__, url_prefix='/api/v1/account')

@bp.route('/', methods = ["GET", "PUT", "DELETE"])
def account():
  if request.method == "GET":
    if 'email' not in session:
      return make_response({"message": "no session"}, 401)
    user = User.query.filter(User.email==session['email']).first()
    if not user:
      return make_response({"message": "no user"}, 401)
    return make_response(user.serializeWithoutPassword, 200)


  elif request.method == "PUT": # require password & user form
    if 'email' not in session:
      return make_response({"message": "no session"}, 401)
    user = User.query.filter(User.email==session['email']).first()
    if not user:
      return make_response({"message": "no user"}, 401)

    message = {"message" : []}

    if request.form.get('new_password'):
      if not user.verify_password(request.form.get('old_password')):
        return make_response({"message" : "password do not match."}, 401)
      user.password = generate_password_hash(request.form["new_password"])
      message["message"].append({"password": "changed password"})
      user.updatedAt = datetime.datetime.now()

    if request.form.get('username') and user.username != request.form.get('username'):
      user.username = request.form.get('username')
      message["message"].append({"password": "changed username"})
      user.updatedAt = datetime.datetime.now()
    
    db.session.commit()

    if not message["message"]:
      message["message"] = "nothing to change"

    return make_response(message, 200)


  elif request.method == "DELETE":
    if 'email' not in session:
      return make_response({"message": "no session"}, 401)
    user = User.query.filter(User.email==session['email']).first()
    if not user:
      return make_response({"message": "no user"}, 401)
    if not user.verify_password(request.form['password']):
      return make_response({"message" : "password do not match."}, 401)
    
    db.session.delete(user)
    db.session.commit()
    session.pop('email', None)

    return make_response({"message" : "Account Delete Success"}, 200)


  else:
    return make_response({"message": "Page Not Found"}, 404)