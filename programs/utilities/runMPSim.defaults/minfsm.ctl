# minimize under FSM solvation
PROJECT                your-project
*
FF                     /ul/caglar/common/ff/dreidii322-mpsim.par
*
BBOX                   -180 180    -180 180     -180 180
*
STRUCTURE              your.bgf                                                        
*
NB_METHOD              CMM
CMM_EXPANSION          CENTROID
LEVEL                  4
*
NB_UPDATE_FREQ         5
CELL_REALLOC_FREQ      5
LOAD_BAL_FREQ          5
*
FSM                     /ul/georgios/solvation_parameters/fsm_params.dat           
FSM_PROBE_RADIUS        1.4
FSM_POLAR               F
FSM_EPSILON_IN          1.3 
FSM_EPSILON_OUT         78.2
#FSM_IONIC_STRENGTH     0.1
FSM_BORN_UPDATE         50
FSM_CELL_UPDATE         1
FSM_VERBOSE             0
*
MIN_RMS_DESIRED  0.2
MIN_MAX_STEPS    1000
MIN_METHOD             CONJUGATE_WAG
ACTION           MINIMIZE
FINAL_BGF
*
SETUP_EEX
DO
#FINAL_ENER
INFO
EXIT
