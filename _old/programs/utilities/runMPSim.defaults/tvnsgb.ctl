# run TVN dynamics with SGB solvation
PROJECT            DUMMY-tvn
*
FF                 /ul/caglar/common/ff/dreidii322-mpsim.par
*
BBOX               -240 240 -240 240 -240 240 
*
STRUCTURE          DUMMY.bgf                     
*
NB_METHOD          CMM
CMM_EXPANSION      CENTROID
LEVEL              4
*
NB_UPDATE_FREQ     5
CELL_REALLOC_FREQ  5
VEL_RESCALE_FREQ   0
LOAD_BAL_FREQ      10
VEL_START           NONMIN
SGBSOLV            Yes
SGBEPSIN           2.0
SGBEPSOUT          80.37
SGBFUPDATE         50
DYN_TEMP           300
DYN_TIME_STEP      1
DYN_STEPS          20000
NOSE               tau 0.01 
*
ACTION             TVN   
SETUP_EEX
DO
INFO
EXIT
