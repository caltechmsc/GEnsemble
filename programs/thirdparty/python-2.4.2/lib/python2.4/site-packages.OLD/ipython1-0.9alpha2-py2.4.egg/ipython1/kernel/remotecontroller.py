# encoding: utf-8
# -*- test-case-name: ipython1.test.test_remotecontroller -*-
"""The kernel interface.

The kernel interface is a set of classes that providse a high level interface
to a running ipython kernel instance.  Currently these classes use blocking
sockets, and thus, do not require Twisted.

TODOs:

 - Organize methods of RemoteController, RemoteControllerView and EngineProxy in 
   a consistent and logical manner.
 - Check to make sure that RemoteControllerView and EngineProxy implement all the 
   methods they should.
 - What should happen if the target given is an integer, but is not valid?

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

import StringIO
import sys

import ipython1.kernel.magic
from ipython1.tools import utils

#-------------------------------------------------------------------------------
# RemoteController stuff
#-------------------------------------------------------------------------------

class RemoteControllerBase(object):
    """The base class for all RemoteController objects.
    
    This calss is meant to provide capabilities that are independent of the
    network protocol used to implement the RemoteController, like testing
    facilities.
    
    It is important to note, that as of now, this is only designed to be
    used with network protocols that use standard non-blocking socket and not
    Twisted.  Such protocols are provided so that standard Python session
    can talk to Controllers.
    
    It is also designed to provide an informal client interface.  It is 
    informal as clients won't necessarily have Twisted or zope.interface
    installed.  The client interface is very similar, but not identical to 
    the IEngineMultiplexer interface.
    
    Methods that should be implemented by subclasses:
    
     * execute
     * executeAll
     * push
     * pushAll
     * pull
     * pullAll
     * getResult
     * getResultAll
     * printResult
     * printResultAll
     * reset
     * resetAll
     * status
     * statusAll
     * kill
     * killAll
     * getIDs
     * getMappedIDs
     * scatter
     * scatterAll
     * gather
     * gatherAll
     * notify (why not call addNotifier/delNotifier?  We should just make a clientAPI!)
     
     * activate     
     * run
     * runAll
     * __setitem__
     * __getitem__
     * map (eventually reduce as well)
     * parallelize
     
     Some methods don't always make sense on RemoteControllerViews:
     
     * pushModule
     * connect
     * disconnect
     
    I can't declare these as pass methods in this base class, because some
    subclasses might generate the methods dynamically if they don't exist.  An
    examples of this are the fooAll() methods which are typically done
    dynamically.     
    """

    #---------------------------------------------------------------------------
    # Testing and timing methods
    #---------------------------------------------------------------------------

    def test(self):
        """Test a RemoteController Object.
        
        To work, this RemoteController must be connected to a ControllerService
        that has Engines connected to it.
        
        We should rethink how the tests here are done to provide more feedback
        for users.  But for now this is a start!
        """
        
        # Setup
        
        ids = self.getMappedIDs()
        hide = StringIO.StringIO('')
        if len(ids) < 4:
            raise Exception("The client test() need to be run with at least 4 engines")    
        print "Running tests on %i engines" %len(ids)

        print "Testing execute..."
        try:
            assert self.execute(0, 'a'),"assert rc.execute(0, 'a')"
            assert self.executeAll('print a'),"assert rc.execute([0,1], 'print a')"
            assert self.execute('all', 'b-3'),"assert rc.execute('all', 'b-3')"
            assert not self.execute(0, ''),"assert not rc.execute(0, '')"
            assert not self.execute([], 'locals'),"assert not rc.execute([], 'locals')"
            s = sys.stdout
            sys.stdout = hide
            assert self.execute(0, 'a', block=True),"assert rc.execute(0, 'a', block=True)"
            assert self.execute([0,0], 'print a', block=True),"assert rc.execute([0,1], 'print a', block=True)"
            assert self.execute('all', 'b-3', block=True),"assert rc.execute('all', 'b-3', block=True)"
            assert not self.execute(0, '', block=True),"assert not rc.execute(0, '', block=True)"
            assert not self.execute([], 'locals', block=True),"assert not rc.execute([], 'locals', block=True)"
            sys.stdout = s
        except Exception, e:
            print "execute FAIL: ", e
        else:
            print "execute OK"
        
        print "Testing push/pull"
        try:
            assert self.push(0, a=5),"assert rc.push(0, a=5)"
            assert self.pull(0, 'a') == 5,"assert rc.pull(0, 'a') == 5"
            assert not self.push(0),"assert not rc.push(0)"
            assert not self.push([], a=5),"assert not rc.push([], a=5)"
            assert self.push([0], b='asdf', c=[1,2]),"assert rc.push([0], b='asdf', c=[1,2])"
            assert self.pull([0], 'b', 'c') == ['asdf', [1,2]],"assert rc.pull([0], 'b', 'c') == ['asdf', [1,2]]"
            assert self.pushAll(c=[1,2,3]),"assert rc.pushAll(c=[1,2,3])"
            assert self.pullAll('c') == ([1,2,3],)*len(ids),"assert rc.pullAll('c') == ([1,2,3],)*len(ids)"
            assert self.push([0,0], a=14),"assert rc.push([0,0], a=14)"
            assert self.pull([0,0,0], 'a') == (14,14,14),"assert rc.pull([0,0,0], 'a') == (14,14,14)"
            assert self.pushAll(a=1, b=2, c=3),"assert rc.pushAll(a=1, b=2, c=3)"
            assert self.pullAll('a','b','c') == [(1,)*len(ids),(2,)*len(ids),(3,)*len(ids)],"assert rc.pullAll('a','b','c') == [(1,1)*len(ids),(2,2)*len(ids),(3,3)*len(ids)]"
            q={'a':5}
            assert self.push(ids, q=q),"assert rc.push(ids, q=q)"
            assert self.pull(ids,'q') == (q,)*len(ids) or len(ids) is 1,"assert rc.pull(ids,'q') == (q,)*len(ids)"
            self['z'] = 'test'
            self[1]['t'] = [1,2,3]
            self[0:max(ids)]['r'] = 'asdf'
            self[0:max(ids):2]['asdf'] = 4
            self[1:max(ids)][0]['qwert'] = 3
        except Exception, e:
           print "push/pull FAIL: ", e
           raise
        else:
           print "push/pull OK"

           
class RemoteControllerView(RemoteControllerBase):
    """A subset interface for RemoteController.__getitem__"""
    def __init__(self, rc, ids):
        self.rc = rc
        if isinstance(ids, slice):
            self._originalIDs = range(*ids.indices(ids.stop))
        elif isinstance(ids, list):
            self._originalIDs = ids
        else:
            raise TypeError("RemoteControllerView requires slice or list")
        # Make sure these exist as of now
        currentIDs = rc.getIDs()
        for id in self._originalIDs:
            if id not in currentIDs:
                raise Exception("The engine with id %i does not exist" % id)
        self._ids = range(len(self._originalIDs))
        # print self._ids
        # print self._originalIDs
    
    def _getBlock(self): return self.rc.block
    def _setBlock(self, block): self.rc.block = block
    
    block = property(_getBlock, _setBlock, None, None)
    
    #---------------------------------------------------------------------------
    # RemoteController methods
    #---------------------------------------------------------------------------
    
    def execute(self, targets, lines, block=None):
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.execute(actualTargets, lines, block)
    
    def executeAll(self, lines, block=None):
        return self.execute('all', lines, block)
        
    def push(self, targets, *keys,**namespace):
        if keys: namespace.update(utils.extractVarsAbove(*keys))
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.push(actualTargets, **namespace)
    
    def pushAll(self, *keys,**namespace):
        if keys: namespace.update(utils.extractVarsAbove(*keys))
        return self.push('all', **namespace)
        
    def pull(self, targets, *keys):
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.pull(actualTargets, *keys)
    
    def pullAll(self, *keys):
        r = self.pull('all', *keys)
        if len(self._ids) is 1:
            r = [r]
        return r
        
    def getResult(self, targets, i=None):
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.getResult(actualTargets, i)
    
    def getResultAll(self, i=None):
        r = self.getResult('all', i)
        if len(self._ids) is 1:
            r = [r]
        return r
        
    def printResult(self, targets, i=None):
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.printResult(actualTargets, i)
             
    def printResultAll(self, i=None):
        return self.printResult('all', i)
             
    def reset(self, targets):
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.reset(actualTargets)
    
    def resetAll(self):
        return self.reset('all')

    def status(self, targets):
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.status(actualTargets)
    
    def statusAll(self):
        r = self.status('all')
        if len(self._ids) is 1:
            r = [r]
        return r
        
    def kill(self, targets):
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.kill(actualTargets)
    
    def killAll(self):
        return self.kill('all')
                
    def getIDs(self):
        """Return the ids of the Engines as the Controller indexes them."""
        
        return self._originalIDs

    def scatter(self, targets, key, seq, style='basic', flatten=False):
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.scatter(actualTargets, key, seq, style, flatten)
    
    def scatterAll(self, key, seq, style='basic', flatten=False):
        return self.scatter('all', key, seq, style, flatten)
        
    def gather(self, targets, key, style='basic'):
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.gather(actualTargets, key, style)        
    
    def gatherAll(self, key, style='basic'):
        return self.gather('all', key, style)
        
    def notify(self, addr=None, flag=True):
        self.rc.notify(addr, flag)
        
    def activate(self):
        try:
            __IPYTHON__.activeController = self
        except NameError:
            print "The IPython Controller magics only work within IPython."
        
    def run(self, targets, fname):
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.run(actualTargets, fname)
    
    def runAll(self, fname):
        return self.run('all', fname)
        
    def __setitem__(self, key, value):
        return self.push('all', **{key:value})
            
    def __getitem__(self, id):
        if isinstance(id, slice):
            return RemoteControllerView(self.rc, self._originalIDs[id])
        elif isinstance(id, int):
            return EngineProxy(self.rc, self._originalIDs[id])
        elif isinstance(id, str):
            return self.pull('all',*(id,))
        else:
            raise TypeError("__getitem__ only takes strs, ints, and slices")
        
    def map(self, targets, functionSource, seq, style='basic'):
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.map(actualTargets, functionSource, seq, style)
    
    def mapAll(self, functionSource, seq, style='basic'):
        return self.map('all', functionSource, seq, style)
    
    def parallelize(self, targets, functionName):
        actualTargets = self._mapIDsToOriginal(targets)
        return self.rc.parallelize(actualTargets, functionName)
    
    def parallelizeAll(self, functionName):
        return self.parallelize('all', functionName)
        
    #---------------------------------------------------------------------------
    # Methods specific to a RemoteControllerView
    #---------------------------------------------------------------------------
        
    def getMappedIDs(self):
        """Return the ids that current operations will succeed on."""
        return self._ids
        
    def _mapIDsToOriginal(self, ids):
        if ids == 'all':
            return self._originalIDs
        elif isinstance(ids, int) and ids in self._ids:
            return self._originalIDs[ids]
        elif isinstance(ids, (list, tuple)):
            return [self._originalIDs[i] for i in ids]
        else:
            raise TypeError("targets/ids must be int, list or tuple")
    
class EngineProxy(object):
    """A proxy for an Engine that goes through a RemoteController.

    The user won't ever create these directly.  Instead, the actual
    RemoteController class does that when a particular Engine is indexed.
    """

    def __init__(self, rc, id):
        self.id = id
        self.rc = rc
    
    def execute(self, strings, block=None):
        return self.rc.execute(self.id, strings, block=block)
        #if block:
        #    return self.rc.execute(self.id, strings, block=True)[0]
        #else:
        #    return self.rc.execute(self.id, strings)
    
    def push(self, *keys,**namespace):
        if keys: namespace.update(utils.extractVarsAbove(*keys))
        return self.rc.push(self.id, **namespace)
    
    def pull(self, *keys):
        return self.rc.pull(self.id, *keys)

    def getResult(self, i=None):
        return self.rc.getResult(self.id, i)
    
    def status(self):
        return self.rc.status(self.id)
    
    def reset(self):
        return self.rc.reset(self.id)
    
    def kill(self):
        return self.rc.kill(self.id)

    def __setitem__(self, key, value):
        return self.push(**{key:value})
        
    def __getitem__(self, key):
        return self.pull(*(key,))
