# encoding: utf-8
# -*- test-case-name: ipython1.test.test_pendingdeferred -*-
"""Classes to manage pending Deferreds.

A pending deferred is a deferred that may or may not have fired.  This module
is useful for taking a class whose methods return deferreds and wrapping it to
provide API that keeps track of those deferreds for later retrieval.  See the
tests for examples of its usage.
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

from twisted.application import service
from twisted.internet import defer, reactor
from twisted.python import log, components, failure
from zope.interface import Interface, implements, Attribute

from ipython1.kernel.util import gatherBoth
from ipython1.kernel import error


class PendingDeferredManager(object):
    """A class to track pending deferreds.
    
    To track a pending deferred, the user of this class must first
    get a deferredID by calling `getNextDeferredID`.  Then the user
    calls `savePendingDeferred` passing that id and the deferred to
    be tracked.  To later retrieve it, the user calls
    `getPendingDeferred` passing the id.
    """
    
    def __init__(self, clientID):
        """Manage pending deferreds for a client.
        
        :Parameters:
            clientID : int
                This is not used currently inside this class
        """

        self.clientID = clientID
        self.deferredID = 0
        self.pendingDeferreds = {}
        
    def getNextDeferredID(self):
        """Get the next available deferred id.
        
        :Returns:
            deferredID : int
                The deferred id that the client should use for the next
                deferred is will save to me.
        """

        did = self.deferredID
        self.deferredID += 1
        return did
        
    def savePendingDeferred(self, deferredID, d):
        """Save a deferred to me by deferredID.
        
        :Parameters:
            deferredID : int
                A deferred id the client got by calling `getNextDeferredID`.
            d : Deferred
                The deferred to save.
        """
        
        pd = self.pendingDeferreds.get(deferredID)
        if pd is not None:
            self.removePendingDeferred(deferredID)
        self.pendingDeferreds[deferredID] = d
        
    def removePendingDeferred(self, deferredID):
        """Remove a deferred I am tracking and add a null Errback.
        
        :Parameters:
            deferredID : int
                The id of a deferred that I am tracking.
        """
        
        pd = self.pendingDeferreds.get(deferredID)
        if pd is not None:
            pd.addErrback(lambda f: None)
            del self.pendingDeferreds[deferredID]
        
    def cleanOutDeferreds(self):
        """Remove all the deferreds I am tracking."""
        for k in self.pendingDeferreds.keys():
            self.removePendingDeferred(k)
        
    def _deleteAndPassThrough(self, r, deferredID):
        self.removePendingDeferred(deferredID)
        return r
        
    def getPendingDeferred(self, deferredID, block):
        """Get a pending deferred that I am tracking by deferredID.
        
        :Parameters:
            deferredID : int
                The id of a deferred I am tracking
            block : boolean
                Should I block until the deferred has fired.
        """
        #log.msg("getPendingDeferred: %s %s" % (repr(deferredID), repr(block)))
        pd = self.pendingDeferreds.get(deferredID)
        if pd is not None:
            if not pd.called and block:    # pd has not fired and we should block
                #log.msg("pendingDeferred has not been called: %s" % deferredID)
                pd.addCallback(self._deleteAndPassThrough, deferredID)
                return pd
            elif not pd.called and not block: # pd has not fired, but we should not block
                return defer.fail(failure.Failure(error.ResultNotCompleted("Result not completed: %i" % deferredID)))
            else:    # pd has fired
                #log.msg("pendingDeferred has been called: %s: %s" % (deferredID, repr(pd.result)))
                if isinstance(pd.result, failure.Failure):
                    dToReturn = defer.fail(pd.result)
                elif isinstance(pd.result, defer.Deferred):
                    dToReturn = pd.result
                else:
                    dToReturn = defer.succeed(pd.result)
                # It has fired so remove it!
                self.removePendingDeferred(deferredID)
            return dToReturn
        else:
            return defer.fail(failure.Failure(error.InvalidDeferredID('Invalid deferredID: ' + repr(deferredID))))
            

def twoPhase(wrappedMethod):
    """Wrap methods that return a deferred into a two phase process.
    
    This transforms::
    
        foo(arg1, arg2, ...) -> foo(clientID, block, arg1, arg2, ...).
    
    The wrapped method will then return a deferred to a deferredID.  This will
    only work on method of classes that inherit from `PendingDeferredAdapter`,
    as that class provides an API for 
    
    clientID is the id of the client making the request.  Each client's pending
    deferreds are tracked independently.  The client id is usually gotten by 
    calling the `registerClient` method of `PendingDeferredAdapter`.
    
    block is a boolean to determine if we should use the two phase process or
    just simply call the wrapped method.  At this point block does not have a
    default and it probably won't.
    """
    
    def wrapperTwoPhase(pendingDeferredAdapter, *args, **kwargs):
        clientID = args[0]
        block = args[1]
        if pendingDeferredAdapter._isValidClientID(clientID):
            if block:
                return wrappedMethod(pendingDeferredAdapter, *args[2:], **kwargs)
            else:
                deferredID = pendingDeferredAdapter.getNextPendingDeferredID(clientID)
                d = wrappedMethod(pendingDeferredAdapter, *args[2:], **kwargs)
                pendingDeferredAdapter.savePendingDeferred(clientID, deferredID, d)
                return defer.succeed(deferredID)
        else:  
            return defer.fail(failure.Failure(
                error.InvalidClientID("Client with ID %r has not been registered." % clientID)))        
                
    return wrapperTwoPhase

class IPendingDeferredAdapter(Interface):
    
    def registerClient():
        """Register a new client of this class.
        
        :Returns:
            clientID : int
                The id the client is given.
        """
        
    def unregisterClient(clientID):
        """Unregister a client by its clientID.
        
        :Parameters:
            clientID : int
                The id that the client was given.
        """
        
    def getPendingDeferred(clientID, deferredID, block):
        """Get a pending deferred by it id.
        
        :Parameters:
            clientID : int
                The id that the client was given.
            deferredID : int
                The id of the deferred that was returned by the client calling
                one of the wrapped methods.
            block : boolean
                Should I wait until the deferred has fired to just return
                the unfired deferred immediately.
        """

    def getAllPendingDeferreds(clientID):
        """Get a deferred to a list of result of all the pending deferreds.
        
        If there are pending deferreds d1, d2, this will return a deferred
        to [d1.result, d2.result].
        """
        
    def flush(clientID):
        """Flush out all pending deferreds for clientID.
        
        :Parameters:
            clientID : int
                Flush PD's for this client.  If clientID is 'all' then
                flush the PD's for all clients.
        """

class PendingDeferredAdapter(object):
    """Convert a class to using pending deferreds."""
    
    implements(IPendingDeferredAdapter)
    
    def __init__(self):
        self.clientID = 0
        self.pdManagers = {}
        
    #---------------------------------------------------------------------------
    # Internal methods
    #---------------------------------------------------------------------------
        
    def _isValidClientID(self, clientID):
        """Check to see if a clientID is valid.
        
        :Parameters:
            clientID : int
                The clientID to verify.
            
        :Returns: True if clientID is valid, False if not.
        """
        if self.pdManagers.has_key(clientID):
            return True
        else:
            return False
            
    def getNextPendingDeferredID(self, clientID):
        """Get the next deferredID for clientID.
        
        The caller of this method should first call _isValidClientID to verfiy that
        clientID is valid.

        :Parameters:
            clientID : int
                The id the client was given.
            
        :Returns:
            deferredID : int
                The next deferred id that will be used.
        """
        return self.pdManagers[clientID].getNextDeferredID()
 
        
    def savePendingDeferred(self, clientID, deferredID, d):
        """Save d for clientID under deferredID.
        
        The caller of this method should first call _isValidClientID to verfiy that
        clientID is valid.
        
        :Parameters:
            clientID : int
                The client's id.
            deferredID : int
                The id under which d will be saved.  
            d : Deferred
                The deferred to save.
        
        """
        return self.pdManagers[clientID].savePendingDeferred(deferredID, d)
 
        
    #--------------------------------------------------------------------------
    # Methods related to pending deferreds
    # See the docstrings for IPendingDeferredAdapter for details.
    #--------------------------------------------------------------------------
        
    def registerClient(self):
        cid = self.clientID
        self.clientID += 1
        self.pdManagers[cid] = PendingDeferredManager(cid)
        return cid
        
    def unregisterClient(self, clientID):
        if self._isValidClientID(clientID):
            self.pdManagers[clientID].cleanOutDeferreds()
            del self.pdManagers[clientID]
        else:
            raise error.InvalidClientID("Client with ID %i has not been registered." % clientID)
        
    def getPendingDeferred(self, clientID, deferredID, block):
        if self._isValidClientID(clientID):
            return self.pdManagers[clientID].getPendingDeferred(deferredID, block)
        else:
            return defer.fail(failure.Failure(
                error.InvalidClientID("Client with ID %i has not been registered." % clientID)))
                
    def getAllPendingDeferreds(self, clientID):
        dList = []
        keys = self.pdManagers[clientID].pendingDeferreds.keys()
        for k in keys:
            dList.append(self.pdManagers[clientID].getPendingDeferred(k, block=True))
        if len(dList) > 0:  
            return gatherBoth(dList, consumeErrors=1)
        else:
            return defer.succeed([None])
    
    def flush(self, clientID):
        if clientID == 'all':
            for pdm in self.pdManagers.values():
                pdm.cleanOutDeferreds()
        else:
            if self._isValidClientID(clientID):
                self.pdManagers[clientID].cleanOutDeferreds()
                return defer.succeed(None)
            else:
                return defer.fail(failure.Failure(
                    error.InvalidClientID("Client with ID %i has not been registered." % clientID)))
                
                
            
            
                
        