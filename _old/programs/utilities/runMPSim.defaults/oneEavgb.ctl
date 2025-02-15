# run one-energy calculation with AVGB solvation
PROJECT            PROJECTNAME
FF                 /ul/caglar/common/ff/dreidii322-mpsim.par
BBOX               -180 180 -180 180 -180 180
STRUCTURE          BGFFILENAME
NB_METHOD          CMM
CMM_EXPANSION      CENTROID
LEVEL              0
HB_CUTOFF          4.0 4.5 5.0 65.0 75.0 90.0
NB_UPDATE_FREQ     5
CELL_REALLOC_FREQ  5
VEL_RESCALE_FREQ   0
LOAD_BAL_FREQ      10
FSM                /ul/georgios/solvation_parameters/cavity_params_1.22.dat
FSM_PROBE_RADIUS   1.4
FSM_POLAR          T
FSM_EPSILON_IN     1.3 
FSM_EPSILON_OUT    78.2
FSM_BORN_UPDATE    50
FSM_CELL_UPDATE    1
FSM_VERBOSE        0
ACTION             ONE_EF
SETUP_EEX
DO
#FINAL_ENER
INFO
EXIT
 
