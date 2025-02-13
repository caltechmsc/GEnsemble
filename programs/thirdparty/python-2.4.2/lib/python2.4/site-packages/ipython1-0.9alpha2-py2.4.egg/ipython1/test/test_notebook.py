# encoding: utf-8
"""
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

from random import randint
from twisted.trial import unittest

from ipython1.kernel.error import NotFoundError

try:# check our dependency
    import sqlalchemy as sqla
    from ipython1.notebook import notebook, dbutil, xmlutil
    from ipython1.notebook.models import TextCell, InputCell, Section, Node, Tag
except ImportError:
    sqla = None
else:
    engine = sqla.create_engine("sqlite:///")

if sqla:
    class NotebookTestCase(unittest.TestCase):
            
        def setUp(self):
            dbutil.initDB("sqlite:///")
            self.nbc = notebook.NotebookController()
            self.u = notebook.NotebookUser(self.nbc, 'userA', 'userA@email')
            self.nb = self.u.addNotebook('title')
    
        def loadNodes(self, n):
            l = []
            for _ in range(n):
                sections = self.nbc.nodeQuery.select_by(nodeType='section')
                parent = (sections + [None])[randint(0, len(sections))]
                if parent is None:
                    l.append(self.u.addNotebook("title"))
                else:
                    i = randint(1,3)
                    if i == 1:
                        c = TextCell()
                    elif i == 2:
                        c = InputCell()
                    else:
                        c = Section()
                    index = None
                    if parent.children:
                        index = randint(0,len(parent.children)-1)
                    l.append(self.u.addNode(parent.nodeID, c, index))
            return l
    
        def testappendNode(self):
            clist = [TextCell(),InputCell(),Section(),TextCell(),InputCell()]
            for c in clist:
                self.u.addNode(self.nb.root.nodeID, c)
            self.assertEquals(clist, self.nb.root.children)
    
        def testprependNode(self):
            clist = [TextCell(),InputCell(),Section(),TextCell(),InputCell()]
            for c in clist:
                self.u.addNode(self.nb.root.nodeID, c, 0)
            clist.reverse()
            self.assertEquals(clist, self.nb.root.children)
    
        def testinsertNode(self):
            clist = [TextCell(),InputCell(),Section(),TextCell(),InputCell()]
            for c in clist:
                self.u.addNode(self.nb.root.nodeID, c, 1)
            clist = clist[:1]+clist[-1:-5:-1]
            self.assertEquals(clist, self.nb.root.children)
    
        def testdropNode(self):
            c = TextCell()
            self.u.addNode(self.nb.root.nodeID, c)
            self.assertEquals(self.u.user.nodes,[self.nb.root, c])
            self.u.dropNode(c.nodeID)
            self.assertEquals(self.u.user.nodes,[self.nb.root])
            self.assertEquals(self.nb.root.children,[])
    
        def testeditNode(self):
            c = TextCell()
            self.u.addNode(self.nb.root.nodeID, c)
            mod1 = c.dateModified
            self.u.editNode(c.nodeID, comment="some comment")
            self.assertEquals(c.comment,"some comment")
            self.assertNotEquals(c.dateModified, mod1)
    
        def testmultiUser(self):
            self.assertRaises(AssertionError, notebook.NotebookUser, self.nbc, 'userB')
            del self.u
            self.assertEquals(self.nbc.users, [])
            ua = notebook.NotebookUser(self.nbc, 'userA')
            ub = notebook.NotebookUser(self.nbc, 'userB', 'b@email')
            self.assertEquals(self.nbc.users, [ua.user.userID, ub.user.userID])
            c = TextCell()
            self.assertRaises(AssertionError, ub.addNode, self.nb.root.nodeID, c)
            self.assertRaises(NotFoundError, ub.addNode, 73, c)
            nb = ub.addNotebook('title')
            ub.addNode(nb.root.nodeID, c)
            c2 = InputCell()
            self.assertRaises(NotFoundError, ub.addNode, c.nodeID, c2)
    
        def testmergeUsers(self):
            ub = notebook.NotebookUser(self.nbc, 'userB', 'b@email')
            self.loadNodes(4)
            books = self.u.user.notebooks
            uid = self.u.user.userID
            self.assertRaises(AssertionError, self.nbc.mergeUsers, ub.user.userID, uid)
            del self.u
            self.nbc.mergeUsers(ub.user.userID, uid)
            for nb in books:
                self.assertIdentical(nb.user, ub.user)
    
        def testmoveNode(self):
            clist = [TextCell(),InputCell(),Section(),TextCell(),InputCell()]
            for c in clist:
                self.u.addNode(self.nb.root.nodeID, c)
            nb = self.u.addNotebook('title')
            root = self.nb.root
            self.u.moveNode(root.nodeID, nb.root.nodeID)
            self.assertEquals(self.u.user.notebooks, [nb])
            self.assertEquals(nb.root.children, [root])
            kids = root.children
            c1 = root[1]
            c = c1.previous
            self.u.moveNode(c1.nodeID, nb.root.nodeID,0)
            self.assertEquals(nb.root.children, [c1,root])
            self.assertEquals(root.children, kids[:1]+kids[2:])
        
            c0 = root[0]
            if c0.nextID is None:
                print 'anomalous next/nextID disagreement',
                n = c0.next
                c0.next = None
                c0.next = n
                self.nbc.session.flush()
            self.u.moveNode(c0.nodeID, nb.root.nodeID,1)
            self.assertEquals(nb.root.children, [c1, c0, root])
            self.assertEquals(root.children, kids[2:])
        
            c2 = root[-1]
            self.u.moveNode(c2.nodeID, nb.root.nodeID,1)
            self.assertEquals(nb.root.children, [c1, c2, c0, root])
            self.assertEquals(root.children, kids[2:-1])
            self.assertIdentical(root.head, kids[2])
            self.assertIdentical(root.tail, kids[-2])
    
        def testxmlBackup(self):
            session = self.nbc.session
            self.loadNodes(8)
            s = xmlutil.dumpDBtoXML(self.nbc.session)
            u = self.u
            nodes = session.query(Node).select()
            kidl = [len(nb.root.children) for nb in u.user.notebooks]
            kidl.sort()
            before = [
            len(session.query(Section).select()),
            len(session.query(InputCell).select()),
            len(session.query(TextCell).select()),
            len([n for n in nodes if n.parentID]),
            len([n for n in nodes if n.parent]),
            len([n for n in nodes if n.nextID]),
            len([n for n in nodes if n.next]),
            len([n for n in nodes if n.previousID]),
            len([n for n in nodes if n.previous]),
            len(nodes),
            kidl,
            s.count("Section"), s.count("InputCell"), s.count("TextCell"),
            s.count("<"), s.count(">"), s.count("comment"),
            ]
            dbutil.initDB("sqlite:///")
            nbc = notebook.NotebookController()
            session = nbc.session
            xmlutil.loadDBfromXML(session, s)
            u = notebook.NotebookUser(nbc, "userA")
            kidl = [len(nb.root.children) for nb in u.user.notebooks]
            kidl.sort()
            s2 = xmlutil.dumpDBtoXML(session)
            after = [
            len(session.query(Section).select()),
            len(session.query(InputCell).select()),
            len(session.query(TextCell).select()),
            len([n for n in nodes if n.parentID]),
            len([n for n in nodes if n.parent]),
            len([n for n in nodes if n.nextID]),
            len([n for n in nodes if n.next]),
            len([n for n in nodes if n.previousID]),
            len([n for n in nodes if n.previous]),
            len(nodes),
            kidl,
            s2.count("Section"), s2.count("InputCell"), s2.count("TextCell"),
            s2.count("<"), s2.count(">"), s2.count("comment"),
            ]
            for b,a in zip(before, after):
                self.assertEquals(b,a)
            err = (len(s)-len(s2))/(1.0*len(s))
            self.assertAlmostEquals(err, 0, 2)
    
        def testnidAgreement(self):
            self.loadNodes(16)
            for n in self.u.user.nodes:
                if n.next is None:
                    self.assertIdentical(n.nextID,None)
                else:
                    self.assertEquals(n.next.nodeID,n.nextID)
                if n.previous is None:
                    self.assertIdentical(n.previousID,None)
                else:
                    self.assertEquals(n.previous.nodeID,n.previousID)
                if n.parent is None:
                    self.assertIdentical(n.parentID,None)
                else:
                    self.assertEquals(n.parent.nodeID,n.parentID)
    
        def testTags(self):
            self.loadNodes(5)
            tags = ["tag%i"%i for i in range(6)]
            for n in self.u.user.nodes:
                self.u.addTag(n.nodeID, tags[5])
            for i in range(5):
                self.u.addTag(self.u.user.nodes[i].nodeID, tags[i])
            taglist = self.nbc.session.query(Tag).select()
            self.assertEquals(len(taglist), 6, "incorrect number of tags exist")
    
else:
    class MissingSQLAlchemy(unittest.TestCase):
        def testSkipNBTests(self):
            pass