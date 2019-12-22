from typing_extensions import Final

from .db import DBConnection

__DB: Final = DBConnection(load_sample_data=False)


def db_connection():
    """ DBconnection function """
    cnx: Final = __DB.db_connect()  # cursor
    cur: Final = cnx.cursor()

    return (cnx, cur)
