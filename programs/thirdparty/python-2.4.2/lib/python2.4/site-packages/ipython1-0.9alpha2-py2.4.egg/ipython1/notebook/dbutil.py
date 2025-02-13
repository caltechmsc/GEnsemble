# encoding: utf-8
# -*- test-case-name: ipython1.test.test_notebook_dbutil -*-
"""The database utils for the notebook system
"""
__docformat__ = "restructuredtext en"
#-------------------------------------------------------------------------------
#       Copyright (C) 2005  Fernando Perez <fperez@colorado.edu>
#                           Brian E Granger <ellisonbg@gmail.com>
#                           Benjamin Ragan-Kelley <benjaminrk@gmail.com>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

import os, sqlalchemy as sqla#, zope.interface as zi

from IPython.genutils import get_home_dir

# from ipython1.config.api import resolveFilePath
from ipython1.kernel.error import DBError
from ipython1.notebook import models
# from ipython1.notebook.xmlutil import loadDBfromXML, dumpDBtoXML
metadata = models.metadata

#-------------------------------------------------------------------------------
# DB Utils
#-------------------------------------------------------------------------------

def connectDB(fname='ipnotebook.db', ipythondir=None):
    """
    BROKEN
    TO BE MOVED TO CONFIG SYSTEM
    
    Connect to aa notebook database, or attempt to create a new one
    if none is found.
    """
    f = resolveFilePath(fname, ipythondir)
    print f
    if f is None:
        print "Could not find DB, attempting to create new DB"
        err = DBError("Could not create DB")
        if ipythondir is not None:
            ipdir = ipythondir
        elif os.environ.get("IPYTHONDIR") is not None:
            ipdir = os.environ.get("IPYTHONDIR")
        else:
            try:
                home = get_home_dir()
                ipdir = home+'/.ipython'
                if not os.path.exists(ipdir):
                    ipdir = home
            except:
                raise err
        q = 'sqlite:///%s'%(ipdir+'/'+fname)
        # print q
        engine = sqla.create_engine(q)
        try:
            engine.connect()
        except sqla.exceptions.DBAPIError:
            raise err
        metadata.connect(engine)
        metadata.create_all()
        return metadata
    else:
        engine = sqla.create_engine('sqlite:///%s'%(f))
        metadata.connect(engine)
        # checkDB(DB)
        return metadata

def initDB(dburi='sqlite://', echo=False, clear=False):
    """create an engine, and connect our metadata object to it.  Then, 
    create our tables in the engine.  
    Defaults to an in-memory sqlite engine."""
    engine = sqla.create_engine(dburi)
    engine.echo=echo
    metadata.connect(engine)
    if clear:
        metadata.drop_all()
    metadata.create_all()
    return metadata

def createUser(session, username, email):
    """create a user with username and email"""
    u = models.User(username, email)
    session.save(u)
    session.flush()
    return u

def dropObject(session, obj):
    """remove any object, and their dependents"""
    if getattr(obj, 'next', None) and getattr(obj, 'previous', None):
        obj.previous.next = obj.next
    session.delete(obj)
    session.flush()
    if isinstance(obj, models.Node):
        for o in map(obj.__getattribute__,['parent','next','previous','notebook']):
            if o is not None:
                session.refresh(o)
    elif isinstance(obj, models.Notebook):
        session.refresh(obj.user)
    
    
def createNotebook(session, user, title):
    """create a root (parentless) Section for `user` with `title
    These objects are the basis for Notebooks.
    """
    root = models.Section()
    root.user = user
    root.title = title
    nb = models.Notebook(user, root)
    root.notebook = nb
    user.touchModified()
    session.save(nb)
    session.flush()
    session.refresh(user)
    return nb


def addTag(session, node, tagName):
    try:
        tag = session.query(models.Tag).selectone_by(name=tagName)
    except:
        tag = models.Tag(tagName)
    if tag not in node.tags:
        node.tags.append(tag)
    session.flush()
    return tag

def dropTag(session, node, tagName):
    tag = session.query(models.Tag).selectone_by(name=tagName)
    node.tags.remove(tag)
    session.flush()
    session.refresh(tag)
    if not tag.providers:
        session.delete(tag)
        session.flush()
    

