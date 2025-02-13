# encoding: utf-8
"""
test template for complete engine object
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

import cPickle as pickle

from twisted.internet import defer, reactor
from twisted.python import failure
from twisted.application import service
import zope.interface as zi

from ipython1.kernel import newserialized
from ipython1.kernel import error 
import ipython1.kernel.engineservice as es
from ipython1.core.interpreter import Interpreter
from ipython1.test.testgenerator import (EngineExecuteTestGenerator, 
    EnginePushPullTestGenerator, 
    EngineFailingExecuteTestGenerator,
    EngineGetResultTestGenerator)

class FailingEngineError(Exception):
    pass

class FailingEngineService(object, service.Service):
    """An EngineSerivce whose methods always raise FailingEngineError.
    
    This class is used in tests to see if errors propagate correctly.
    """
    
    zi.implements(es.IEngineBase)
                
    def __init__(self, shellClass=None, mpi=None):
        self.id = None
    
    def _setID(self, id):
        self._id = id
        
    def _getID(self):
        return self._id
        
    id = property(_getID, _setID)
        
    def startService(self):
        pass
            
    def execute(self, lines):
        return defer.fail(failure.Failure(FailingEngineError("error text")))

    def push(self, **namespace):
        return defer.fail(failure.Failure(FailingEngineError("error text")))

    def pull(self, *keys):
        return defer.fail(failure.Failure(FailingEngineError("error text")))
        
    def getResult(self, i=None):
        return defer.fail(failure.Failure(FailingEngineError("error text")))
    
    def reset(self):
        return defer.fail(failure.Failure(FailingEngineError("error text")))
    
    def kill(self):
        return defer.fail(failure.Failure(FailingEngineError("error text")))

    def keys(self):
        return defer.fail(failure.Failure(FailingEngineError("error text")))

    def pushSerialized(self, **sNamespace):
        return defer.fail(failure.Failure(FailingEngineError("error text")))
    
    def pullSerialized(self, *keys):
        return defer.fail(failure.Failure(FailingEngineError("error text")))
    
# A sequence of valid commands run through execute
validCommands = ['a=5',
                 'b=10',
                 'c=a+b',
                 'import math',
                 '2.0*math.pi',
                 """def f():
    result = 0.0
    for i in range(10):
        result += i
""",
                 'if 1<2: a=5',
                 """import time
time.sleep(0.1)""",
                """from math import cos;
x = 1.0*cos(0.5)""", # Semicolons lead to Discard ast nodes that should be discarded
                """from sets import Set
s = Set()
   """, # Trailing whitespace should be allowed.
                """import math
math.cos(1.0)""", # Test a method call with a discarded return value
                """x=1.0234
a=5; b=10""", # Test an embedded semicolon
                """x=1.0234
