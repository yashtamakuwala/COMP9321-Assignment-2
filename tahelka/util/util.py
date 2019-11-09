# Checks if all fields have values, True when all are None
def areFieldsEmpty(*argv):
    if all(p is None for p in argv):
        return True