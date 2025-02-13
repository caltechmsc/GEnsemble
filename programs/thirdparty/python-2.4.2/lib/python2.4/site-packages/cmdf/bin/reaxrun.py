#!/usr/bin/env python
#######################################################################
#                                                                     #
# This script runs standalone Reax wrapped in CMDF.                   #
# Input files: control, geo, ffield                                   #
#                                                                     # 
# Created on Aug 21, 2006, Last revision on Aug. 21, 2006 Yi Liu      #
#                                                                     # 
#######################################################################
import os
from cmdf.reaxFF import reax
os.system('cp geo fort.3')
os.system('cp ffield fort.4')
os.system('echo %d.1 > fort.35' % 234535.1)
print 'Reax run started...'
reax.reaxrun()
print 'Reax run completed.'