a=5; b=10;""" # Test both an embedded and trailing semicolon
                 ]
                 
# A sequence of commands that raise various exceptions
invalidCommands = [('a=1/0',ZeroDivisionError),
                   ('print v',NameError),
                   ('l=[];l[0]',IndexError),
                   ("d={};d['a']",KeyError),
                   ("assert 1==0",AssertionError),
                   ("import abababsdbfsbaljasdlja",ImportError),
                   ("raise Exception()",Exception)]

class IEngineCoreTestCase(object):
    """Test an IEngineCore implementer."""

    def createShell(self):
        return Interpreter()

    def catchQueueCleared(self, f):
        try:
            f.raiseException()
        except error.QueueCleared:
            pass
        
    def testIEngineCoreInterface(self):
        """Does self.engine claim to implement IEngineCore?"""
        self.assert_(es.IEngineCore.providedBy(self.engine))
        
    def testIEngineCoreInterfaceMethods(self):
        """Does self.engine have the methods and attributes in IEngireCore."""
        for m in list(es.IEngineCore):
            self.assert_(hasattr(self.engine, m))
            
    def testIEngineCoreDeferreds(self):
        commands = [(self.engine.execute, ('a=5',)), 
            (self.engine.pull, ('a',)),
            (self.engine.getResult, ()),
            (self.engine.keys, ())]
        dList = []
        for c in commands:
            d = c[0](*c[1])
            self.assert_(isinstance(d, defer.Deferred))
            dList.append(d)
        d = self.engine.push(a=5)
        self.assert_(isinstance(d, defer.Deferred))
        dList.append(d)
        D = defer.DeferredList(dList)
        return D
        
    def testExecute(self):
        eTester = EngineExecuteTestGenerator(validCommands, self)
        d = eTester.performTests()
        return d

    def testExecuteFailures(self):
        cmds = [x[0] for x in invalidCommands]
        excpts = [x[1] for x in invalidCommands]
        eTester = EngineFailingExecuteTestGenerator(cmds, excpts, self)
        d = eTester.performTests()
        return d
            
    def testPushPull(self):
        objs = [10,"hi there",1.2342354,{"p":(1,2)},None]
        eTester = EnginePushPullTestGenerator(objs, self)
        d = eTester.performTests()
        d.addCallback(lambda _:self.engine.reset())
        d.addCallback(lambda _: self.engine.pull("a"))
        d.addErrback(lambda f: self.assertRaises(NameError, f.raiseException))
        return d        

    def testPushPullFailures(self):
        d = self.engine.pull('a')
        d.addErrback(lambda f: self.assertRaises(NameError, f.raiseException))
        d.addCallback(lambda _: self.engine.execute('l = lambda x: x'))
        d.addCallback(lambda _: self.engine.pull('l'))
        d.addErrback(lambda f: self.assertRaises(pickle.PicklingError, f.raiseException))
        d.addCallback(lambda _: self.engine.push(l=lambda x: x))
        d.addErrback(lambda f: self.assertRaises(pickle.PicklingError, f.raiseException))
        return d
        
    def testPushPullArray(self):
        try:
            import numpy
        except:
            print 'no numpy, ',
            return
        a = numpy.random.random(1000)
        d = self.engine.push(a=a)
        d.addCallback(lambda _: self.engine.pull('a'))
        d.addCallback(lambda b: b==a)
        d.addCallback(lambda c: c.all())
        return self.assertDeferredEquals(d, True)
        
    def testGetResultFailure(self):
        d = self.engine.getResult(None)
        d.addErrback(lambda f: self.assertRaises(IndexError, f.raiseException))
        d.addCallback(lambda _: self.engine.getResult(10))
        d.addErrback(lambda f: self.assertRaises(IndexError, f.raiseException))
        return d
            
    def testGetResult(self):
        eTester = EngineGetResultTestGenerator(validCommands, self)
        d = eTester.performTests()
        return d

    def testGetResultDefault(self):
        cmd = 'a=5'
        shell = self.createShell()
        shellResult = shell.execute(cmd)
        def popit(dikt, key):
            dikt.pop(key)
            return dikt
        d = self.engine.execute(cmd)
        d.addCallback(lambda _: self.engine.getResult())
        d.addCallback(lambda r: self.assertEquals(shellResult, popit(r,'id')))
        return d

    def testKeys(self):
        d = self.engine.keys()
        d.addCallback(lambda s: isinstance(s, list))
        d.addCallback(lambda r: self.assertEquals(r, True))
        return d
            
            
class IEngineSerializedTestCase(object):
    """Test an IEngineCore implementer."""
        
    def testIEngineSerializedInterface(self):
        """Does self.engine claim to implement IEngineCore?"""
        self.assert_(es.IEngineSerialized.providedBy(self.engine))
        
    def testIEngineSerializedInterfaceMethods(self):
        """Does self.engine have the methods and attributes in IEngireCore."""
        for m in list(es.IEngineSerialized):
            self.assert_(hasattr(self.engine, m))
       
    def testIEngineSerializedDeferreds(self):
        dList = []
        d = self.engine.pushSerialized(key=newserialized.serialize(12345))
        self.assert_(isinstance(d, defer.Deferred))
        dList.append(d)
        d = self.engine.pullSerialized('key')
        self.assert_(isinstance(d, defer.Deferred))
        dList.append(d)
        D = defer.DeferredList(dList)
        return D
                
    def testPushPullSerialized(self):
        objs = [10,"hi there",1.2342354,{"p":(1,2)}]
        d = defer.succeed(None)
        for o in objs:
            self.engine.pushSerialized(key=newserialized.serialize(o))
            value = self.engine.pullSerialized('key')
            value.addCallback(lambda serial: newserialized.IUnSerialized(serial).getObject())
            d = self.assertDeferredEquals(value,o,d)
        return d

    def testPullSerializedFailures(self):
        d = self.engine.pullSerialized('a')
        d.addErrback(lambda f: self.assertRaises(NameError, f.raiseException))
        d.addCallback(lambda _: self.engine.execute('l = lambda x: x'))
        d.addCallback(lambda _: self.engine.pullSerialized('l'))
        d.addErrback(lambda f: self.assertRaises(pickle.PicklingError, f.raiseException))
        return d

class IEngineQueuedTestCase(object):
    """Test an IEngineCore implementer."""
        
    def testIEngineQueuedInterface(self):
        """Does self.engine claim to implement IEngineCore?"""
        self.assert_(es.IEngineQueued.providedBy(self.engine))
        
    def testIEngineQueuedInterfaceMethods(self):
        """Does self.engine have the methods and attributes in IEngireCore."""
        for m in list(es.IEngineQueued):
            self.assert_(hasattr(self.engine, m))
            
    def testIEngineQueuedDeferreds(self): 
        dList = []
        d = self.engine.clearQueue()
        self.assert_(isinstance(d, defer.Deferred))
        dList.append(d)
        d = self.engine.queueStatus()
        self.assert_(isinstance(d, defer.Deferred))
        dList.append(d)
        D = defer.DeferredList(dList)
        return D
            
    def testClearQueue(self):
        result = self.engine.clearQueue()
        d1 = self.assertDeferredEquals(result, True)
        d1.addCallback(lambda _: self.engine.queueStatus())
        d2 = self.assertDeferredEquals(d1, {'queue':[], 'pending':'None'})
        return d2
        
    def testQueueStatus(self):
        result = self.engine.queueStatus()
        result.addCallback(lambda r: 'queue' in r and 'pending' in r)
        d = self.assertDeferredEquals(result, True)
        return d
