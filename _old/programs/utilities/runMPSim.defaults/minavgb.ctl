# minimize under AVGB solvation
PROJECT          YOURPROJECTHERE   
FF                 /ul/caglar/common/ff/dreidii322-mpsim.par
BBOX            -180.0  180.0     -180.0 180.0    -180.0 180.0       
STRUCTURE        YOURBGFFILEHERE
NB_METHOD          CMM
CMM_EXPANSION      CENTROID
LEVEL              4 
NB_UPDATE_FREQ     5
CELL_REALLOC_FREQ  5
LOAD_BAL_FREQ      10
*SGBSOLV            Yes
*SGBEPSIN           2.0
*SGBEPSOUT          80.37
*SGBFUPDATE         50
FSM                /ul/georgios/solvation_parameters/cavity_params_1.3.dat
FSM_PROBE_RADIUS        1.4
FSM_POLAR                T
FSM_EPSILON_IN          1.3
FSM_EPSILON_OUT         78.2
#FSM_IONIC_STRENGTH     0.1
FSM_BORN_UPDATE       250
FSM_CELL_UPDATE       250
FSM_VERBOSE            0
MIN_RMS_DESIRED  0.2
MIN_MAX_STEPS    1000
MIN_METHOD      CONJUGATE_WAG  
ACTION           MINIMIZE      
FINAL_BGF
SETUP_EEX
DO
INFO
EXIT
