
SWIG      = swig

SRCS = vmd_python.C

vmd_python.C : vmd.i VMDApp.h typemaps-python.i
	$(SWIG) -python -c++ -DVMDSWIG_BUILDPYTHON -o vmd_python.C vmd.i

swigclean:
	$(DELETE) vmd_python.C vmd.py
	
