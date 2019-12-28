# pylint: disable=missing-module-docstring

from typing import Iterable
from flask import jsonify


# NB: Type - List is more rigid so use Iteratble instead
def route_response(res_ok: bool, data: Iterable[str]) -> Iterable[str]:
    """ return response for routes """
    if not res_ok:
        return jsonify(err=data)
        #return '{"err": data}'

    return jsonify(data=data)


def strip_lower(arg: str) -> str:
    """ strip whitespacess """
    return arg.strip().lower()


def set_to_slug(arg: str) -> str:
    """ set slug for arg: str """
    return arg.replace(' ', '-')


def get_from_slug(arg: str) -> str:
    """ set slug for arg: str """
    return arg.replace('-', ' ')


def returns_noting(arg: str) -> None:
    """ returns none """
    print(f'this func returnes {arg}')
