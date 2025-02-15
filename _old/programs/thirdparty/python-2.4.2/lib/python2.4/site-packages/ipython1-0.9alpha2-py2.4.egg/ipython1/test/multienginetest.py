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
from ipython1.test.engineservicetest import validCommands, invalidCommands
from ipython1.test.testgenerator import (MultiEngineExecuteAllTestGenerator,
    MultiEngineFailingExecuteTestGenerator,
    MultiEngineGetResultTestGenerator)
from ipython1.core.interpreter import Interpreter

class IMultiEngineBaseTestCase(object):
    """Basic utilities for working with multiengine tests.
    
    Some subclass should define:
    
    * self.multiengine
    * self.engines to keep track of engines for clean up"""

    def createShell(self):
        return Interpreter()

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
        self.addEngine(4)
        targets = [0,3]
        eTester = MultiEngineExecuteAllTestGenerator(validCommands, self, targets)
        d = eTester.performTests()
        return d

    def testExecuteFailures(self):
        self.addEngine(4)
        targets = [0,2]
        cmds = [x[0] for x in invalidCommands]
        excpts = [x[1] for x in invalidCommands]
        eTester = MultiEngineFailingExecuteTestGenerator(cmds, excpts, self, targets)
        d = eTester.performTests()
        return d
    
    def testExecuteAll(self):
        self.addEngine(2)
        eTester = MultiEngineExecuteAllTestGenerator(validCommands, self)
        d = eTester.performTests()
        return d
        
    def testExecuteAllFailures(self):
        self.addEngine(4)
        cmds = [x[0] for x in invalidCommands]
        excpts = [x[1] for x in invalidCommands]
        eTester = MultiEngineFailingExecuteTestGenerator(cmds, excpts, self)
        d = eTester.performTests()
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
            
    def testGetResult(self):
        self.addEngine(4)
        targets = [0,1,2]
        eTester = MultiEngineGetResultTestGenerator(validCommands, self, targets)
        d = eTester.performTests()
        return d

    def testGetResultDefault(self):
        self.addEngine(1)
        target = 0
        cmd = 'a=5'
        shell = self.createShell()
        shellResult = shell.execute(cmd)
        def popit(dikt, key):
            dikt.pop(key)
            return dikt
        d = self.multiengine.execute(target, cmd)
        d.addCallback(lambda _: self.multiengine.getResult(target))
        d.addCallback(lambda r: self.assertEquals(shellResult, popit(r[0],'id')))
        return d

    def testGetResultFailure(self):
        self.addEngine(1)
        d = self.multiengine.getResult(0, None)
        d.addErrback(lambda f: self.assertRaises(IndexError, f.raiseException))
        d.addCallback(lambda _: self.multiengine.getResult(0, 10))
        d.addErrback(lambda f: self.assertRaises(IndexError, f.raiseException))
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
    

