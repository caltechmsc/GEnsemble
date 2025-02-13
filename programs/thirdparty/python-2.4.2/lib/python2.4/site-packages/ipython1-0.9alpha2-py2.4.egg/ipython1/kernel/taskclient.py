# encoding: utf-8
# -*- test-case-name: ipython1.test.test_taskcontrollerxmlrpc -*-
"""The Generic Task Client object.  This must be subclassed based on your 
connection method.
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

# from twisted.python import failure

from ipython1.kernel import task

#-------------------------------------------------------------------------------
# Connecting Task Client
#-------------------------------------------------------------------------------

class InteractiveTaskClient(object):
    """XML-RPC version of the Connecting TaskControllerClient"""
    
    ############
    # ConnectingTaskController
    ############
    def irun(self, *args, **kwargs):
        """Run a task on the `TaskController`.
        
        This method is a shorthand for run(task) and its arguments are simply
        passed onto a `Task` object:
        
        irun(*args, **kwargs) -> run(Task(*args, **kwargs))

        :Parameters:
            expression : str
                A str that is valid python code that is the task.
            resultNames : str or list of str 
                The names of objects to be pulled as results.
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
            
        :Returns: A `TaskResult` object.      
        """
        block = kwargs.pop('block', self.block)
        if len(args) == 1 and isinstance(args[0], task.Task):
            t = args[0]
        else:
            t = task.Task(*args, **kwargs)
        taskID = self.run(t)
        print "TaskID = %i"%taskID
        return self.getTaskResult(taskID, block)
