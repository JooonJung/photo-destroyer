from db import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from utils import strTagToTagsList

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(50), nullable=True)
    confirmed = db.Column(db.Boolean, nullable=True, default = False)
    createdAt = db.Column(db.DateTime(), nullable=True)
    updatedAt = db.Column(db.DateTime(), nullable=True)
    confirmedAt = db.Column(db.DateTime(), nullable=True)
    tags = db.Column(db.Text)

    def __init__(self, username, password, email, confirmed, confirmedAt = None):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.confirmed = confirmed
        self.createdAt = datetime.datetime.now()
        self.updatedAt = datetime.datetime.now()
        self.confirmedAt = confirmedAt

    def __repr__(self):
        return f'<User {self.username}>'
    
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    @property
    def numberOfPhotos(self):
        return len(self.photo_user)

    @property
    def numberOfAlbums(self):
        return len(self.album_user)

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'username': self.username,
            'email': self.email,
            'confirmed' : self.confirmed,
            'numberOfPhotos' : self.numberOfPhotos,
            'numberOfAlbums' : self.numberOfAlbums,
            'password': self.password,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
            'confirmedAt': self.confirmedAt
        }

    @property
    def serializeWithoutPassword(self):
        serialized_user = self.serialize
        serialized_user.pop('password')
        return serialized_user


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref('photo_user', cascade='all, delete-orphan'))
    mimetype = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text)
    createdAt = db.Column(db.DateTime(), nullable=True)
    updatedAt = db.Column(db.DateTime(), nullable=True)

    def __init__(self):
        self.createdAt = datetime.datetime.now()
        self.updatedAt = datetime.datetime.now()

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'img': self.img,
            'mimetype': self.mimetype,
            'user_id' : self.user_id,
            'tags' : strTagToTagsList(self.tags),
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref('album_user', cascade='all, delete-orphan'))
    mimetype = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text)
    createdAt = db.Column(db.DateTime(), nullable=True)
    updatedAt = db.Column(db.DateTime(), nullable=True)

    def __init__(self):
        self.createdAt = datetime.datetime.now()
        self.updatedAt = datetime.datetime.now()

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'img': self.img,
            'mimetype': self.mimetype,
            'user_id' : self.user_id,
            'tags' : strTagToTagsList(self.tags),
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }