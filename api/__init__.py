from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# initialize db
db = SQLAlchemy()


def create_app(config="config.py"):
    # initialize Flask
    app = Flask(__name__)
    # to configure a database
    app.config.from_pyfile(config)
    # pass 'app' to SQLAlchemy/db
    db.init_app(app)

    with app.app_context():
        # import routes
        from . import routes
        # create database tables
        db.create_all()
        return app
