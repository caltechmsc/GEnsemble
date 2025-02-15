# encoding: utf-8
# -*- test-case-name: ipython1.test.test_engineservice -*-
"""A Twisted Service Representation of the IPython core.

The IPython Core exposed to the network is called the Engine.  Its
representation in Twisted in the EngineService.  Interfaces and adapters
are used to abstract out the details of the actual network protocol used.
The EngineService is an Engine that knows nothing about the actual protocol
used.

The EngineService is exposed with various network protocols in modules like:

enginepb.py
enginevanilla.py

As of 12/12/06 the classes in this module have been simplified greatly.  It was 
felt that we had over-engineered things.  To improve the maintainability of the
code we have taken out the ICompleteEngine interface and the completeEngine
method that automatically added methods to engines.

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

import os
import cPickle as pickle
from new import instancemethod

from twisted.application import service
from twisted.internet import defer, reactor
from twisted.python import log, failure, components
import zope.interface as zi

from ipython1.core.shell import InteractiveShell
from ipython1.kernel import newserialized, error, util
from ipython1.kernel.util import gatherBoth, DeferredList


#-------------------------------------------------------------------------------
# Interface specification for the Engine
#-------------------------------------------------------------------------------

class IEngineCore(zi.Interface):
    """The minimal required interface for the IPython Engine.
    
    This interface provides a formal specification of the IPython core.
    All these methods should return deferreds regardless of what side of a
    network connection they are on.
    
    In general, this class simply wraps a shell class and wraps its return
    values as Deferred objects.  If the underlying shell class method raises
    an exception, this class should convert it to a twisted.failure.Failure
    that will be propagated along the Deferred's errback chain.
    
    In addition, Failures are aggressive.  By this, we mean that if a method
    is performing multiple actions (like pulling multiple object) if any
    single one fails, the entire method will fail with that Failure.  It is
    all or nothing. 
    """
    
    id = zi.interface.Attribute("the id of the Engine object")
    
    def execute(lines):
        """Execute lines of Python code.
        
        Returns a dictionary with keys (id, commandIndex, stdin, stdout, stderr)
        upon success.
        
        Returns a failure object if the execution of lines raises an exception.
        """
    
    def push(**namespace):
        """Push dict namespace into the user's namespace.
        
        Returns a deferred to None or a failure.
        """
    
    def pull(*keys):
        """Pulls values out of the user's namespace by keys.
        
        Returns a deferred to tuple objects or a single object.
        
        Raises NameError is any one of objects does not exist.
        """
    
    def getResult(i=None):
        """Get the stdin/stdout/stderr of command i.
        
        Returns a deferred to a dict with keys
        (id, commandIndex, stdin, stdout, stderr).
        
        Raises IndexError if command i does not exist.
        Raises TypeError if i in not an int.
        """
    
    def reset():
        """Reset the shell.
        
        This clears the users namespace.  Won't cause modules to be
        reloaded.  Should also re-initialize certain variables like id.
        """
    
    def kill():
        """Kill the engine by stopping the reactor."""
    
    def keys():
        """Return the top level variables in the users namspace.
        
        Returns a deferred to a dict."""
    

class IEngineSerialized(zi.Interface):
    """Push/Pull methods that take Serialized objects.  
    
    All methods should return deferreds.
    """
    
    def pushSerialized(**namespace):
        """Push a dict of keys and Serialized objects into the user's namespace."""
    
    def pullSerialized(*keys):
        """Pull objects by key from the user's namespace as Serialized.
        
        Returns a list of or one Serialized.
        
        Raises NameError is any one of the objects does not exist.
        """
    
class IEngineBase(IEngineCore, IEngineSerialized):
    """The basic engine interface that EngineService will implement.
    
    This exists so it is easy to specify adapters that adapt to and from the
    API that the basic EngineService implements.
    """
    pass

