# pylint: disable=missing-docstring
from typing import Tuple, Iterable, Dict, Union, Optional, Any
from typing_extensions import Final
from flask import Blueprint, request as req
from mysql.connector import Error as MySQLError, errorcode

from main.model.db import db_connect
from main.util import reports as rp, lib

bp: Final = Blueprint(name='pages', import_name=__name__, url_prefix='/api/pages')


# @overload
#def index() -> Iterable[Dict[str, str]]:
 #   """ overload for index with empty body"""
#    ...
#

#
#@overload
#def index() -> Iterable[str]:
 #   """ overload for index with empty body"""
 #   ... 
#


@bp.route('/', methods=['GET'])
def index() -> Union[Iterable[Dict[str, str]], str]:
    """ list all pages """

    if req.method == 'GET':

        err: Optional[str] = None
        pages: Final[Iterable[Dict[str, str]]] = []
        p_obj = None

        try:
            _, cur = db_connect()  # cursor
            cur.execute(""" SELECT
                            p.page_id, 
                            n.title nav_menu,
                            p.title page_title,
                            p.image_url image
                            FROM pages as p
                            INNER JOIN nav_menu as n
                            ON n.nav_id = p.nav_id
                            ORDER BY n.title ASC """)

            for row in cur.fetchall():
                p_obj = {
                    'id': row[0],
                    'nav_menu': row[1],
                    'title': row[2],
                    'image': row[3]
                }
                pages.append(p_obj)

        except MySQLError as error:
            if error.errno == errorcode.ER_NO_DB_ERROR:
                err = rp.STDOUT.get('pages').get('empty')
        finally:
            cur.close()

        if err is None:
            return lib.route_response(res_ok=True, data=pages)

        return lib.route_response(res_ok=False, data=err), 301


@bp.route('/<int:page_id>', methods=['GET'])
def get_by_id(page_id) -> Dict[str, str]:
    """ list all pages """

    if req.method == 'GET':

        err: Optional[str] = None
        p_obj: Any = None
        page: Optional[Dict[str, str]] = None

        try:
            _, cur = db_connect()  # cursor

            query = """ SELECT
                            p.page_id, 
                            n.title nav_menu,
                            p.title page_title,
                            p.image_url image
                            FROM pages as p
                            INNER JOIN nav_menu as n
                            ON n.nav_id = p.nav_id
                            WHERE p.page_id = %s
                            ORDER BY n.title ASC """
            vals = (page_id, )
            cur.execute(query, vals)

            p_obj = cur.fetchone() # get one row

            if p_obj is None:
                err = rp.STDOUT.get('pages').get('empty')
            else:
                while p_obj:
                    page = {
                        'id': p_obj[0],
                        'nav_menu': p_obj[1],
                        'title': p_obj[2],
                        'image': p_obj[3]
                    }

                    p_obj = cur.fetchone() # conditional check


        except MySQLError as error:
            if error.errno == errorcode.ER_NO_DB_ERROR:
                err = rp.STDOUT.get('pages').get('empty')
        finally:
            cur.close()

        if err is None:
            return lib.route_response(res_ok=True, data=page)

        return lib.route_response(res_ok=False, data=err), 400


@bp.route('/create', methods=['POST'])
def create() -> str:
    """ create a page """
    if req.method == 'POST':

        err: Optional[str] = None
        res: Optional[str] = None

        title: str = lib.strip_lower(req.json['title'])
        nav_id: str = lib.strip_lower(req.json['nav_id'])
        slug: str = lib.set_to_slug(lib.strip_lower(req.json['title']))
        image_url: str = lib.strip_lower(req.json['image_url'])

        if title is None:
            err = rp.STDOUT.get('page').get('required')

        try:
            cnx, cur = db_connect()

            query: str = """ INSERT INTO pages (title,nav_id,slug,image_url)
            VALUES (%s, %s, %s, %s) """
            vals: Tuple(str) = (title, nav_id, slug, image_url)

            cur.execute(query, vals)
            cnx.commit()

            if cur.rowcount > 0:
                res = f"{title.capitalize()} {rp.STDOUT.get('pages').get('created')}"

        except MySQLError as error:
            if error.errno == errorcode.ER_DUP_ENTRY:
                err = f"[{title.capitalize()}] {rp.STDOUT.get('pages').get('exists')}"

        finally:
            cur.close()

        if err is None:
            return lib.route_response(res_ok=True, data=res), 201

        return lib.route_response(res_ok=False, data=err), 409


