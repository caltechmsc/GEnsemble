# encoding: utf-8
"""This file contains unittests for the enginepb.py module.
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


from twisted.python import components
from twisted.internet import reactor, defer
from twisted.spread import pb
from twisted.internet.base import DelayedCall
DelayedCall.debug = True

import zope.interface as zi

from ipython1.kernel import pbconfig
from ipython1.kernel.error import PBMessageSizeError
from ipython1.kernel import engineservice as es
from ipython1.test.util import DeferredTestCase
from ipython1.kernel.controllerservice import IControllerBase
from ipython1.kernel.enginepb import \
    PBRemoteEngineRootFromService, \
    PBEngineClientFactory
    
from ipython1.test.engineservicetest import \
    IEngineCoreTestCase, \
    IEngineSerializedTestCase, \
    IEngineQueuedTestCase

class EnginePBTest(DeferredTestCase, 
                   IEngineCoreTestCase, 
                   IEngineSerializedTestCase,
                   IEngineQueuedTestCase
                   ):
        
    zi.implements(IControllerBase)
        
    def setUp(self):
        self.services = []
        self.clients = []
        self.servers = []

        # Start a server and append to self.servers
        self.sroot = PBRemoteEngineRootFromService(self)
        self.sf = pb.PBServerFactory(self.sroot)
        self.servers.append(reactor.listenTCP(10201, self.sf))
        
        # Start an EngineService and append to services/client
        self.engineService = es.EngineService()
        ef = PBEngineClientFactory(self.engineService)
        client = reactor.connectTCP('127.0.0.1', 10201, ef)
        self.clients.append(client)
        self.services.append(self.engineService)
        self.engineService.startService()

        # Create and returna Deferred that will fire when self.registerEngine
        # is called.  By returning this deferred, the actual tests will not
        # be run until the client has connected and is registered.
        self.setUpDeferred = defer.Deferred()
        return self.setUpDeferred
    
    def tearDown(self):
        l = []
        for s in self.servers:
            try:
                d = s.stopListening()
                if d is not None:
                    l.append(d)
            except:
                pass
        for c in self.clients:
            c.disconnect()
            del c
        dl = defer.DeferredList(l)
        return dl
    
    def testNull(self):
        return
    
    #---------------------------------------------------------------------------
    # Make me look like a basic controller
    #---------------------------------------------------------------------------
    
    def registerEngine(self, remoteEngine, id=None, ip=None, port=None, pid=None):
        self.engine = remoteEngine
        # This fires the callbackchain to allow the tests to run
        # The time delay seems to be important
        reactor.callLater(0.1, self.setUpDeferred.callback, None)
        return {'id':id}
    
    def unregisterEngine(self, id):
        pass

    #---------------------------------------------------------------------------
    # Specific tests
    #---------------------------------------------------------------------------

    def testMessageSizeLimit(self):
        sizeLimit = 64*1024
        savedLimit = pbconfig.banana.SIZE_LIMIT
        pbconfig.banana.SIZE_LIMIT = sizeLimit
        # Test that smaller size is allows
        toSend = (sizeLimit-1)*'0'
        d = self.engine.push(a=toSend)
        d.addCallback(lambda _: self.engine.pull('a'))
        d.addCallback(lambda r: self.assert_(r==toSend))
        d.addCallback(lambda _: self.engine.execute("a=%i*'0'" % sizeLimit-1))
        d.addCallback(lambda _: self.engine.pull('a'))
        d.addCallback(lambda r: self.assert_(r==toSend))
        # Test for failure at the SIZE_LIMIT
        toSend = (sizeLimit)*'0'
        d.addCallback(lambda _: self.engine.push(a=toSend))
        d.addErrback(lambda f: self.assertRaises(PBMessageSizeError, f.raiseException))
        d.addCallback(lambda _: self.engine.execute("a=%i*'0'" % ((sizeLimit-1),)))
        d.addCallback(lambda _: self.engine.pull('a'))
        d.addErrback(lambda f: self.assertRaises(PBMessageSizeError, f.raiseException))

        pbconfig.banana.SIZE_LIMIT = savedLimit
        return d