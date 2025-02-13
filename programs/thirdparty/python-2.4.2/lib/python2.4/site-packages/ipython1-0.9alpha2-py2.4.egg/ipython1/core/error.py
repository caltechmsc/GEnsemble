# encoding: utf-8
"""
error.py

We declare here a class hierarchy for all exceptions produced by IPython, in
cases where we don't just raise one from the standard library.

Created by Brian Granger on 2006-08-10.
Copyright (c) 2006 __MyCompanyName__. All rights reserved.
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


class IPythonError(Exception):
    """Base exception that all of our exceptions inherit from.

    This can be raised by code that doesn't have any more specific
    information."""

    pass

# Exceptions associated with the controller objects
class ControllerError(IPythonError): pass

class ControllerCreationError(ControllerError): pass


# Exceptions associated with the Engines
class EngineError(IPythonError): pass

class EngineCreationError(EngineError): pass
