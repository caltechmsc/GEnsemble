# encoding: utf-8
"""This file contains unittests for the kernel.engineservice.py module.

Things that should be tested:

 - Should the EngineService return Deferred objects?
 - Run the same tests that are run in shell.py.
 - Make sure that the Interface is really implemented.
 - The startService and stopService methods.
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
import zope.interface as zi

from ipython1.kernel import engineservice as es
from ipython1.kernel import error
from ipython1.test.util import DeferredTestCase
from ipython1.kernel.controllerservice import \
    IControllerCore


class IControllerCoreTestCase(object):
    """Tests for objects that implement IControllerCore.
    
    This test assumes that self.controller is defined and implements
    IControllerCore.
    """
    
    def testIControllerCoreInterface(self):
        """Does self.engine claim to implement IEngineCore?"""
        self.assert_(IControllerCore.providedBy(self.controller))
        
    def testIControllerCoreInterfaceMethods(self):
        """Does self.engine have the methods and attributes in IEngireCore."""
        for m in list(IControllerCore):
            self.assert_(hasattr(self.controller, m))
    
    def testRegisterUnregisterEngine(self):
        engine = es.EngineService()
        qengine = es.QueuedEngine(engine)
        regDict = self.controller.registerEngine(qengine, 0)
        self.assert_(isinstance(regDict, dict))
        self.assert_(regDict.has_key('id'))
        self.assert_(regDict['id']==0)
        self.controller.unregisterEngine(0)
        self.assert_(self.controller.engines.get(0, None) == None)

    def testRegisterUnregisterMultipleEngines(self):
        e1 = es.EngineService()
        qe1 = es.QueuedEngine(e1)
        e2 = es.EngineService()
        qe2 = es.QueuedEngine(e2)
        rd1 = self.controller.registerEngine(qe1, 0)
        self.assertEquals(rd1['id'], 0)
        rd2 = self.controller.registerEngine(qe2, 1)
        self.assertEquals(rd2['id'], 1)
        self.controller.unregisterEngine(0)
        rd1 = self.controller.registerEngine(qe1, 0)
        self.assertEquals(rd1['id'], 0)
        self.controller.unregisterEngine(1)
        rd2 = self.controller.registerEngine(qe2, 0)
        self.assertEquals(rd2['id'], 1)
        self.controller.unregisterEngine(0)
        self.controller.unregisterEngine(1)
        self.assertEquals(self.controller.engines,{})
        
    def testRegisterCallables(self):
        e1 = es.EngineService()
        qe1 = es.QueuedEngine(e1)
        self.registerCallableCalled = ';lkj'
        self.unregisterCallableCalled = ';lkj'
        self.controller.onRegisterEngineDo(self._registerCallable, False)
        self.controller.onUnregisterEngineDo(self._unregisterCallable, False)
        self.controller.registerEngine(qe1, 0)
        self.assertEquals(self.registerCallableCalled, 'asdf')
        self.controller.unregisterEngine(0)
        self.assertEquals(self.unregisterCallableCalled, 'asdf')
        self.controller.onRegisterEngineDoNot(self._registerCallable)
        self.controller.onUnregisterEngineDoNot(self._unregisterCallable)
            
    def _registerCallable(self):
        self.registerCallableCalled = 'asdf'
        
    def _unregisterCallable(self):
        self.unregisterCallableCalled = 'asdf'
        
    def testBadUnregister(self):
        self.assertRaises(AssertionError, self.controller.unregisterEngine, 'foo')