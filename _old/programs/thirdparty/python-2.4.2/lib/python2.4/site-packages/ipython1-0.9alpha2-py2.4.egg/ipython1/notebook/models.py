# encoding: utf-8
"""The main notebook Classes, serialization, and database system
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
import sqlalchemy
from sqlalchemy import *
import datetime
try:
    import simplejson
except:
    simplejson = None

if not hasattr(MetaData, 'connect'):
    msg = getattr(sqlalchemy, "__version__", "")
    if msg:
        msg = "You are running SQLAlchemy version: %s\n"%msg
    msg += "Need SQLAlchemy version >= 0.3.5, try 'easy_install -U sqlalchemy'\
        or goto http://www.sqlalchemy.org/ for up to date code."
    raise ImportError(msg)

def indent(s, n):
    """indent a multi-line string `s`, `n` spaces"""
    addline = 0
    if s and s[-1] == '\n':
        s = s[:-1]
        addline=1
    s = " "*n+s.replace("\n", "\n"+" "*n)
    return s +'\n'*addline

#-------------------------------------------------------------------------------
# Sparse representations of notebook objects
#-------------------------------------------------------------------------------

def sparseTextCell(cell):
    if '"""\n' in cell.textData and "'''\n" in cell.textData:
        # make a trivial alteration, to prevent misparsing
        s = "'''%s'''\n"%cell.textData.replace("'''\n", "'''\n ")
    elif '"""' in cell.textData:
        s = "'''%s'''\n"%cell.textData
    else:
        s = '"""%s"""\n'%cell.textData
    if cell.comment:
        s += '#' + cell.comment.replace('\n', '\n#') + '\n'
    return s

def sparseInputCell(cell):
    inlines = cell.input.splitlines()
    if inlines:
        s = '>>> '+inlines.pop(0)+'\n'
        while inlines:
            s += '... '+inlines.pop(0)+'\n'
    else:
        s = '>>> \n'
    s += indent(cell.output,4) + '\n'
    if cell.comment:
        s += '#' + cell.comment.replace('\n', '\n#') + '\n'
    return s

def sparseSection(sec):
    s = "# py-section %s\n"%sec.title
    if sec.comment:
        s += '#' + sec.comment.replace('\n', '\n#') + '\n'
    for c in sec.children:
        s += c.sparse()
    return s + "# py-section-end\n"
        
    
def sparseNotebook(nb):
    return nb.root.sparse()


#-------------------------------------------------------------------------------
# XML representations of notebook objects
#-------------------------------------------------------------------------------
def escape(s):
    if s is None:
        return None
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

tformat = "%Y-%m-%d-%H:%M:%S"

def XMLUser(u, justme=False):
    s  = "<userID>%i</userID>\n"%u.userID
    s += "<username>%s</username>\n"%escape(u.username)
    s += "<email>%s</email>\n"%escape(u.email)
    s += "<dateCreated>%s</dateCreated>\n"%(u.dateCreated.strftime(tformat))
    s += "<dateModified>%s</dateModified>\n"%(u.dateModified.strftime(tformat))
    s += "<justme>"+ '1'*justme + "</justme>\n"
    s += "<Notebooks>"
    if justme:
        nbstr = ','.join([str(c.nodeID) for c in u.notebooks])
        s += indent(nb,2)
    else:
        s += '\n'
        for nb in u.notebooks:
            s += indent(nb.xmlize(justme=False), 2)
    s += "</Notebooks>\n"
    s += "<Nodes>"
    nstr = ','.join([str(c.nodeID) for c in u.nodes])
    s += nstr
    s += "</Nodes>\n"
    return "<User>\n%s</User>\n"%indent(s,2)
    
def XMLNodeBase(node, justme):
    """The base of an XML representation of a Node"""
    s  = "<comment>%s</comment>\n"%escape(node.comment)
    for idname in ['nodeID', 'nextID','previousID', 'parentID', 'notebookID']:
        value = getattr(node, idname)
        if value is None:
            s += "<%s></%s>\n"%(idname, idname)
        else:
            s += "<%s>%i</%s>\n"%(idname, value, idname)
    s += "<tags>"
    s += ','.join([tag.name for tag in node.tags])
    s += "</tags>\n"
    s += "<dateCreated>%s</dateCreated>\n"%(node.dateCreated.strftime(tformat))
    s += "<dateModified>%s</dateModified>\n"%(node.dateModified.strftime(tformat))
    return s

