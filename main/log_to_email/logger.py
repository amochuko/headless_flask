import logging
from logging.handlers import SMTPHandler
import logging.config
from flask import current_app
import yaml


def mail_log():
    """ mail logging setup """
    with open('log_config.yaml') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    MAIL_GANDLER = SMTPHandler(mailhost='127.0.0.1',
                               fromaddr='server-error@example.com',
                               toaddrs=['admin@me.com'],
                               subject='Application Error')

    MAIL_GANDLER.setLevel(logging.ERROR)
    MAIL_GANDLER.setFormatter(
        logging.Formatter(
            '[%(asctime)s %(levelname)s in %(module)s: %(message)s]'))

    if not current_app.debug:
        current_app.logger.addHandler(MAIL_GANDLER)
