from db import db 
from models import User
from flask import Blueprint, make_response, request, session
from werkzeug.security import generate_password_hash
import datetime
from Forms import AccountForm, PasswordChangeForm

bp = Blueprint('account', __name__, url_prefix='/api/v1/account')

@bp.route('/', methods = ["GET", "PUT", "DELETE"])
def account():
  if request.method == "GET":
    if 'user_id' not in session:
      return make_response({"error": "no session"}, 401)
    user = User.query.filter(User.id==session['user_id']).first()
    if not user:
      return make_response({"error": "no user"}, 401)
    return make_response({"success": user.serializeWithoutPassword}, 200)


  elif request.method == "PUT":
    ''' Receive username '''
    if 'user_id' not in session:
      return make_response({"error": "no session"}, 401)
    user = User.query.filter(User.id==session['user_id']).first()
    if not user:
      return make_response({"error": "no user"}, 401)

    form = AccountForm(request.form)

    if not form.validate():
      return make_response({"errors": form.errors}, 401)
      
    user.username = request.form.get('username')
    user.updatedAt = datetime.datetime.now()
    db.session.commit()

    return make_response({"success" : user.serializeWithoutPassword }, 200)


  elif request.method == "DELETE":
    if 'user_id' not in session:
      return make_response({"message": "no session"}, 401)
    user = User.query.filter(User.id==session['user_id']).first()
    if not user:
      return make_response({"message": "no user"}, 401)
    if not user.verify_password(request.form['password']):
      return make_response({"message" : "password do not match."}, 401)
    
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id', None)

    return make_response({"message" : "Account Delete Success"}, 200)


@bp.route('/changePassword', methods = ["POST"])
def changePassword():
  ''' Receive oldPassword, newPassword, newPasswordConfirm '''
  if request.method == "POST":
    if 'user_id' not in session:
      return make_response({"error": "no session"}, 401)
    user = User.query.filter(User.id==session['user_id']).first()
    if not user:
      return make_response({"error": "no user"}, 401)

    if not user.verify_password(request.form.get('oldPassword')):
      return make_response({"error" : "password do not match."}, 401)

    form = PasswordChangeForm(request.form)

    if not form.validate():
      return make_response({"errors": form.errors}, 401)

    user.password = generate_password_hash(request.form["newPassword"])
    user.updatedAt = datetime.datetime.now()
    db.session.commit()

    session.pop("user_id", None)

    return make_response({"success" : {"password": ["changed password"]}}, 200)


if __name__ == "__main__":
    bp.run(debug = True)