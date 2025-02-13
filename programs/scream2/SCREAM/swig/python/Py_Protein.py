# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.
import _Py_Protein
def _swig_setattr(self,class_type,name,value):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    self.__dict__[name] = value

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class Protein(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Protein, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Protein, name)
    def __init__(self,*args):
        _swig_setattr(self, Protein, 'this', apply(_Py_Protein.new_Protein,args))
        _swig_setattr(self, Protein, 'thisown', 1)
    def __del__(self, destroy= _Py_Protein.delete_Protein):
        try:
            if self.thisown: destroy(self)
        except: pass
    def get_AAChain(*args): return apply(_Py_Protein.Protein_get_AAChain,args)
    def get_Ligand(*args): return apply(_Py_Protein.Protein_get_Ligand,args)
    def get_res_type(*args): return apply(_Py_Protein.Protein_get_res_type,args)
    def get_sc_atoms(*args): return apply(_Py_Protein.Protein_get_sc_atoms,args)
    def get_variable_atoms(*args): return apply(_Py_Protein.Protein_get_variable_atoms,args)
    def getAtomList(*args): return apply(_Py_Protein.Protein_getAtomList,args)
    def getAtom(*args): return apply(_Py_Protein.Protein_getAtom,args)
    def getTheseAtoms(*args): return apply(_Py_Protein.Protein_getTheseAtoms,args)
    def totalComponents(*args): return apply(_Py_Protein.Protein_totalComponents,args)
    def ntrlRotamerPlacement(*args): return apply(_Py_Protein.Protein_ntrlRotamerPlacement,args)
    def conformerPlacement(*args): return apply(_Py_Protein.Protein_conformerPlacement,args)
    def conformerExtraction(*args): return apply(_Py_Protein.Protein_conformerExtraction,args)
    def mutation(*args): return apply(_Py_Protein.Protein_mutation,args)
    def sc_clash(*args): return apply(_Py_Protein.Protein_sc_clash,args)
    def conformer_clash(*args): return apply(_Py_Protein.Protein_conformer_clash,args)
    def sc_CRMS(*args): return apply(_Py_Protein.Protein_sc_CRMS,args)
    def conformer_CRMS(*args): return apply(_Py_Protein.Protein_conformer_CRMS,args)
    def max_atom_dist_on_SC(*args): return apply(_Py_Protein.Protein_max_atom_dist_on_SC,args)
    def fix_entire_atom_list_ordering(*args): return apply(_Py_Protein.Protein_fix_entire_atom_list_ordering,args)
    def fix_toggle(*args): return apply(_Py_Protein.Protein_fix_toggle,args)
    def fix_sc_toggle(*args): return apply(_Py_Protein.Protein_fix_sc_toggle,args)
    def append_to_filehandle(*args): return apply(_Py_Protein.Protein_append_to_filehandle,args)
    def pdb_append_to_filehandle(*args): return apply(_Py_Protein.Protein_pdb_append_to_filehandle,args)
    def print_bgf_file(*args): return apply(_Py_Protein.Protein_print_bgf_file,args)
    def print_Me(*args): return apply(_Py_Protein.Protein_print_Me,args)
    def print_ordered_by_n(*args): return apply(_Py_Protein.Protein_print_ordered_by_n,args)
    def __repr__(self):
        return "<C Protein instance at %s>" % (self.this,)

class ProteinPtr(Protein):
    def __init__(self,this):
        _swig_setattr(self, Protein, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, Protein, 'thisown', 0)
        _swig_setattr(self, Protein,self.__class__,Protein)
_Py_Protein.Protein_swigregister(ProteinPtr)


