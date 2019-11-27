import os  # pylint: disable=missing-module-docstring
import mysql.connector
from mysql.connector import errorcode
from flask import g

from main.util import reports

DB_NAME = os.getenv("DB_NAME")


class DBConnection(object):
    """ Data Layer Class: takes an argument 'load_sample_data' of a boolean value (True or False) to determine if the database setup includes sample data seeded in.
    For example: 
    db = DBConnection(load_sample_data=True) would laod sample data
    db = DBConnection(load_sample_data=False) would not load the sample data."""
    def __init__(self, load_sample_data: bool = False):
        self.load_sample_data = load_sample_data

    def db_connect(self):
        """ setting up database connection """
        cnx, cursor = None, None  # pylint: disable=unused-variable

        if 'db' not in g:
            try:
                cnx = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                )
                cursor = cnx.cursor()

                # set global db access
                g.cnx = cnx
                g.cursor = cursor
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print(reports.STDOUT.get("access_denied"))
                else:
                    print("DB connection error: {}".format(err))
            else:
                print(reports.STDOUT.get("connect_db_passed"))

        return (g.cnx, g.cursor)

    def create_db(self):
        """ Create database """
        g.cnx, g.cursor = self.db_connect()  # pylint: disable=unused-variable
        try:
            # create db
            g.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(
                    DB_NAME))
            print("Database {} created successfully.".format(DB_NAME))

            # create table
            if self.load_sample_data:
                self.create_tables_from_file(cursor=g.cursor,
                                             db_to_use=DB_NAME)
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def create_tables_from_file(self,
                                cursor: mysql.connector.cursor,
                                db_to_use=''):
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
        else:
            pass

    def db_close(self, e=None):  # pylint: disable=invalid-name
        """ Close db connection """
        cnx = g.pop('cnx', e)

        if cnx is not None:
            cnx.close()
            print('Closing db connection...')

    def init_db(self):
        """ Initialize database """
        g.cnx, g.cursor = self.db_connect()

        try:
            g.cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_db()
                g.cnx.database = DB_NAME
            else:
                print(err)
                exit(1)

    def init_app(self, app):
        """ init app for db """
        with app.app_context():
            # Flask to call that function when cleaning up after returning the response.
            app.teardown_appcontext(self.db_close)

            # init db
            self.init_db()
