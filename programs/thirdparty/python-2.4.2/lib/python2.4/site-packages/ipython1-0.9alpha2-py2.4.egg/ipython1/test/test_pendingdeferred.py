#!/usr/bin/env python
# encoding: utf-8
"""Tests for pendingdeferred.py
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

import tcommon
from tcommon import *

from ipython1.test.util import DeferredTestCase

from twisted.internet import defer
import ipython1.kernel.pendingdeferred as pd
from ipython1.kernel import error


#-------------------------------------------------------------------------------
# Setup for inline and standalone doctests
#-------------------------------------------------------------------------------


# If you have standalone doctests in a separate file, set their names in the
# dt_files variable (as a single string  or a list thereof):
dt_files = []

# If you have any modules whose docstrings should be scanned for embedded tests
# as examples accorging to standard doctest practice, set them here (as a
# single string or a list thereof):
dt_modules = []

#-------------------------------------------------------------------------------
# Regular Unittests
#-------------------------------------------------------------------------------


class Foo(object):
    
    def bar(self, bahz):
        return defer.succeed('blahblah' + bahz)

class TwoPhaseFoo(pd.PendingDeferredAdapter):
    
    def __init__(self, foo):
        self.foo = foo
        pd.PendingDeferredAdapter.__init__(self)

    @pd.twoPhase
    def bar(self, bahz):
        return self.foo.bar(bahz)


class PendingDeferredManagerTest(DeferredTestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def testBasic(self):
        pdm = pd.PendingDeferredManager(0)
        for i in range(10):
            id = pdm.getNextDeferredID()
            self.assert_(id==i)
        dDict = {}
        for i in range(10):
            d = defer.Deferred()
            pdm.savePendingDeferred(i, d)
            dDict[i] = d
        for i in range(5):
            d = pdm.getPendingDeferred(i,block=True)
            dDict[i].callback('foo')
            d.addCallback(lambda r: self.assert_(r=='foo'))
        for i in range(5,10):
            d = pdm.getPendingDeferred(i,block=False)
            d.addErrback(lambda f: self.assertRaises(error.ResultNotCompleted, f.raiseException))
        for i in range(5,10):
            dDict[i].callback('foo')
            d = pdm.getPendingDeferred(i,block=False)
            d.addCallback(lambda r: self.assert_(r=='foo'))
        for i in range(10):
            d = pdm.getPendingDeferred(i,False)
            d.addErrback(lambda f: self.assertRaises(error.InvalidDeferredID, f.raiseException))
            
    def testPDA(self):
        f = Foo()
        tpf = TwoPhaseFoo(f)
        clientID = tpf.registerClient()
        self.assert_(clientID==0)
        d = tpf.bar(clientID, True, 'hi there')
        d.addCallback(lambda r: self.assertEquals(r, 'blahblahhi there'))
        d = tpf.bar(clientID, False, 'foobah')
        d.addCallback(lambda r: 
            self.assertEquals(len(tpf.pdManagers[clientID].pendingDeferreds.keys()), 1))
        d.addCallback(lambda r: tpf.flush(clientID))
        d.addCallback(lambda r: 
            self.assertEquals(len(tpf.pdManagers[clientID].pendingDeferreds.keys()), 0))
        tpf.unregisterClient(clientID)
        d = tpf.bar(1000, True, 'boo')
        d.addErrback(lambda f: self.assertRaises(error.InvalidClientID, f.raiseException))
        
        
        
#-------------------------------------------------------------------------------
# Regular Unittests
#-------------------------------------------------------------------------------

# This ensures that the code will run either standalone as a script, or that it
# can be picked up by Twisted's `trial` test wrapper to run all the tests.
if tcommon.pexpect is not None:
    if __name__ == '__main__':
        unittest.main(testLoader=IPDocTestLoader(dt_files,dt_modules))
    else:
        testSuite = lambda : makeTestSuite(__name__,dt_files,dt_modules)
