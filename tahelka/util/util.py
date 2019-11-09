# Checks if all fields have values, True when all are None
def areFieldsEmpty(*argv):
    params = list()
    for arg in argv:
        params.append(arg)

    if all(p is None for p in params):
        return True