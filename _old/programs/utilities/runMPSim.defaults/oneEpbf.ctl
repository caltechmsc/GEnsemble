# run one-energy calculation with PBF solvation
PROJECT             fm11_oneEpbf                  
*
FF                 /ul/caglar/common/ff/dreidii322-mpsim.par
*                  FF  /ul/vaid/ff/dreidii322-mpsim.par                   
*
BBOX               -180 180 -180 180 -180 180
*
STRUCTURE          fm11_min.fin.bgf
*
NB_METHOD          CMM
CMM_EXPANSION      CENTROID
LEVEL              0
*
*
PBSOLV             Yes
PBEUPDATE          1
PBFUPDATE          1
ACTION             ONE_EF
SETUP_EEX
DO
INFO
EXIT

