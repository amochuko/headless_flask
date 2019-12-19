# pylint: disable=missing-module-docstring
import os
from flask import Flask, jsonify
from dotenv import load_dotenv

from main.data.db import DBConnection
from main.config import Config

# Globals
load_data: bool = False
db = DBConnection(load_sample_data=load_data)  # pylint: disable=invalid-name



def create_app(test_config=None):
    """Initialize the core application."""
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    # default config
    app.config.from_object(Config)

    # ensure instance path
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        #print("Directory {} not available".format(app.instance_path))

    # test config
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # init route
    @app.route('/')
    def index():  # pylint: disable=unused-variable
        return {'data': 'Hello WOrld!'}

    # Initialize Plugins
    # Import and call this functions from the factory before returning the app
    # with app.app_context():
    db.init_app(app)

    # register blueprint

    # pylint: disable=import-outside-toplevel
    from .views import auth
    app.register_blueprint(auth.bp)

    from .views import nav_menu
    app.register_blueprint(nav_menu.bp)
    return app
