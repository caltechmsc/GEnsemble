import sys, os, math
from types import *
from cmdf.pymodsim.io.parameters import get_defaults_param_path, modsim_type_map, get_param_dict, init_parameters, set_parameters, set_params_from_dict, check_dir
import ModulaSim

# Definition of SCREAM_parameters structure.  this is derived from PARAMTERS, a C struct that has been swigged.
# 

class SCREAM_parameters(ModulaSim.PARAMETERS):
    '''
    Derives from Parameters for easier handling of init, set, read params.
    '''

    def __init__(self):
        ModulaSim.PARAMETERS.__init__(self)
        self.SCREAM_ctl_file = ''
    def init_parameters(self):
         """
         Initializes the parameters object with
         the default values found in defaults.param
         """
         filepath = get_defaults_param_path()
         if not filepath:
             raise 'No defaults.param file found.'
         
         # initialize modsim parameters from defaults.param file
         self.set_parameters(filepath)
         
    def set_parameters(self, filename):
        """
        Reads the specified .param file and sets
        the parameters object accordingly.
        Calls parameters::set_parameters. 
        """
        if not os.path.exists(filename):
            raise '.param file not found.'
        
        params_dict = get_param_dict(filename)
        type_map = modsim_type_map
        type_map['SCREAM_ctl_file'] = StringType
        
        # sets modsim parameters from .param file
        set_params_from_dict(self, params_dict, type_map)
        print 'printing SCREAM_ctl_file', getattr(self, 'SCREAM_ctl_file', 'NO_SCREAM_CTL_FILE_FOUND')
        # calculate derived parameters
        self.ctheta_on_hbdre = math.cos(self.theta_on_hbdre * math.pi / 180.0)
        self.ctheta_off_hbdre = math.cos(self.theta_off_hbdre * math.pi / 180.0)
        self.epsilon = 332.0637 / self.epsilon
        check_dir(self)


