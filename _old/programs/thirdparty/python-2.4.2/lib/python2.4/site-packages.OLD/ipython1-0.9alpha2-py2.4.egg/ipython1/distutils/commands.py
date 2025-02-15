# encoding: utf-8
__docformat__ = "restructuredtext en"

from distutils.command import config as orig_config
from distutils.command import build as orig_build
from distutils.command import build_ext as orig_build_ext
from distutils.command import install as orig_install
from distutils import sysconfig
import os

mpi_cmd_opt = [('mpicc=',  None, "MPI C/C++ compiler command")]

_ConfigTest = """\
int main(int argc, char **argv) {
  MPI_Init(&argc,&argv);
  MPI_Finalize();
  return 0;
}
"""

def setMPIEnvironment(mpicc, mpicxx=None):
    # Swap out just the binaryies, but keep the flags
    # I still need to check to make sure mpicc and mpicxx are 
    # executables in the user's path
       
    ldshared = sysconfig.get_config_var('LDSHARED')
    ldshared = mpicc + ' ' + ldshared.split(' ',1)[1]

    # Override the default compiler with the mpi one
    os.environ['CC'] = mpicc
    if mpicxx is None:
        os.environ['CXX'] = mpicc
    else:
        os.environ['CXX'] = mpicxx    
    os.environ['LDSHARED'] = ldshared  

class config(orig_config.config):

    user_options = orig_config.config.user_options + mpi_cmd_opt
    
    def initialize_options(self):
        orig_config.config.initialize_options(self)
        self.mpicc = None
        
    def finalize_options(self):
        orig_config.config.finalize_options(self)
        if self.mpicc is not None:
            setMPIEnvironment(self.mpicc)
            
    def run(self):
        if self.mpicc is not None:
            self.try_link(_ConfigTest, headers=['mpi.h'])
       
class build(orig_build.build):
    
    user_options = orig_build.build.user_options + mpi_cmd_opt
    
    def initialize_options(self):
        orig_build.build.initialize_options(self)
        self.mpicc = None
        
    def finalize_options(self):
        orig_build.build.finalize_options(self)
        self.set_undefined_options('config',
                                   ('mpicc', 'mpicc'))
        if self.mpicc is not None:
            setMPIEnvironment(self.mpicc)
    
class build_ext(orig_build_ext.build_ext):
    
    user_options = orig_build_ext.build_ext.user_options + mpi_cmd_opt
    
    def initialize_options(self):
        orig_build_ext.build_ext.initialize_options(self)
        self.mpicc = None
        
    def finalize_options(self):
        orig_build_ext.build_ext.finalize_options(self)
        self.set_undefined_options('build',
                                   ('mpicc', 'mpicc'))
        if self.mpicc is not None:
            setMPIEnvironment(self.mpicc)

    def build_extensions(self):
        # First, sanity-check the 'extensions' list
        self.check_extensions_list(self.extensions)

        for ext in self.extensions:
            if ext.name == 'ipython1.mpi' and self.mpicc is None:
                pass
            else:
                self.build_extension(ext)