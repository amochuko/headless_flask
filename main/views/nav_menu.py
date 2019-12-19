from typing import Dict, Iterable, Union, Optional, overload, Tuple
from typing_extensions import Final
from flask import Blueprint, g, redirect, request as req, jsonify, Markup
from werkzeug.exceptions import abort
from mysql.connector import Error
from mysql.connector import errorcode

from main.data.db import DBConnection
from main.util import reports as rp
from main.util import lib

__DB: Final = DBConnection(load_sample_data=False)
bp: Final = Blueprint(name='nav_menu', import_name=__name__, url_prefix='/nav')


def db_cnx():
    """ DBconnection function """
    cnx: Final = __DB.db_connect()  # cursor
    cur: Final = cnx.cursor()
    return (cnx, cur)


@overload
def index() -> Iterable[Dict[str, str]]:
    """ Overload the return type for index() with empty body """
    ...


@overload
def index() -> Iterable[str]:
    """ Overload the return type for index() with empty body """
    ...  # use  ellipsis (...) literal instead of pass


@bp.route('/')
def index() -> Union[Iterable[Dict[str, str]],
                     str]:  # return can be a list[{str, str}] or str
    """ list all nav menu """
    err: Optional[str] = None
    nav: Final[Iterable[Dict[str, str]]] = []

    try:

        _, cur = db_cnx()  # cursor
        cur.execute(""" SELECT * FROM nav_menu
                        ORDER BY id ASC """)

        for (id, title) in cur.fetchall():
            nav.append({'id': id, 'title': title})

    except Error as error:
        if error.errno == errorcode.ER_NO_DB_ERROR:
            err = rp.STDOUT.get('menu_list_empty')

    finally:
        cur.close()

    if err is None:

        return lib.route_response(res_ok=True, data=nav)

    return lib.route_response(res_ok=False, data=err), 301


@bp.route('/create', methods=['POST', 'GET'])
def create():
    """ create nav menu """
    if req.method == 'POST':
        err: str = None
        title: str = lib.strip_lower(req.json['title'])
        res: str = None

        if not title:
            err = rp.STDOUT.get('nav_menu').get('title_required')

        try:
            cnx, cur = db_cnx()  # cursor

            # db
            sql: str = "INSERT INTO nav_menu (title) VALUES (%s)"
            vals: Tuple(str) = (title, )
            cur.execute(sql, vals)
            cnx.commit()

            if cur.rowcount >= 1:
                res = "{}".format(title)

        except Error as error:
            if error.errno == errorcode.ER_DUP_ENTRY:
                err = '{} - {}'.format(
                    title,
                    rp.STDOUT.get('nav_menu').get('title_exists'))
            print('err caught:', error.errno, error.sqlstate, error.msg)
        finally:
            cur.close()

        if err is None:
            return lib.route_response(res_ok=True, data=res), 201

        return lib.route_response(res_ok=False, data=err), 409


@bp.route('/edit/<string:slug>', methods=['POST', 'PUT'])
def edit(slug):
    """ edit nav menu """
    if req.method == 'PUT':
        err = None
        res = None
        new_title = req.json['title']

        try:
            cnx, cur = db_cnx()  # cursor

            query = """ UPDATE nav_menu
                            SET title = %s
                            WHERE title = %s """

            # TODO: check up with update statement

            data = (new_title, lib.get_from_slug(slug))

            p = cur.execute(query, data)
            print('ppp:', p)
            cnx.commit()
            res = rp.STDOUT.get('nav_menu').get('update_ok')

        except Error as error:
            print('error:', error)
            err = error

            if error.errno == errorcode.ER_DUP_ENTRY:
                err = '{} - {}'.format(
                    new_title,
                    rp.STDOUT.get('nav_menu').get('title_exists'))

        finally:
            cur.close()

        if err is None:
            return lib.route_response(res_ok=True, data=res)

        return lib.route_response(res_ok=False, data=err), 301


@bp.route('/delete/<int:nav_id>', methods=['GET', 'POST', 'DELETE'])
def delete(nav_id):
    """ delete nav menu by id """
    if req.method == 'DELETE':
        err = None
        res = None

        try:
            cnx, cur = db_cnx()  # cursor

            query = """ DELETE FROM nav_menu
                            WHERE id = %s """
            data = (nav_id, )

            cur.execute(query, data)
            cnx.commit()

            if cur.rowcount >= 1:
                res = rp.STDOUT.get('nav_menu').get('delete_ok')

        except Error as error:
            err = error
            if error.errno == errorcode.ER_DUP_ENTRY:
                err = '{} - {}'.format(nav_id,
                                       rp.STDOUT.get('nav_menu').get('empty'))
        finally:
            cur.close()

        if err is None:
            return lib.route_response(res_ok=True, data=res)

        return lib.route_response(res_ok=False, data=err), 302


@bp.route('/details/<string:slug>', methods=['GET'])
def get_nav(slug):
    """ list all nav menu """
    err = None
    nav = None

    if req.method == 'GET':

        try:
            _, cur = db_cnx()  # cursor

            query = """ SELECT id, title FROM nav_menu
                            WHERE title = %s
                            """
            vals = (lib.get_from_slug(slug), )
            cur.execute(query, vals)

            nav = []
            for (id, title) in cur.fetchall():
                nav.append({'id': id, 'title': title})

        except Error as error:
            print('err:', error)
            if error.errno == errorcode.ER_NO_DB_ERROR:
                err = rp.STDOUT.get('menu_list_empty')

        finally:
            cur.close()

        if err is None:

            return lib.route_response(res_ok=True, data=nav)

        return lib.route_response(res_ok=False, data=err), 404
