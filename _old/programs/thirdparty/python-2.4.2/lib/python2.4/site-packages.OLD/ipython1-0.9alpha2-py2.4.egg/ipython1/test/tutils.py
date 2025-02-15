"""Utilities for testing code.
"""

# Required modules and packages

# Standard Python lib
import os
import sys

# From this project

# path to our own installation, so we can find source files under this.
TEST_PATH = os.path.dirname(os.path.abspath(__file__))

# Global flag, used by vprint
VERBOSE = '-v' in sys.argv or '--verbose' in sys.argv

##########################################################################
# Code begins

# Some utility functions
def vprint(*args):
    """Print-like function which relies on a global VERBOSE flag."""
    if not VERBOSE:
        return

    write = sys.stdout.write
    for item in args:
        write(str(item))
    write('\n')
    sys.stdout.flush()

def test_path(path):
    """Return a path as a subdir of the test package.

    This finds the correct path of the test package on disk, and prepends it
    to the input path."""
    
    return os.path.join(TEST_PATH,path)
