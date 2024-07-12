import logging
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    log_handler = RotatingFileHandler('./storage/log/video-platform.log', maxBytes=1024 * 1024, backupCount=5)
    log_handler.setFormatter(log_formatter)
    app.logger.addHandler(log_handler)

    app.config['PROPAGATE_EXCEPTIONS'] = True