@bp.route('/edit/<int:page_id>', methods=['PUT'])
def edit_put(page_id) -> str:
    """ PUT - update a page """
    if req.method == 'PUT':

        print('page_id:', page_id)
        err: Optional[str] = None
        res: Optional[str] = None

        title: str = lib.strip_lower(req.json['title'])
        nav_id: str = lib.strip_lower(req.json['nav_id'])
        slug: str = lib.set_to_slug(lib.strip_lower(req.json['title']))
        image_url: str = lib.strip_lower(req.json['image_url'])

        if title is None:
            err = rp.STDOUT.get('page').get('required')

        try:
            cnx, cur = db_connect()
            query: str = """ UPDATE pages
                                SET 
                                    title = %s,
                                    nav_id = %s,
                                    slug = %s,
                                    image_url = %s
                                WHERE page_id = %s """
            vals: Tuple(str) = (title, nav_id, slug, image_url, page_id)

            cur.execute(query, vals)
            cnx.commit()

            if cur.rowcount > 0:
                res = f"{rp.STDOUT.get('pages').get('updated')}"

        except MySQLError as error:
            print('error:', error)
            err = 'error here'

        finally:
            cur.close()

        if err is None:
            return lib.route_response(res_ok=True, data=res), 201

        return lib.route_response(res_ok=False, data=err), 409


@bp.route('/edit/<int:page_id>', methods=['PATCH'])
def edit_patch(page_id) -> str:
    """ PATCH: update a page """

    if req.method == 'PATCH':
        err: Optional[str] = None
        res: Optional[str] = None

        title: str = lib.strip_lower(req.json['title'])
        nav_id: str = lib.strip_lower(req.json['nav_id'])
        slug: str = lib.set_to_slug(lib.strip_lower(req.json['title']))
        image_url: str = lib.strip_lower(req.json['image_url'])

        if title is None:
            err = rp.STDOUT.get('page').get('required')

        try:
            cnx, cur = db_connect()
            query: str = """ UPDATE pages
                                SET 
                                    title = %s,
                                    nav_id = %s,
                                    slug = %s,
                                    image_url = %s
                                WHERE page_id = %s """
            vals: Tuple(str) = (title, nav_id, slug, image_url, page_id)

            cur.execute(query, vals)
            cnx.commit()

            if cur.rowcount > 0:
                res = f"{rp.STDOUT.get('pages').get('updated')}"

        except MySQLError as error:
            print('error:', error)
            err = 'error here'

        finally:
            cur.close()

        if err is None:
            return lib.route_response(res_ok=True, data=res), 201

        return lib.route_response(res_ok=False, data=err), 409


@bp.route('/delete/<int:page_id>', methods=['DELETE'])
def delete(page_id) -> str:
    """ create a page """

    if req.method == 'DELETE':
        err: Optional[str] = None
        res: Optional[str] = None

        if page_id is None:
            err = rp.STDOUT.get('page').get('err')

        try:
            cnx, cur = db_connect()
            q_del: str = """ DELETE FROM pages WHERE page_id = %s """
            v_del: Tuple(str) = (page_id, )

            q_id = """ SELECT count(*) FROM pages WHERE page_id = %s """
            v_id = (page_id, )

            cur.execute(q_id, v_id)
            for r_id in cur.fetchone():
                print('row:', r_id)
                if r_id > 0:
                    cur.execute(q_del, v_del)  # delete by id
                    cnx.commit()

                    if cur.rowcount > 0:
                        print('cur.rowcount:', cur.rowcount)
                        res = f"{rp.STDOUT.get('pages').get('deleted')}"
                    else:
                        err = f"{rp.STDOUT.get('pages').get('not_deleted')}"
                else:
                    err = f"{rp.STDOUT.get('pages').get('not_deleted')}"

        except MySQLError as error:
            err = error
        finally:
            cur.close()

        if err is None:
            return lib.route_response(res_ok=True, data=res), 201

        return lib.route_response(res_ok=False, data=err), 409
