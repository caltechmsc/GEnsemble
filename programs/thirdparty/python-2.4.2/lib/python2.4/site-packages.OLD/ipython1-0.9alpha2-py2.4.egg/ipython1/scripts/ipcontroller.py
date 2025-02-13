#!/usr/bin/env python
"""The ipython controller.
"""

#-------------------------------------------------------------------------------
#       Copyright (C) 2005  Fernando Perez <fperez@colorado.edu>
#                           Brian E Granger <ellisonbg@gmail.com>
#                           Benjamin Ragan-Kelley <benjaminrk@gmail.com>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-------------------------------------------------------------------------------

import sys, time, os
from optparse import OptionParser

from twisted.internet import reactor, error
from twisted.python import log

from ipython1.kernel import controllerservice
from ipython1.kernel.multiengine import IMultiEngine
from ipython1.kernel.task import ITaskController

import ipython1.config.api as config

controllerConfig = config.getConfigObject('controller')


        

def main(logfile):
    if logfile:
        logfile = logfile + str(os.getpid()) + '.log'
        try:
            openLogFile = open(logfile, 'w')
        except:
            openLogFile = sys.stdout
    else:
        openLogFile = sys.stdout
    log.startLogging(openLogFile)
    
    # Execute any user defined import statements
    if controllerConfig.controllerImportStatement:
        try:
            exec controllerConfig.controllerImportStatement
        except:
            log.msg("Error running controllerImportStatement: %s" % controllerConfig.controllerImportStatement)
    
    # Create and configure the core ControllerService
    cs = controllerservice.ControllerService()
    
    # Start listening for engines  
    efac = controllerConfig.engineServerProtocolInterface(cs)
    reactor.listenTCP(
        port=controllerConfig.listenForEnginesOn['port'],
        factory=efac,
        interface=controllerConfig.listenForEnginesOn['ip'])
        
    for ciname, ci in controllerConfig.controllerInterfaces.iteritems():
        log.msg("Starting controller interface: " + ciname)
        adaptedController = ci['controllerInterface'](cs)
        for niname, ni in ci['networkInterfaces'].iteritems():
            log.msg("Starting controller network interface (%s): %s:%s:%i" % (ciname,niname,ni['ip'],ni['port']))
            fac = ni['interface'](adaptedController)
            reactor.listenTCP(
                port=ni['port'],
                factory=fac,
                interface=ni['ip'])
                    
    # Start the controller service and set things running
    cs.startService()
    reactor.run()

def start():
    parser = OptionParser()
    parser.set_defaults(logfile='')
        
    parser.add_option("--engine-port", type="int", dest="engineport",
        help="the TCP port the controller will listen on for engine connections")
    parser.add_option("--engine-ip", type="string", dest="engineip",
        help="the TCP ip address the controller will listen on for engine connections")
        
    parser.add_option("--task-port", type="int", dest="taskport",
        help="the TCP port the controller will listen on for task client connections")
    parser.add_option("--task-ip", type="string", dest="taskip",
        help="the TCP ip address the controller will listen on for task client connections")

    parser.add_option("--remote-cont-port", type="int", dest="rcport",
        help="the TCP port the controller will listen on for Remote Controller client connections")
    parser.add_option("--remote-cont-ip", type="string", dest="rcip",
        help="the TCP ip address the controller will listen on for Remote Controller client connections")

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
        config.updateConfigWithProfile('ipcontroller', options.profile, options.ipythondir)
    elif options.rcfile and not options.profile:
        config.updateConfigWithFile(options.rcfile, options.ipythondir)
    else:
        config.updateConfigWithFile('ipcontrollerrc.py', options.ipythondir)
        
    # Update withh command line options
    if options.engineip is not None:
        controllerConfig.listenForEnginesOn['ip'] = options.engineip
    if options.engineport is not None:
        controllerConfig.listenForEnginesOn['port'] = options.engineport
    di = controllerConfig.controllerInterfaces['multiengine']['default']
    if options.rcip is not None:
        controllerConfig.controllerInterfaces['multiengine']['networkInterfaces'][di]['ip'] = options.rcip
    if options.rcport is not None:
        controllerConfig.controllerInterfaces['multiengine']['networkInterfaces'][di]['port'] = options.rcport
    di = controllerConfig.controllerInterfaces['task']['default']
    if options.taskip is not None:
        controllerConfig.controllerInterfaces['task']['networkInterfaces'][di]['ip'] = options.taskip
    if options.taskport is not None:
        controllerConfig.controllerInterfaces['task']['networkInterfaces'][di]['port'] = options.taskport
        
    main(options.logfile)
    
    
if __name__ == "__main__":
    start()