def XMLSection(sec, justme=False):
    """Return an XML representation of a Section"""
    s  = XMLNodeBase(sec, justme)
    s += "<justme>"+ '1'*justme + "</justme>\n"
    s += "<title>%s</title>\n"%escape(sec.title)
    for idname in ['headID','tailID']:
        value = getattr(sec, idname)
        if value is None:
            s += "<%s></%s>\n"%(idname, idname)
        else:
            s += "<%s>%i</%s>\n"%(idname, value, idname)
    s += "<children>"
    if justme:
        kids = ','.join([str(sec[i].nodeID) for i in range(len(sec.children))])
        s += kids
    else:
        s += '\n'
        for i in range(len(sec.children)):
            s += indent(sec[i].xmlize(justme), 2)
    s += "</children>\n"
    return "<Section>\n%s</Section>\n"%indent(s,2)

def XMLTextCell(cell, justme=False):
    s  = XMLNodeBase(cell, justme)
    s += "<format>%s</format>\n"%escape(cell.format)
    s += "<textData>%s</textData>\n"%escape(cell.textData)
    return "<TextCell>\n%s</TextCell>\n"%indent(s,2)

def XMLInputCell(cell, justme=False):
    s  = XMLNodeBase(cell, justme)
    s += "<input>%s</input>\n"%escape(cell.input)
    s += "<output>%s</output>\n"%escape(cell.output)
    return "<InputCell>\n%s</InputCell>\n"%indent(s,2)

def XMLNotebook(nb, justme=False):
    s = ""
    for idname in ['notebookID', 'userID']:
        value = getattr(nb, idname)
        if value is None:
            s += "<%s></%s>\n"%(idname, idname)
        else:
            s += "<%s>%i</%s>\n"%(idname, value, idname)
    s += "<dateCreated>%s</dateCreated>\n"%(nb.dateCreated.strftime(tformat))
    s += "<dateModified>%s</dateModified>\n"%(nb.dateModified.strftime(tformat))
    if justme:
        s += "<rootID>%i</rootID>\n"%nb.rootID
    else:
        s += "<root>\n%s</root>\n"%indent(nb.root.xmlize(justme=False),2)
    return "<Notebook>\n%s</Notebook>\n"%indent(s,2)

#-------------------------------------------------------------------------------
# JSON Representations of Notebook Objects
#-------------------------------------------------------------------------------

def jsonStarter(obj):
    d = {}
    d['dateCreated'] = obj.dateCreated.strftime(tformat)
    d['dateModified'] = obj.dateModified.strftime(tformat)
    return d

def jsonifyUser(u, keepdict=False, justme=False):
    d = jsonStarter(u)
    d['userID'] = u.userID
    d['username'] = u.username
    d['email'] = u.email
    if not justme:
        d['notebooks'] = [nb.jsonify(keepdict=True) for nb in u.notebooks]
    else:
        d['notebooks'] = [nb.notebookID for nb in u.notebooks]
    # print d
    if keepdict or simplejson is None:
        return d
    return simplejson.dumps(d)

def jsonifyNode(n, nodeType="node", keepdict=False, justme=False):
    d = jsonStarter(n)
    d['nodeType'] = nodeType
    for key in ['notebookID','nodeID', 'parentID', 'nextID', 'comment']:
        d[key] = getattr(n, key)
    d['tags'] = [t.name for t in n.tags]
    # print d
    if keepdict or simplejson is None:
        return d
    return simplejson.dumps(d)

def jsonifySection(sec, keepdict=False, justme=False):
    d = jsonifyNode(sec,"section",True)
    d['title'] = sec.title
    if justme:
        d['children'] = [sec[i].cellID for i in range(len(sec._children))]
    else:
        d['children'] = [sec[i].jsonify(True,False) for i in range(len(sec._children))]
    # print d
    if keepdict or simplejson is None:
        return d
    return simplejson.dumps(d)

def jsonifyTextCell(tc, keepdict=False, justme=False):
    d = jsonifyNode(tc,"textCell",True)
    d['format'] = tc.format
    d['textData'] = tc.textData
    # print d
    if keepdict or simplejson is None:
        return d
    return simplejson.dumps(d)

def jsonifyInputCell(ic, keepdict=False, justme=False):
    d = jsonifyNode(ic,"inputCell",True)
    d['input'] = ic.input
    d['output'] = ic.output
    # print d
    if keepdict or simplejson is None:
        return d
    return simplejson.dumps(d)

