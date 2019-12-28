import os  # pylint: disable=missing-docstring
from os.path import exists, join
import logging
from typing import Dict
from typing_extensions import Final
from flask import Flask, jsonify, send_from_directory, make_response
from dotenv import load_dotenv
from flask_cors import CORS

from main.model.db import DBConnection
from config import Config
from main.util.constants import CONSTANTS

# Globals
load_data: bool = False
db: Final = DBConnection(load_sample_data=load_data)  # pylint: disable=invalid-name


def create_app(test_config=None):
    """Initialize the core application."""
    load_dotenv()

    app: Final = Flask(__name__,
                       instance_relative_config=True,
                       static_folder='static')
    # init cors
    CORS(app)

    # log cors activity
    logging.getLogger('flask_cors').level = logging.DEBUG
    logging.debug('flask_cors')

    # default config
    app.config.from_object(Config)

    # ensure instance path
    try:
        if not app.instance_path:
            os.makedirs(app.instance_path)
    except OSError as err:
        # pylint: disable=no-member
        app.logger.info('{}: {} instance directory not available'.format(
            err, app.instance_path))

    # test config
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # init route
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):  # pylint: disable=unused-variable
        print('req path:', path)
        file_to_serve = path if path and exists(join(app.static_folder,
                                                     path)) else 'index.html'
        return send_from_directory(app.static_folder, file_to_serve)

    @app.errorhandler(404)
    def page_not_found(error):  # pylint: disable=unused-variable
        print('error:', error)
        json_res = jsonify(error='Page not found')
        return make_response(json_res,
                             CONSTANTS['HTTP_STATUS']['404_NOT_FOUND'])

    # Initialize Plugins
    # Import and call this functions from the factory before returning the app
    # with app.app_context():
    db.init_app(app)

    # pylint: disable=import-outside-toplevel

    from main.controllers import auth
    app.register_blueprint(auth.bp)

    from main.controllers import nav_menu
    app.register_blueprint(nav_menu.bp)

    from main.controllers import pages
    app.register_blueprint(pages.bp)

    return app
