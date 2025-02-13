# run 10 short annealing cycles without solvation
PROJECT            DUMMY_anneal            
FF                 /ul/caglar/common/ff/dreidii322-mpsim.par
BBOX               -180 180 -180 180 -180 180
STRUCTURE          DUMMY_anneal.bgf            
* 
NB_METHOD          CMM
CMM_EXPANSION      CENTROID
LEVEL              4
*
NB_UPDATE_FREQ     10
CELL_REALLOC_FREQ  10
RESET_GLOBAL_V     T
RESTART_FREQ       500
VEL_START          NONMIN
BGF_TRAJ           T
BGF_TRAJ_FREQ      10
#DYN_TEMP           50    (not needed for T annealing)
DYN_TIME_STEP      1
#DYN_STEPS         1000   (not needed for annealing)
NOSE               tau 0.01

#T stands for true.  Volume(V) and Pressure(P) will also be 
#implemented someday.
ANNEALING_DYNAMICS	T 
#Number of up-down annealing cycles
AD_NUM_CYCLES		10
#minimum setting for annealing variable. (e.g. T-min)
AD_MIN			50
#maximum setting for annealing variable. (e.g. T-max)
AD_MAX			600
#how much to change annealing variable by at each change step
AD_RATE			50
#number of steps between annealing variable changes
AD_STEP_SIZE		100

# Annealing with sgb
*SGBSOLV            Yes
*SGBEPSIN           2.0
*SGBEPSOUT          80.37
*SGBFUPDATE         50

# Annealing with AVGB
*FSM                /ul/georgios/solvation_parameters/cavity_params_1.3.dat
*FSM_PROBE_RADIUS        1.4
*FSM_POLAR                T
*FSM_EPSILON_IN          1.3
*FSM_EPSILON_OUT         78.2
*FSM_IONIC_STRENGTH     0.1
*FSM_BORN_UPDATE       250
*FSM_CELL_UPDATE       250
*FSM_VERBOSE            0

#needed for the minimization done at the end of each ad cycle
MIN_RMS_DESIRED  0.2
MIN_MAX_STEPS    100
MIN_METHOD      CONJUGATE_WAG

#output bgf file at end of simulation
FINAL_BGF
ACTION             TVN
SETUP_EEX
DO
#FINAL_ENER
INFO
EXIT
