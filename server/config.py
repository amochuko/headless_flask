# pylint: disable=missing-module-docstring
import os

class Config(object):
    SECRETE_KEY = os.environ.get('SECRETE_KEY') or 'key+-you-never=know',
    DATABASE_URI = os.getenv('DATABASE_URI')
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    #database = os.getenv('DB_NAME'),
    raise_on_warnings = True
