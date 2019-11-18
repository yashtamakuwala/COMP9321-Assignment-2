from sys import argv
import os

# Remove tahelka.db if exists and -d specified
if (len(argv) >= 2 and argv[1] == '-d'):
    if (os.path.isfile('tahelka.db')):
        os.remove('tahelka.db')

import db_setup
import data_setup
