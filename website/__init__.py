from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

DB_NAME = "postgresql://rwcxwbvtjxvupg:dbc898eed79e2efde528386684276dd6e3cf546412ec9fde4aa1098b06f1302a@ec2-34-253-119-24.eu-west-1.compute.amazonaws.com:5432/d45fk8ej32orba"



def create_app():
    app = Flask(__name__)
    migrate = Migrate(app,db)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


