# encoding: utf-8
"""Classes and functions for kernel related errors and exceptions.
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

from ipython1.core import error

#-------------------------------------------------------------------------------
# Error classes
#-------------------------------------------------------------------------------

class KernelError(error.IPythonError):
    pass

class NotDefined(KernelError):
    def __init__(self, name):
        self.name = name
        self.args = (name,)

    def __repr__(self):
        return '<NotDefined: %s>' % self.name
    
    __str__ = __repr__

class QueueCleared(KernelError):
    pass

class IdInUse(KernelError):
    pass

class ProtocolError(KernelError):
    pass
    
class InvalidEngineID(KernelError):
    pass
    
class NoEnginesRegistered(KernelError):
    pass
    
class InvalidClientID(KernelError):
    pass
    
class InvalidDeferredID(KernelError):
    pass
    
class SerializationError(KernelError):
    pass
    
class MessageSizeError(KernelError):
    pass
    
class PBMessageSizeError(MessageSizeError):
    pass
    
class ResultNotCompleted(KernelError):
    pass
    
class ResultAlreadyRetrieved(KernelError):
    pass
    
class ClientError(KernelError):
    pass

class TaskAborted(KernelError):
    pass

class NotAPendingResult(KernelError):
    pass

class UnpickleableException(KernelError):
    pass


# DB Error for database related errors in notebook
class DBError(KernelError):
    pass

class NotFoundError(KernelError):
    pass

