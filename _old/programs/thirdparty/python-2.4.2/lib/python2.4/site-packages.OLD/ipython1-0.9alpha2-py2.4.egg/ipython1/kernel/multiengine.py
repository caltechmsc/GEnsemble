# encoding: utf-8
# -*- test-case-name: ipython1.test.test_multiengine -*-
"""Adapt the IPython ControllerServer to IMultiEngine.

This module provides classes that adapt a ControllerService to the 
IMultiEngine interface.  This interface is a basic interactive interface
for working with a set of engines where it is desired to have explicit 
access to each registered engine.  

The classes here are exposed to the network in files like:

* multienginevanilla.py
* multienginepb.py
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

from new import instancemethod
from twisted.application import service
from twisted.internet import defer, reactor
from twisted.python import log, components, failure
from zope.interface import Interface, implements, Attribute

from ipython1.kernel.util import gatherBoth
from ipython1.kernel import map as Map
from ipython1.kernel import error
from ipython1.kernel.controllerservice import \
    ControllerAdapterBase, \
    ControllerService, \
    IControllerBase
from ipython1.kernel.pendingdeferred import PendingDeferredAdapter, twoPhase

#-------------------------------------------------------------------------------
# Interfaces for the MultiEngine representation of a controller
#-------------------------------------------------------------------------------

class IEngineMultiplexer(Interface):
    """Interface to multiple engines implementing IEngineCore/Serialized/Queued.
    
    This class simply acts as a multiplexer of methods that are in the 
    various IEngines* interfaces.  Thus the methods here are jut like those 
    in the IEngine* interfaces, but with an extra first argument, targets.  
    The targets argument can have the following forms:
    
    * targets = 10            # Engines are indexed by ints
    * targets = [0,1,2,3]     # A list of ints
    * targets = 'all'         # A string to indicate all targets

    If targets is bad in any way, an InvalidEngineID will be raised.  This
    includes engines not being registered.

    All IEngineMultiplexer multiplexer methods must return a Deferred to a list 
    with length equal to the number of targets.  The elements of the list will 
    correspond to the return of the corresponding IEngine method.
    
    Failures are aggressive, meaning that if an action fails for any target, 
    the overall action will fail immediately with that Failure.
    
    :Parameters:
        targets : int, list of ints, or 'all'
            Engine ids the action will apply to.

    :Returns: Deferred to a list of results for each engine.

    :Exception:
        InvalidEngineID
            If the targets argument is bad or engines aren't registered.
        NoEnginesRegistered
            If there are no engines registered and targets='all'
    """
        
    #---------------------------------------------------------------------------
    # Mutiplexed methods
    #---------------------------------------------------------------------------
     
    def execute(targets, lines):
        """Execute lines of Python code on targets.
              
        See the class docstring for information about targets and possible
        exceptions this method can raise.
              
        :Parameters:
            lines : str
                String of python code to be executed on targets.
        """
    
    def executeAll(lines):
        """Execute on all targets."""
        
    def push(targets, **namespace):
        """Push dict namespace into the user's namespace on targets.

        See the class docstring for information about targets and possible
        exceptions this method can raise.
        
        :Parameters:
            namspace : dict
                Dict of key value pairs to be put into the users namspace.
        """
        
    def pushAll(**namespace):
        """Push to all targets."""
        
    def pull(targets, *keys):
        """Pull values out of the user's namespace on targets by keys.

        See the class docstring for information about targets and possible
        exceptions this method can raise.
        
        :Parameters:
            keys : tuple of strings
                Sequence of keys to be pulled from user's namespace.
        """
        
    def pullAll(*keys):
        """Pull from all targets."""
                
    def getResult(targets, i=None):
        """Get the result for command i from targets.

        See the class docstring for information about targets and possible
        exceptions this method can raise.

        :Parameters:
            i : int or None
                Command index or None to indicate most recent command.                
        """
        
    def getResultAll(i=None):
        """Get the result tuple for command i from all targets."""
        
    def reset(targets):
        """Reset targets.
        
        This clears the users namespace of the Engines, but won't cause
        modules to be reloaded.
        """
        
    def resetAll():
        """Reset all targets."""
        
    def keys(targets):
        """Get variable names defined in user's namespace on targets."""
        
    def keysAll():
        """Get variable names on all targets."""
        
    def kill(targets, controller=False):
        """Kill the targets Engines and possibly the controller.
        
        :Parameters:
            controller : boolean
                Should the controller be killed as well.  If so all the 
                engines will be killed first no matter what targets is.
        """
        
    def killAll(controller=False):
        """Kill all the Engines and possibly the controller."""
        
    def pushSerialized(targets, **namespace):
        """Push a namespace of Serialized objects to targets.
        
        :Parameters:
            namespace : dict
                A dict whose keys are the variable names and whose values
                are serialized version of the objects.
        """
        
    def pushSerializedAll(**namespace):
        """Push Serialized to all targets."""
        
    def pullSerialized(targets, *keys):
        """Pull Serialized objects by keys from targets.
        
        :Parameters:
            keys : tuple of strings
                Sequence of variable names to pull as serialized objects.
        """
        
    def pullSerializedAll(*keys):
        """Pull Serialized from all targets."""
        
    def clearQueue(targets):
        """Clear the queue of pending command for targets."""
        
    def clearQueueAll():
        """Clear the queue of pending commands for all targets."""
        
    def queueStatus(targets):
        """Get the status of the queue on the targets."""
        
    def queueStatusAll():
        """Get the status of all the queues."""
        
