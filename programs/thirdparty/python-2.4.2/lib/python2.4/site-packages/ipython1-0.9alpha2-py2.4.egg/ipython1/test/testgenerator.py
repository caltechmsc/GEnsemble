# encoding: utf-8
"""
Classes for generator sequences of tests.
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

from twisted.internet import defer

#-------------------------------------------------------------------------------
# The main class of this module
#-------------------------------------------------------------------------------

class TestGenerator(object):
    """An object for creating a set of tests that require Deferreds.
    
    The idea of this class is to call a method on a set of inputs and compare
    the set of outputs to the known outputs.  But, the caveat is that
    the method using to compute the outputs actually returns a Deferred to
    the computed output.  Writing such tests is extremely subtle and all the
    naive approach don't work.  The approach used here uses generators
    to make sure that the variables are bound at the correct moment in time.
    """
    
    def __init__(self, inputs, outputs, testCaseInstance):
        """Create a set of tests consisting of inputs and known outputs.
        
        :Parameters:
            inputs : list
                List of inputs
            outputs : list
                List of corresponding known outputs
            testCaseInstance : TestCase
                The test case we are using.
        """
        self.inputs = inputs
        self.outputs = outputs
        self.testCaseInstance = testCaseInstance

    def compare(self, actual, computed):
        """Perform the actual test by comparing the actual+computed output.
        
        Developers writing particular tests should override this method to
        perform the specific type of assertion and comparison that is
        appropriate for the particular type of test being performed.  This
        means the user will need to call one of the assertion methods of
        testCaseInstance.
        """
        return self.testCaseInstance.assert_(actual == computed)
        
    def computeOutput(self, i):
        """Return a deferred to the computed output of the input i.
        
        Users should override this method to cmopute the output given i.
        This method must return a deferred to the computed output.
        """
        pass
        
    def performTests(self):
        """Perform all the tests that this class knows about."""
        d = defer.succeed(None)
        g = (c for c in zip(self.inputs,self.outputs))
        def performNextTest(g):
            i,actualOutput = g.next()
            dToComputedOutput = self.computeOutput(i)
            dToComputedOutput.addBoth(lambda r: self.compare(actualOutput,r))
            return dToComputedOutput
        for i in range(len(self.inputs)):
            d.addCallback(lambda _: performNextTest(g))
        return d

#-------------------------------------------------------------------------------
# Classes for testing engine methods
#-------------------------------------------------------------------------------


from ipython1.core.interpreter import Interpreter

class EngineExecuteTestGenerator(TestGenerator):
    """A class for testing execute on the Engine."""
    
    def __init__(self, inputs, testCaseInstance):
        self.shell = Interpreter()
        outputs = [self.shell.execute(c) for c in inputs]
        TestGenerator.__init__(self, inputs, outputs, testCaseInstance)
        
    def compare(self, actual, computed):
        actual['id'] = computed['id']
        return self.testCaseInstance.assert_(actual == computed)
        
    def computeOutput(self, i):
        return self.testCaseInstance.engine.execute(i)

class EngineFailingExecuteTestGenerator(TestGenerator):
    """A class for testing execute on the Engine."""
    
    def __init__(self, inputs, outputs, testCaseInstance):
        TestGenerator.__init__(self, inputs, outputs, testCaseInstance)
        
    def compare(self, actual, computed):
        return self.testCaseInstance.assertRaises(actual, computed.raiseException)
        
    def computeOutput(self, i):
        return self.testCaseInstance.engine.execute(i)

class EnginePushPullTestGenerator(TestGenerator):
    """A class for testing basic push/pull on the engine."""
    
    def __init__(self, objects, testCaseInstance):
        TestGenerator.__init__(self, objects, objects, testCaseInstance)
    
    def compare(self, actual, computed):
        return self.testCaseInstance.assertEquals(actual, computed)
        
    def computeOutput(self, i):
        d = self.testCaseInstance.engine.push(a=i)
        d.addCallback(lambda r: self.testCaseInstance.engine.pull('a'))
        return d

class EngineGetResultTestGenerator(TestGenerator):
    """A class for testing execute on the Engine."""
    
    def __init__(self, inputs, testCaseInstance):
        self.shell = Interpreter()
        outputs = [self.shell.execute(c) for c in inputs]
        TestGenerator.__init__(self, inputs, outputs, testCaseInstance)
        
    def compare(self, actual, computed):
        actual['id'] = computed['id']
        return self.testCaseInstance.assertEquals(actual, computed)
        
    def computeOutput(self, i):
        d = self.testCaseInstance.engine.execute(i)
        d.addCallback(lambda r: self.testCaseInstance.engine.getResult(r['number']))
        return d


#-------------------------------------------------------------------------------
# Classes for testing multiengine methods
#-------------------------------------------------------------------------------

class MultiEngineExecuteAllTestGenerator(TestGenerator):
    """A class for testing execute on the Engine."""
    
    def __init__(self, inputs, testCaseInstance, targets='all'):
        self.targets = targets
        self.shell = Interpreter()
        outputs = [self.shell.execute(c) for c in inputs]
        TestGenerator.__init__(self, inputs, outputs, testCaseInstance)
        
    def compare(self, actual, computed):
        for c in computed:
            actual['id'] = c['id']
            self.testCaseInstance.assertEquals(actual, c)
        
    def computeOutput(self, i):
        return self.testCaseInstance.multiengine.execute(self.targets, i)
        
class MultiEngineFailingExecuteTestGenerator(TestGenerator):
    """A class for testing execute on the Engine."""
    
    def __init__(self, inputs, outputs, testCaseInstance, targets='all'):
        self.targets = targets
        TestGenerator.__init__(self, inputs, outputs, testCaseInstance)
        
    def compare(self, actual, computed):
        return self.testCaseInstance.assertRaises(actual, computed.raiseException)
        
    def computeOutput(self, i):
        return self.testCaseInstance.multiengine.execute(self.targets, i)

class MultiEngineGetResultTestGenerator(TestGenerator):
    """A class for testing execute on the Engine."""
    
    def __init__(self, inputs, testCaseInstance, targets):
        self.targets = targets
        self.shell = Interpreter()
        outputs = [self.shell.execute(c) for c in inputs]
        TestGenerator.__init__(self, inputs, outputs, testCaseInstance)
        
    def compare(self, actual, computed):
        for c in computed:
            actual['id'] = c['id']
            return self.testCaseInstance.assertEquals(actual, c)
        
    def computeOutput(self, i):
        d = self.testCaseInstance.multiengine.execute(self.targets, i)
        # d.addCallback(lambda r: self.testCaseInstance.multiengine.getResult(self.targets, r[0]['number']))
        return d
