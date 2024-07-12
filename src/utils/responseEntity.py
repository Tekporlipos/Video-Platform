def success_response(message=None, data=None, status_code=200, logger=None, logger_type=None):
    response = {
        'success': True,
        'message': message,
        'data': data
    }

    if logger is not None and logger_type is not None:
        from src.utils.helpers import logger
        logger(logger_type, logger, message + " " + str(status_code))
    return response, status_code


def error_response(message=None, data=None, status_code=404, logger=None, logger_type=None):
    response = {
        'success': False,
        'message': message,
        'data': data
    }
    if logger is not None and logger_type is not None:
        from src.utils.helpers import logger
        logger(logger_type, logger, message + " " + str(status_code))
    return response, status_code