class IEngineCoordinator(Interface):
    """Methods that work on multiple engines explicitly."""
        
    #---------------------------------------------------------------------------
    # Coordinated methods
    #---------------------------------------------------------------------------
         
    def scatter(targets, key, seq, style='basic', flatten=False):
        """Partition and distribute a sequence to targets.
        
        :Parameters:
            key : str
                The variable name to call the scattered sequence.
            seq : list, tuple, array
                The sequence to scatter.  The type should be preserved.
            style : string
                A specification of how the sequence is partitioned.  Currently 
                only 'basic' is implemented.
            flatten : boolean
                Should single element sequences be converted to scalars.
        """
    
    def scatterAll(key, seq, style='basic', flatten=False):
        """Scatter to all targets."""
    
    def gather(targets, key, style='basic'):
        """Gather object key from targets.

        :Parameters:
            key : string
                The name of a sequence on the targets to gather.
            style : string
                A specification of how the sequence is partitioned.  Currently 
                only 'basic' is implemented.                
        """
    
    def gatherAll(key, style='basic'):
        """Gather from all targets."""
        
        
class IMultiEngine(IEngineMultiplexer, 
                   IEngineCoordinator):
    """A controller that exposes an explicit interface to all of its engines.
    
    This is the primary inteface for interactive usage.
    """

    def getIDs():
        """Return list of currently registered ids.
        
        Unlike other IMultiEngine methods, this does not return a deferred.
        It actually returns a list of ids.
        
        :Returns:  A list of registered engine ids.
        """
        
        
#-------------------------------------------------------------------------------
# Implementation of the ControllerService
#-------------------------------------------------------------------------------
        
