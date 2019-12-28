from main import create_app
from main.util.constants import CONSTANTS


# pylint: disable=invalid-name
def run_app():
    """ ceate app """
    try:
        app = create_app()
    except ImportError as err:
        raise Exception(f'Error: {err}')
    else:
        if __name__ == '__main__':
            app.run(port=CONSTANTS['PORT'])

#run_app()

app = create_app()
if __name__ == '__main__':
    app.run()
