from datetime import datetime
from db import db 
from models import User, Photo
from flask import Blueprint, make_response, request, session
from werkzeug.utils import secure_filename
from utils import strTagToTagsList, saveImageAndReturnUrl
import time
import mimetypes

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
    return make_response({"photos": [photo.serialize for photo in user.possessingPhotos]}, 200)

  if request.method == "POST":
    ''' Receive photo QRcodeUrl, brand, tags '''

    if 'user_id' not in session:
      return make_response({"error" : "no session"}, 401)

    ## TODO : form validation
    QRcodeUrl = request.form["QRcodeUrl"]
    brand = request.form["brand"]
    filename = f'{session["user_id"]}_{brand}_{"_".join(str(time.time()).split("."))}'

    imgUrl = saveImageAndReturnUrl(QRcodeUrl=QRcodeUrl, brand=brand, filename=filename)    
    mimetype = mimetypes.guess_type(imgUrl)[0]
    tags = strTagToTagsList(request.form['tags'])
    owner_id = session['user_id']

    photo = Photo(imgUrl=imgUrl, owner_id=owner_id, mimetype=mimetype, tags=tags)
    db.session.add(photo)
    db.session.commit()

    return make_response({"success": {"photo" : photo.serialize }}, 200)


@bp.route('/<photo_id>', methods = ["GET", "POST", "DELETE"])
def photosDetail(photo_id):
  if request.method == "GET":
    if 'user_id' not in session:
      return make_response({"error": "no session"}, 401)
    
    photo = Photo.query.filter(Photo.id==photo_id).first()
    if not photo:
      return make_response({"error": "no matching photo"}, 401)

    if photo.owner_id != session['user_id']:
      return make_response({"error": "not owner of photo"}, 401)

    return make_response({"photo": photo.serialize}, 200)


  if request.method == "DELETE":
    if 'user_id' not in session:
      return make_response({"error": "no session"}, 401)
    
    photo = Photo.query.filter(Photo.id==photo_id).first()
    if not photo:
      return make_response({"error": "no matching photo"}, 401)

    if photo.user_id != session['user_id']:
      return make_response({"error": "not owner of photo"}, 401)

    db.session.delete(photo)
    db.session.commit()

    return make_response({"success": "photo delete success"}, 200)

@bp.route('/upload', methods = ['POST'])
def photoUpload():
  if 'user_id' not in session:
    return make_response({"error" : "no session"}, 401)
  
  file = request.files['file']
  mimetype = file.mimetype
  imgUrl = './static/upload/' + secure_filename(file.filename)
  tags = list(request.form['tags'])
  file.save(imgUrl)
  owner_id = session['user_id']

  photo = Photo(imgUrl=imgUrl, owner_id=owner_id, mimetype=mimetype, tags=tags)
  db.session.add(photo)
  db.session.commit()

  return make_response({"success":"photo uploaded"}, 200)

if __name__ == "__main__":
    bp.run(debug = True)