class IEngineQueued(IEngineBase):
    """Interface for adding a queue to an IEngineBase.  
    
    This interface extends the IEngineBase interface to add methods for managing
    the engine's queue.  The implicit details of this interface are that the 
    execution of all methods declared in IEngineBase should appropriately be
    put through a queue before execution. 
    
    All methods should return deferreds.
    """
    
    def clearQueue():
        """Clear the queue."""
        
    def queueStatus():
        """Get the queued and pending commands in the queue."""
        
    def registerFailureObserver(obs):
        """Register an observer of pending Failures.
        
        The observer must implement IFailureObserver.
        """
    
    def unregisterFailureObserver(obs):
        """Unregister an observer of pending Failures."""

    
    
class IEngineThreaded(zi.Interface):
    """A place holder for threaded commands.  
    
    All methods should return deferreds.
    """
    pass
    
    
#-------------------------------------------------------------------------------
# Functions and classes to implement the EngineService
#-------------------------------------------------------------------------------

class EngineService(object, service.Service):
    """Adapt a IPython shell into a IEngine implementing Twisted Service."""
    
    zi.implements(IEngineBase)
                
    def __init__(self, shellClass=InteractiveShell, mpi=None):
        """Create an EngineService.
        
        shellClass: a subclass of core.InteractiveShell
        mpi:        an mpi module that has rank and size attributes
        """
        self.shellClass = shellClass
        self.shell = self.shellClass()
        self.mpi = mpi
        self.id = None
        if self.mpi is not None:
            log.msg("MPI started with rank = %i and size = %i" % 
                (self.mpi.rank, self.mpi.size))
            self.id = self.mpi.rank
    
    # Make id a property so that the shell can get the updated id
        
    def _setID(self, id):
        self._id = id
        self.shell.update({'id': id})
        
    def _getID(self):
        return self._id
        
    id = property(_getID, _setID)
        
    def startService(self):
        """Start the service and seed the user's namespace."""
        
        self.shell.update({'mpi': self.mpi, 'id' : self.id})
        
    # The IEngine methods.  See the interface for documentation.
    
    def execute(self, lines):
        d = defer.execute(self.shell.execute, lines)
        d.addCallback(self.addIDToResult)
        return d

    def addIDToResult(self, result):
        result['id'] = self.id
        return result

    def push(self, **namespace):
        return defer.execute(self.shell.update, namespace)

    def pull(self, *keys):
        if len(keys) > 1:
            pulledDeferreds = []
            for key in keys:
                pulledDeferreds.append(defer.execute(self.shell.get,key))
            # This will fire on the first failure and log the rest.
            d = gatherBoth(pulledDeferreds, 
                           fireOnOneErrback=1,
                           logErrors=1, 
                           consumeErrors=1)
            return d
        else:
            return defer.execute(self.shell.get, keys[0])
    
    def getResult(self, i=None):
        d = defer.execute(self.shell.getCommand, i)
        d.addCallback(self.addIDToResult)
        return d
    
    def reset(self):
        return defer.execute(self.shell.reset)
    
    def kill(self):
        try:
            reactor.stop()
        except RuntimeError:
            log.msg('The reactor was not running apparently.')
            return defer.fail()
        else:
            return defer.succeed(None)

    def keys(self):
        """Return a list of variables names in the users top level namespace.
        
        This used to return a dict of all the keys/repr(values) in the 
        user's namespace.  This was too much info for the ControllerService
        to handle so it is now just a list of keys.
        """
        
        remotes = []
        for k in self.shell.locals.iterkeys():
            if k not in ['__name__', '__doc__', '__console__', '__builtins__']:
                remotes.append(k)
        return defer.succeed(remotes)

    def pushSerialized(self, **sNamespace):
        ns = {}
        for k,v in sNamespace.iteritems():
            try:
                unserialized = newserialized.IUnSerialized(v)
                ns[k] = unserialized.getObject()
            except:
                return defer.fail()
        return defer.execute(self.shell.update, ns)
    
    def pullSerialized(self, *keys):
        if len(keys) > 1:
            pulledDeferreds = []
            for key in keys:
                d = defer.execute(self.shell.get,key)
                pulledDeferreds.append(d)
            # This will fire on the first failure and log the rest.
            dList = gatherBoth(pulledDeferreds, 
                              fireOnOneErrback=1,
                              logErrors=0, 
                              consumeErrors=1)
            @dList.addCallback
            def packThemUp(values):
                serials = []
                for v in values:
                    try:
                        serials = newserialized.serialize(v)
                    except:
                        return defer.fail(failure.Failure())
                return dict(zip(keys, values))
            return packThemUp
        else:
            key = keys[0]
            d = defer.execute(self.shell.get, key)
            d.addCallback(newserialized.serialize)
            return d
    
    
