#!/usr/bin/env python

import time

import ipython1.kernel.api as kernel
from ipython1.scripts import ipcluster1 as ipc

# Start controller/engine for testing

controller, engines = ipc.startLocalCluster(n=1)

#stop

try:
    # Get a remote controller instance
    rc = kernel.RemoteController(('127.0.0.1',10105))
    print 'IDs:',rc.getIDs()

    rc.executeAll('a=[0]')
    aa = rc.gatherAll('a')
    print "aa=",aa

    rc.executeAll('a[0]')  # OK
    rc.executeAll('a[1]')  # Error
    #rc.executeAll('execfile("/home/fperez/test/error.py")')  # error
finally:
    print 'Stopping cluster'
    ipc.stopCluster(controller,engines)
    print 'done.'
    print '-'*77
