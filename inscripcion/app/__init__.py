from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from feature import Feature
from flask_mail import Mail

db = SQLAlchemy()
feature = Feature()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

preventa_camisetas_admin = {}


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    preventa_camisetas_admin['data'] = app.config[
        'ECCEJU_PREVENTA_CAMISETAS_ADMIN'
    ]

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .preventa import preventa as preventa_blueprint
    app.register_blueprint(preventa_blueprint, url_prefix='/preventa')

    return app
