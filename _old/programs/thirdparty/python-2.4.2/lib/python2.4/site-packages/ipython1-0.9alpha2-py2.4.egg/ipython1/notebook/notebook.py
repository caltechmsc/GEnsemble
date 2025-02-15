# encoding: utf-8
# -*- test-case-name: ipython1.test.test_notebook -*-
"""The main notebook server system
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

import zope.interface as zi
import sqlalchemy as sqla
from twisted.python.failure import Failure
from ipython1.kernel.error import NotFoundError
from ipython1.notebook import models, dbutil, xmlutil


#-------------------------------------------------------------------------------
# Notebook Server
#-------------------------------------------------------------------------------

class INotebookController(zi.Interface):
    """The IPython Notebook Server Interface"""
    
    def connectUser(uname, email):
        """connect, and if necessary create, a user with `uname` and `email`"""
    
    def disconnectUser(userID):
        """disconnect a user by userID"""
    
    def dropUser(userID):
        """Drop a User by userID"""
    
    def addNode(userID, parentID, node, index=None):
        """add a Node to a parent Section, owned by userID"""
    
    def dropNode(userID, nodeID):
        """Drop a Node by nodeID, owned by userID"""
    
    def getNode(userID, **selectflags):
        """get Node(s) by flags passed to selectone_by, 
        with at least read permissions for userID"""
    
    def editNode(userID, nodeID, **options):
        """update attributes of node nodeID with keyword options"""
    
    def moveNode(userID, nodeID, newParentID, index=None):
        """move a node to new parent at index"""
    
    def execute(userID, nodeID):
        """executes the input of an IO cell, updating the output on completion"""
        
    def addNotebook(userID, title):
        """create a notebook and root Section for `user` with `title`"""
    
    def dropNotebook(userID, nbID):
        """drop a notebook by ID"""
    
    def getNotebook(userID, **selectflags):
        """get Notebook(s) by flags, owned"""
    
    def addWriter(userID, nbID, writerID):
        """adds write permissions on a notebook for a user"""
    
    def dropWriter(userID, nbID, writerID):
        """removes write permissions on a notebook for a user"""
    
    def addReader(userID, nbID, readerID):
        """adds read permissions on a notebook for a user"""
    
    def dropReader(userID, nbID, readerID):
        """removes read permissions on a notebook for a user"""
    
    def addTag(userID, nodeID, tag):
        """add a tag to a node by ID"""
    
    def dropTag(userID, nodeID, tag):
        """drop a tag from a node by ID"""
    
    def loadNotebookFromXML(xmlstr):
        """load a notebook from an xmlstring"""
    
    

class NotebookController(object):
    """The basic IPython Notebook Server object"""
    zi.implements(INotebookController)
    
    def __init__(self, engine=None, session=None):
        if session is None:
            session = sqla.create_session()
        self.session = session
        self.engine = engine
        self.userQuery = session.query(models.User)
        self.nodeQuery = session.query(models.Node)
        self.nbQuery = session.query(models.Notebook)
        self.users = []
    
    # utility functions
    
    def checkUser(self, userID):
        assert userID in self.users, "You are not an active user!"
        return self.userQuery.selectone_by(userID=userID)
    
    def checkNode(self, user, nodeID):
        node = self.nodeQuery.selectone_by(nodeID=nodeID)
        assert user in node.notebook.writers or user is node.notebook.user,\
            "you do not have write permissions on this Notebook"
        return node
    
    def checkNotebook(self, user, notebookID):
        nb = self.nbQuery.selectone_by(notebookID=notebookID)
        assert user is nb.user, "this is not your Notebook"
        return nb
    
    # user functions
    
    def connectUser(self, usernameOrID, email=None):
        try:
            if email is None:
                if isinstance(usernameOrID, str):
                    user = self.userQuery.selectone_by(username=usernameOrID)
                elif isinstance(usernameOrID, int):
                    user = self.userQuery.selectone_by(userID=usernameOrID)
            else:
                user = self.userQuery.selectone_by(username=usernameOrID, email=email)
        except sqla.exceptions.InvalidRequestError:
            assert email is not None, "need to specify email to create new user"
            user = dbutil.createUser(self.session, usernameOrID, email)
        # assert user.userID not in self.users, "User already connected"
        self.users.append(user.userID)
        return user
    
    def disconnectUser(self, userID):
        self.users.remove(userID)
    
    def dropUser(self, userID):
        assert userID not in self.users, "You cannot drop an active user!"
        user = self.userQuery.selectone_by(userID=userID)
        dbutil.dropObject(self.session, user)
    
    def mergeUsers(self, userIDa, userIDb):
        assert userIDb not in self.users, "You cannot drop an active user!"
        userB = self.userQuery.selectone_by(userID=userIDb)
        userA = self.userQuery.selectone_by(userID=userIDa)
        while userB.notebooks:
            nb = userB.notebooks.pop()
            nb.user = userA
            nb.touchModified()
        self.dropUser(userIDb)
        return userA
    
    # Node functions
    
    def getNode(self, userID, **selectflags):
        user = self.checkUser(userID)
        nodes = []
        for node in self.nodeQuery.select_by(**selectflags):
            if user in node.notebook.writers or user in node.notebook.readers\
                or user is node.notebook.user:
                nodes.append(node)
        return nodes
    
    def addNode(self, userID, parentID, node, index=None):
        """add a node to user's Section with nodeID `parentID`.  Index
        can be None or int.
        """
        user = self.checkUser(userID)
        try:
            parent = self.nodeQuery.selectone_by(nodeID=parentID, nodeType='section')
        except sqla.exceptions.InvalidRequestError:
            raise NotFoundError("No such Section, nodeID:%i"%(parentID))
        assert user in parent.notebook.writers or user is parent.notebook.user,\
            "you do not have write permissions on this Notebook"
        n = parent.addChild(node, index)
        self.session.flush()
        return n
    
    def editNode(self, userID, nodeID, **options):
        user = self.checkUser(userID)
        node = self.checkNode(user, nodeID)
        
        for k,v in options.iteritems():
            assert hasattr(node, k), "no such attr '%s' to edit"%k
            if k in ['parentID', 'nextID', 'previousID']:
                assert v is None or self.nodeQuery.select_by(nodeID=v)
            elif k == 'userID':
                assert v is None or self.userQuery.select_by(userID=v)
            setattr(node,k,v)
        node.touchModified()
        self.session.flush()
        # print node
        return node
    
    def moveNode(self, userID, nodeID, newParentID, newIndex=None):
        """move a node to newParent, at newIndex"""
        user = self.checkUser(userID)
        node = self.checkNode(user, nodeID)
        parent = self.checkNode(user, newParentID)
        assert isinstance(parent, models.Section), "parent must be Section"
        
        nb = node.notebook
        isroot = nb.root is node
        if not isroot:# have parent, update head/tail links
            if node.parent.head is node:
                node.parent.head = node.next
            if node.parent.tail is node:
                node.parent.tail = node.previous
            self.session.flush()
            # self.session.refresh(node.parent)
        # update next/previous links
        p = node.previous
        n = node.next
        if p is not None:
            p.next = None
            self.session.flush()
            p.next = n
        elif n is not None:
            n.previous = None
        node.next = node.previous = None
        self.session.flush()
        n = self.addNode(userID, newParentID, node, newIndex)
        self.session.refresh(nb)
        if isroot:# check this
            dbutil.dropObject(self.session, nb)
        return n
    
    def dropNode(self, userID, nodeID):
        user = self.checkUser(userID)
        node = self.checkNode(user, nodeID)
        dbutil.dropObject(self.session, node)
    
    def _updateOutput(self, result, node):
        if isinstance(result, Failure):
            result = result.getTraceback()
        else:
            result = result.get("stdout","")
        node.output = result
        print result
        return result
        
    def execute(self, userID, nodeID):
        user = self.checkUser(userID)
        assert self.engine is not None, "No engine to execute"
        node = self.checkNode(user, nodeID)
        assert isinstance(node, models.InputCell), "Only Execute IO Cells"
        d = self.engine.execute(node.input)
        d.addBoth(self._updateOutput, node)
        return d
        
    # notebook functions
    
    def addNotebook(self, userID, title):
        user = self.checkUser(userID)
        return dbutil.createNotebook(self.session, user, title)
    
    def dropNotebook(self, userID, nbID):
        user = self.checkUser(userID)
        nb = self.checkNotebook(user, nbID)
        dbutil.dropObject(self.session, nb)
    
    def getNotebook(self, userID, **selectFlags):
        user = self.checkUser(userID)
        nbs = self.nbQuery.select_by(**selectFlags)
        return [nb for nb in nbs if user is nb.user or user in nb.writers\
                or user in nb.readers]
    
    def addWriter(self, userID, nbID, writerID):
        """adds write permissions on a notebook for a user"""
        assert writerID != userID, "cannot have self as a writer"
        user = self.checkUser(userID)
        nb = self.checkNotebook(user, nbID)
        writer = self.userQuery.selectone_by(userID=writerID)
        if writer not in nb.writers:
            nb.writers.append(writer)
        if writer in nb.readers:
            nb.readers.remove(writer)
        self.session.flush()
    
    def dropWriter(self, userID, nbID, writerID):
        """removes write permissions on a notebook for a user"""
        assert writerID != userID, "cannot have self as a writer"
        user = self.checkUser(userID)
        nb = self.checkNotebook(user, nbID)
        writer = self.userQuery.selectone_by(userID=writerID)
        if writer in nb.writers:
            nb.writers.remove(writer)
        self.session.flush()
    
    def addReader(self, userID, nbID, readerID):
        """adds read permissions on a notebook for a user"""
        assert readerID != userID, "cannot have self as a reader"
        user = self.checkUser(userID)
        nb = self.checkNotebook(user, nbID)
        reader = self.userQuery.selectone_by(userID=readerID)
        if reader not in nb.readers:
            nb.readers.append(reader)
        if reader in nb.writers:
            nb.writers.remove(reader)
        self.session.flush()
    
    def dropReader(self, userID, nbID, readerID):
        """removes read permissions on a notebook for a user"""
        assert readerID != userID, "cannot have self as a reader"
        user = self.checkUser(userID)
        nb = self.checkNotebook(user, nbID)
        reader = self.userQuery.selectone_by(userID=readerID)
        if reader in nb.readers:
            nb.readers.remove(reader)
        self.session.flush()
    
    def addTag(self, userID, nodeID, tag):
        """add a tag to a node by ID"""
        user = self.checkUser(userID)
        node = self.checkNode(user, nodeID)
        return dbutil.addTag(self.session, node, tag)
    
    def dropTag(self, userID, nodeID, tag):
        """drop a tag from a node by ID"""
        user = self.checkUser(userID)
        node = self.checkNode(user, nodeID)
        dbutil.dropTag(self.session, node, tag)
    
    def loadNotebookFromXML(self, userID, xmlstr, parentID=None):
        user = self.checkUser(userID)
        if parentID is not None:
            parent = self.nodeQuery.selectone_by(userID=userID, nodeID=parentID)
        else:
            parent = None
        sec = xmlutil.loadNotebookFromXML(self.session, user, xmlstr)
        return sec
    

class INotebookUser(zi.Interface):
    
    def getNode(**selectflags):
        """"""
    
    def dropNode(nodeID):
        """"""
    
    def addNode(parentID, node, indices=None):
        """"""
    
    def editNode(nodeID, **options):
        """"""
    
    def moveNode(nodeID, newParentID, index=None):
        """move a node to new parent at index"""
    
    def execute(nodeID):
        """"""
    
    def addNotebook(title):
        """"""
    
    def dropNotebook(nbID):
        """"""
    
    def getNotebook(**selectFlags):
        """"""
    
    def addWriter(nbID, writerID):
        """adds write permissions on a notebook for a user"""
    
    def dropWriter(nbID, writerID):
        """removes write permissions on a notebook for a user"""
    
    def addReader(nbID, readerID):
        """adds read permissions on a notebook for a user"""
    
    def dropReader(nbID, readerID):
        """removes read permissions on a notebook for a user"""
    
    def addTag(nodeID, tag):
        """add a tag to a node by ID"""
    
    def dropTag(nodeID, tag):
        """drop a tag from a node by ID"""
    
    def loadNotebookFromXML(xmlstr, parentID=None):
        """"""
    


class NotebookUser(object):
    """A User connected to the Notebook System"""
    
    def __init__(self, nbcontroller, usernameOrID, email=None):
        self.nbc = nbcontroller
        self.user = self.nbc.connectUser(usernameOrID, email)
    
    def __del__(self):
        try:
            self.disconnect()
        except:
            pass
    
    def disconnect(self):
        self.nbc.disconnectUser(self.user.userID)
    
    def getNode(self, **selectflags):
        return self.nbc.getNode(self.user.userID, **selectflags)
    
    def dropNode(self, nodeID):
        return self.nbc.dropNode(self.user.userID, nodeID)
    
    def addNode(self, parentID, node, index=None):
        return self.nbc.addNode(self.user.userID, parentID, node, index)
    
    def moveNode(self, nodeID, newParentID, index=None):
        return self.nbc.moveNode(self.user.userID, nodeID, newParentID, index)
    
    def editNode(self, nodeID, **options):
        return self.nbc.editNode(self.user.userID, nodeID, **options)
    
    def execute(self, nodeID):
        return self.nbc.execute(self.user.userID, nodeID)
    
    def addNotebook(self, title):
        return self.nbc.addNotebook(self.user.userID, title)
    
    def dropNotebook(self, nbID):
        return self.nbc.dropNotebook(self.user.userID, nbID)
    
    def getNotebook(self, **selectflags):
        return self.nbc.getNotebook(self.user.userID, **selectflags)
    
    def addWriter(self, nbID, writerID):
        return self.nbc.addWriter(self.user.userID, nbID, writerID)
    
    def dropWriter(self, nbID, writerID):
        return self.nbc.dropWriter(self.user.userID, nbID, writerID)
    
    def addReader(self, nbID, readerID):
        return self.nbc.addReader(self.user.userID, nbID, readerID)
    
    def dropReader(self, nbID, readerID):
        return self.nbc.dropReader(self.user.userID, nbID, readerID)
    
    def addTag(self, nodeID, tag):
        return self.nbc.addTag(self.user.userID, nodeID, tag)
    
    def dropTag(self, nodeID, tag):
        return self.nbc.dropTag(self.user.userID, nodeID, tag)
    
    def loadNotebookFromXML(self, xmlstr, parentID=None):
        return self.nbc.loadNotebookFromXML(self.user.userID, xmlstr, parentID)
    

