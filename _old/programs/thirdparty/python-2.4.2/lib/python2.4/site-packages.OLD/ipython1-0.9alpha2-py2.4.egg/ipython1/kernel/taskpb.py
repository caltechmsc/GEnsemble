# encoding: utf-8
# -*- test-case-name: ipython1.test.test_taskcontrollerpb -*-
"""
A PB interface to a TaskController.
Ken Kinder <ken@kenkinder.com>

TO DO:

  - Client classes(?) that make pickling unnecessary or transparent.
  
  - Serializing errors/Failure objects. (Twisted considers its own errors
    unsafe. go figure...)
  
  - Aborting processes -- there is probably a Perspective Broker (tm) way to
    do this.

  - Send taskId's back on deferred stuff(??)
"""

__docformat__ = "restructuredtext en"

#from ipython1.external.twisted.web2 import xmlrpc, server, channel
from ipython1.kernel import error, task as Task, taskclient
from ipython1.kernel.multiengineclient import PendingResult
from ipython1.kernel.xmlrpcutil import Transport
from ipython1.kernel.pbutil import packageFailure, unpackageFailure
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from twisted.cred.credentials import UsernamePassword
from twisted.cred.portal import IRealm, Portal
from twisted.internet import defer, reactor
from twisted.python import components, failure
from twisted.python.failure import Failure
from twisted.spread import pb
from zope.interface import Interface, implements
import cPickle as pickle

#-------------------------------------------------------------------------------
# CONTROLLER CLASSES
#-------------------------------------------------------------------------------

class IPBTaskController(Interface):
    ''
    def perspective_run(task):
        ''
    
class PBTaskControllerFromTaskController(pb.Avatar):
    ''
    implements(IPBTaskController)
    
    def __init__(self, taskController):
        self.staskcontroller = taskController
    
    def packageFailure(self, result):
        ### TODO: This is weird... Find out why.
        if type(result) is tuple and len(result) == 2 and isinstance(result[1], Failure):
            return packageFailure(result[1])
        else:
            return result
    
    def perspective_run(self, task):
        d = self.staskcontroller.run(pickle.loads(task))
        d.addCallback(self.staskcontroller.getTaskResult, True)
        d.addCallback(self.packageFailure)
        return d
    
    def logout(self):
        #### TODO: This should probably do something meaningful.
        print self, "logged out"
    
class IPythonRealm(object):
    implements(IRealm)

    def __init__(self, taskController):
        self.taskController = taskController

    def requestAvatar(self, avatarId, mind, *interfaces):
        if pb.IPerspective in interfaces:
            avatar = PBTaskControllerFromTaskController(self.taskController)
            return pb.IPerspective, avatar, avatar.logout
        else:
            raise NotImplementedError("no interface")

class IPBTaskControllerFactory(Interface):
    pass

def PBServerFactoryFromTaskController(taskController):
    #### TODO: Real authentication here
    portal = Portal(IPythonRealm(taskController))
    checker = InMemoryUsernamePasswordDatabaseDontUse()
    checker.addUser("guest", "guest")
    portal.registerChecker(checker)
    return pb.PBServerFactory(portal)

components.registerAdapter(PBTaskControllerFromTaskController,
            Task.TaskController, IPBTaskController)
components.registerAdapter(PBServerFactoryFromTaskController,
            Task.TaskController, IPBTaskControllerFactory)

#-------------------------------------------------------------------------------
# CLIENT CLASSES
#-------------------------------------------------------------------------------
class PBTaskClient(object):
    """
    XMLRPC based TaskController client that implements ITaskController.
    """
    implements(Task.ITaskController)
    def __init__(self, perspective):
        self.perspective = perspective
    
    def run(self, task):
        assert isinstance(task, Task.Task), "task must be a Task object!"
        d = self.perspective.callRemote('run', pickle.dumps(task, 2))
        d.addCallback(unpackageFailure)
        return d
    
    def getTaskResult(self, taskID):
        raise ImportError
    
    def abort(self, taskID):
        raise NotImplementedError