class MultiEngine(ControllerAdapterBase):
    """The representation of a ControllerService as a IMultiEngine.
    
    Although it is not implemented currently, this class would be where a
    client/notification API is implemented.  It could inherit from something
    like results.NotifierParent and then use the notify method to send
    notifications.
    """
    
    implements(IMultiEngine)
    
    def __init(self, controller):
        ControllerAdapterBase.__init__(self, controller)

    #---------------------------------------------------------------------------
    # Helper methods
    #---------------------------------------------------------------------------

    def engineList(self, targets):
        """Parse the targets argument into a list of valid engine objects.
        
        :Parameters:
            targets : int, list of ints or 'all'
                The targets argument to be parsed.
                
        :Returns: List of engine objects.
        
        :Exception:
            InvalidEngineID
                If targets is not valid or if an engine is not registered.
        """
        if isinstance(targets, int):
            if targets not in self.engines.keys():
                log.msg("Engine with id %d is not registered" % targets)
                raise error.InvalidEngineID("Engine with id %d is not registered" % targets)
            else: 
                return [self.engines[targets]]
        elif isinstance(targets, (list, tuple)):
            for id in targets:
                if id not in self.engines.keys():
                    log.msg("Engine with id %s is not registered" % repr(id))
                    raise error.InvalidEngineID("Engine with id %s is not registered" % repr(id))  
            return map(self.engines.get, targets)
        elif targets == 'all':
            eList = self.engines.values()
            if len(eList) == 0:
                msg = """There are no engines registered.
                     Check the logs in ~/.ipython/log if you think there should have been."""
                raise error.NoEnginesRegistered(msg)
            else:
                return eList
        else:
            raise error.InvalidEngineID("targets argument is not an int, list of ints or 'all'")
    
    def _performOnEngines(self, methodName, targets, *args, **kwargs):
        """Calls a method on engines and returns deferred to list of results.
        
        :Parameters:
            methodName : str
                Name of the method to be called.
            targets : int, list of ints, 'all'
                The targets argument to be parsed into a list of engine objects.
            args
                The positional keyword arguments to be passed to the engines.
            kwargs
                The keyword arguments passed to the method
                
        :Returns: List of deferreds to the results on each engine
        
        :Exception:
            InvalidEngineID
                If the targets argument is bad in any way.
            AttributeError
                If the method doesn't exist on one of the engines.
        """
        log.msg("Performing %s on %s" % (methodName, targets))
        # This will and should raise if targets is not valid!
        engines = self.engineList(targets)
        dList = []
        for e in engines:
            meth = getattr(e, methodName, None)
            if meth is not None:
                dList.append(meth(*args, **kwargs))
            else:
                raise AttributeError("Engine %i does not have method %s" % (engine.id, methodName))
        return dList
    
    def _performOnEnginesAndGatherBoth(self, methodName, targets, *args, **kwargs):
        """Called _performOnEngines and wraps result/exception into deferred."""
        try:
            dList = self._performOnEngines(methodName, targets, *args, **kwargs)
        except (error.InvalidEngineID, AttributeError, error.NoEnginesRegistered):
            return defer.fail(failure.Failure())
        else:
            return gatherBoth(dList, 
                              fireOnOneErrback=1,
                              consumeErrors=1,
                              logErrors=0)
              
    #---------------------------------------------------------------------------
    # General IMultiEngine methods
    #---------------------------------------------------------------------------
    
    def getIDs(self):
        return self.engines.keys()
    
    #---------------------------------------------------------------------------
    # IEngineMultiplexer methods
    #---------------------------------------------------------------------------
        
    def execute(self, targets, lines):
        return self._performOnEnginesAndGatherBoth('execute', targets, lines)
    
    def executeAll(self, lines):
        return self.execute('all', lines)
    
    def push(self, targets, **ns):
        return self._performOnEnginesAndGatherBoth('push', targets, **ns)
    
    def pushAll(self, **ns):
        return self.push('all', **ns)
        
    def pull(self, targets, *keys):
        return self._performOnEnginesAndGatherBoth('pull', targets, *keys)
    
    def pullAll(self, *keys):
        return self.pull('all', *keys)
    
    def getResult(self, targets, i=None):
        return self._performOnEnginesAndGatherBoth('getResult', targets, i)
                
    def getResultAll(self, i=None):
        return self.getResult('all', i)
    
    def reset(self, targets):
        return self._performOnEnginesAndGatherBoth('reset', targets)

    def resetAll(self):
        return self.reset('all')
    
    def keys(self, targets):
        return self._performOnEnginesAndGatherBoth('keys', targets)

    def keysAll(self):
        return self.keys('all')
    
    def kill(self, targets, controller=False):
        if controller:
            targets = 'all'
        d = self._performOnEnginesAndGatherBoth('kill', targets)
        if controller:
            log.msg("Killing controller")
            d.addCallback(lambda _: reactor.callLater(2.0, reactor.stop))
            # Consume any weird stuff coming back
            d.addBoth(lambda _: None)
        return d
        
    def killAll(self, controller=False):
        return self.kill('all', controller)
    
    def pushSerialized(self, targets, **namespace):
        for k, v in namespace.iteritems():
            log.msg("Pushed object %s is %f MB" % (k, v.getDataSize()))
        d = self._performOnEnginesAndGatherBoth('pushSerialized', targets, **namespace)      
        return d
                              
    def pushSerializedAll(self, **namespace):
        return self.pushSerialized('all', **namespace)
        
    def pullSerialized(self, targets, *keys):
        try:
            dList = self._performOnEngines('pullSerialized', targets, *keys)
        except (error.InvalidEngineID, AttributeError, error.NoEnginesRegistered):
            return defer.fail(failure.Failure())
        else:
            for d in dList:
                d.addCallback(self._logSizes)
            return gatherBoth(dList, 
                              fireOnOneErrback=1,
                              consumeErrors=1,
                              logErrors=0)  
                              
    def _logSizes(self, listOfSerialized):
        if isinstance(listOfSerialized, (list, tuple)):
            for s in listOfSerialized:
                log.msg("Pulled object is %f MB" % s.getDataSize())
        else:
            log.msg("Pulled object is %f MB" % listOfSerialized.getDataSize())
        return listOfSerialized
    
    def pullSerializedAll(self, *keys):
        return self.pullSerialized('all', *keys)
    
    def clearQueue(self, targets):
        return self._performOnEnginesAndGatherBoth('clearQueue', targets)         
                              
    def clearQueueAll(self):
        return self.clearQueue('all')
    
    def queueStatus(self, targets):
        log.msg("Getting queue status on %s" % targets)
        try:
            engines = self.engineList(targets)
        except (error.InvalidEngineID, AttributeError, error.NoEnginesRegistered):
            return defer.fail(failure.Failure())            
        else:
            dList = []
            for e in engines:
                dList.append(e.queueStatus().addCallback(lambda s:(e.id, s)))
            return gatherBoth(dList, 
                              fireOnOneErrback=1,
                              consumeErrors=1,
                              logErrors=0)  
                          
    def queueStatusAll(self):
        return self.queueStatus('all')

    #---------------------------------------------------------------------------
    # IEngineCoordinator methods
    #---------------------------------------------------------------------------

    def scatter(self, targets, key, seq, style='basic', flatten=False):
        log.msg("Scattering %s to %s" % (key, targets))
        try:
            engines = self.engineList(targets)
        except (error.InvalidEngineID, AttributeError, error.NoEnginesRegistered):
            return defer.fail(failure.Failure())
        else:
            nEngines = len(engines)    
            mapClass = Map.styles[style]
            mapObject = mapClass()
            dList = []
            for index, engine in enumerate(engines):
                partition = mapObject.getPartition(seq, index, nEngines)
                if flatten and len(partition) == 1:    
                    dList.append(engine.push(**{key: partition[0]}))
                else:
                    dList.append(engine.push(**{key: partition}))
            return gatherBoth(dList, 
                              fireOnOneErrback=1,
                              consumeErrors=1,
                              logErrors=0)  
                              
    def scatterAll(self, key, seq, style='basic', flatten=False):
        return self.scatter('all', key, seq, style, flatten)
    
    def gather(self, targets, key, style='basic'):
        """gather a distributed object, and reassemble it"""
        log.msg("Gathering %s from %s" % (key, targets))
        try:
             engines = self.engineList(targets)
        except (error.InvalidEngineID, AttributeError, error.NoEnginesRegistered):
            return defer.fail(failure.Failure())
        else:
            nEngines = len(engines)    
            dList = []
            for e in engines:
                dList.append(e.pull(key))    
            mapClass = Map.styles[style]
            mapObject = mapClass()
            d = gatherBoth(dList, 
                           fireOnOneErrback=1,
                           consumeErrors=1,
                           logErrors=0)  
            return d.addCallback(mapObject.joinPartitions)
    
    def gatherAll(self, key, style='basic'):
        return self.gather('all', key, style)


