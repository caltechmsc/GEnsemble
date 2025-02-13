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

from twisted.application.service import IService
from ipython1.kernel.controllerservice import ControllerService
from ipython1.test import multienginetest as met
from controllertest import IControllerCoreTestCase
from ipython1.test.util import DeferredTestCase

class BasicControllerServiceTest(DeferredTestCase,
    IControllerCoreTestCase):
    
    def setUp(self):
        self.controller  = ControllerService()
        self.controller.startService()
    
    def tearDown(self):
        self.controller.stopService()
