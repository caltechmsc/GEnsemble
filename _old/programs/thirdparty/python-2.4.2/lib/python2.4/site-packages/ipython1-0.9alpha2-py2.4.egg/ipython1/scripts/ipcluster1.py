#!/usr/bin/env python
# encoding: utf-8
"""Start an IPython cluster conveniently, either locally or remotely.

Basic usage
-----------

For local operation, the simplest mode of usage is:

  %prog -n N

where N is the number of engines you want started.

For remote operation, you must call it with a cluster description file:

  %prog -f clusterfile.py

The cluster file is a normal Python script which gets run via execfile().  You
can have arbitrary logic in it, but all that matters is that at the end of the
execution, it declares the variables 'controller', 'engines', and optionally
'sshx'.  See the accompanying examples for details on what these variables must
contain.


Notes
-----

WARNING: this code is still UNFINISHED and EXPERIMENTAL!  It is incomplete,
some listed options are not really implemented, and all of its interfaces are
subject to change.

When operating over SSH for a remote cluster, this program relies on the
existence of a particular script called 'sshx'.  This script must live in the
target systems where you'll be running your controller and engines, and is
needed to configure your PATH and PYTHONPATH variables for further execution of
python code at the other end of an SSH connection.  The script can be as simple
as:

#!/bin/sh
. $HOME/.bashrc
"$@"

which is the default one provided by IPython.  You can modify this or provide
your own.  Since it's quite likely that for different clusters you may need
this script to configure things differently or that it may live in different
locations, its full path can be set in the same file where you define the
cluster setup.  IPython's order of evaluation for this variable is the
following:

  a) Internal default: 'sshx'.  This only works if it is in the default system
  path which SSH sets up in non-interactive mode.

  b) Environment variable: if $IPYTHON_SSHX is defined, this overrides the
  internal default.

  c) Variable 'sshx' in the cluster configuration file: finally, this will
  override the previous two values.
 
This code is Unix-only, with precious little hope of any of this ever working
under Windows, since we need SSH from the ground up, we background processes,
etc.  Ports of this functionality to Windows are welcome.


Call summary
------------

    %prog [options]
"""

__docformat__ = "restructuredtext en"

#-------------------------------------------------------------------------------
#       Copyright (C) 2006  Fernando Perez <fperez@colorado.edu>
#                           Brian E Granger <ellisonbg@gmail.com>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-------------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import signal
import socket
import sys
import time

from optparse import OptionParser
from subprocess import Popen,call

#---------------------------------------------------------------------------
# IPython imports
#---------------------------------------------------------------------------
import ipython1.kernel.api as kernel

from ipython1.config import cutils
from ipython1.core import error
from ipython1.tools import utils
from ipython1.tools.hatch import start, stop 


#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


def parse_args():
    """Parse command line and return opts,args."""

    parser = OptionParser(usage=__doc__)
    newopt = parser.add_option  # shorthand

    newopt("--controller-port", type="int", dest="controllerport",
           help="the TCP port the controller is listening on")

    newopt("--controller-ip", type="string", dest="controllerip",
           help="the TCP ip address of the controller")

    newopt("-n", "--num", type="int", dest="n",default=2,
           help="the number of engines to start")

    newopt("--engine-port", type="int", dest="engineport",
           help="the TCP port the controller will listen on for engine "
           "connections")
    
    newopt("--engine-ip", type="string", dest="engineip",
           help="the TCP ip address the controller will listen on "
           "for engine connections")

    newopt("-l", "--logfile", type="string", dest="logfile",
           help="log file name")

    newopt('-f','--cluster-file',dest='clusterfile',
           help='file describing a remote cluster')

    return parser.parse_args()


def startMsg(control_host,control_port=10105):
    """Print a startup message"""
    print
    print 'Your cluster is up and running.'
    print
    print 'For interactive use, you can make a Remote Controller with:'
    print
    print 'import ipython1.kernel.api as kernel'
    print "ipc = kernel.RemoteController((%r,%s))" % \
          (control_host,control_port)
    print
    print 'You can then cleanly stop the cluster from IPython using:'
    print
    print 'ipc.killAll(controller=True)'
    print


def main():
    """Main driver for the two big options: local or remote cluster."""
    
    opt,arg = parse_args()

    clusterfile = opt.clusterfile
    if clusterfile:
        clusterRemote(opt,arg)
    else:
        clusterLocal(opt,arg)
        
            
if __name__=='__main__':
    main()
