# encoding: utf-8
# -*- test-case-name: ipython1.test.test_taskcontrollerxmlrpc -*-
"""An XML-RPC interface to a TaskController.

This class lets XML-RPC clients talk to a TaskController.
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

from ipython1.kernel import error, task as Task, taskclient
from ipython1.kernel.xmlrpcutil import Transport

#-------------------------------------------------------------------------------
# The Controller side of things
#-------------------------------------------------------------------------------

# This is used by twisted.web2 to determine the timeout between different 
# requests by a single client.
BETWEEN_REQUESTS_TIMEOUT = 15*60


class IXMLRPCTaskController(Interface):
    """XML-RPC interface to task controller.
        
    See the documentation of ITaskController for documentation about the methods.
    """
    def xmlrpc_run(request, binTask):
        """"""
    
    def xmlrpc_abort(request, taskID):
        """"""
        
    def xmlrpc_getTaskResult(request, taskID, block=False):
        """"""
        
    def xmlrpc_barrier(request, taskIDs):
        """"""


class XMLRPCTaskControllerFromTaskController(xmlrpc.XMLRPC):
    """XML-RPC attachmeot for controller.
        
    See IXMLRPCTaskController and ITaskController (and its children) for documentation. 
    """
    implements(IXMLRPCTaskController)
    
    addSlash = True
    
    def __init__(self, taskController):
        xmlrpc.XMLRPC.__init__(self)
        self.taskController = taskController
    
    #---------------------------------------------------------------------------
    # Non interface methods
    #---------------------------------------------------------------------------
    
    def packageFailure(self, f):
        f.cleanFailure()
        return self.packageSuccess(f)
    
    def packageSuccess(self, obj):
        # print 'returning: ',obj
        serial = pickle.dumps(obj, 2)
        return xmlrpc.Binary(serial)
    
    #---------------------------------------------------------------------------
    # ITaskController related methods
    #---------------------------------------------------------------------------
    
    def xmlrpc_run(self, request, binTask):
        try:
            task = pickle.loads(binTask.data)
        except:
            d = defer.fail(pickle.UnPickleableError("Could not unmarshal task"))
        else:
            d = self.taskController.run(task)
        d.addCallback(self.packageSuccess)
        d.addErrback(self.packageFailure)
        return d
    
    def xmlrpc_abort(self, request, taskID):
        d = self.taskController.abort(taskID)
        d.addCallback(self.packageSuccess)
        d.addErrback(self.packageFailure)
        return d
        
    def xmlrpc_getTaskResult(self, request, taskID, block=False):
        d = self.taskController.getTaskResult(taskID, block)
        d.addCallback(self.packageSuccess)
        d.addErrback(self.packageFailure)
        return d

    def xmlrpc_barrier(self, request, taskIDs):
        d = self.taskController.barrier(taskIDs)
        d.addCallback(self.packageSuccess)
        d.addErrback(self.packageFailure)
        return d        

components.registerAdapter(XMLRPCTaskControllerFromTaskController,
            Task.TaskController, IXMLRPCTaskController)


class IXMLRPCTaskControllerFactory(Interface):
    pass

def XMLRPCServerFactoryFromTaskController(taskController):
    """Adapt a TaskController to a XMLRPCServerFactory."""
    s = server.Site(IXMLRPCTaskController(taskController))
    return channel.HTTPFactory(s, betweenRequestsTimeOut=BETWEEN_REQUESTS_TIMEOUT)


components.registerAdapter(XMLRPCServerFactoryFromTaskController,
            Task.TaskController, IXMLRPCTaskControllerFactory)
        

#-------------------------------------------------------------------------------
# The Client side of things
#-------------------------------------------------------------------------------

class XMLRPCTaskClient(object):
    """XML-RPC based TaskController client that implements ITaskController.
        
    :Parameters:
        addr : (ip, port)
            The ip (str) and port (int) tuple of the `TaskController`.  
    """
    implements(Task.ITaskController)
    
    #---------------------------------------------------------------------------
    # Begin copy from XMLRPCMultiEngineClient
    # Should these methods be in a base XMLRPCClient class?
    #---------------------------------------------------------------------------
    
    def __init__(self, addr):
        self.addr = addr
        self.url = 'http://%s:%s/' % self.addr
        self._server = xmlrpclib.ServerProxy(self.url, transport=Transport(), 
            verbose=0)
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
      
    #---------------------------------------------------------------------------
    # ITaskController related methods
    #---------------------------------------------------------------------------
    def run(self, task):
        """Run a task on the `TaskController`.
                
        :Parameters:
            task : a `Task` object
        
        The Task object is created using the following signature:
        
        Task(expression, resultNames=None, setupNS={}, clearBefore=False, 
            clearAfter=False, retries=0, **options):)

        The meaning of the arguments is as follows:

        :Task Parameters:
            expression : str
                A str that is valid python code that is the task.
            resultNames : str or list of str 
                The names of objects to be pulled as results.  If not specified, 
                will return {'result', None}
            setupNS : dict
                A dict of objects to be pushed into the engines namespace before
                execution of the expression.
            clearBefore : boolean
                Should the engine's namespace be cleared before the task is run.
                Default=False.
            clearAfter : boolean 
                Should the engine's namespace be cleared after the task is run.
                Default=False.
            retries : int
                The number of times to resumbit the task if it fails.  Default=0.
            options : dict
                Any other keyword options for more elaborate uses of tasks
            
        :Returns: The int taskID of the submitted task.
        """
        assert isinstance(task, Task.Task), "task must be a Task object!"
        binTask = xmlrpc.Binary(pickle.dumps(task,2))
        result = self._executeRemoteMethod(self._server.run, binTask)
        return result
    
    def getTaskResult(self, taskID, block=None):
        """The task result by taskID.
        
        :Parameters:
            taskID : int
                The taskID of the task to be retrieved.
            block : boolean
                Should I block until the task is done?
        """
        localBlock = self._reallyBlock(block)
        result = self._executeRemoteMethod(self._server.getTaskResult, taskID, localBlock)
        return result
    
    def abort(self, taskID):
        """Abort a task by taskID.
        
        :Parameters:
            taskID : int
                The taskID of the task to be aborted.
            block : boolean
                Should I block until the task is aborted.        
        """
        result = self._executeRemoteMethod(self._server.abort, taskID)
        return result
        
    def barrier(self, taskIDs):
        """Block until all tasks are completed.
        
        :Parameters:
            taskIDs : list, tuple
                A sequence of taskIDs to block on.
        """
        result = self._executeRemoteMethod(self._server.barrier, taskIDs)
    

components.registerAdapter(XMLRPCTaskClient, 
        xmlrpclib.ServerProxy, Task.ITaskController)
    

class XMLRPCInteractiveTaskClient(XMLRPCTaskClient, taskclient.InteractiveTaskClient):
    pass