def queue(methodToQueue):
    def queuedMethod(this, *args, **kwargs):
        name = methodToQueue.__name__
        return this.submitCommand(Command(name, *args, **kwargs))
    return queuedMethod
    
class QueuedEngine(object):
    """Adapt an IEngineBase to an IEngineQueued by wrapping it.
    
    The resulting object will implement IEngineQueued which extends
    IEngineCore which extends (IEngineBase, IEngineSerialized). 
    
    This seems like the best way of handling it, but I am not sure.  The
    other option is to have the various base interfaces be used like
    mix-in intefaces.  The problem I have with this is adpatation is
    more difficult and complicated because there can be can multiple
    original and final Interfaces. 
    """
    
    zi.implements(IEngineQueued)
    
    def __init__(self, engine):
        """Create a QueuedEngine object from an engine
        
        engine:       An implementor of IEngineCore and IEngineSerialized
        keepUpToDate: whether to update the remote status when the 
                      queue is empty.  Defaults to False.
        """

        # This is the right way to do these tests rather than 
        # IEngineCore in list(zi.providedBy(engine)) which will only 
        # picks of the interfaces that are directly declared by engine.
        assert IEngineBase.providedBy(engine), \
            "engine passed to QueuedEngine doesn't provide IEngineBase"

        self.engine = engine
        self.id = engine.id
        self.queued = []
        self.history = {}
        self.engineStatus = {}
        self.currentCommand = None
        self.failureObservers = []
        
    # Queue management methods.  You should not call these directly
    
    def submitCommand(self, cmd):
        """Submit command to queue."""
        
        d = defer.Deferred()
        cmd.setDeferred(d)
        if self.currentCommand is not None:
            if self.currentCommand.finished:
                self.currentCommand = cmd
                self.runCurrentCommand()
            else:  # command is still running  
                self.queued.append(cmd)
        else:
            self.currentCommand = cmd
            self.runCurrentCommand()
        return d
    
    def runCurrentCommand(self):
        """Run current command."""
        
        cmd = self.currentCommand
        f = getattr(self.engine, cmd.remoteMethod, None)
        if f:
            d = f(*cmd.args, **cmd.kwargs)
            if cmd.remoteMethod is 'execute':
                d.addCallback(self.saveResult)
            d.addCallback(self.finishCommand)
            d.addErrback(self.abortCommand)
        else:
            return defer.fail(AttributeError(cmd.remoteMethod))
    
    def _flushQueue(self):
        """Pop next command in queue and run it."""
        
        if len(self.queued) > 0:
            self.currentCommand = self.queued.pop(0)
            self.runCurrentCommand()
    
    def saveResult(self, result):
        """Put the result in the history."""
        
        self.history[result['commandIndex']] = result
        return result
    
    def finishCommand(self, result):
        """Finish currrent command."""
        
        # The order of these commands is absolutely critical.
        self.currentCommand.handleResult(result)
        self.currentCommand.finished = True
        self._flushQueue()
        return result
    
    def abortCommand(self, reason):
        """Abort current command.
        
        This eats the Failure but first passes it onto the Deferred that the 
        user has.
        
        It also clear out the queue so subsequence commands don't run.
        """

        # The order of these 3 commands is absolutely critical.  The currentCommand
        # must first be marked as finished BEFORE the queue is cleared and before
        # the current command is sent the failure.
        # Also, the queue must be cleared BEFORE the current command is sent the Failure
        # otherwise the errback chain could trigger new commands to be added to the 
        # queue before we clear it.  We should clear ONLY the commands that were in
        # the queue when the error occured. 
        self.currentCommand.finished = True
        self.clearQueue()
        self.currentCommand.handleError(reason)
        
        return None
    
    #---------------------------------------------------------------------------
    # IEngineCore methods
    #---------------------------------------------------------------------------
    
    @queue
    def execute(self, lines):
        pass

    @queue
    def push(self, **namespace):
        pass      
    
    @queue
    def pull(self, *keys):
        pass
        
    def getResult(self, i=None):
        if i is None:
            i = max(self.history.keys()+[None])

        cmd = self.history.get(i, None)
        # Uncomment this line to disable chaching of results
        #cmd = None
        if cmd is None:
            return self.submitCommand(Command('getResult', i))
        else:
            return defer.succeed(cmd)
        
    def reset(self):
        self.clearQueue()
        self.history = {}  # reset the cache - I am not sure we should do this
        return self.submitCommand(Command('reset'))
    
    def kill(self):
        self.clearQueue()
        return self.submitCommand(Command('kill'))
    
    @queue
    def keys(self):
        pass
    
    #---------------------------------------------------------------------------
    # IEngineSerialized methods
    #---------------------------------------------------------------------------

    @queue
    def pushSerialized(self, **namespace):
        pass
        
    @queue
    def pullSerialized(self, *keys):
        pass
    
    #---------------------------------------------------------------------------
    # IQueuedEngine methods
    #---------------------------------------------------------------------------
    
    def clearQueue(self):
        """Clear the queue, but doesn't cancel the currently running commmand."""
        
        for cmd in self.queued:
            cmd.deferred.errback(failure.Failure(error.QueueCleared()))
        self.queued = []
        return defer.succeed(True)
    
    def queueStatus(self):
        if self.currentCommand is not None:
            if self.currentCommand.finished:
                pending = repr(None)
            else:
                pending = repr(self.currentCommand)
        else:
            pending = repr(None)
        dikt = {'queue':map(repr,self.queued), 'pending':pending}
        return defer.succeed(dikt)
        
    def registerFailureObserver(obs):
        self.failureObservers.append(obs)
    
    def unregisterFailureObserver(obs):
        self.failureObservers.remove(obs)
    

