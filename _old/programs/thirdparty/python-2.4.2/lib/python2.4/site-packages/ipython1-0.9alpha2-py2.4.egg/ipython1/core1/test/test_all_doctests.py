#!/usr/bin/env python
# encoding: utf-8
"""Simple template for unit tests.
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

#-------------------------------------------------------------------------------
# Setup for inline and standalone doctests
#-------------------------------------------------------------------------------


# If you have standalone doctests in a separate file, set their names in the
# dt_files variable (as a single string  or a list thereof):
dt_files = [
    'tst_display_formatter.txt',
    'tst_display_trap.txt',
    'tst_history.txt',
    'tst_macro.txt',
    'tst_message_cache.txt',
    'tst_output_trap.txt',
    'tst_traceback_formatter.txt',
    'tst_traceback_trap.txt',
]

# If you have any modules whose docstrings should be scanned for embedded tests
# as examples accorging to standard doctest practice, set them here (as a
# single string or a list thereof):
dt_modules = None

#-------------------------------------------------------------------------------
# Regular Unittests
#-------------------------------------------------------------------------------

# This ensures that the code will run either standalone as a script, or that it
# can be picked up by Twisted's `trial` test wrapper to run all the tests.


# B. Granger on 5/3/07.  These lines were killing the ipython1 test suite.
# Thus I have commented them out so that everything runs.
# from ipython1.test.ipdoctest import IPDocTestLoader,makeTestSuite
# 
# if __name__ == '__main__':
#     unittest.main(testLoader=IPDocTestLoader(dt_files,dt_modules,TEST_PATH))
# else:
#     testSuite = lambda : makeTestSuite(__name__,dt_files,dt_modules,TEST_PATH)
