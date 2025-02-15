import datetime
from sqlalchemy import *

from ipython1.notebook.models import *

db = create_engine('sqlite:///notebook.db')

metadata.connect(db)

def createTables():
    metadata.create_all()
    
def dropTables():
    metadata.drop_all()

createTables()

# Actually do some transactions

session = create_session()

def createUser(session):
    # Create user
    u = User()
    u.username = 'bgranger'
    u.email = 'ellisonbg@gmail.com'
    session.save(u)
    session.flush()
    return u
    
def createNotebook(session, user):
    nb = Notebook()
    nb.user = user
    session.save(nb)
    session.flush()
    return nb

u = createUser(session)
nb = createNotebook(session, u)
n = Node("Main Title")
nb.root = n
tc = TextCell("This is how to import time:")
tc.parent = n
tc.insertAfter(InputCell('import time'))
tc.next.insertAfter(TextCell("What to do next"))
session.flush()