# Setup - all imports are done in tcommon
from ipython1.test import tcommon
from ipython1.test.tcommon import *

# Doctest code begins here
from ipython1.tools import utils

# Some other tests for utils

utils.marquee('Testing marquee')

utils.marquee('Another test',30,'.')

