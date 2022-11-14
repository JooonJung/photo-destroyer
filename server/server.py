from flask import Flask
from db import db_init, db
from flask_migrate import Migrate
import config
from flask_cors import CORS
from views import main_views, account_views, photo_views

def create_app():
    app = Flask(__name__)
    app.secret_key = "12345678910"
    app.config.from_object(config)
    db_init(app)
    migrate = Migrate()

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    # 블루프린트
    app.register_blueprint(main_views.bp)
    app.register_blueprint(account_views.bp)
    app.register_blueprint(photo_views.bp)

    CORS(app)

    return app