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

from twisted.internet import defer
from ipython1.test.util import DeferredTestCase
from ipython1.kernel.controllerservice import ControllerService
from ipython1.kernel.multiengine import IMultiEngine, ISynchronousMultiEngine
from ipython1.test.multienginetest import \
    IEngineMultiplexerTestCase, \
    IEngineCoordinatorTestCase, \
    IMultiEngineBaseTestCase
    
    
class BasicMultiEngineTestCase(DeferredTestCase,
    IEngineMultiplexerTestCase,
    IEngineCoordinatorTestCase):
    
    def setUp(self):
        self.controller = ControllerService()
        self.controller.startService()
        self.multiengine = IMultiEngine(self.controller)
        self.engines = []
        
    def tearDown(self):
        self.controller.stopService()
        for e in self.engines:
            e.stopService()
            
class SynchronousMultiEngineTestCase(DeferredTestCase,
    IMultiEngineBaseTestCase):
            
    def setUp(self):
        self.controller = ControllerService()
        self.controller.startService()
        self.multiengine = IMultiEngine(self.controller)
        self.smultiengine = ISynchronousMultiEngine(self.multiengine)
        self.engines = []
        
    def tearDown(self):
        self.controller.stopService()
        for e in self.engines:
            e.stopService()
            
    def testExecuteNoBlock(self):
        self.addEngine(2)
        result = [{'commandIndex': 0, 'stdin': 'a=5', 'id': 0, 'stderr': '', 'stdout': ''},
         {'commandIndex': 0, 'stdin': 'a=5', 'id': 1, 'stderr': '', 'stdout': ''}]
        cid = self.smultiengine.registerClient()
        d = self.smultiengine.execute(cid, False, 'all', 'a=5')
        d.addCallback(lambda r: self.smultiengine.getPendingDeferred(cid, r, True))
        d.addCallback(lambda r: self.assert_(r==result))
        return d
        
    def testExecuteBlock(self):
        self.addEngine(2)
        result = [{'commandIndex': 0, 'stdin': 'a=5', 'id': 0, 'stderr': '', 'stdout': ''},
         {'commandIndex': 0, 'stdin': 'a=5', 'id': 1, 'stderr': '', 'stdout': ''}]
        cid = self.smultiengine.registerClient()
        d = self.smultiengine.execute(cid, True, 'all', 'a=5')
        d.addCallback(lambda r: self.assert_(r==result))
        return d