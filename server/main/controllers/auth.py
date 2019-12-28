import functools
from flask import Blueprint, g, request as req, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from main.model.db import DBConnection

# Globals

__DB = DBConnection(load_sample_data=False)
bp = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')
__POST = 'POST'
__GET = 'GET'


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """ Register route """
    cursor = __DB.db_connect()[1]  # get __DB.db_connect()[1] == cursor
    if req.method == __POST:
        cursor = __DB.db_connect()

    return {'register': 'hello reg!'}
