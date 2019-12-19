# pylint disable=missing-module-docstring

import os
from typing import Optional, Iterable, Dict, ClassVar
from typing_extensions import final, Final
import mysql.connector
from mysql.connector import errorcode
from flask import current_app

from main.data.db import DBConnection
from main.util import reports as rp


# pylint: disable=invalid-name
@final  # prevent from subclassing
class NavMenu(object):
    """ Model for the Navigation menu """
    err: Optional[str] = None
    amp: ClassVar[int] = 1  # annotation as class or static variable only

    def __init__(self) -> None:
        self.db = DBConnection()
        self.db.init_app(current_app)  # init db
        self.cnx, self.cursor = self.db.db_connect()  # cursor

        self.cursor.execute(f"USE {'headless_101_cms'}")
        self.cursor.execute(f'USE DATABASE {os.getenv("DB_NAME")}')

    @final  # prevent from overriding
    def get_menus(self):
        """ get all nav menus """

        nav_list: Final[Iterable[Dict[str, str]]] = []  # nav_list is a const - 'Final'

        try:
            self.cursor.execute(f"SELECT * FROM {'nav_menu'}")

            for (id, title) in self.cursor.fetchall():  # pylint: disable=redefined-builtin
                nav_list.append({'id': id, 'title': title})
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_NO_DB_ERROR:
                err = rp.STDOUT.get('menu_list_empty')
                print('err:', err)

        if err is None:
            return nav_list

        return err

    def hello_nav(self) -> int:
        """ test """
        return 23 + 2

    def __repr__(self) -> str:
        """ print class  """
        return f"<NavMenu {self.cursor}>"
