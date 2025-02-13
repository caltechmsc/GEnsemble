# run one-energy calculation with SGB solvation
PROJECT           DUMMY_oneEsgb
FF                /ul/caglar/common/ff/dreidii322-mpsim.par
BBOX               -180 180 -180 180 -180 180
STRUCTURE         DUMMY.bgf
NB_METHOD          CMM
CMM_EXPANSION      CENTROID
LEVEL              0
NB_UPDATE_FREQ     5
CELL_REALLOC_FREQ  5
LOAD_BAL_FREQ      10
SGBSOLV            Yes
SGBEPSIN           2.0
SGBEPSOUT          80.37
SGBFUPDATE         50
ACTION           ONE_EF  
SETUP_EEX
DO
#FINAL_ENER
INFO
EXIT