components.registerAdapter(MultiEngine, 
                           IControllerBase, 
                           IMultiEngine)


#-------------------------------------------------------------------------------
# Synchronous MultiEngine
#-------------------------------------------------------------------------------

class ISynchronousMultiEngine(Interface):
    """Synchronous, two-phase version of IMultiEngine.
    
    Methods in this interface are identical to those of IMultiEngine, but they
    take two additional arguments:
    
    execute(targets, lines) -> execute(clientID, block, targets, lines)
    
    :Parameters:
        clientID : int
            The id that a client has been given by calling `registerClient`
        block : boolean
            Should the method return a deferred to a deferredID or the 
            actual result.  If block=False a deferred to a deferredId is 
            returned and the user must call `getPendingDeferred` at a later
            point.  If block=True, a deferred to the actual result comes back.
    """
    pass


class SynchronousMultiEngine(PendingDeferredAdapter):
    """Adapt an `IMultiEngine` -> `ISynchronousMultiEngine`"""
    
    implements(ISynchronousMultiEngine)
    
    def __init__(self, multiengine):
        self.multiengine = multiengine
        PendingDeferredAdapter.__init__(self)

    #---------------------------------------------------------------------------
    # Decorated pending deferred methods
    #---------------------------------------------------------------------------

    @twoPhase
    def execute(self, targets, lines):
        return self.multiengine.execute(targets, lines)

    @twoPhase
    def push(self, targets, **namespace):
        return self.multiengine.push(targets, **namespace)
        
    @twoPhase
    def pull(self, targets, *keys):
        return self.multiengine.pull(targets, *keys)
        
    @twoPhase
    def getResult(self, targets, i=None):
        return self.multiengine.getResult(targets, i=None)
        
    @twoPhase
    def reset(self, targets):
        return self.multiengine.reset(targets)
        
    @twoPhase
    def keys(self, targets):
        return self.multiengine.keys(targets)

    @twoPhase
    def kill(self, targets, controller=False):
        return self.multiengine.kill(targets, controller)
        
    @twoPhase
    def pushSerialized(self, targets, **namespace):
        return self.multiengine.pushSerialized(targets, **namespace)
        
    @twoPhase
    def pullSerialized(self, targets, *keys):
        return self.multiengine.pullSerialized(targets, *keys)
        
    @twoPhase
    def clearQueue(self, targets):
        return self.multiengine.clearQueue(targets)
        
    @twoPhase
    def queueStatus(self, targets):
        return self.multiengine.queueStatus(targets)

    @twoPhase
    def scatter(self, targets, key, seq, style='basic', flatten=False):
        return self.multiengine.scatter(targets, key, seq, style, flatten)

    @twoPhase
    def gather(self, targets, key, style='basic'):
        return self.multiengine.gather(targets, key, style)
        
    #---------------------------------------------------------------------------
    # IMultiEngine methods
    #---------------------------------------------------------------------------

    def getIDs(self):
        """Return a list of registered engine ids.
        
        Does not return a deferred.
        """
        return self.multiengine.getIDs()

components.registerAdapter(SynchronousMultiEngine, IMultiEngine, ISynchronousMultiEngine)