def jsonifyNotebook(nb, keepdict=False, justme=False):
    d = jsonStarter(nb)
    d['notebookID'] = nb.notebookID
    d['userID'] = nb.userID
    # d['rootID'] = nb.root.nodeID
    d['writers'] = [u.userID for u in nb.writers]
    d['readers'] = [u.userID for u in nb.readers]
    d['title'] = nb.root.title
    if not justme:
        d['root'] = nb.root.jsonify(keepdict=True)
    else:
        d['rootID'] = nb.root.nodeID
    # print d
    if keepdict or simplejson is None:
        return d
    return simplejson.dumps(d)

#-------------------------------------------------------------------------------
# SQLAlchemy Tables
#-------------------------------------------------------------------------------

metadata = MetaData()
# Tables

tagsTable = Table('tags', metadata,
    Column('tagID', Integer, primary_key=True),
    Column('name', String(64))
)

tagLinksTable = Table('taglinks', metadata,
    Column('tagID', Integer, ForeignKey('tags.tagID'), primary_key=True),
    Column('nodeID', Integer, ForeignKey('nodes.nodeID'), primary_key=True),
)

nodesTable = Table('nodes', metadata,
    Column('nodeID', Integer, primary_key=True),
    Column('dateCreated', DateTime),
    Column('dateModified', DateTime),
    Column('comment',String()),
    # Column('userID', Integer, ForeignKey('users.userID')),
    Column('notebookID', Integer, ForeignKey('notebooks.notebookID')),
    Column('parentID', Integer, ForeignKey('nodes.nodeID')),
    Column('previousID', Integer, ForeignKey('nodes.nodeID')),
    Column('nextID', Integer, ForeignKey('nodes.nodeID')),
    Column('nodeType', String(32))
    )

sectionsTable = Table('sections', metadata,
    Column('nodeID', Integer, ForeignKey('nodes.nodeID'), primary_key=True),
    Column('headID', Integer, ForeignKey('nodes.nodeID')),
    Column('tailID', Integer, ForeignKey('nodes.nodeID')),
    Column('title',String())
)

inputCellsTable = Table('inputCells', metadata,
    Column('nodeID', Integer, ForeignKey('nodes.nodeID'), primary_key=True),
    Column('input', String()),
    Column('output', String()) 
)

textCellsTable = Table('textCells', metadata,
    Column('nodeID', Integer, ForeignKey('nodes.nodeID'), primary_key=True),
    Column('format', String()),
    Column('textData', String()),
)

usersTable = Table('users', metadata,
    Column('userID', Integer, primary_key=True),
    Column('username', String(64), unique=True),
    Column('email', String(64)),
    Column('dateCreated', DateTime),
    Column('dateModified', DateTime)
)

notebooksTable = Table('notebooks', metadata,
    Column('notebookID', Integer, primary_key=True),
    Column('userID', Integer, ForeignKey('users.userID')),
    Column('dateCreated', DateTime),
    Column('dateModified', DateTime),
    # Column('rootID', Integer, ForeignKey('nodes.nodeID')),
)

writersTable = Table('writers', metadata,
    Column('userID', Integer, ForeignKey('users.userID'), primary_key=True),
    Column('notebookID', Integer, ForeignKey('notebooks.notebookID'), primary_key=True),
)

readersTable = Table('readers', metadata,
    Column('userID', Integer, ForeignKey('users.userID'), primary_key=True),
    Column('notebookID', Integer, ForeignKey('notebooks.notebookID'), primary_key=True),
)

#-------------------------------------------------------------------------------
# SQLAlchemy Mapper Classes
#-------------------------------------------------------------------------------

class Tag(object):
    def __init__(self, name):
        self.name = name

class Created(object):
    def __init__(self):
        self.dateCreated = datetime.datetime.now()

class Modified(object):
    def touchModified(self):
        # return
        """This will touch our dateModified, and also our parent's.  If we do
        not have a parent (i.e., we are a Root), then we touch our User.
        That way, a root's dateModified is as late as the latest in its 
        descendents, and a user's is as late as the latest of its nodes.
        """
        self.dateModified = datetime.datetime.now()
        if getattr(self, 'parent', None) is not None:
            self.parent.touchModified()
        elif getattr(self, 'notebook', None) is not None:
            self.notebook.touchModified()
        elif getattr(self, 'user', None) is not None:
            self.user.touchModified()

