from datetime import datetime
from db import db 
from models import User, Album
from flask import Blueprint, make_response, request, session
from werkzeug.utils import secure_filename
from utils import strTagToTagsList, saveImageAndReturnUrl, tagsListToStrTag
import time
import mimetypes
from Forms import PhotoCreateForm

bp = Blueprint('albums', __name__, url_prefix='/api/v1/albums')

@bp.route('/', methods = ["GET"])
def albums():
  if request.method == "GET":
    ## pagination 어떻게 할지 논의 필요
    if 'user_id' not in session:
      return make_response({"error": "no session"}, 401)
    user = User.query.filter(User.id==session['user_id']).first()
    if not user:
      return make_response({"error": "no user"}, 401)
    return make_response({"albums": [album.serialize for album in user.possessingAlbums]}, 200)


@bp.route('/create', methods = ["POST"])
def albumCreate():
  if request.method == "POST":

    ''' Receive Album image, tags  '''

    if 'user_id' not in session:
      return make_response({"error": "no session"}, 401)
    user = User.query.filter(User.id==session['user_id']).first()
    if not user:
      return make_response({"error": "no user"}, 401)

    ## 0. validate form : Forms 가서 폼부터 만들어야 함

    # validate tags
    '''
    try:
      tags = strTagToTagsList(request.form['tags'])
    except:
      return make_response({"errors": {"tags" : "invalid tags"}}, 401)
    '''

    ## 1. save image from request and generate url
    ### filename = f'{user.id}_album_{"_".join(str(time.time()).split("."))}'
    
    ## 2. create an album instance from url of image, tags
    ### mimetype = mimetypes.guess_type(imgUrl)[0]
    ### album = Album(imgUrl=, owner_id=user.id, mimetype=mimetype, tags=tags)

    ## 3. save album
    ### db.session.add(album)
    
    ## 4. update user tags
    ###  user.updateUserTags()
    
    ## 5. save to db
    ### db.session.commit()


@bp.route('/<album_id>', methods = ["GET", "POST", "DELETE"])
def albumDetail(album_id):
  if request.method == "GET":
    if 'user_id' not in session:
      return make_response({"error": "no session"}, 401)
    user = User.query.filter(User.id==session['user_id']).first()
    if not user:
      return make_response({"error": "no user"}, 401)
    
    album = Album.query.filter(Album.id==album_id).first()
    if not album:
      return make_response({"error": "no matching album"}, 401)

    if album.owner_id != session['user_id']:
      return make_response({"error": "not owner of album"}, 401)

    return make_response({"album": album.serialize}, 200)


  if request.method == "POST":
    ''' Receive tags '''
    
    if 'user_id' not in session:
      return make_response({"error": "no session"}, 401)
    user = User.query.filter(User.id==session['user_id']).first()
    if not user:
      return make_response({"error": "no user"}, 401)

    album = Album.query.filter(Album.id==album_id).first()
    if not album:
      return make_response({"error": "no matching album"}, 401)

    if album.owner_id != session['user_id']:
      return make_response({"error": "not owner of album"}, 401)
    
    # tags validate
    try:
      tags = strTagToTagsList(request.form['tags'])
    except:
      return make_response({"errors": {"tags" : "invalid tags"}}, 401)
    
    album.tags = tagsListToStrTag(tags)
    user.updateUserTags()
    album.updatedAt = datetime.now()
    db.session.commit()
    return make_response({"album": album.serialize}, 200)


  if request.method == "DELETE":
    if 'user_id' not in session:
      return make_response({"error": "no session"}, 401)
    user = User.query.filter(User.id==session['user_id']).first()
    if not user:
      return make_response({"error": "no user"}, 401)
    
    album = Album.query.filter(Album.id==album_id).first()
    if not album:
      return make_response({"error": "no matching album"}, 401)

    if album.owner_id != session['user_id']:
      return make_response({"error": "not owner of album"}, 401)

    db.session.delete(album)
    user.updateUserTags()
    db.session.commit()

    return make_response({"success": "album delete success"}, 200)


if __name__ == "__main__":
    bp.run(debug = True)