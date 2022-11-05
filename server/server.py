from flask import Flask
from db import db_init, db
from flask_migrate import Migrate
import config
from views import main_views

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db_init(app)
    migrate = Migrate()

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    import models

    # 블루프린트
    from views import main_views
    app.register_blueprint(main_views.bp)

    return app