class Timestamper(Created, Modified):
    def __init__(self):
        super(Timestamper, self).__init__()
        self.touchModified()

class Node(Timestamper):
    
    def __init__(self, comment='', parent=None):
        super(Node, self).__init__()
        self.comment = comment
        self.parent = parent
    
    def __str__(self):
        d = {}
        for k in ['notebookID','nodeID','previousID','nextID', 'parentID']:
            d[k] = getattr(self, k)
        return "<%s: %s>"%(self.nodeType, d)
    
    def insertBefore(self, c):
        """Insert a cell before this one."""
        assert self.parent is not None, "Cannot insert Before/After root"
        assert c not in self.parent.children, "Already in Children"
        c.parent = self.parent
        c.notebook = self.notebook
        if isinstance(c, Section):# cascade
            for node in c.nodes:
                node.notebook = parent.notebook
        
        c.previous = self.previous
        if c.previous is not None:
            c.previous.next = c
        self.previous = c
        c.next = self

        self.touchModified()
        c.touchModified()
        
    def insertAfter(self, c):
        """Insert a cell after this one."""
        assert self.parent is not None, "Cannot insert Before/After root"
        assert c not in self.parent.children, "Already in Children"
        c.parent = self.parent
        c.notebook = self.notebook
        if isinstance(c, Section):# cascade
            for node in c.nodes:
                node.notebook = parent.notebook
        
        c.next = self.next
        if c.next is not None:
            c.next.previous = c
        self.next = c
        c.previous = self
        
        self.touchModified()
        c.touchModified()
    

class Section(Node):
    
    def _getNodes(self):
        """get all descendents of a Section into a flat list of Nodes."""
        kids = []
        secs = [self]
        while secs:
            sec = secs.pop()
            for kid in sec._children:
                if isinstance(kid, Section):
                    secs.append(kid)
                kids.append(kid)
        return kids
    
    nodes = property(_getNodes)
    
    def __init__(self, title='', comment='', parent=None):
        super(Section, self).__init__(comment, parent)
        self.title = title
    
    def __str__(self):
        d = {}
        for k in ['notebookID','nodeID','previousID','nextID', 'parentID']:
            d[k] = getattr(self, k)
        d['children'] = [c.nodeID for c in self.children]
        return "<%s: %s>"%(self.nodeType, d)
    
    def _getChildren(self):
        return [self[i] for i in range(len(self._children))]
    
    def _setChildren(self, children):
        self._children = children
    
    children = property(_getChildren, _setChildren)
    
    def __getitem__(self, index):
        if index >= 0:
            c = self.head
            for i in range(index):
                c = c.next
            return c
        else:
            c = self.tail
            for i in range(-1-index):
                c = c.previous
            return c

    def addChild(self, child, index=None):
        """Add `child` to Section `parent` at position `index`, 
        defaulting to the end."""

        if self._children: # already have some children
            if index is None or index == len(self._children):
                n = self[-1]
                n.insertAfter(child)
                self.tail = child
            else:
                self[index].insertBefore(child)
                if index == 0:
                    self.head = child
        else: # this is self's first child
            child.parent = self
            # child.user = self.user
            child.notebook = self.notebook
            self.head = self.tail = child
            if isinstance(child, Section):
                for node in child.nodes:
                    node.notebook = self.notebook
        child.touchModified()
        self.touchModified()
        return child
    
    sparse  = sparseSection
    xmlize  = XMLSection
    jsonify = jsonifySection

class Cell(Node):
    pass

class InputCell(Cell):
    
    def __init__(self, input='', output='', comment='', parent=None):
        super(InputCell, self).__init__(comment, parent)
        self.input = input
        self.output = output
    
    sparse  = sparseInputCell
    xmlize  = XMLInputCell
    jsonify = jsonifyInputCell

class TextCell(Cell):
    
    def __init__(self, textData='', comment='', parent=None):
        super(TextCell, self).__init__(comment, parent)
        self.textData = textData
    
    sparse  = sparseTextCell
    xmlize  = XMLTextCell
    jsonify = jsonifyTextCell

class User(Timestamper):
    
    def _getNodes(self):
        nodes = []
        for nb in self.notebooks:
            nodes.extend(nb.nodes)
        return nodes
    
    nodes = property(_getNodes)
    
    def __init__(self, username='', email=''):
        super(User, self).__init__()
        self.username = username
        self.email = email
    
    xmlize = XMLUser
    
    jsonify = jsonifyUser

