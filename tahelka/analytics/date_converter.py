from datetime import datetime
from werkzeug.exceptions import BadRequest

class DateConverter:
    def __init__(self, date_string):
        self.date_string = date_string

    def convert(self):
        if self.date_string is None:
            return

        try:
            dt = datetime.strptime(self.date_string, '%Y-%m-%d')
        except(ValueError):
            raise BadRequest

        return datetime.date(dt)
