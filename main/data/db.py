# pylint: disable=missing-module-docstring
import os
import mysql.connector
from mysql.connector import errorcode
from flask import g
from typing_extensions import Final

from main.util import reports


class DBConnection(object):
    """ Data Layer Class: takes an argument 'load_sample_data' of a
    boolean value (True or False) to determine if the database setup
    includes sample data seeded in.
    For example:
    db = DBConnection(load_sample_data=True) would laod sample data """

    __DB_NAME = os.getenv("DB_NAME")

    def __init__(self, load_sample_data: bool = False):
        self.load_sample_data = load_sample_data

    # method without an instance
    @staticmethod
    def db_connect():
        """ setting up database connection """
        conn, _ = None, None  # pylint: disable=unused-variable

        if 'db' not in g:
            try:
                conn = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv('DB_NAME'))

                # set global db access
                g.conn = conn
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print(reports.STDOUT.get("access_denied"))
                else:
                    print("DB connection error: {}".format(err))
            else:
                print(reports.STDOUT.get("connect_db_passed"))

        return conn

    def create_db(self):
        """ Create database """
        #g.cnx, g.cursor = self.db_connect()  # pylint: disable=unused-variable
        conn = self.db_connect()  # pylint: disable=unused-variable
        try:
            cur = conn.cursor()
            # create db
            cur.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(
                    self.__DB_NAME))
            print("Database {} created successfully.".format(self.__DB_NAME))

            # create table
            if self.load_sample_data:
                self.create_tables_from_file(cursor=g.cursor,
                                             db_to_use=self.__DB_NAME)
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    @staticmethod
    def create_tables_from_file(cursor: mysql.connector.cursor, db_to_use=''):
        """ Create database tables """
        try:
            with open("schema.sql", 'r') as sql_f:
                sql_cmd = sql_f.read().split(';')

                for cmd in sql_cmd:
                    try:
                        cursor.execute(cmd)
                        print(reports.STDOUT.get("create_table_passed"))
                    except mysql.connector.Error as err:
                        if err.errno == 1046:  # 1046 (3D000): No database selected
                            cursor.execute("USE {}".format(db_to_use))
                            cursor.execute(cmd)
                        print(reports.STDOUT.get("create_table_failed"))
                    else:
                        pass
        except EOFError as err:
            print("{} {}".format(
                err, reports.STDOUT.get("access_error_table_script")))
        finally:
            cursor.close()

    @staticmethod
    def db_close(e=None):  # pylint: disable=invalid-name
        """ Close db connection """
        conn = g.pop('conn', e)

        if conn is not None:
            conn.close()
            print('Closing db connection...')

    def init_db(self):
        """ Initialize database """
        conn = self.db_connect()

        try:
            cur = conn.cursor()
            cur.execute("USE {}".format(self.__DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(self.__DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_db()
                #g.conn.database = self.__DB_NAME
            else:
                print('err:', err)
                exit(1)

    def init_app(self, app):
        """ init app for db """
        with app.app_context():
            # Flask to call that function when cleaning up after returning the response.
            app.teardown_appcontext(self.db_close)

            # init db
            self.init_db()

    def __repr__(self):
        return '<DBConnection {}>'.format(self.load_sample_data)


def db_connect():
    # pylint: disable=invalid-name
    """ DBconnection function """
    __DB_obj: Final = DBConnection(load_sample_data=False)
    cnx: Final = __DB_obj.db_connect()  # cursor
    cur: Final = cnx.cursor()

    return (cnx, cur)