class Notebook(Timestamper):
    def __init__(self, user=None, root=None):
        super(Notebook, self).__init__()
        self.user = user
        self.root = root
    
    sparse  = sparseNotebook
    xmlize  = XMLNotebook
    jsonify = jsonifyNotebook
        

#-------------------------------------------------------------------------------
# SQLAlchemy Mappers and Joins
#-------------------------------------------------------------------------------


tagMapper = mapper(Tag, tagsTable,
    properties = {
        'providers': relation(Node, secondary=tagLinksTable)
    }
)

nodeJoin = polymorphic_union(
    {
        'inputCell':nodesTable.join(inputCellsTable),
        'textCell':nodesTable.join(textCellsTable),
        'section':nodesTable.join(sectionsTable, sectionsTable.c.nodeID==nodesTable.c.nodeID),
        'node':nodesTable.select(nodesTable.c.nodeType=='node')
    }, None, 'pjoin'
)

nodeMapper = mapper(Node, nodesTable, 
    select_table=nodeJoin, 
    polymorphic_on=nodeJoin.c.nodeType, 
    polymorphic_identity='node',
    properties = {
        'previous': relation(Node,
            primaryjoin=nodesTable.c.previousID==nodesTable.c.nodeID,
            remote_side=[nodesTable.c.nodeID],
            post_update = True,
            uselist=False),
        'next': relation(Node,
                primaryjoin=nodesTable.c.nextID==nodesTable.c.nodeID,
                remote_side=[nodesTable.c.nodeID],
                post_update = True,
                uselist=False),
        'tags': relation(Tag, secondary=tagLinksTable)
    }
)

cellJoin = polymorphic_union(
    {
        'inputCell':nodesTable.join(inputCellsTable),
        'textCell':nodesTable.join(textCellsTable),
        'cell':nodesTable.select(nodesTable.c.nodeType=='cell')
    }, None, 'pjoin'
)

cellMapper = mapper(Cell, nodesTable, 
    select_table=cellJoin, 
    polymorphic_on=cellJoin.c.nodeType, 
    polymorphic_identity='cell',
    inherits=nodeMapper
)

inputCellMapper = mapper(InputCell, inputCellsTable, inherits=cellMapper, polymorphic_identity='inputCell')
textCellMapper = mapper(TextCell, textCellsTable, inherits=cellMapper, polymorphic_identity='textCell')

sectionMapper = mapper(Section, sectionsTable, inherits = nodeMapper, polymorphic_identity='section',
    inherit_condition=sectionsTable.c.nodeID==nodesTable.c.nodeID,
    properties={
        '_children': relation(# an unsorted list, self.children is sorted
            Node,
            primaryjoin=nodesTable.c.parentID==nodesTable.c.nodeID,
            remote_side=[nodesTable.c.parentID],
            cascade='all, delete-orphan',
            backref=backref("parent",
                primaryjoin=nodesTable.c.parentID==nodesTable.c.nodeID,
                remote_side=[nodesTable.c.nodeID],
                uselist=False
                )
            ),
        'head': relation(Node,
            primaryjoin=and_(sectionsTable.c.headID==nodesTable.c.nodeID),
            remote_side=[nodesTable.c.nodeID],
            post_update = True,
            uselist=False),
        'tail': relation(Node,
            primaryjoin=and_(sectionsTable.c.tailID==nodesTable.c.nodeID),
            remote_side=[nodesTable.c.nodeID],
            post_update = True,
            uselist=False),
    }
)

userMapper = mapper(User, usersTable,
    properties={
        'notebooks':relation(Notebook,
        primaryjoin=usersTable.c.userID==notebooksTable.c.userID,
        cascade="all, delete-orphan", backref='user',
        )
    }
)
notebookMapper = mapper(Notebook, notebooksTable,
    properties={
        'root': relation(Section,
                primaryjoin=and_(nodesTable.c.parentID==None,
                    nodesTable.c.notebookID==notebooksTable.c.notebookID),
                uselist=False), 
        'writers': relation(User, secondary=writersTable),
        'readers': relation(User, secondary=readersTable),
        'nodes':relation(Node, 
        primaryjoin=notebooksTable.c.notebookID==nodesTable.c.notebookID,
        cascade="all, delete-orphan", backref='notebook'),
    }
)