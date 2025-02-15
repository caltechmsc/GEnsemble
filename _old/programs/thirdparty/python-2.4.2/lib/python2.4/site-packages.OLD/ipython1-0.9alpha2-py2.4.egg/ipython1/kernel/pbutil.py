# encoding: utf-8
"""Utilities for PB using modules.
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

from twisted.python.failure import Failure
from twisted.python import failure
from twisted.internet import reactor, defer
import threading, sys

from ipython1.kernel import pbconfig
from ipython1.kernel.error import PBMessageSizeError


#-------------------------------------------------------------------------------
# The actual utilities
#-------------------------------------------------------------------------------

def packageFailure(f):
    """Clean and pickle a failure preappending the string FAILURE:"""
    
    f.cleanFailure()
    # This is sometimes helpful in debugging
    #f.raiseException()
    pString = pickle.dumps(f, 2)
    return 'FAILURE:' + pString

def unpackageFailure(r):
    """
    See if a returned value is a pickled Failure object.

    To distinguish between general pickled objects and pickled Failures, the
    other side should prepend the string FAILURE: to any pickled Failure.
    """
    if isinstance(r, str):
        if r.startswith('FAILURE:'):
            try:
                result = pickle.loads(r[8:])
            except pickle.PickleError:
                return failure.Failure( \
                    FailureUnpickleable("Could not unpickle failure."))
            else:
                return result
    return r

def checkMessageSize(m, info):
    """Check string m to see if it violates banana.SIZE_LIMIT.
    
    This should be used on the client side of things for push, scatter
    and pushSerialized and on the other end for pull, gather and pullSerialized.
    
    :Parameters:
        `m` : string
            Message whose size will be checked.
        `info` : string
            String describing what object the message refers to.
            
    :Exceptions:
        - `PBMessageSizeError`: Raised in the message is > banana.SIZE_LIMIT

    :returns: The original message or a Failure wrapping a PBMessageSizeError
    """

    if len(m) > pbconfig.banana.SIZE_LIMIT:
        s = """Objects too big to transfer:
Names:            %s
Actual Size (kB): %d
SIZE_LIMIT  (kB): %d
* SIZE_LIMIT can be set in kernel.pbconfig""" \
            % (info, len(m)/1024, pbconfig.banana.SIZE_LIMIT/1024)
        return Failure(PBMessageSizeError(s))
    else:
        return m
        
        
class ReactorInThread(threading.Thread):
    """Run the twisted reactor in a different thread."""
    def run(self):
        reactor.run(installSignalHandlers=0)


# This code is from 
# http://twistedmatrix.com/trac/ticket/1042
def blockingCallFromThread(func, *args, **kwargs):
    # print func
    # print args
    # print kwargs
    e = threading.Event()
    l = []
    def _got_result(result):
        # print result
        l.append(result)
        e.set()
        return None
    def wrapped_func():
        d = defer.maybeDeferred(func, *args, **kwargs)
        d.addBoth(_got_result)
    reactor.callFromThread(wrapped_func)
    e.wait()
    result = l[0]
    if isinstance(result, Failure):
        # Whee!  Cross-thread exceptions!
        result.raiseException()
    else:
        return result