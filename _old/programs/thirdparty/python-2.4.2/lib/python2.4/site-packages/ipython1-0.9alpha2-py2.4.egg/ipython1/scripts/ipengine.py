#!/usr/bin/env python
"""Start the IPython Engine.
"""

#-------------------------------------------------------------------------------
#       Copyright (C) 2005  Fernando Perez <fperez@colorado.edu>
#                           Brian E Granger <ellisonbg@gmail.com>
#                           Benjamin Ragan-Kelley <benjaminrk@gmail.com>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-------------------------------------------------------------------------------

# Python looks for an empty string at the beginning of sys.path to enable
# importing from the cwd.
import sys
sys.path.insert(0, '')

import sys, os
from optparse import OptionParser

from twisted.internet import reactor
from twisted.python import log

from ipython1.kernel.engineservice import EngineService
import ipython1.config.api as config

engineConfig = config.getConfigObject('engine')
shellConfig = config.getConfigObject('shell')
mpiConfig = config.getConfigObject('mpi')
config.updateConfigWithFile('mpirc.py')

# MPI module should be loaded first

mpi = None
if mpiConfig.mpiImportStatement:
    try:
        exec mpiConfig.mpiImportStatement
    except ImportError:
        mpi = None

def main(n, logfile):
    if logfile:
        logfile = logfile + str(os.getpid()) + '.log'
        try:
            openLogFile = open(logfile, 'w')
        except:
            openLogFile = sys.stdout
    else:
        openLogFile = sys.stdout
    log.startLogging(openLogFile)
    for i in range(n):
        service = EngineService(shellConfig.shellClass,
            mpi=mpi)
        fac = engineConfig.engineClientProtocolInterface(service)
        reactor.connectTCP(
            host=engineConfig.connectToControllerOn['ip'], 
            port=engineConfig.connectToControllerOn['port'],
            factory=fac)
        service.startService()
        if shellConfig.shellImportStatement:
            try:
                service.execute(shellConfig.shellImportStatement)
            except:
                log.msg("Error running shellImportStatement: %s" % shellConfig.shellImportStatement)
                
    reactor.run()

def start(n=1):
    parser = OptionParser()
    parser.set_defaults(n=n)
    parser.set_defaults(profile = '')
    parser.set_defaults(rcfile='')
    parser.set_defaults(ipythondir='')
    parser.set_defaults(logfile='')

    parser.add_option("--controller-port", type="int", dest="controllerport",
        help="the TCP port the controller is listening on")
    parser.add_option("--controller-ip", type="string", dest="controllerip",
        help="the TCP ip address of the controller")
    parser.add_option("-n", "--num", type="int", dest="n",
        help="the number of engines to start in this process")
    parser.add_option("-l", "--logfile", type="string", dest="logfile",
        help="log file name (default is stdout)")
    
    # Configuration files and profiles
    parser.add_option("-p", "--profile", type="string", dest="profile",
        help="the name of a profile")
    parser.add_option("--rcfile", type="string", dest="rcfile",
        help="the name of a configuration file")
    parser.add_option("--ipythondir", type="string", dest="ipythondir",
        help="look for config files and profiles in this directory")
    (options, args) = parser.parse_args()
            
    # Configuration files and profiles
    if options.profile and not options.rcfile:
        config.updateConfigWithProfile('ipengine', options.profile, options.ipythondir)
    elif options.rcfile and not options.profile:
        config.updateConfigWithFile(options.rcfile, options.ipythondir)
    else:
        config.updateConfigWithFile('ipenginerc.py', options.ipythondir)
        
    # Now override with command line options
    if options.controllerip is not None:
        engineConfig.connectToControllerOn['ip'] = options.controllerip
    if options.controllerport is not None:
        engineConfig.connectToControllerOn['port'] = options.controllerport
        
    main(options.n, options.logfile)
    
if __name__ == "__main__":
    start()
