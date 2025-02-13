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
from ipython1.notebook import notebook, xmlutil, dbutil
import ipython1.config.api as config

notebookConfig = config.getConfigObject('notebook')
shellConfig = config.getConfigObject('shell')


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
    
    service = EngineService(shellConfig.shellClass)
    service.startService()
    if shellConfig.shellImportStatement:
        try:
            service.execute(shellConfig.shellImportStatement)
        except:
            log.msg("Error running shellImportStatement: %s" % shellConfig.shellImportStatement)
    engine = notebookConfig.engineInterface(service)
    
    dbutil.initDB(notebookConfig.activeDB)
    
    if notebookConfig.externalDBs:
        log.msg("Loading External DBs: %s"%notebookConfig.externalDBs)
        xmlutil.mergeDBs([notebookConfig.activeDB]+notebookConfig.externalDBs)
    
    nbc = notebook.NotebookController(engine)
    for niname, ni in notebookConfig.networkInterfaces.iteritems():
        log.msg("Starting notebook network interface: %s:%s:%i" % (niname,ni['ip'],ni['port']))
        reactor.listenTCP(
            port=ni['port'],
            factory=ni['interface'](nbc),
            interface=ni['ip'])
    reactor.run()

def start(n=1):
    parser = OptionParser()
    parser.set_defaults(n=n)
    parser.set_defaults(profile = '')
    parser.set_defaults(rcfile='')
    parser.set_defaults(ipythondir='')
    parser.set_defaults(logfile='')

    parser.add_option("--port", type="int", dest="port",
        help="the TCP port the notebook server is listening on")
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
        config.updateConfigWithProfile('ipnotebook', options.profile, options.ipythondir)
    elif options.rcfile and not options.profile:
        config.updateConfigWithFile(options.rcfile, options.ipythondir)
    else:
        config.updateConfigWithFile('ipnotebookrc.py', options.ipythondir)
    
    for dbname in args:
        if "://" not in dbname:
            dbname = notebookConfig.defaultDBMode+dbname
        assert os.path.isfile(dbname[dbname.find("://"+4)]), "no such DB:"%dbname
        if dbname not in notebookConfig.externalDBs:
            notebookConfig.externalDBs.append(dbname)
        
    # Now override with command line options
    main(options.logfile)
    
if __name__ == "__main__":
    start()
