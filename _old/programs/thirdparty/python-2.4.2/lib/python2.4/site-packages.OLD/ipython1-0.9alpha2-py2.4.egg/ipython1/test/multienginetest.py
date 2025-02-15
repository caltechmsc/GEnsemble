# encoding: utf-8
""""""
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

from twisted.internet import defer

from ipython1.kernel import engineservice as es
from ipython1.kernel.multiengine import IEngineMultiplexer, IEngineCoordinator 
from ipython1.kernel import newserialized
from ipython1.kernel.error import NotDefined
from ipython1.test import util
from ipython1.kernel import newserialized
from ipython1.kernel.error import InvalidEngineID, NoEnginesRegistered

resultKeys = ('id', 'commandIndex', 'stdin', 'stdout', 'stderr')

class IMultiEngineBaseTestCase(object):
    """Basic utilities for working with multiengine tests.
    
    Some subclass should define:
    
    * self.multiengine
    * self.engines to keep track of engines for clean up"""

    def addEngine(self, n=1):
        for i in range(n):
            e = es.EngineService()
            e.startService()
            regDict = self.multiengine.registerEngine(es.QueuedEngine(e), None)
            e.id = regDict['id']
            self.engines.append(e)


class IEngineMultiplexerTestCase(IMultiEngineBaseTestCase):
    """A test for any object that implements IEngineMultiplexer.
    
    self.multiengine must be defined and implement IEngineMultiplexer.
    """
    
    def testIEngineMultiplexerInterface(self):
        """Does self.engine claim to implement IEngineCore?"""
        self.assert_(IEngineMultiplexer.providedBy(self.multiengine))
        
    def testIEngineMultiplexerInterfaceMethods(self):
        """Does self.engine have the methods and attributes in IEngireCore."""
        for m in list(IEngineMultiplexer):
            self.assert_(hasattr(self.multiengine, m))
    
    def testIEngineMultiplexerDeferreds(self):
        self.addEngine(1)
        
        l = [
        self.multiengine.execute(0, 'a=5'),
        self.multiengine.push(0, a=5),
        self.multiengine.push(0, a=5, b='asdf', c=[1,2,3]),
        self.multiengine.pull(0, 'a', 'b', 'c'),
        self.multiengine.getResult(0),
        self.multiengine.reset(0),
        self.multiengine.keys(0),
        self.multiengine.pushSerialized(0, a=newserialized.serialize(10)),
        self.multiengine.pullSerialized(0, 'a'),
        self.multiengine.clearQueue(0),
        self.multiengine.queueStatus(0),
        ]
        for d in l:
            self.assert_(isinstance(d, defer.Deferred))
        return defer.DeferredList(l, consumeErrors=1)
    
    def testInvalidEngineID(self):
         self.addEngine(1)
         badID = 100
         d = self.multiengine.execute(badID, 'a=5')
         d.addErrback(lambda f: self.assertRaises(InvalidEngineID, f.raiseException))
         d.addCallback(lambda _: self.multiengine.push(badID, a=5))
         d.addErrback(lambda f: self.assertRaises(InvalidEngineID, f.raiseException))
         d.addCallback(lambda _: self.multiengine.pull(badID, 'a'))     
         d.addErrback(lambda f: self.assertRaises(InvalidEngineID, f.raiseException))
         d.addCallback(lambda _: self.multiengine.getResult(badID))   
         d.addErrback(lambda f: self.assertRaises(InvalidEngineID, f.raiseException))
         d.addCallback(lambda _: self.multiengine.reset(badID))     
         d.addErrback(lambda f: self.assertRaises(InvalidEngineID, f.raiseException))   
         d.addCallback(lambda _: self.multiengine.keys(badID))     
         d.addErrback(lambda f: self.assertRaises(InvalidEngineID, f.raiseException))
         d.addCallback(lambda _: self.multiengine.pushSerialized(badID, a=newserialized.serialize(10)))
         d.addErrback(lambda f: self.assertRaises(InvalidEngineID, f.raiseException))
         d.addCallback(lambda _: self.multiengine.pullSerialized(badID, 'a'))
         d.addErrback(lambda f: self.assertRaises(InvalidEngineID, f.raiseException))
         d.addCallback(lambda _: self.multiengine.queueStatus(badID))
         d.addErrback(lambda f: self.assertRaises(InvalidEngineID, f.raiseException))
         return d
    
    def testNoEnginesRegistered(self):
        badID = 'all'
        d = self.multiengine.execute(badID, 'a=5')
        d.addErrback(lambda f: self.assertRaises(NoEnginesRegistered, f.raiseException))
        d.addCallback(lambda _: self.multiengine.push(badID, a=5))
        d.addErrback(lambda f: self.assertRaises(NoEnginesRegistered, f.raiseException))
        d.addCallback(lambda _: self.multiengine.pull(badID, 'a'))     
        d.addErrback(lambda f: self.assertRaises(NoEnginesRegistered, f.raiseException))
        d.addCallback(lambda _: self.multiengine.getResult(badID))   
        d.addErrback(lambda f: self.assertRaises(NoEnginesRegistered, f.raiseException))
        d.addCallback(lambda _: self.multiengine.reset(badID))     
        d.addErrback(lambda f: self.assertRaises(NoEnginesRegistered, f.raiseException))   
        d.addCallback(lambda _: self.multiengine.keys(badID))     
        d.addErrback(lambda f: self.assertRaises(NoEnginesRegistered, f.raiseException))
        d.addCallback(lambda _: self.multiengine.pushSerialized(badID, a=newserialized.serialize(10)))
        d.addErrback(lambda f: self.assertRaises(NoEnginesRegistered, f.raiseException))
        d.addCallback(lambda _: self.multiengine.pullSerialized(badID, 'a'))
        d.addErrback(lambda f: self.assertRaises(NoEnginesRegistered, f.raiseException))
        d.addCallback(lambda _: self.multiengine.queueStatus(badID))
        d.addErrback(lambda f: self.assertRaises(NoEnginesRegistered, f.raiseException))
        return d        
    
    def testExecute(self):
        self.addEngine(6)
        commands = [(0, 0,"a = 5","",""),
            (0, 1,"b = 10","",""),
            (0, 2,"c = a + b","",""),
            (0, 3,"print c","15\n",""),
            (0, 4,"import math","",""),
            (0, 5,"2.0*math.pi","6.2831853071795862\n","")]
        d = defer.succeed(None)
        for c in commands:
            result = self.multiengine.execute(0, c[2])
            d = self.assertDeferredEquals(result, [dict(zip(resultKeys, c))], d)
        return d
    
    def testExecuteFailures(self):
        self.addEngine(4)
        d = self.multiengine.execute(0,'a=1/0')
        d.addErrback(lambda f: self.assertRaises(ZeroDivisionError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.execute(0,'print v'))
        d.addErrback(lambda f: self.assertRaises(NameError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.execute(0,'a = 2**1000000'))
        d.addErrback(lambda f: self.assertRaises(OverflowError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.execute(0,'l=[];l[0]'))
        d.addErrback(lambda f: self.assertRaises(IndexError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.execute(0,"d={};d['a']"))
        d.addErrback(lambda f: self.assertRaises(KeyError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.execute(0,"assert 1==0"))
        d.addErrback(lambda f: self.assertRaises(AssertionError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.execute(0,"import abababsdbfsbaljasdlja"))
        d.addErrback(lambda f: self.assertRaises(ImportError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.execute(0,"raise Exception()"))
        d.addErrback(lambda f: self.assertRaises(Exception, f.raiseException))
        return d
    
    def testExecuteAll(self):
        self.addEngine(2)
        result = [{'commandIndex': 0, 'stdin': 'a=5', 'id': 0, 'stderr': '', 'stdout': ''},
         {'commandIndex': 0, 'stdin': 'a=5', 'id': 1, 'stderr': '', 'stdout': ''}]
        d = self.multiengine.execute('all', 'a=5')
        d.addCallback(lambda r: self.assert_(r==result))
        d.addCallback(lambda _: self.multiengine.execute(0, 'a=10'))
        d.addCallback(lambda _: self.multiengine.execute(1, 'a=5'))
        d.addCallback(lambda _: self.multiengine.pull([0,1],'a'))
        d.addCallback(lambda r: self.assert_(r==[10,5]))        
        return d
    
    def testExecuteAllFailures(self):
        self.addEngine(4)
        d = self.multiengine.executeAll('a=1/0')
        d.addErrback(lambda f: self.assertRaises(ZeroDivisionError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.executeAll('print v'))
        d.addErrback(lambda f: self.assertRaises(NameError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.executeAll('a = 2**1000000'))
        d.addErrback(lambda f: self.assertRaises(OverflowError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.executeAll('l=[];l[0]'))
        d.addErrback(lambda f: self.assertRaises(IndexError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.executeAll("d={};d['a']"))
        d.addErrback(lambda f: self.assertRaises(KeyError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.executeAll("assert 1==0"))
        d.addErrback(lambda f: self.assertRaises(AssertionError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.executeAll("import abababsdbfsbaljasdlja"))
        d.addErrback(lambda f: self.assertRaises(ImportError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.executeAll("raise Exception()"))
        d.addErrback(lambda f: self.assertRaises(Exception, f.raiseException))
        return d
    
    def testPushPull(self):
        self.addEngine(1)
        objs = [10,"hi there",1.2342354,{"p":(1,2)}]
        d = defer.succeed(None)
        for o in objs:
            d0 = self.multiengine.push(0, key=o)
            value = self.multiengine.pull(0, 'key')
            d = self.assertDeferredEquals(value, [o] , d)
        self.multiengine.reset(0)
        d1 = self.multiengine.pull(0, "a")
        d1.addErrback(lambda f: self.assertRaises(NameError, f.raiseException))
        return defer.DeferredList([d, d0, d1])
    
    def testPushPullAll(self):
        self.addEngine(4)
        d = self.multiengine.pushAll(a=10)
        d.addCallback(lambda _: self.multiengine.pullAll('a'))
        d.addCallback(lambda r: self.assert_(r==[10,10,10,10]))
        d.addCallback(lambda _: self.multiengine.pushAll(a=10, b=20))
        d.addCallback(lambda _: self.multiengine.pullAll('a','b'))
        d.addCallback(lambda r: self.assert_(r==4*[[10,20]]))
        d.addCallback(lambda _: self.multiengine.push(0, a=10, b=20))
        d.addCallback(lambda _: self.multiengine.pull(0,'a','b'))  
        d.addCallback(lambda r: self.assert_(r==[[10,20]]))
        d.addCallback(lambda _: self.multiengine.push(0, a=None, b=None))
        d.addCallback(lambda _: self.multiengine.pull(0, 'a','b'))  
        d.addCallback(lambda r: self.assert_(r==[[None,None]]))
        return d
    
    def testPushPullSerialized(self):
        self.addEngine(1)
        objs = [10,"hi there",1.2342354,{"p":(1,2)}]
        d = defer.succeed(None)
        for o in objs:
            self.multiengine.pushSerialized(0, key=newserialized.serialize(o))
            value = self.multiengine.pullSerialized(0, 'key')
            value.addCallback(lambda serial: newserialized.IUnSerialized(serial[0]).getObject())
            d = self.assertDeferredEquals(value,o,d)
        return d
    
    def testResult(self):
        self.addEngine(1)
        d = self.multiengine.getResult(0)
        d.addCallback(lambda r: r[0])
        d = self.assertDeferredRaises(d, IndexError)
        d.addCallback(lambda _:self.multiengine.execute(0, "a = 5"))
        d.addCallback(lambda _:self.multiengine.getResult(0))
        d = self.assertDeferredEquals(d,[dict(zip(resultKeys, (0, 0,"a = 5","","")))])
        d.addCallback(lambda _:self.multiengine.getResult(0, 0))
        d = self.assertDeferredEquals(d,[dict(zip(resultKeys, (0, 0,"a = 5","","")))])
        d.addCallback(lambda _:self.multiengine.reset(0))
        return d
    
    
class IEngineCoordinatorTestCase(IMultiEngineBaseTestCase):
    """A test for any object that implements IEngineCoordinator.
    
    self.multiengine must be defined and implement IEngineCoordinator.
    self.engine must be a list of engines.
    """
    
    def testIEngineCoordinatorInterface(self):
        """Does self.engine claim to implement IEngineCore?"""
        self.assert_(IEngineCoordinator.providedBy(self.multiengine))
        
    def testIEngineCoordinatorInterfaceMethods(self):
        """Does self.engine have the methods and attributes in IEngireCore."""
        for m in list(IEngineCoordinator):
            self.assert_(hasattr(self.multiengine, m))
    
    def testIEngineCoordinatorDeferreds(self):
        self.addEngine(1)
        l = [
        self.multiengine.scatterAll('a', range(10)),
        self.multiengine.gatherAll('a')
        ]
        for d in l:
            self.assert_(isinstance(d, defer.Deferred))
        return defer.DeferredList(l)
    
    def testScatterGather(self):
        self.addEngine(8)
        try:
            import numpy
            a = numpy.random.random(100)
            d = self.multiengine.scatterAll('a', a)
            d.addCallback(lambda _: self.multiengine.gatherAll('a'))
            d.addCallback(lambda b: (a==b).all())
            d = self.assertDeferredEquals(d, True)
        except ImportError:
            print "no numpy"
            d = defer.succeed(None)
        l = range(100)
        d.addCallback(lambda _: self.multiengine.scatterAll('l', l))
        d.addCallback(lambda _: self.multiengine.gatherAll('l'))
        return self.assertDeferredEquals(d,l)
    

