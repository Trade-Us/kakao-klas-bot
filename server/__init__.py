from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from .views import assignment_views, notice_views, onlinelecture_views
    app.register_blueprint(assignment_views.bp)
    app.register_blueprint(notice_views.bp)
    app.register_blueprint(onlinelecture_views.bp)

    return app
