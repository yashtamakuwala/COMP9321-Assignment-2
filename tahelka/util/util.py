# Checks if all fields have values, True when all are None
from werkzeug.exceptions import BadRequest

def areFieldsEmpty(*argv):
    if all(p is None for p in argv):
        return True



def limitCheck(limit):
    if limit == "all":
        limit = -1
        return limit
    else:
        try:
            limit = int(limit)
            return limit
        except:
            raise BadRequest

def is_filter_valid(filter):
    possible_filters = [
        'lga',
        'property_type',
        'room_type',
        'bed_count',
        'guest_count',
    ]
    return filter in possible_filters