# Now register QueuedEngine as an adpater class that makes an IEngineBase into a
# IEngineQueued.  
components.registerAdapter(QueuedEngine, IEngineBase, IEngineQueued)
    

class Command(object):
    """A command object that encapslates queued commands.
    
    This class basically keeps track of a command that has been queued
    in a QueuedEngine.  It manages the deferreds and hold the method to be called
    and the arguments to that method.
    """
    
    
    def __init__(self, remoteMethod, *args, **kwargs):
        """Build a new Command object."""
        
        self.remoteMethod = remoteMethod
        self.args = args
        self.kwargs = kwargs
        self.finished = False
    
    def setDeferred(self, d):
        """Sets the deferred attribute of the Command."""  
          
        self.deferred = d
    
    def __repr__(self):
        if not self.args:
            args = ''
        else:
            args = str(self.args)[1:-2]  #cut off (...,)
        for k,v in self.kwargs.iteritems():
            if args:
                args += ', '
            args += '%s=%r' %(k,v)
        return "%s(%s)" %(self.remoteMethod, args)
    
    def handleResult(self, result):
        """When the result is ready, relay it to self.deferred."""
        
        self.deferred.callback(result)
    
    def handleError(self, reason):
        """When an error has occured, relay it to self.deferred."""
        
        self.deferred.errback(reason)

