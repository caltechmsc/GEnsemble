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

resultKeys = ('id', 'commandIndex', 'stdin', 'stdout', 'stderr')


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
        
        
class IEngineCoreTestCase(object):
    """Test an IEngineCore implementer."""

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
        commands = [(self.engine.id, 0,"a = 5","",""),
            (self.engine.id, 1,"b = 10","",""),
            (self.engine.id, 2,"c = a + b","",""),
            (self.engine.id, 3,"print c","15\n",""),
            (self.engine.id, 4,"import math","",""),
            (self.engine.id, 5,"2.0*math.pi","6.2831853071795862\n","")]
        # I tried getting these into a loop but the dependencies of the Deferred's
        # were extremely buggy and wierd
        d1 = self.engine.execute(commands[0][2])
        d2 = self.assertDeferredEquals(d1, dict(zip(resultKeys,commands[0])))
        d2.addCallback(lambda _: self.engine.execute(commands[1][2]))
        d3 = self.assertDeferredEquals(d2, dict(zip(resultKeys,commands[1])))
        d3.addCallback(lambda _: self.engine.execute(commands[2][2]))
        d4 = self.assertDeferredEquals(d3, dict(zip(resultKeys,commands[2])))
        d4.addCallback(lambda _: self.engine.execute(commands[3][2]))
        d5 = self.assertDeferredEquals(d4, dict(zip(resultKeys,commands[3])))
        d5.addCallback(lambda _: self.engine.execute(commands[4][2]))
        d6 = self.assertDeferredEquals(d5, dict(zip(resultKeys,commands[4])))        
        d6.addCallback(lambda _: self.engine.execute(commands[5][2]))
        d7 = self.assertDeferredEquals(d6, dict(zip(resultKeys,commands[5])))
        return d7    
        
    def testExecuteFailures(self):
        d = self.engine.execute('a=1/0')
        d.addErrback(lambda f: self.assertRaises(ZeroDivisionError, f.raiseException))
        d.addCallback(lambda _: self.engine.execute('print v'))
        d.addErrback(lambda f: self.assertRaises(NameError, f.raiseException))
        d.addCallback(lambda _: self.engine.execute('a = 2**1000000'))
        d.addErrback(lambda f: self.assertRaises(OverflowError, f.raiseException))
        d.addCallback(lambda _: self.engine.execute('l=[];l[0]'))
        d.addErrback(lambda f: self.assertRaises(IndexError, f.raiseException))
        d.addCallback(lambda _: self.engine.execute("d={};d['a']"))
        d.addErrback(lambda f: self.assertRaises(KeyError, f.raiseException))
        d.addCallback(lambda _: self.engine.execute("assert 1==0"))
        d.addErrback(lambda f: self.assertRaises(AssertionError, f.raiseException))
        d.addCallback(lambda _: self.engine.execute("import abababsdbfsbaljasdlja"))
        d.addErrback(lambda f: self.assertRaises(ImportError, f.raiseException))
        d.addCallback(lambda _: self.engine.execute("raise Exception()"))
        d.addErrback(lambda f: self.assertRaises(Exception, f.raiseException))
        return d
    
    def testPushPull(self):
        objs = [10,"hi there",1.2342354,{"p":(1,2)}]
        dList = []
        for o in objs:
            d1 = self.engine.push(key=o)
            d1.addCallback(lambda _: self.engine.pull('key'))
            d1.addCallback(lambda r: self.assertEquals(r, o))
            dList.append(d1)
        d = defer.DeferredList(dList, consumeErrors=1)
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

    def testSimplePushPull(self):
        d = self.engine.push(a=10)
        d.addCallback(lambda _: self.engine.pull('a'))
        d.addCallback(lambda r: self.assertEquals(r, 10))
        d.addCallback(lambda _: self.engine.push(b=20))
        d.addCallback(lambda _: self.engine.pull('b'))
        d.addCallback(lambda r: self.assertEquals(r, 20))
        d.addCallback(lambda _: self.engine.push(c=None))
        d.addCallback(lambda _: self.engine.pull('c'))
        d.addCallback(lambda r: self.assertEquals(r, None))        
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
            
    def testGetResult(self):
        d = self.engine.getResult()
        @d.addErrback
        def nextd(f):
            self.assertRaises(IndexError, f.raiseException)
            return self.engine.execute('a = 5')
        nextd.addCallback(lambda _: self.engine.getResult())
        d = self.assertDeferredEquals(nextd, 
            dict(zip(resultKeys, (self.engine.id, 0,"a = 5","",""))))
        d.addCallback(lambda _: self.engine.getResult(0))
        d = self.assertDeferredEquals(d, dict(zip(resultKeys, (self.engine.id, 0,"a = 5","",""))))
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
