from flask import Flask, render_template, session
from flask.ext.session import Session
from flask_bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.mongoengine import MongoEngine
from config import config
from flask.ext.login import LoginManager
from dotenv import parse_dotenv, load_dotenv

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = MongoEngine()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    try:
        load_dotenv('.env')
        app.config.update(parse_dotenv('.env'))
    except TypeError:
        print('Error parsing .env')
    app.config['SECRET_KEY']
    app.config['SESSION_TYPE']= 'filesystem'
    app.config['MONGODB_SETTINGS'] = {
        'db': app.config['MONGO_DBNAME'],
        'host': app.config['MONGO_URI']
    }

    #MAIL 
    app.config.update(
        DEBUG=True,
        #EMAIL SETTINGS
        MAIL_SERVER= app.config['MAIL_SERVER'],
        MAIL_PORT = app.config['MAIL_PORT'],
        MAIL_USE_TLS = False,
        MAIL_USE_SSL = True,
        MAIL_USERNAME = app.config['MAIL_USERNAME'],
        MAIL_PASSWORD = app.config['MAIL_PASSWORD']
    )

    mail = Mail(app)


    config[config_name].init_app(app)
    bootstrap.init_app(app)
    # mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    Session(app)

# additional _init_.py file in each of these modules
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .browse import browse as browse_blueprint
    app.register_blueprint(browse_blueprint)

    from .literature import lit as lit_blueprint
    app.register_blueprint(lit_blueprint)

    from .preferences import pref as pref_blueprint
    app.register_blueprint(pref_blueprint)

    from .search import search as search_blueprint
    app.register_blueprint(search_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

 # attach routes and custom error pages here
    return app


# Actually connects to the DB
def connect_db():
    connection = connect(app.config['MONGO_DBNAME'], username = app.config['MONGO_USERNAME'], password = app.config['MONGO_PASSWORD'], host = app.config['MONGO_URI'])
    print('Connected to DB.')
    return connection

def get_db():
    db = connect_db()
    db = db[app.config['MONGO_DBNAME']]

    # Authenticate that connection
    db.authenticate(app.config['MONGO_USERNAME'], app.config['MONGO_PASSWORD'])
    return db
