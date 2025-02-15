/* $Id: libmpi.h 24 2007-02-24 23:19:13Z dalcinl $ */

#ifndef Py_LIBMPI_H
#define Py_LIBMPI_H

/* Below, some stuff from the top of MPICH2 mpicxx.h ...

   There is a name conflict between stdio.h and the MPI C++ binding 
   with respect to the names SEEK_SET, SEEK_CUR, and SEEK_END.  MPI
   wants these in the MPI namespace, but stdio.h will #define these
   to integer values.  #undef'ing these can cause obscure problems
   with other include files (such as iostream), so we instead use
   #error to indicate a fatal error.  Users can either #undef 
   the names before including mpi.h or include mpi.h *before* stdio.h
   or iostream.

   The MPI STANDARD HAS TO BE CHANGED to prevent this nonsense. 
*/

#include <Python.h>
#include <mpi.h>

#ifdef __cplusplus
extern "C" {
#endif

#if !defined(libmpi_MODULE)

#define libmpi_FatalApiError \
(Py_FatalError("Call to API function without first calling " \
	       "import_libmpi(). [file: " __FILE__ "]"), 0)

#endif /* !libmpi_MODULE */


#if !defined(MPI_VERSION) || (MPI_VERSION < 2)
#if !defined(MPI_INFO_NULL)
#define libmpi_MPI_Info
#define MPI_Info void*
#define MPI_INFO_NULL ((MPI_Info)0)
#endif
#endif

#if !defined(MPI_VERSION) || (MPI_VERSION < 2)
#if !defined(MPI_WIN_NULL)
#define libmpi_MPI_Win
#define MPI_Win void*
#define MPI_WIN_NULL ((MPI_Win)0)
#endif
#endif

#if !defined(MPI_VERSION) || (MPI_VERSION < 2)
#if !defined(MPI_FILE_NULL)
#define libmpi_MPI_File
#define MPI_File void*
#define MPI_FILE_NULL ((MPI_File)0)
#endif
#endif

typedef struct _Py_MPI_Comm {
  PyObject_HEAD
  MPI_Comm comm;
} _Py_MPI_Comm;

typedef struct PyMPICommObject {
  PyObject_HEAD
  PyObject* comm;
} PyMPICommObject;

#define PyMPIComm(ob) \
  ((PyMPICommObject*)(ob))

#define PyMPIComm_AS_COMM(ob) \
  (((_Py_MPI_Comm*)(PyMPIComm(ob)->comm))->comm)

#define PyMPIComm_AS_COMM_PTR(ob) \
  (&PyMPIComm_AS_COMM(ob))


#if defined(libmpi_MODULE)


static int		PyMPIComm_Check(PyObject*);

static int		PyMPIComm_CheckExact(PyObject*);

static PyObject*	PyMPIComm_FromComm(MPI_Comm);

static MPI_Comm 	PyMPIComm_AsComm(PyObject*);

static MPI_Comm*	PyMPIComm_AsCommPtr(PyObject*);


#else /* !defined(libmpi_MODULE) */


static PyTypeObject* PyMPIComm_TYPE = 0;

static void (**PyMPIComm_API)(void) = 0;

#define PyMPIComm_Type \
((PyMPIComm_TYPE?PyMPIComm_TYPE:(PyTypeObject*)libmpi_FatalApiError))

#define PyMPIComm_Check \
( *(int (*)(PyObject*))  \
  (PyMPIComm_API?PyMPIComm_API[0]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIComm_CheckExact \
( *(int (*)(PyObject*)) \
  (PyMPIComm_API?PyMPIComm_API[1]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIComm_FromComm \
( *(PyObject* (*)(MPI_Comm)) \
  (PyMPIComm_API?PyMPIComm_API[2]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIComm_AsComm \
( *(MPI_Comm (*)(PyObject*)) \
  (PyMPIComm_API?PyMPIComm_API[3]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIComm_AsCommPtr \
( *(MPI_Comm* (*)(PyObject*)) \
  (PyMPIComm_API?PyMPIComm_API[4]:(void(*)(void))libmpi_FatalApiError) )


#endif /* libmpi_MODULE */

typedef struct _Py_MPI_Datatype {
  PyObject_HEAD
  MPI_Datatype datatype;
} _Py_MPI_Datatype;

typedef struct PyMPIDatatypeObject {
  PyObject_HEAD
  PyObject* datatype;
} PyMPIDatatypeObject;

#define PyMPIDatatype(ob) \
  ((PyMPIDatatypeObject*)(ob))

#define PyMPIDatatype_AS_DATATYPE(ob) \
  (((_Py_MPI_Datatype*)(PyMPIDatatype(ob)->datatype))->datatype)

#define PyMPIDatatype_AS_DATATYPE_PTR(ob) \
  (&PyMPIDatatype_AS_DATATYPE(ob))


#if defined(libmpi_MODULE)


static int		PyMPIDatatype_Check(PyObject*);

static int		PyMPIDatatype_CheckExact(PyObject*);

static PyObject*	PyMPIDatatype_FromDatatype(MPI_Datatype);

static MPI_Datatype 	PyMPIDatatype_AsDatatype(PyObject*);

static MPI_Datatype*	PyMPIDatatype_AsDatatypePtr(PyObject*);


#else /* !defined(libmpi_MODULE) */


static PyTypeObject* PyMPIDatatype_TYPE = 0;

static void (**PyMPIDatatype_API)(void) = 0;

#define PyMPIDatatype_Type \
((PyMPIDatatype_TYPE?PyMPIDatatype_TYPE:(PyTypeObject*)libmpi_FatalApiError))

#define PyMPIDatatype_Check \
( *(int (*)(PyObject*))  \
  (PyMPIDatatype_API?PyMPIDatatype_API[0]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIDatatype_CheckExact \
( *(int (*)(PyObject*)) \
  (PyMPIDatatype_API?PyMPIDatatype_API[1]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIDatatype_FromDatatype \
( *(PyObject* (*)(MPI_Datatype)) \
  (PyMPIDatatype_API?PyMPIDatatype_API[2]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIDatatype_AsDatatype \
( *(MPI_Datatype (*)(PyObject*)) \
  (PyMPIDatatype_API?PyMPIDatatype_API[3]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIDatatype_AsDatatypePtr \
( *(MPI_Datatype* (*)(PyObject*)) \
  (PyMPIDatatype_API?PyMPIDatatype_API[4]:(void(*)(void))libmpi_FatalApiError) )


#endif /* libmpi_MODULE */

typedef struct _Py_MPI_Errhandler {
  PyObject_HEAD
  MPI_Errhandler errhandler;
} _Py_MPI_Errhandler;

typedef struct PyMPIErrhandlerObject {
  PyObject_HEAD
  PyObject* errhandler;
} PyMPIErrhandlerObject;

#define PyMPIErrhandler(ob) \
  ((PyMPIErrhandlerObject*)(ob))

#define PyMPIErrhandler_AS_ERRHANDLER(ob) \
  (((_Py_MPI_Errhandler*)(PyMPIErrhandler(ob)->errhandler))->errhandler)

#define PyMPIErrhandler_AS_ERRHANDLER_PTR(ob) \
  (&PyMPIErrhandler_AS_ERRHANDLER(ob))


#if defined(libmpi_MODULE)


static int		PyMPIErrhandler_Check(PyObject*);

static int		PyMPIErrhandler_CheckExact(PyObject*);

static PyObject*	PyMPIErrhandler_FromErrhandler(MPI_Errhandler);

static MPI_Errhandler 	PyMPIErrhandler_AsErrhandler(PyObject*);

static MPI_Errhandler*	PyMPIErrhandler_AsErrhandlerPtr(PyObject*);


#else /* !defined(libmpi_MODULE) */


static PyTypeObject* PyMPIErrhandler_TYPE = 0;

static void (**PyMPIErrhandler_API)(void) = 0;

#define PyMPIErrhandler_Type \
((PyMPIErrhandler_TYPE?PyMPIErrhandler_TYPE:(PyTypeObject*)libmpi_FatalApiError))

#define PyMPIErrhandler_Check \
( *(int (*)(PyObject*))  \
  (PyMPIErrhandler_API?PyMPIErrhandler_API[0]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIErrhandler_CheckExact \
( *(int (*)(PyObject*)) \
  (PyMPIErrhandler_API?PyMPIErrhandler_API[1]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIErrhandler_FromErrhandler \
( *(PyObject* (*)(MPI_Errhandler)) \
  (PyMPIErrhandler_API?PyMPIErrhandler_API[2]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIErrhandler_AsErrhandler \
( *(MPI_Errhandler (*)(PyObject*)) \
  (PyMPIErrhandler_API?PyMPIErrhandler_API[3]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIErrhandler_AsErrhandlerPtr \
( *(MPI_Errhandler* (*)(PyObject*)) \
  (PyMPIErrhandler_API?PyMPIErrhandler_API[4]:(void(*)(void))libmpi_FatalApiError) )


#endif /* libmpi_MODULE */

typedef struct _Py_MPI_File {
  PyObject_HEAD
  MPI_File file;
} _Py_MPI_File;

typedef struct PyMPIFileObject {
  PyObject_HEAD
  PyObject* file;
} PyMPIFileObject;

#define PyMPIFile(ob) \
  ((PyMPIFileObject*)(ob))

#define PyMPIFile_AS_FILE(ob) \
  (((_Py_MPI_File*)(PyMPIFile(ob)->file))->file)

#define PyMPIFile_AS_FILE_PTR(ob) \
  (&PyMPIFile_AS_FILE(ob))


#if defined(libmpi_MODULE)


static int		PyMPIFile_Check(PyObject*);

static int		PyMPIFile_CheckExact(PyObject*);

static PyObject*	PyMPIFile_FromFile(MPI_File);

static MPI_File 	PyMPIFile_AsFile(PyObject*);

static MPI_File*	PyMPIFile_AsFilePtr(PyObject*);


#else /* !defined(libmpi_MODULE) */


static PyTypeObject* PyMPIFile_TYPE = 0;

static void (**PyMPIFile_API)(void) = 0;

#define PyMPIFile_Type \
((PyMPIFile_TYPE?PyMPIFile_TYPE:(PyTypeObject*)libmpi_FatalApiError))

#define PyMPIFile_Check \
( *(int (*)(PyObject*))  \
  (PyMPIFile_API?PyMPIFile_API[0]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIFile_CheckExact \
( *(int (*)(PyObject*)) \
  (PyMPIFile_API?PyMPIFile_API[1]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIFile_FromFile \
( *(PyObject* (*)(MPI_File)) \
  (PyMPIFile_API?PyMPIFile_API[2]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIFile_AsFile \
( *(MPI_File (*)(PyObject*)) \
  (PyMPIFile_API?PyMPIFile_API[3]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIFile_AsFilePtr \
( *(MPI_File* (*)(PyObject*)) \
  (PyMPIFile_API?PyMPIFile_API[4]:(void(*)(void))libmpi_FatalApiError) )


#endif /* libmpi_MODULE */

typedef struct _Py_MPI_Group {
  PyObject_HEAD
  MPI_Group group;
} _Py_MPI_Group;

typedef struct PyMPIGroupObject {
  PyObject_HEAD
  PyObject* group;
} PyMPIGroupObject;

#define PyMPIGroup(ob) \
  ((PyMPIGroupObject*)(ob))

#define PyMPIGroup_AS_GROUP(ob) \
  (((_Py_MPI_Group*)(PyMPIGroup(ob)->group))->group)

#define PyMPIGroup_AS_GROUP_PTR(ob) \
  (&PyMPIGroup_AS_GROUP(ob))


#if defined(libmpi_MODULE)


static int		PyMPIGroup_Check(PyObject*);

static int		PyMPIGroup_CheckExact(PyObject*);

static PyObject*	PyMPIGroup_FromGroup(MPI_Group);

static MPI_Group 	PyMPIGroup_AsGroup(PyObject*);

static MPI_Group*	PyMPIGroup_AsGroupPtr(PyObject*);


#else /* !defined(libmpi_MODULE) */


static PyTypeObject* PyMPIGroup_TYPE = 0;

static void (**PyMPIGroup_API)(void) = 0;

#define PyMPIGroup_Type \
((PyMPIGroup_TYPE?PyMPIGroup_TYPE:(PyTypeObject*)libmpi_FatalApiError))

#define PyMPIGroup_Check \
( *(int (*)(PyObject*))  \
  (PyMPIGroup_API?PyMPIGroup_API[0]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIGroup_CheckExact \
( *(int (*)(PyObject*)) \
  (PyMPIGroup_API?PyMPIGroup_API[1]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIGroup_FromGroup \
( *(PyObject* (*)(MPI_Group)) \
  (PyMPIGroup_API?PyMPIGroup_API[2]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIGroup_AsGroup \
( *(MPI_Group (*)(PyObject*)) \
  (PyMPIGroup_API?PyMPIGroup_API[3]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIGroup_AsGroupPtr \
( *(MPI_Group* (*)(PyObject*)) \
  (PyMPIGroup_API?PyMPIGroup_API[4]:(void(*)(void))libmpi_FatalApiError) )


#endif /* libmpi_MODULE */

typedef struct _Py_MPI_Info {
  PyObject_HEAD
  MPI_Info info;
} _Py_MPI_Info;

typedef struct PyMPIInfoObject {
  PyObject_HEAD
  PyObject* info;
} PyMPIInfoObject;

#define PyMPIInfo(ob) \
  ((PyMPIInfoObject*)(ob))

#define PyMPIInfo_AS_INFO(ob) \
  (((_Py_MPI_Info*)(PyMPIInfo(ob)->info))->info)

#define PyMPIInfo_AS_INFO_PTR(ob) \
  (&PyMPIInfo_AS_INFO(ob))


#if defined(libmpi_MODULE)


static int		PyMPIInfo_Check(PyObject*);

static int		PyMPIInfo_CheckExact(PyObject*);

static PyObject*	PyMPIInfo_FromInfo(MPI_Info);

static MPI_Info 	PyMPIInfo_AsInfo(PyObject*);

static MPI_Info*	PyMPIInfo_AsInfoPtr(PyObject*);


#else /* !defined(libmpi_MODULE) */


static PyTypeObject* PyMPIInfo_TYPE = 0;

static void (**PyMPIInfo_API)(void) = 0;

#define PyMPIInfo_Type \
((PyMPIInfo_TYPE?PyMPIInfo_TYPE:(PyTypeObject*)libmpi_FatalApiError))

#define PyMPIInfo_Check \
( *(int (*)(PyObject*))  \
  (PyMPIInfo_API?PyMPIInfo_API[0]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIInfo_CheckExact \
( *(int (*)(PyObject*)) \
  (PyMPIInfo_API?PyMPIInfo_API[1]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIInfo_FromInfo \
( *(PyObject* (*)(MPI_Info)) \
  (PyMPIInfo_API?PyMPIInfo_API[2]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIInfo_AsInfo \
( *(MPI_Info (*)(PyObject*)) \
  (PyMPIInfo_API?PyMPIInfo_API[3]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIInfo_AsInfoPtr \
( *(MPI_Info* (*)(PyObject*)) \
  (PyMPIInfo_API?PyMPIInfo_API[4]:(void(*)(void))libmpi_FatalApiError) )


#endif /* libmpi_MODULE */

typedef struct _Py_MPI_Op {
  PyObject_HEAD
  MPI_Op op;
} _Py_MPI_Op;

typedef struct PyMPIOpObject {
  PyObject_HEAD
  PyObject* op;
} PyMPIOpObject;

#define PyMPIOp(ob) \
  ((PyMPIOpObject*)(ob))

#define PyMPIOp_AS_OP(ob) \
  (((_Py_MPI_Op*)(PyMPIOp(ob)->op))->op)

#define PyMPIOp_AS_OP_PTR(ob) \
  (&PyMPIOp_AS_OP(ob))


#if defined(libmpi_MODULE)


static int		PyMPIOp_Check(PyObject*);

static int		PyMPIOp_CheckExact(PyObject*);

static PyObject*	PyMPIOp_FromOp(MPI_Op);

static MPI_Op 	PyMPIOp_AsOp(PyObject*);

static MPI_Op*	PyMPIOp_AsOpPtr(PyObject*);


#else /* !defined(libmpi_MODULE) */


static PyTypeObject* PyMPIOp_TYPE = 0;

static void (**PyMPIOp_API)(void) = 0;

#define PyMPIOp_Type \
((PyMPIOp_TYPE?PyMPIOp_TYPE:(PyTypeObject*)libmpi_FatalApiError))

#define PyMPIOp_Check \
( *(int (*)(PyObject*))  \
  (PyMPIOp_API?PyMPIOp_API[0]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIOp_CheckExact \
( *(int (*)(PyObject*)) \
  (PyMPIOp_API?PyMPIOp_API[1]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIOp_FromOp \
( *(PyObject* (*)(MPI_Op)) \
  (PyMPIOp_API?PyMPIOp_API[2]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIOp_AsOp \
( *(MPI_Op (*)(PyObject*)) \
  (PyMPIOp_API?PyMPIOp_API[3]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIOp_AsOpPtr \
( *(MPI_Op* (*)(PyObject*)) \
  (PyMPIOp_API?PyMPIOp_API[4]:(void(*)(void))libmpi_FatalApiError) )


#endif /* libmpi_MODULE */

typedef struct _Py_MPI_Request {
  PyObject_HEAD
  MPI_Request request;
} _Py_MPI_Request;

typedef struct PyMPIRequestObject {
  PyObject_HEAD
  PyObject* request;
} PyMPIRequestObject;

#define PyMPIRequest(ob) \
  ((PyMPIRequestObject*)(ob))

#define PyMPIRequest_AS_REQUEST(ob) \
  (((_Py_MPI_Request*)(PyMPIRequest(ob)->request))->request)

#define PyMPIRequest_AS_REQUEST_PTR(ob) \
  (&PyMPIRequest_AS_REQUEST(ob))


#if defined(libmpi_MODULE)


static int		PyMPIRequest_Check(PyObject*);

static int		PyMPIRequest_CheckExact(PyObject*);

static PyObject*	PyMPIRequest_FromRequest(MPI_Request);

static MPI_Request 	PyMPIRequest_AsRequest(PyObject*);

static MPI_Request*	PyMPIRequest_AsRequestPtr(PyObject*);


#else /* !defined(libmpi_MODULE) */


static PyTypeObject* PyMPIRequest_TYPE = 0;

static void (**PyMPIRequest_API)(void) = 0;

#define PyMPIRequest_Type \
((PyMPIRequest_TYPE?PyMPIRequest_TYPE:(PyTypeObject*)libmpi_FatalApiError))

#define PyMPIRequest_Check \
( *(int (*)(PyObject*))  \
  (PyMPIRequest_API?PyMPIRequest_API[0]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIRequest_CheckExact \
( *(int (*)(PyObject*)) \
  (PyMPIRequest_API?PyMPIRequest_API[1]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIRequest_FromRequest \
( *(PyObject* (*)(MPI_Request)) \
  (PyMPIRequest_API?PyMPIRequest_API[2]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIRequest_AsRequest \
( *(MPI_Request (*)(PyObject*)) \
  (PyMPIRequest_API?PyMPIRequest_API[3]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIRequest_AsRequestPtr \
( *(MPI_Request* (*)(PyObject*)) \
  (PyMPIRequest_API?PyMPIRequest_API[4]:(void(*)(void))libmpi_FatalApiError) )


#endif /* libmpi_MODULE */

typedef struct _Py_MPI_Status {
  PyObject_HEAD
  MPI_Status status;
} _Py_MPI_Status;

typedef struct PyMPIStatusObject {
  PyObject_HEAD
  PyObject* status;
} PyMPIStatusObject;

#define PyMPIStatus(ob) \
  ((PyMPIStatusObject*)(ob))

#define PyMPIStatus_AS_STATUS(ob) \
  (((_Py_MPI_Status*)(PyMPIStatus(ob)->status))->status)

#define PyMPIStatus_AS_STATUS_PTR(ob) \
  (&PyMPIStatus_AS_STATUS(ob))


#if defined(libmpi_MODULE)


static int		PyMPIStatus_Check(PyObject*);

static int		PyMPIStatus_CheckExact(PyObject*);

static PyObject*	PyMPIStatus_FromStatus(MPI_Status);

static MPI_Status 	PyMPIStatus_AsStatus(PyObject*);

static MPI_Status*	PyMPIStatus_AsStatusPtr(PyObject*);


#else /* !defined(libmpi_MODULE) */


static PyTypeObject* PyMPIStatus_TYPE = 0;

static void (**PyMPIStatus_API)(void) = 0;

#define PyMPIStatus_Type \
((PyMPIStatus_TYPE?PyMPIStatus_TYPE:(PyTypeObject*)libmpi_FatalApiError))

#define PyMPIStatus_Check \
( *(int (*)(PyObject*))  \
  (PyMPIStatus_API?PyMPIStatus_API[0]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIStatus_CheckExact \
( *(int (*)(PyObject*)) \
  (PyMPIStatus_API?PyMPIStatus_API[1]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIStatus_FromStatus \
( *(PyObject* (*)(MPI_Status)) \
  (PyMPIStatus_API?PyMPIStatus_API[2]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIStatus_AsStatus \
( *(MPI_Status (*)(PyObject*)) \
  (PyMPIStatus_API?PyMPIStatus_API[3]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIStatus_AsStatusPtr \
( *(MPI_Status* (*)(PyObject*)) \
  (PyMPIStatus_API?PyMPIStatus_API[4]:(void(*)(void))libmpi_FatalApiError) )


#endif /* libmpi_MODULE */

typedef struct _Py_MPI_Win {
  PyObject_HEAD
  MPI_Win win;
} _Py_MPI_Win;

typedef struct PyMPIWinObject {
  PyObject_HEAD
  PyObject* win;
} PyMPIWinObject;

#define PyMPIWin(ob) \
  ((PyMPIWinObject*)(ob))

#define PyMPIWin_AS_WIN(ob) \
  (((_Py_MPI_Win*)(PyMPIWin(ob)->win))->win)

#define PyMPIWin_AS_WIN_PTR(ob) \
  (&PyMPIWin_AS_WIN(ob))


#if defined(libmpi_MODULE)


static int		PyMPIWin_Check(PyObject*);

static int		PyMPIWin_CheckExact(PyObject*);

static PyObject*	PyMPIWin_FromWin(MPI_Win);

static MPI_Win 	PyMPIWin_AsWin(PyObject*);

static MPI_Win*	PyMPIWin_AsWinPtr(PyObject*);


#else /* !defined(libmpi_MODULE) */


static PyTypeObject* PyMPIWin_TYPE = 0;

static void (**PyMPIWin_API)(void) = 0;

#define PyMPIWin_Type \
((PyMPIWin_TYPE?PyMPIWin_TYPE:(PyTypeObject*)libmpi_FatalApiError))

#define PyMPIWin_Check \
( *(int (*)(PyObject*))  \
  (PyMPIWin_API?PyMPIWin_API[0]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIWin_CheckExact \
( *(int (*)(PyObject*)) \
  (PyMPIWin_API?PyMPIWin_API[1]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIWin_FromWin \
( *(PyObject* (*)(MPI_Win)) \
  (PyMPIWin_API?PyMPIWin_API[2]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIWin_AsWin \
( *(MPI_Win (*)(PyObject*)) \
  (PyMPIWin_API?PyMPIWin_API[3]:(void(*)(void))libmpi_FatalApiError) )

#define PyMPIWin_AsWinPtr \
( *(MPI_Win* (*)(PyObject*)) \
  (PyMPIWin_API?PyMPIWin_API[4]:(void(*)(void))libmpi_FatalApiError) )


#endif /* libmpi_MODULE */


#if defined(libmpi_MPI_Info)
#undef libmpi_MPI_Info
#undef MPI_Info
#undef MPI_INFO_NULL
#endif

#if defined(libmpi_MPI_Win)
#undef libmpi_MPI_Win
#undef MPI_Win
#undef MPI_WIN_NULL
#endif

#if defined(libmpi_MPI_File)
#undef libmpi_MPI_File
#undef MPI_File
#undef MPI_FILE_NULL
#endif


#if !defined(libmpi_MODULE)

static int import_libmpi(void)
{ 
  PyObject* m = PyImport_ImportModule("mpi4py.libmpi");
  if (m == NULL) return -1;
# define LIBMPI_GET_PYTYPE_AND_CAPI(m,Type) {            \
  PyObject *tp, *api;                                    \
  tp  = PyObject_GetAttrString(m,#Type"Type");           \
  if (tp == NULL) goto fail;                             \
  PyMPI##Type##_TYPE = (PyTypeObject*) tp;               \
  Py_DECREF(tp);                                         \
  api = PyObject_GetAttrString(m,#Type"_API");           \
  if (api == NULL) goto fail;                            \
  PyMPI##Type##_API =                                    \
    (void(**)(void)) PyCObject_AsVoidPtr(api);		 \
  Py_DECREF(api);                                        \
  if (PyMPI##Type##_API == NULL) goto fail;              \
  }
  LIBMPI_GET_PYTYPE_AND_CAPI(m, Op         );
  LIBMPI_GET_PYTYPE_AND_CAPI(m, Win        );
  LIBMPI_GET_PYTYPE_AND_CAPI(m, Comm       );
  LIBMPI_GET_PYTYPE_AND_CAPI(m, Info       );
  LIBMPI_GET_PYTYPE_AND_CAPI(m, File       );
  LIBMPI_GET_PYTYPE_AND_CAPI(m, Group      );
  LIBMPI_GET_PYTYPE_AND_CAPI(m, Status     );
  LIBMPI_GET_PYTYPE_AND_CAPI(m, Request    );
  LIBMPI_GET_PYTYPE_AND_CAPI(m, Datatype   );
  LIBMPI_GET_PYTYPE_AND_CAPI(m, Errhandler );
# undef LIBMPI_GET_PYTYPE_AND_CAPI
  Py_DECREF(m);
  return 0;
 fail:
  Py_DECREF(m);
  PyErr_Clear();
  PyErr_SetString(PyExc_ImportError,
		  "Can't get MPI types or C API from module 'libmpi'");
  return -1;
}

#endif /* !libmpi_MODULE */


#ifdef __cplusplus
}
#endif

#endif /* !Py_LIBMPI_H */

/* 
 * Local Variables:
 * mode: C
 * End:
 */
