#!/usr/bin/env python
#####################################################################################
##                             CMDF Driver                                         ##
#####################################################################################
# This top-level script is used to start CMDF runs. Current functions include       #
# minimization and molecular dynamics in the NVE, NVT, and NPT ensembles.           #
#                                                                                   #
# Usage: "cmdfrun.py inputFileName"                                                 #
#        CMDF runs needs .bgf and .key files as input.                              #
#        Customized control can be done by editing the .key file.                   #
#                                                                                   #
# Last revision: Sep 05, 2006 yi                                                    #
#####################################################################################
import sys
import profile
import datetime
import cmdf.utility.bgfio as bgfio
from cmdf.utility.utility_pf import Utility  
from cmdf.utility.control import Control
#from cmdf.conjugateGradient import *            
#from cmdf.simulatedAnnealing import *
from cmdf.dynamics.mdEngine import MDEngine   
#from cmdf.integrator_pf import *
#from cmdf.thermostat_pf import *
#from cmdf.barostat_pf import *
#from cmdf.distribution import *
#from cmdf.forceEngine import MasterForceEngine
from cmdf.mee.meeForceEngine import MeeForceEngine
from cmdf.mee.mpeForceEngine import MpeForceEngine
#from cmdf.reaxFF.reaxForceEngine import ReaxForceEngine

CMDFstart = datetime.datetime.now()
helpString = """
CMDF usage: cmdfrun.py inputFile
inputFile:  Input file name without extension. 
Note: CMDF runs need .bgf and .key files.
"""
util = Utility()
# Read input file name from command line.
if len(sys.argv) == 1:
    inputFileName = raw_input("Please give an input file name. ") 
else:
    try:
        inputFileName = sys.argv[1]
    except:
        print helpString
        sys.exit(1)

setupStart = datetime.datetime.now()
job = Control()                                      
job.loadSystem(inputFileName)        # Read system from structure file.
job.setParameters(job.system)        # Setup parameters and create objects.
job.setForceEngine(job.forceEngine)  # Setup force engine.
#job.setForceEngine(job.valenceForceEngine, job.coulombForceEngine, job.vdwForceEngine, job.solvationForceEngine)             # Setup force engine.
setupEnd = datetime.datetime.now()
logFile = open(job.molName+'.log', 'a')
logFile.write('System setup timing:\n'); logFile.flush()
util.timer(job.molName, setupStart, setupEnd)

taskStart = datetime.datetime.now()
# Minimization
if (job.task == 'minimize'):  
    profile.run("job.minimizer.run(job.system, job.forceEngine)")  # Run minimizer. 

# Molecular Dynamics 
elif (job.task == 'md'):  
    mdEngine = MDEngine(job.integrator, job.thermostats, job.thermoList, job.barostat, job.gaussian, 
         job.numSteps, job.freqOutputMD, job.freqOutputTrj, job.freqCheckThermoRegion, job.initTemps)

    profile.run("mdEngine.run(job.system, job.forceEngine)")  # Run MD engine.

taskEnd = datetime.datetime.now()
logFile.write('Overall task timing:\n'); logFile.flush()
util.timer(job.molName, taskStart, taskEnd)

writeSystemStart = datetime.datetime.now()
job.writeSystem()  # Write out final system.
writeSystemEnd = datetime.datetime.now()
logFile.write('Write system timing:\n'); logFile.flush()
util.timer(job.molName, writeSystemStart, writeSystemEnd)

CMDFend = datetime.datetime.now()
util.timer(job.molName, CMDFstart, CMDFend)
########################################################################################

