# encoding: utf-8
# -*- test-case-name: ipython1.test.test_multienginexmlrpc -*-
"""An XML-RPC interface for an `ISynchronousMultiEngine`.

This class lets XML-RPC clients talk to a `ControllerService` through the
`ISynchronousMultiEngine` interface.  The main things this class needs to do
is serialize/unserialize Python objects (using pickle) to be sent as XML-RPC
binary entities.
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
import xmlrpclib

from zope.interface import Interface, implements
from twisted.internet import defer
from twisted.python import components, failure

from ipython1.external.twisted.web2 import xmlrpc, server, channel

from ipython1.kernel import error
from ipython1.kernel.multiengine import MultiEngine, IMultiEngine
from ipython1.kernel.multiengine import ISynchronousMultiEngine
from ipython1.kernel.multiengineclient import PendingResult
from ipython1.kernel.multiengineclient import ResultList, QueueStatusList
from ipython1.kernel.multiengineclient import wrapResultList
from ipython1.kernel.multiengineclient import InteractiveMultiEngineClient
from ipython1.kernel.xmlrpcutil import Transport

#-------------------------------------------------------------------------------
# The Controller side of things
#-------------------------------------------------------------------------------


# This sets the timeout that twisted/web2 uses between requests.
BETWEEN_REQUESTS_TIMEOUT = 15*60


class IXMLRPCMultiEngine(Interface):
    """XML-RPC interface to `ISynchronousMultiEngine`.  

    The methods in this interface are similar to those of 
    `ISynchronousMultiEngine`, but their arguments and return values are pickled
    if they are not already simple Python types that can be send over XML-RPC.

    See the documentation of `ISynchronousMultiEngine` and `IMultiEngine` for 
    documentation about the methods.

    The methods here take one additional argument (request) that is required
    by XML-RPC, but is not used.
    
    Most methods in this interface act like the `ISynchronousMultiEngine`
    versions and can be called in blocking or non-blocking mode.  There are 
    three methods that always block:
    
    * xmlrpc_queueStatus
    * xmlrpc_clearQueue
    * xmlrpc_getIDs
    
    These methods should always return actual results as they don't need to
    touch the actual engines and can be completed instantly.
    """
            
    #---------------------------------------------------------------------------
    # IEngineMultiplexer related methods
    #---------------------------------------------------------------------------
            
    def xmlrpc_execute(request, clientID, block, targets, lines):
        """"""
        
    def xmlrpc_push(request, clientID, block, targets, namespace):
        """"""
        
    def xmlrpc_pull(request, clientID, block, targets, *keys):
        """"""
        
    def xmlrpc_getResult(request, clientID, block, targets, i=None):
        """"""
        
    def xmlrpc_reset(request, clientID, block, targets):
        """"""
        
    def xmlrpc_keys(request, clientID, block, targets):
        """"""
        
    def xmlrpc_kill(request, clientID, block, targets, controller=False):
        """"""
        
    def xmlrpc_pushSerialized(request, clientID, block, targets, namespace):
        """"""
        
    def xmlrpc_pullSerialized(request, clientID, block, targets, *keys):
        """"""
        
    def xmlrpc_clearQueue(request, clientID, targets):
        """Clear the queue on targets.
        
        This method always blocks.  This means that it will always waits for
        the queues to be cleared before returning.  This method will never
        return the id of a pending deferred.
        """
        
    def xmlrpc_queueStatus(request, clientID, targets):
        """Get the queue status on targets.
        
        This method always blocks.  This means that it will always return
        the queues status's.  This method will never return the id of a pending 
        deferred.    
        """
        
    #---------------------------------------------------------------------------
    # IMultiEngine related methods
    #---------------------------------------------------------------------------
        
    def xmlrpc_getIDs(request):
        """Get the ids of the registered engines.
        
        This method always blocks.
        """
        
    #---------------------------------------------------------------------------
    # IEngineCoordinator related methods
    #---------------------------------------------------------------------------
        
    def xmlrpc_scatter(request, clientID, block, targets, key, seq, style='basic', flatten=False):
        """"""
        
    def xmlrpc_gather(request, clientID, block, targets, key, style='basic'):
        """"""
    #---------------------------------------------------------------------------
    # Pending Deferred related methods
    #---------------------------------------------------------------------------            
    
    def xmlrpc_registerClient(request):
        """"""
        
    def xmlrpc_unregisterClient(request, clientID):
        """"""

    def xmlrpc_getPendingResult(request, clientID, resultID):
        """"""
        
    def xmlrpc_getAllPendingResults(request, clientID):
        """"""
    
    def xmlrpc_flush(self, clientID):
        """"""


def packageResult(wrappedMethod):
    """Decorator for the methods of XMLRPCMultiEngineFromMultiEngine.
    
    This decorator takes methods of XMLRPCMultiEngineFromMultiEngine
    that return deferreds to results/failures and then registers
    callbacks/errbacks that serialize the result/failure to be sent over
    the wire."""
    def wrappedPackageResult(self, *args, **kwargs):
        d = wrappedMethod(self, *args, **kwargs)
        d.addCallback(self.packageSuccess)
        d.addErrback(self.packageFailure)
        return d
    return wrappedPackageResult


class XMLRPCMultiEngineFromMultiEngine(xmlrpc.XMLRPC):
    """Adapt `IMultiEngine` -> `ISynchronousMultiEngine` -> `IXMLRPCMultiEngine`.
    """
    
    implements(IXMLRPCMultiEngine)
    
    addSlash = True
    
    def __init__(self, multiengine):
        xmlrpc.XMLRPC.__init__(self)
        # Adapt the raw multiengine to `ISynchronousMultiEngine` before saving
        # it.  This allow this class to do two adaptation steps.
        self.smultiengine = ISynchronousMultiEngine(multiengine)

    #---------------------------------------------------------------------------
    # Non interface methods
    #---------------------------------------------------------------------------
    
    def packageFailure(self, f):
        f.cleanFailure()
        return self.packageSuccess(f)

    def packageSuccess(self, obj):    
        serial = pickle.dumps(obj, 2)
        return xmlrpc.Binary(serial)
       
    #---------------------------------------------------------------------------
    # IEngineMultiplexer related methods
    #---------------------------------------------------------------------------
    
    @packageResult
    def xmlrpc_execute(self, request, clientID, block, targets, lines):     
        return self.smultiengine.execute(clientID, block, targets, lines)
    
    @packageResult    
    def xmlrpc_push(self, request, clientID, block, targets, binaryNS):
        try:
            namespace = pickle.loads(binaryNS.data)
        except:
            d = defer.fail(failure.Failure())
        else:
            d = self.smultiengine.push(clientID, block, targets, **namespace)
        return d

    @packageResult
    def xmlrpc_pull(self, request, clientID, block, targets, *keys):
        return self.smultiengine.pull(clientID, block, targets, *keys)
    
    @packageResult
    def xmlrpc_getResult(self, request, clientID, block, targets, i=None):
        if i == 'None':
            i = None
        return self.smultiengine.getResult(clientID, block, targets, i)
    
    @packageResult
    def xmlrpc_reset(self, request, clientID, block, targets):
        return self.smultiengine.reset(clientID, block, targets)
    
    @packageResult
    def xmlrpc_keys(self, request, clientID, block, targets):
        return self.smultiengine.keys(clientID, block, targets)
    
    @packageResult
    def xmlrpc_kill(self, request, clientID, block, targets, controller=False):
        return self.smultiengine.kill(clientID, block, targets, controller)

    @packageResult
    def xmlrpc_clearQueue(self, request, clientID, targets):
        return self.smultiengine.clearQueue(clientID, True, targets)

    @packageResult
    def xmlrpc_queueStatus(self, request, clientID, targets):
        return self.smultiengine.queueStatus(clientID, True, targets)
    
    #---------------------------------------------------------------------------
    # IMultiEngine related methods
    #---------------------------------------------------------------------------
    
    def xmlrpc_getIDs(self, request):
        return self.smultiengine.getIDs()
     
    #---------------------------------------------------------------------------
    # IEngineCoordinator related methods
    #---------------------------------------------------------------------------
    
    @packageResult
    def xmlrpc_scatter(self, request, clientID, block, targets, key, bseq, style='basic', flatten=False):
        try:
            seq = pickle.loads(bseq.data)
        except:
            d = defer.fail(failure.Failure())
        else:
            d = self.smultiengine.scatter(clientID, block, targets, key, seq, style, flatten)
        return d      
    
    @packageResult
    def xmlrpc_gather(self, request, clientID, block, targets, key, style='basic'):
        return self.smultiengine.gather(clientID, block, targets, key, style)
    
    #---------------------------------------------------------------------------
    # Pending Deferred related methods
    #---------------------------------------------------------------------------            
    
    def xmlrpc_registerClient(self, request):
        """"""
        clientID = self.smultiengine.registerClient()
        return clientID
        
    def xmlrpc_unregisterClient(self, request, clientID):
        """"""
        try:
            self.smultiengine.unregisterClient(clientID)
        except error.InvalidClientID:
            f = failure.Failure()
            return self.packageFailure(f)
        else:
            return True
            
    @packageResult
    def xmlrpc_getPendingResult(self, request, clientID, resultID, block):
        """"""
        return self.smultiengine.getPendingDeferred(clientID, resultID, block)
        
    @packageResult
    def xmlrpc_getAllPendingResults(self, request, clientID):
        """"""    
        return self.smultiengine.getAllPendingDeferreds(clientID)

    @packageResult
    def xmlrpc_flush(self, request, clientID):
        """"""    
        return self.smultiengine.flush(clientID)
    

# The __init__ method of `XMLRPCMultiEngineFromMultiEngine` first adapts the
# `IMultiEngine` to `ISynchronousMultiEngine` so this is actually doing a
# two phase adaptation.
components.registerAdapter(XMLRPCMultiEngineFromMultiEngine,
            IMultiEngine, IXMLRPCMultiEngine)


class IXMLRPCMultiEngineFactory(Interface):
    pass
    
    
def XMLRPCServerFactoryFromMultiEngine(multiengine):
    """Adapt a MultiEngine to a XMLRPCServerFactory."""
    s = server.Site(IXMLRPCMultiEngine(multiengine))
    cf = channel.HTTPFactory(s, betweenRequestsTimeOut=BETWEEN_REQUESTS_TIMEOUT)
    return cf

# This adaptation does the final step in:
# `IMultiEngine` -> `ISynchronousMultiEngine` ->
# `IXMLRPCMultiEngine` -> `IXMLRPCMultiEngineFactory`
# The first two steps of this are done above in XMLRPCMultiEngineFromMultiEngine
components.registerAdapter(XMLRPCServerFactoryFromMultiEngine,
            IMultiEngine, IXMLRPCMultiEngineFactory)
        

#-------------------------------------------------------------------------------
# The Client side of things
#-------------------------------------------------------------------------------

class XMLRPCMultiEngineClient(object):
    """Client that talks to a IMultiEngine adapted controller over XML-RPC.
    
    This class is usually aliased to RemoteController in ipython1.kernel.api
    so create one like this:
    
    >>> import ipython1.kernel.api as kernel
    >>> rc = kernel.RemoteController(('myhost.work.com', 10105))
    
    This class has a attribute named block that controls how most methods
    work.  If block=True (default) all methods will actually block until
    their action has been completed.  Then they will return their result
    or raise any Exceptions.  If block=False, the method will simply
    return a `PendingResult` object whose `getResult` method or `r` attribute
    can then be used to later retrieve the result.
    """
    
    def __init__(self, addr):
        """Create a client that will connect to addr.
        
        Once created, this class will autoconnect and reconnect to the
        controller as needed.
        
        :Parameters:
            addr : tuple
                The (ip, port) of the IMultiEngine adapted controller.
        """
        self.addr = addr
        self.url = 'http://%s:%s/' % self.addr
        self._server = xmlrpclib.ServerProxy(self.url, transport=Transport(), 
            verbose=0)
        self._clientID = None
        self.block = True

    #---------------------------------------------------------------------------
    # Non interface methods
    #---------------------------------------------------------------------------
        
    def _reallyBlock(self, block=None):
        if block is None:
            return self.block
        else:
            if block in (True, False):
                return block
            else:
                raise ValueError("block must be True or False")

    def _executeRemoteMethod(self, f, *args):
        try:
            rawResult = f(*args)
            result = self._unpackageResult(rawResult)
        except error.InvalidClientID:
            self._getClientID()
            rawResult = f(*args)
            result = self._unpackageResult(rawResult)
        return result

    def _unpackageResult(self, result):
        result = pickle.loads(result.data)
        return self._returnOrRaise(result)
        
    def _returnOrRaise(self, result):
        if isinstance(result, failure.Failure):
            result.raiseException()
        else:
            return result
        
    def _checkClientID(self):
        if self._clientID is None:
            self._getClientID()
            
    def _getClientID(self):
        clientID = self._server.registerClient()
        self._clientID = clientID

    def _getPendingResult(self, resultID, block=True):
        self._checkClientID()
        return self._executeRemoteMethod(self._server.getPendingResult,
            self._clientID, resultID, block)
    
    #---------------------------------------------------------------------------
    # Methods to help manage pending results
    #--------------------------------------------------------------------------- 
     
    def barrier(self, *pendingResults):
        """Synchronize a set of `PendingResults`.
        
        This method is a synchronization primitive that waits for a set of
        `PendingResult` objects to complete.  More specifically, barier does
        the following.
        
        * The `PendingResult`s are sorted by resultID.
        * The `getResult` method is called for each `PendingResult` sequentially
          with block=True.
        * If a `PendingResult` gets a result that is an exception, it is 
          trapped and can be re-raised later by calling `getResult` again.
        * The `PendingResult`s are flushed from the controller.
                
        After barrier has been called on a `PendingResult`, its results can 
        be retrieved by calling `getResult` again or accesing the `r` attribute
        of the instance.
        """
        self._checkClientID()

        # Convert to list for sorting and check class type 
        prList = list(pendingResults)
        for pr in prList:
            if not isinstance(pr, PendingResult):
                raise error.NotAPendingResult("Objects passed to barrier must be PendingResult instances")
                            
        # Sort the PendingResults so they are in order
        prList.sort()
        # Block on each PendingResult object
        for pr in prList:
            try:
                result = pr.getResult(block=True)
            except Exception:
                pass
        
    def flush(self, clientID=None):
        """Flush the PendingResults in the controller.
        
        :Parameters:
            clientID : None, int or 'all'
                Which clients `PendingResult` references shoould be deleted
                in the controller.  None means the current client.  An
                int is used to specify a particular clientID.  The string
                'all' is used to specify all clients. 
        
        This method is needed because the controller keeps track of
        all the `PendingResult` the client has been handed.  There are two
        ways that these references go away:
        
        * If `getResult` is called on a `PendingResult` the controller 
          deletes the reference to it.
        * If `flush` is called the controller deletes all refereces to the 
          `PendingResults` it is tracking.
        
        Once the flush method has been called, any existing `PendingResult`
        object will have become stale and raise an `InvalidDeferredID`
        exception.  One way to think about `flush` is that is is a way
        of telling the controller you are not interested in any 
        the results attached to any existing `PendingResult` object.
        
        Another important point is that this method does not block in any
        way.  The asynchronous results the `PendingResult` is hooked up 
        to still happens, but the result and any failures are simply 
        discarded.
        """
        self._checkClientID()
        if clientID is None:
            cid = self._clientID
        result = self._executeRemoteMethod(self._server.flush, cid)
        return result
        
    #---------------------------------------------------------------------------
    # IEngineMultiplexer related methods
    #---------------------------------------------------------------------------
        
    def execute(self, targets, lines, block=None):
        """Execute lines of code on targets and possibly block.
        
        :Parameters:
            targets : int, list or 'all'
                The engine ids the action will apply to.  Call `getIDs` to see
                a list of currently available engines. 
            lines : str
                A string of Python code to execute.
            block : boolean
                Should I block or not.  If block=True, wait for the action to
                complete and return the result.  If block=False, return a
                `PendingResult` object that can be used to later get the
                result.  If block is not specified, the block attribute 
                will be used instead.
            
        :Returns: A list of dictionaries with the stdin/stdout/stderr of the 
        command on each targets.
        """
        self._checkClientID()
        localBlock = self._reallyBlock(block)
        result = self._executeRemoteMethod(self._server.execute, self._clientID, localBlock, targets, lines)
        if not localBlock:
            result = PendingResult(self, result)
            result.addCallback(wrapResultList)
        else:
            result = ResultList(result)
        return result
    
    def executeAll(self, lines, block=None):
        """Execute lines of code on all targets.
        
        See the docstring for `execute` for full details.
        """
        return self.execute('all', lines, block)
    
    def push(self, targets, **namespace):
        """Push Python objects by key to targets.
        
        This method takes all key/value pairs passed in as keyword arguments
        and pushes (sends) them to the engines specified in targets.  Most Python objects
        are pickled, but numpy arrays are send using their raw buffers.
        
        :Parameters:
            targets : int, list or 'all'
                The engine ids the action will apply to.  Call `getIDs` to see
                a list of currently available engines.
            namespace : dict
                The keyword arguments of that contain the key/value pairs
                that will be pushed.
                
        Examples
        ========
        
        >>> rc.push('all', a=5)    # pushes 5 to all engines as 'a'
        >>> rc.push(0, b=30)       # pushes 30 to 0 as 'b'
        """
        
        self._checkClientID()
        binPackage = xmlrpc.Binary(pickle.dumps(namespace, 2))
        localBlock = self._reallyBlock()
        result = self._executeRemoteMethod(self._server.push, self._clientID, localBlock, targets, binPackage)
        if not localBlock:
            result = PendingResult(self, result)
        return result
                
    def pushAll(self, **ns):
        """Push Python objects by key to all targets.
        
        See the docstring for `push` for full details.
        """
        return self.push('all', **ns)
    
    def pull(self, targets, *keys):
        """Pull Python objects by key from targets.
        
        This method gets the Python objects specified in keys from the engines specified
        in targets.
        
        :Parameters:
            targets : int, list or 'all'
                The engine ids the action will apply to.  Call `getIDs` to see
                a list of currently available engines.
            keys: list or tuple of str
                A list of variable names as string of the Python objects to be pulled
                back to the client.
                
        :Returns: A list of pulled Python objects for each target.
        
        Examples
        ========
        
        >> rc.pullAll('a')
        [10,10,10,10]
        """
        self._checkClientID()
        localBlock = self._reallyBlock()
        result = self._executeRemoteMethod(self._server.pull, self._clientID, localBlock, targets, *keys)
        if not localBlock:
            result = PendingResult(self, result)
        return result
    
    def pullAll(self, *keys):
        """Pull Python objects by key from all targets.
        
        See the docstring for `pull` for full details.
        """
        return self.pull('all', *keys)
        
    def getResult(self, targets, i=None):
        """Get the stdin/stdout/stderr of a previously executed command on targets.
        
        :Parameters:
            targets : int, list or 'all'
                The engine ids the action will apply to.  Call `getIDs` to see
                a list of currently available engines.
            i : None or int
                The command number to retrieve.  The default will retrieve the most recent
                command.
                
        :Returns: The result dict for the command.
        """
        if i is None: # This is because None cannot be marshalled by xml-rpc
            i = 'None'
        self._checkClientID()
        localBlock = self._reallyBlock()
        result = self._executeRemoteMethod(self._server.getResult, self._clientID, localBlock, targets, i)
        if not localBlock:
            result = PendingResult(self, result)
            result.addCallback(wrapResultList)
        else:
            result = ResultList(result)
        return result
         
    def getResultAll(self, i=None):
        """Get the stdin/stdout/stderr of a previously executed command on all targets.
        
       See the docstring for `getResult` for full details.     
        """
        return self.getResult('all', i)
    
    def reset(self, targets):
        """Reset the namespace on targets.
        
        This method resets the persistent namespace in which computations are done in the
        each engine.  This is is sort of like a soft reset.  Use `kill` to actually stop
        the engines.
        
        :Parameters:
            targets : int, list or 'all'
                The engine ids the action will apply to.  Call `getIDs` to see
                a list of currently available engines.
        """
        self._checkClientID()
        localBlock = self._reallyBlock()
        result = self._executeRemoteMethod(self._server.reset, self._clientID, localBlock, targets)
        if not localBlock:
            result = PendingResult(self, result)
        return result    
        
    def resetAll(self):
        """Reset the namespace on all targets.
        
       See the docstring for `reset` for full details.         
        """
        return self.reset('all')
    
    def keys(self, targets):
        """List all the variable names defined on each target.
        
        :Parameters:
            targets : int, list or 'all'
                The engine ids the action will apply to.  Call `getIDs` to see
                a list of currently available engines.
        
        :Returns: A list of the variables names on each engine.
        """
        
        self._checkClientID()
        localBlock = self._reallyBlock()
        result = self._executeRemoteMethod(self._server.keys, self._clientID, localBlock, targets)
        if not localBlock:
            result = PendingResult(self, result)
        return result 
          
    def keysAll(self):
        """List all the variable names defined on each engine/target.
        
        See the docstring for `keys` for full details.         
        """
        return self.keys('all')
    
    def kill(self, targets, controller=False):
        """Kill the engines/targets specified.
        
        This actually stops the engine processes for good.
        
        :Parameters:
            targets : int, list or 'all'
                The engine ids the action will apply to.  Call `getIDs` to see
                a list of currently available engines.
            controller : boolean
                Kill the controller process as well?
        """
        self._checkClientID()
        localBlock = self._reallyBlock()
        result = self._executeRemoteMethod(self._server.kill, self._clientID, localBlock, targets, controller)
        if not localBlock:
            result = PendingResult(self, result)
        return result
    
    def killAll(self, controller=False):
        """Kill all the engines/targets.
        
        See the docstring for `kill` for full details.
        """
        return self.kill('all', controller)
        
    def clearQueue(self, targets):
        """Clear the command queue on targets.
        
        Each engine has a queue associated with it.  This queue lives in the controller
        process.  This command is used to kill all commmands that are waiting in the queue.
        These commands will then errback with `QueueCleared`.  Use `queueStatus` to see the
        commands in the queues.
        
        :Parameters:
            targets : int, list or 'all'
                The engine ids the action will apply to.  Call `getIDs` to see
                a list of currently available engines.    
        """
        
        self._checkClientID()
        result = self._executeRemoteMethod(self._server.clearQueue, self._clientID, targets)
        return result
        
    def clearQueueAll(self):
        """Clear the command queue on all targets.
        
        See the docstring for `clearQueue` for full details.
        """
        return self.clearQueue('all')
    
    def queueStatus(self, targets):
        """Get the status of the command queue on targets.
        
        :Parameters:
            targets : int, list or 'all'
                The engine ids the action will apply to.  Call `getIDs` to see
                a list of currently available engines.
        
        :Returns:  A list of dicts that describe each queue.
        """
        self._checkClientID()
        result = self._executeRemoteMethod(self._server.queueStatus, self._clientID, targets)
        return QueueStatusList(result)
    
    def queueStatusAll(self):
        """Get the status of the command queue on all targets/engines.
        
        See the docstring for `queueStatus` for full details.
        """
        return self.queueStatus('all')
    
    #---------------------------------------------------------------------------
    # IMultiEngine related methods
    #---------------------------------------------------------------------------
    
    def getIDs(self):
        """Get a list of the ids of the engines that are registered."""
        return self._server.getIDs()
    
    #---------------------------------------------------------------------------
    # IEngineCoordinator related methods
    #---------------------------------------------------------------------------
    
    def scatter(self, targets, key, seq, style='basic', flatten=False):
        """Partition and distribute a sequence to a set of targets/engines.
        
        This method partitions a Python sequence and then pushes the partitions
        to a set of engines.
        
        :Parameters:
            targets : int, list or 'all'
                The engine ids the action will apply to.  Call `getIDs` to see
                a list of currently available engines.
            key : str
                What to call the partitions on the engines.
            seq : list, tuple or numpy array
                The sequence to be partitioned and pushed.
            style : str
                The style of partitioning to use.  Only 'basic' is supported
            flatten : boolean
                Should length 1 partitions be flattened to scalars upon pushing.
        """
        self._checkClientID()
        bseq = xmlrpc.Binary(pickle.dumps(seq,2))
        localBlock = self._reallyBlock()
        result = self._executeRemoteMethod(self._server.scatter, self._clientID, 
            localBlock, targets, key, bseq, style, flatten)
        if not localBlock:
            result = PendingResult(self, result)
        return result
        
    def scatterAll(self, key, seq, style='basic', flatten=False):
        """Partition and distribute a sequence to all targets/engines.
        
        See the docstring for `scatter` for full details.
        """
        return self.scatter('all', key, seq, style, flatten)
    
    def gather(self, targets, key, style='basic'):
        """Gather a set of sequence partitions that are distributed on targets.
        
        This method is the inverse of `scatter` and gather parts of an overall
        sequence that are distributed among the engines and reassembles the 
        partitions into a single sequence which is returned.
        
        :Parameters:
            targets : int, list or 'all'
                The engine ids the action will apply to.  Call `getIDs` to see
                a list of currently available engines.
            key : str
                The name of the sequences on the engines.
            style : str
                Only 'basic' is supported currently.
                
        :Returns:  The reassembled sequence.
        """
        self._checkClientID()
        localBlock = self._reallyBlock()
        result = self._executeRemoteMethod(self._server.gather, self._clientID, 
            localBlock, targets, key, style)
        if not localBlock:
            result = PendingResult(self, result)
        return result        
        
    def gatherAll(self, key, style='basic'):
        """Gather a set of sequence partitions that are distributed on all targets.
        
        See the docstring for `gather` for full details.
        """
        return self.gather('all', key, style)


class XMLRPCInteractiveMultiEngineClient(XMLRPCMultiEngineClient, InteractiveMultiEngineClient):
    
    __doc__ = XMLRPCMultiEngineClient.__doc__
    
    def __init__(self, addr):
        XMLRPCMultiEngineClient.__init__(self, addr)
        InteractiveMultiEngineClient.__init__(self)

    __init__.__doc__ = XMLRPCMultiEngineClient.__init__.__doc__
    
