# Checks if all fields have values, True when all are None
from werkzeug.exceptions import BadRequest

def is_all_none(*argv):
    if all(p is None for p in argv):
        return True

def check_limit(limit):
    if limit == "all":
        limit = -1
        return limit
    else:
        try:
            limit = int(limit)
            return limit
        except:
            raise BadRequest

def validate_integer_param(param):
    try:
        param = int(param)
        if param < 0:
            raise BadRequest
        return param
    except:
        raise BadRequest
