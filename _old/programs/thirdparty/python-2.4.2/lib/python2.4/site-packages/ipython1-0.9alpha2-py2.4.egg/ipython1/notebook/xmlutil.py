# encoding: utf-8
# -*- test-case-name: ipython1.test.test_notebook_xmlutil -*-
"""The XML Representation of Notebook components
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

import sqlalchemy as sqla
import StringIO, datetime
try:
    import xml.etree.ElementTree as ET
except ImportError:
    import elementree.ElementTree as ET

from twisted.python import components

from ipython1.notebook import models
from ipython1.notebook.dbutil import addTag

tformat = models.tformat
#-------------------------------------------------------------------------------
# Export a Notebook to XML
#-------------------------------------------------------------------------------
def unescape(s):
    if s is None:
        return ""
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&amp;", "&")

def unindent(s, n):
    return s.replace('\n'+' '*n,'\n')

def dumpDBtoXML(session=None, fname=None):
    """Build an XML String"""
    if session is None:
        session = sqla.create_session()
    users = session.query(models.User).select()
    s = "<XMLBackup>\n"
    for u in users:
        s += models.indent(u.xmlize(justme=False),2)
    s += "</XMLBackup>\n"
    
    if fname is not None:
        f = open(fname, 'w')
        f.write(s)
        f.close()
    # else:
    return s

#-------------------------------------------------------------------------------
# Notebook object from XML strings
#-------------------------------------------------------------------------------

def initFromE(Klass, element):
    c = Klass()
    try:
        c.dateCreated = datetime.datetime.strptime(element.find('dateCreated').text, tformat)
    except AttributeError:
        c.dateCreated = datetime.datetime.now()
    try:
        c.dateModified = datetime.datetime.strptime(element.find('dateModified').text, tformat)
    except AttributeError:
        c.dateCreated = datetime.datetime.now()
    return c
    
def userFromElement(session, ue, nodes={}):
    username = unescape(ue.find('username').text)
    email = unescape(ue.find('email').text)
    try: # get from db
        user = session.query(models.User).selectone_by(username=username, email=email)
    except: # user does not exist, so add to db
        user = initFromE(models.User, ue)
        user.username = username
        user.email = email
        session.save(user)
        session.flush()
    justme = bool(ue.find('justme').text)
    if not justme:
        for nbe in ue.find('Notebooks').findall('Notebook'):
            nb = notebookFromElement(nbe, user, nodes)
    return user
        
    
def anyNodeFromElement(element, user, notebook, parent, nodes={}):
    """switcher function"""
    if element.tag == 'Section':
        cell = sectionFromElement(element, user, notebook, parent, nodes)
    elif element.tag == 'TextCell':
        cell = textCellFromElement(element, user, notebook, parent, nodes)
    elif element.tag == 'InputCell':
        cell = inputCellFromElement(element, user, notebook, parent, nodes)
    else:
        raise Exception("We have no way to handle: %s"%element.tag)
    return cell

def initNodeFromE(Klass, element, user, notebook, parent, nodes):
    node = initFromE(Klass, element)
    s = unescape(element.find('comment').text)
    node.comment = unindent(s, element.text.count(' '))
    for idname in ['nextID', 'previousID']:
        s = element.find(idname).text
        if s:
            value = int(s)
        else:
            value = None
        setattr(node, idname, value)
    node.user = user
    node.parent = parent
    node.notebook = notebook
    nodeID = int(element.find('nodeID').text)
    nodes[nodeID] = node
    tage = element.find('tags')
    if tage.text:
        nodes[nodeID].temptags = element.find('tags').text.split(',')
    else:
        nodes[nodeID].temptags = []
    # check for existing node, if updating
    return node

def textCellFromElement(element, user, notebook, parent, nodes):
    cell = initNodeFromE(models.TextCell, element, user, notebook, parent, nodes)
    s = unescape(element.find('textData').text)
    cell.textData = unindent(s, element.text.count(' '))
    s = unescape(element.find('format').text)
    cell.format = unindent(s, element.text.count(' '))
    return cell

def inputCellFromElement(element, user, notebook, parent, nodes):
    cell = initNodeFromE(models.InputCell, element, user, notebook, parent, nodes)
    s = unescape(element.find('input').text)
    cell.input = unindent(s, element.text.count(' '))
    s = unescape(element.find('output').text)
    cell.output = unindent(s, element.text.count(' '))
    return cell

def sectionFromElement(element, user, notebook, parent, nodes):
    sec = initNodeFromE(models.Section, element, user, notebook, parent, nodes)
    s = unescape(element.find('title').text)
    sec.title = unindent(s, element.text.count(' '))
    for idname in ['headID', 'tailID']:
        s = element.find(idname).text
        if s:
            value = int(s)
        else:
            value = None
        setattr(sec, idname, value)
    kide = element.find('children')
    justme = bool(element.find('justme').text)
    if not justme:
        kids = kide.findall('Section')+kide.findall('InputCell')+\
                        kide.findall('TextCell')
        for e in kids:
            anyNodeFromElement(e, user, notebook, sec, nodes)
    return sec

def notebookFromElement(element, user, nodes):
    nb = initFromE(models.Notebook, element)
    nb.user = user
    rootE = element.find("root").find("Section")
    nb.root = sectionFromElement(rootE, user, nb, None, nodes)
    return nb

def relinkNodes(session, nodes):
    for node in nodes.values(): # correct node ID values
        for key in ['next', 'previous']:
            setattr(node, key, nodes.get(getattr(node, key+"ID")))
        if isinstance(node, models.Section):
            for key in ['head', 'tail']:
                setattr(node, key, nodes.get(getattr(node, key+"ID")))
        for tag in node.temptags:
            addTag(session, node, tag)
        del node.temptags
    return nodes

def loadDBfromXML(session, s, isfilename=False):
    """loads a whole DB Backup from an XML string or file"""
    if isfilename:
        f = open(s)
    else:
        f = StringIO.StringIO(s)
    tree = ET.ElementTree(file=f)
    root = tree.getroot()
    userElements = root.findall('User')
    nodeElements = root.findall('Section')+root.findall('InputCell')+root.findall('TextCell')
    nodes = {}
    users = [userFromElement(session, ue, nodes) for ue in userElements]
    
    f.close()
    
    relinkNodes(session, nodes)
    session.flush()
    for user in users:
        # for nb in user.
        session.refresh(user)
    return users

def loadNotebookFromXML(session, user, s, isfilename=False):
    if isfilename:
        f = open(s)
    else:
        f = StringIO.StringIO(s)
    tree = ET.ElementTree(file=f)
    root = tree.getroot()
    nodes = {}
    nb = notebookFromElement(root, user, nodes)
    f.close()
    relinkNodes(session, nodes)
    # session.save(nb)
    session.flush()
    session.refresh(user)
    return nb

def mergeDB(*dburis):
    """merge databases through XML
    *this should go in dbutil, but cannot until it can be done without xml*
    """
    dblist = []
    for name in dburis:
        if '://' not in name:# guess it is just a filename, use sqlite
            name = 'sqlite:///'+name
        dblist.append(name)
    targetURI = dblist.pop(0)
    if targetURI == 'sqlite://':
        dbutil.initDB(targetURI)
    while dblist:
        engine = sqla.create_engine(dblist.pop(0))
        models.metadata.connect(engine)
        s = dumpDBtoXML()
        
        session = sqla.create_session()
        engine = sqla.create_engine(targetURI)
        models.metadata.connect(engine)

        loadDBfromXML(session, s)

