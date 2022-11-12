from db import db 
from models import User, Photo
from flask import Blueprint, make_response, request, session

bp = Blueprint('photos', __name__, url_prefix='/api/v1/photos')

@bp.route('/', methods = ["GET", "POST"])
def photos():
  if request.method == "GET":
    ## pagination 어떻게 할지 논의 필요
    if 'user_id' not in session:
      return make_response({"error": "no session"}, 401)
    user = User.query.filter(User.id==session['user_id']).first()
    if not user:
      return make_response({"error": "no user"}, 401)
    return make_response({"photos": [photo.serialize for photo in user.photo_user]}, 200)


if __name__ == "__main__":
    bp.run(debug = True)