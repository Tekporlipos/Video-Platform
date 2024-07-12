def logger(logger_type, log=None, message=None):
    from app import app
    if logger_type == "info" and log is not None:
        app.logger.info(message)
    elif logger_type == "warning" and log is not None:
        app.logger.warning(message)
    elif logger_type == "error" and log is not None:
        app.logger.error(message)
