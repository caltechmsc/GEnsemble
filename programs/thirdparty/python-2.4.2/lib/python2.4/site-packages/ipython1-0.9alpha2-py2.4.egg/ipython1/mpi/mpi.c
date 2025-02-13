#include <Python.h>
#include "mpi.h"

/* This code was taken from Lisandro Dalcin's mpi4py. */

static int module_called_init = 0;
static int module_called_finalize = 0;


static void mpi_atexit(void) 
{
  int flag, ierr;
  MPI_Initialized(&flag);
  if (!flag || !module_called_init) return;
  MPI_Finalized(&flag);
  if (flag || module_called_finalize) return;
  ierr = MPI_Finalize();
  module_called_finalize = 1;
  if (ierr != MPI_SUCCESS)
  {
    fflush(stderr);
    fprintf(stderr,"MPI_Finalize() failed [error code: %d]",ierr);
    fflush(stderr);
  }
}



static int mpi_init(void) 
{
  int flag_i, flag_f;
  MPI_Finalized(&flag_f);
  if (flag_f) 
  {
    PyErr_SetString(PyExc_RuntimeError,
		    "MPI_Finalize() has been already called");
    return -1;
  }
  MPI_Initialized(&flag_i);
  if (!flag_i) {
    /* initialize MPI */
    int ierr;
    int argc; char** argv;
    Py_GetArgcArgv(&argc, &argv);
    /* This does not work with MPICH !!! */
    ierr = MPI_Init(&argc,&argv);
    if (ierr != MPI_SUCCESS) {
      PyErr_Format(PyExc_RuntimeError,
		   "MPI_Init() failed [error code: %d]",ierr);
      return -1;
    }
    if (Py_AtExit(mpi_atexit) < 0)
      PyErr_Warn(PyExc_RuntimeWarning,
		 "cannot register MPI_Finalize() with Py_AtExit()");
    module_called_init = 1; /* set init flag */
  }
  return 0;
}


static struct PyMethodDef mpi_methods[] = {
    {NULL, NULL}
};

PyMODINIT_FUNC
initmpi(void) 
{

  PyObject* m;

  m = Py_InitModule3("mpi", mpi_methods, "MPI for Brian");
  if (m == NULL)
    return;

  if (mpi_init() < 0) 
    return;

  {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    
    PyModule_AddObject(m, "rank", Py_BuildValue("i",rank)); 
    PyModule_AddObject(m, "size", Py_BuildValue("i",size)); 
  }


}
