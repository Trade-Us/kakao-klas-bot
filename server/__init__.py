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

    from .views import register_views,subjectName_views,test_views,mypage_views,logout_views
    app.register_blueprint(register_views.bp)
    app.register_blueprint(subjectName_views.bp)
    app.register_blueprint(test_views.bp)
    app.register_blueprint(mypage_views.bp)
    app.register_blueprint(logout_views.bp)

    return app
