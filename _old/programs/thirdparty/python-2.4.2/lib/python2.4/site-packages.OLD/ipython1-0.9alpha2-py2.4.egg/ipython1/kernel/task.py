# encoding: utf-8
# -*- test-case-name: ipython1.test.test_task -*-
"""Task farming representation of the ControllerService.
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

import zope.interface as zi
from twisted.internet import defer, reactor
from twisted.python import components, log, failure

from ipython1.kernel import engineservice as es, error
from ipython1.kernel import controllerservice as cs
from ipython1.kernel.pendingdeferred import PendingDeferredAdapter, twoPhase
from ipython1.kernel.util import gatherBoth, DeferredList

def _printer(r):
    print "_print: ",r
    return r

class Task(object):
    """Our representation of a task for the `TaskController` interface.

    The user should create instances of this class to represent a task that 
    needs to be done.
    
    :Parameters:
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
    
    Examples
    --------
    
    >>> t = Task('dostuff(args)')
    >>> t = Task('a=5', resultNames='a')
    >>> t = Task('a=5\nb=4', resultNames=['a','b'])
    >>> t = Task('os.kill(os.getpid(),9)', retries=100) # this is a bad idea
    """
    def __init__(self, expression, resultNames=None, setupNS={},
            clearBefore=False, clearAfter=False, retries=0, **options):
        self.expression = expression
        if isinstance(resultNames, str):
            self.resultNames = [resultNames]
        else:
            self.resultNames = resultNames
        self.setupNS = setupNS
        self.clearBefore = clearBefore
        self.clearAfter = clearAfter
        self.retries=retries
        self.options = options
        self.taskID = None
    

class IWorker(zi.Interface):
    """The Basic Worker Interface. 
    
    A worked is a representation of an Engine that is ready to run tasks.
    """
    def run(task):
        """Run task in worker's namespace.
        
        :Parameters:
            task : a `Task` object
        
        :Returns: `Deferred` to the result of the task in the form of a `dict`,
            {resultName:result}.  If no `resultNames`, then returns {'result':None} on 
            success.
        """
    

class WorkerFromQueuedEngine(object):
    """Adapt an `IQueuedEngine` to an `IWorker` object"""
    zi.implements(IWorker)
    
    def __init__(self, qe):
        self.queuedEngine = qe
        self.workerID = None
    
    def run(self, task):
        """Run task in worker's namespace.
        
        :Parameters:
            task : a `Task` object
        
        :Returns: `Deferred` to the result of the task in the form of a `dict`,
            {resultName:result}.  If no `resultNames`, then returns {'result':None} on 
            success.
        """
        
        dl = []
        index = 1
        if task.clearBefore:
            dl.append(self.queuedEngine.reset())
            index += 1
        if task.setupNS:
            dl.append(self.queuedEngine.push(**task.setupNS))
            index += 1
        
        dl.append(self.queuedEngine.execute(task.expression))
        
        if task.resultNames:
            d = self.queuedEngine.pull(*task.resultNames)
        else:
            d = defer.succeed(None)
        dl.append(d)
        if task.clearAfter:
            dl.append(self.queuedEngine.reset())
        
        names = task.resultNames or ['result']
        d = gatherBoth(dl, consumeErrors = True)
        return d.addBoth(self._zipResults, names, index)
    
    def _zipResults(self, rlist, names, index):
        """callback for constructing the results dict"""
        for r in rlist:
            if isinstance(r, failure.Failure):
                return r
        if len(names) == 1:
            return {names[0]:rlist[index]}
        return dict(zip(names, rlist[index]))
    

components.registerAdapter(WorkerFromQueuedEngine, es.IEngineQueued, IWorker)

class IScheduler(zi.Interface):
    """The interface for a Scheduler.
    """
    
    def addTask(task, **flags):
        """Add a task to the queue of the Scheduler.
        
        :Parameters:
            task : a `Task` object
                The task to be queued.
            flags : dict
                General keywords for more sophisticated scheduling
        """
    
    def popTask(id=None):
        """Pops a Task object.
        
        This gets the next task to be run.  If no `id` is requested, the highest priority
        task is returned.
        
        :Parameters:
            id
                The id of the task to be popped.  The default (None) is to return 
                the highest priority task.
                
        :Returns: a `Task` object
        
        :Exceptions:
            IndexError : raised if no taskID in queue
        """
    
    def addWorker(worker, **flags):
        """Add a worker to the worker queue.
        
        :Parameters:
            worker : an IWorker implementing object
            flags : General keywords for more sophisticated scheduling
        """
    
    def popWorker(id=None):
        """Pops an IWorker object that is ready to do work.
        
        This gets the next IWorker that is ready to do work. 
        
        :Parameters:
            id : if specified, will pop worker with workerID=id, else pops
                 highest priority worker.  Defaults to None.
        
        :Returns:
            an IWorker object
        
        :Exceptions:
            IndexError : raised if no workerID in queue
        """
    
    def ready():
        """Returns True if there is something to do, False otherwise"""
    

class FIFOScheduler(object):
    """A basic First-In-First-Out (Queue) Scheduler.
    
    See the docstrings for IScheduler for details.
    """
    
    zi.implements(IScheduler)
    
    def __init__(self):
        self.tasks = []
        self.workers = []
    
    def addTask(self, task, **flags):    
        self.tasks.append(task)
    
    def popTask(self, id=None):
        if id is None:
            return self.tasks.pop(0)
        else:
            for i in range(len(self.tasks)):
                taskID = self.tasks[i].taskID
                if id == taskID:
                    return self.tasks.pop(i)
            raise IndexError("No task #%i"%id)
    
    def addWorker(self, worker, **flags):        
        self.workers.append(worker)
    
    def popWorker(self, id=None):
        if id is None:
            return self.workers.pop(0)
        else:
            for i in range(len(self.workers)):
                workerID = self.workers[i].workerID
                if id == workerID:
                    return self.workers.pop(i)
            raise IndexError("No worker #%i"%id)
    
    def ready(self):
        return bool(self.workers and self.tasks)
    
        

class ITaskController(cs.IControllerBase):
    """The Task based interface to a `ControllerService` object
    
    This adapts a `ControllerService` to the ITaskController interface.
    """
    
    def run(task):
        """Run a task.
        
        :Parameters:
            task : an IPython `Task` object
        
        :Returns: the integer ID of the task
        """
    
    def getTaskResult(taskID):
        """Get the result of a task by its ID.
        
        :Parameters:
            taskID : int
                the id of the task whose result is requested
        
        :Returns: `Deferred` to (taskID, actualResult) if the task is done, and None
            if not.
        
        :Exceptions:
            actualResult will be an `IndexError` if no such task has been submitted
        """
    
    def abort(taskID):
        """Remove task from queue if task is has not been submitted.
        
        If the task has already been submitted, wait for it to finish and discard 
        results and prevent resubmission.

        :Parameters:
            taskID : the id of the task to be aborted
        
        :Returns:
            `Deferred` to abort attempt completion.  Will be None on success.
        
        :Exceptions:
            deferred will fail with `IndexError` if no such task has been submitted
            or the task has already completed.
        """
        
    def barrier(taskIDs):
        """Block until the list of taskIDs are completed.
        
        Returns None on success.
        """

class TaskController(cs.ControllerAdapterBase):
    """The Task based interface to a Controller object.
    
    If you want to use a different scheduler, just subclass this and set
    the `SchedulerClass` member to the *class* of your chosen scheduler.
    """
    
    zi.implements(ITaskController)
    SchedulerClass = FIFOScheduler
    
    def __init__(self, controller):
        self.controller = controller
        self.controller.onRegisterEngineDo(self.registerWorker, True)
        self.controller.onUnregisterEngineDo(self.unregisterWorker, True)
        self.taskID = 0
        self.failurePenalty = 1 # the time in seconds to penalize
                                # a worker for failing a task
        self.pendingTasks = {} # dict of {workerID:(taskID, task)}
        self.deferredResults = {} # dict of {taskID:deferred}
        self.finishedResults = {} # dict of {taskID:actualResult}
        self.workers = {} # dict of {workerID:worker}
        self.abortPending = [] # dict of {taskID:abortDeferred}
        self.scheduler = self.SchedulerClass()
        for id in self.controller.engines.keys():
                self.workers[id] = IWorker(self.controller.engines[id])
                self.workers[id].workerID = id
                self.schedule.addWorker(self.workers[id])
    
    def registerWorker(self, id):
        """Called by controller.registerEngine."""
        
        if self.workers.get(id):
            raise "We already have one!  This should not happen."
        self.workers[id] = IWorker(self.controller.engines[id])
        self.workers[id].workerID = id
        if not self.pendingTasks.has_key(id):# if not working
            self.scheduler.addWorker(self.workers[id])
        self.distributeTasks()
    
    def unregisterWorker(self, id):
        """Called by controller.unregisterEngine"""
        
        if self.workers.has_key(id):
            try:
                self.scheduler.popWorker(id)
            except IndexError:
                pass
            self.workers.pop(id)
    
    def _pendingTaskIDs(self):
        return [t.taskID for t in self.pendingTasks.values()]
    
    
    def _wrapResult(self, result, taskID):
        if isinstance(result, failure.Failure):
            result.cleanFailure()
        return (taskID, result)
    #---------------------------------------------------------------------------
    # Interface methods
    #---------------------------------------------------------------------------
    
    def run(self, task):
        """Run a task and return `Deferred` to its taskID."""
        task.taskID = self.taskID
        self.taskID += 1
        d = defer.Deferred()
        self.scheduler.addTask(task)
        log.msg('queuing task #%i' %task.taskID)
        
        self.deferredResults[task.taskID] = []
        self.distributeTasks()
        return defer.succeed(task.taskID)
    
    def getTaskResult(self, taskID, block=False):
        """Returns a `Deferred` to a (taskID, result) tuple or None."""
        log.msg("getting result %i"%taskID)
        if self.finishedResults.has_key(taskID):
            return defer.succeed((taskID, self.finishedResults[taskID]))
        elif self.deferredResults.has_key(taskID):
            if block:
                d = defer.Deferred().addBoth(self._wrapResult, taskID)
                self.deferredResults[taskID].append(d)
                return d
            else:
                return defer.succeed(None)
        else:
            return defer.succeed((taskID, IndexError("task ID not registered")))
    
    def abort(self, taskID):
        """Remove a task from the queue if it has not been run already."""
        try:
            self.scheduler.popTask(taskID)
        except IndexError, e:
            if taskID in self.finishedResults.keys():
                d = defer.fail(IndexError("Task Already Completed"))
            elif taskID in self.abortPending:
                d = defer.fail(IndexError("Task Already Aborted"))
            elif taskID in self._pendingTaskIDs():# task is pending
                self.abortPending.append(taskID)
                d = defer.succeed(None)
            else:
                d = defer.fail(e)
        else:
            d = defer.execute(self._doAbort, taskID)
        
        return d
    
    def barrier(self, taskIDs):
        dList = []
        for id in taskIDs:
            d = self.getTaskResult(id, block=True)
            dList.append(d)
        d = DeferredList(dList, consumeErrors=1)
        d.addCallbacks(lambda r: None)
        return d
    
    #---------------------------------------------------------------------------
    # Queue methods
    #---------------------------------------------------------------------------
    
    def _doAbort(self, taskID):
        """Helper function for aborting a pending task."""
        log.msg("Task #%i Aborted"%taskID)
        result = failure.Failure(error.TaskAborted())
        self._finishTask(taskID, result)
        if taskID in self.abortPending:
            self.abortPending.remove(taskID)
    
    def _finishTask(self, taskID, result):
        dlist = self.deferredResults.pop(taskID)
        self.finishedResults[taskID] = result
        for d in dlist:
            d.callback(result)

    def distributeTasks(self):
        """Distribute tasks while self.scheduler has things to do."""
        
        while self.scheduler.ready():
            # get worker
            worker = self.scheduler.popWorker()
            # get task
            task = self.scheduler.popTask()
            # add to pending
            self.pendingTasks[worker.workerID] = task
            # run/link callbacks
            d = worker.run(task)
            log.msg("running task #%i on worker %i" %(task.taskID, worker.workerID))
            d.addBoth(self.taskCompleted, task.taskID, worker.workerID)
            
    def taskCompleted(self, result, taskID, workerID):
        """This is the err/callback for a completed task."""
        try:
            task = self.pendingTasks.pop(workerID)
        except:
            # this should not happen
            log.msg("tried to pop bad pending task#%i from worker #%i"%(taskID, workerID))
            log.msg("result: %s"%result)
            log.msg("pending tasks:%s"%self.pendingTasks)
            return
        
        # Check if aborted while pending
        aborted = False
        if taskID in self.abortPending:
            self._doAbort(taskID)
            aborted = True
        
        if not aborted:
            if isinstance(result, failure.Failure): # we failed
                log.msg("Task #%i failed on worker %i"% (taskID, workerID))
                if task.retries > 0: # resubmit
                    task.retries -= 1
                    self.scheduler.addTask(task)
                    s = "resubmitting task #%i, %i retries remaining" %(taskID, task.retries)
                    log.msg(s)
                    self.distributeTasks()
                else: # done trying
                    self._finishTask(taskID, result)
                # wait a second before readmitting a worker that failed
                # it may have died, and not yet been unregistered
                reactor.callLater(self.failurePenalty, self.readmitWorker, workerID)
            else: # we succeeded
                log.msg("Task #%i completed "% taskID)
                self._finishTask(taskID, result)
                self.readmitWorker(workerID)
        else:# we aborted the task
            if isinstance(result, failure.Failure): # it failed, penalize worker
                reactor.callLater(self.failurePenalty, self.readmitWorker, workerID)
            else:
                self.readmitWorker(workerID)
    
    def readmitWorker(self, workerID):
        """Readmit a worker to the scheduler.  
        
        This is outside `taskCompleted` because of the `failurePenalty` being 
        implemented through `reactor.callLater`.
        """
        
        if workerID in self.workers.keys() and workerID not in self.pendingTasks.keys():
            self.scheduler.addWorker(self.workers[workerID])
            self.distributeTasks()
        
    
components.registerAdapter(TaskController, cs.IControllerBase, ITaskController)
