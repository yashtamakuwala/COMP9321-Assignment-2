from datetime import datetime

class DateConverter:
    def __init__(self, date_string):
        self.date_string = date_string

    def convert(self):
        if self.date_string is None:
            return
    
        dt = datetime.strptime(self.date_string, '%Y-%m-%d')
        return datetime.date(dt)
