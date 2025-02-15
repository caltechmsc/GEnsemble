# Temp python paths, on /victor/modulasim

setenv PYTHONPATH

# Edit paths to SCREAM script and rotamer libraries here.

set INSTALL_PATH = $1

setenv SCREAM_MAIN_SCRIPT_PATH $INSTALL_PATH/scripts/
setenv SCREAM_LIB_PATH $INSTALL_PATH/lib/v3.0/Clustered/lib/
setenv SCWRL_LIB_PATH $INSTALL_PATH/lib/v3.0/SCWRL/lib/
setenv SCREAM_CNN_PATH $INSTALL_PATH/lib/v3.0/NtrlAARotConn/
setenv SCREAM_DELTA_PAR_FILE_PATH $INSTALL_PATH/lib/SCREAM_delta_par_files/
#set INSTALL_PATH_UP = `dirname $1`
setenv FORCE_FIELD_FILE $INSTALL_PATH/../FF/dreiding-0.3.par
setenv PYTHON_EXE $INSTALL_PATH/../thirdparty/python-2.4.2/bin/python


# Python dependencies.

setenv PYTHONPATH ${PYTHONPATH}:$INSTALL_PATH/SCREAM/swig/python/build/lib.linux-i686-2.3/
setenv PYTHONPATH ${PYTHONPATH}:$INSTALL_PATH/SCREAM/python/app/

# Python dependencies for some of the SCREAM scripts.
setenv PYTHONPATH ${PYTHONPATH}:$INSTALL_PATH/PythonDeps/

