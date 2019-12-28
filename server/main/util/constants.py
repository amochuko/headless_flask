import os # pylint:disable=missing-docstring

CONSTANTS = {
    'PORT': os.environ.get('PORT', 5000),
    'DB_HOST':os.environ.get("DB_HOST"),
    'DB_USER':os.environ.get("DB_USER"),
    'DB_PASSWORD':os.environ.get("DB_PASSWORD"),
    'DB_NAME':os.environ.get('DB_NAME'),
    'HTTP_STATUS': {
        '404_NOT_FOUND': 404,
        '201_CREATED': 201,
        '500_INTERNAL_SERVER_ERROR': 500
    },
    'ENDPOINT': {
        'MASTER_DETAIL': '/api/masterdetail',
        'LIST': '/api/list',
        'GRID': '/api/grid',
    }
}
