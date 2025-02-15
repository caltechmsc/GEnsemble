 
#!/usr/bin/env python
import sys
import os
import re


def findbuild(dirlist):
    for dir in dirlist:
        for name in os.listdir(dir):
            if name == 'build':
                topdir = dir + os.sep + 'build'
                break

    regexp = re.compile("^lib")
    for name in os.listdir(topdir):
        if(regexp.search(name)):
            return topdir + os.sep + name


#### append the system path to find the build directory
buildpath = findbuild([os.curdir, os.pardir])
sys.path.append(buildpath)

import unittest
import test1


class GlobalTest(unittest.TestCase):
     def setUp(self):
	 test1.cvar.d_var = 2.2
	 test1.cvar.i_var = 3

     def testGlobals(self):
	 assert test1.cvar.d_var == 2.2, 'testing global double'
	 assert test1.cvar.i_var == 3, 'testing global integer'
	 

class FunctionTest(unittest.TestCase):
      def setUp(self):
	  self.i = 4
	  self.j = 5

      def testAddTwo(self):
	  assert test1.addtwo(self.i, self.j) == 9, 'testing function call'


######## MAIN COMMAND

if __name__ == "__main__":
    unittest.main()
