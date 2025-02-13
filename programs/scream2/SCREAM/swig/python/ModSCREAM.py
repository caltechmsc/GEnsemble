# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _ModSCREAM

def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name) or (name == "thisown"):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

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
del types


class stringV(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, stringV, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, stringV, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ std::vector<std::string > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def empty(*args): return _ModSCREAM.stringV_empty(*args)
    def size(*args): return _ModSCREAM.stringV_size(*args)
    def clear(*args): return _ModSCREAM.stringV_clear(*args)
    def swap(*args): return _ModSCREAM.stringV_swap(*args)
    def get_allocator(*args): return _ModSCREAM.stringV_get_allocator(*args)
    def pop_back(*args): return _ModSCREAM.stringV_pop_back(*args)
    def __init__(self, *args):
        _swig_setattr(self, stringV, 'this', _ModSCREAM.new_stringV(*args))
        _swig_setattr(self, stringV, 'thisown', 1)
    def push_back(*args): return _ModSCREAM.stringV_push_back(*args)
    def front(*args): return _ModSCREAM.stringV_front(*args)
    def back(*args): return _ModSCREAM.stringV_back(*args)
    def assign(*args): return _ModSCREAM.stringV_assign(*args)
    def resize(*args): return _ModSCREAM.stringV_resize(*args)
    def reserve(*args): return _ModSCREAM.stringV_reserve(*args)
    def capacity(*args): return _ModSCREAM.stringV_capacity(*args)
    def __nonzero__(*args): return _ModSCREAM.stringV___nonzero__(*args)
    def __len__(*args): return _ModSCREAM.stringV___len__(*args)
    def pop(*args): return _ModSCREAM.stringV_pop(*args)
    def __getslice__(*args): return _ModSCREAM.stringV___getslice__(*args)
    def __setslice__(*args): return _ModSCREAM.stringV___setslice__(*args)
    def __delslice__(*args): return _ModSCREAM.stringV___delslice__(*args)
    def __delitem__(*args): return _ModSCREAM.stringV___delitem__(*args)
    def __getitem__(*args): return _ModSCREAM.stringV___getitem__(*args)
    def __setitem__(*args): return _ModSCREAM.stringV___setitem__(*args)
    def append(*args): return _ModSCREAM.stringV_append(*args)
    def __del__(self, destroy=_ModSCREAM.delete_stringV):
        try:
            if self.thisown: destroy(self)
        except: pass


class stringVPtr(stringV):
    def __init__(self, this):
        _swig_setattr(self, stringV, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, stringV, 'thisown', 0)
        _swig_setattr(self, stringV,self.__class__,stringV)
_ModSCREAM.stringV_swigregister(stringVPtr)

class ExcitationEnumeration(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ExcitationEnumeration, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ExcitationEnumeration, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ std::map<std::string,int > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, ExcitationEnumeration, 'this', _ModSCREAM.new_ExcitationEnumeration(*args))
        _swig_setattr(self, ExcitationEnumeration, 'thisown', 1)
    def empty(*args): return _ModSCREAM.ExcitationEnumeration_empty(*args)
    def size(*args): return _ModSCREAM.ExcitationEnumeration_size(*args)
    def clear(*args): return _ModSCREAM.ExcitationEnumeration_clear(*args)
    def swap(*args): return _ModSCREAM.ExcitationEnumeration_swap(*args)
    def get_allocator(*args): return _ModSCREAM.ExcitationEnumeration_get_allocator(*args)
    def erase(*args): return _ModSCREAM.ExcitationEnumeration_erase(*args)
    def count(*args): return _ModSCREAM.ExcitationEnumeration_count(*args)
    def __nonzero__(*args): return _ModSCREAM.ExcitationEnumeration___nonzero__(*args)
    def __len__(*args): return _ModSCREAM.ExcitationEnumeration___len__(*args)
    def __getitem__(*args): return _ModSCREAM.ExcitationEnumeration___getitem__(*args)
    def __setitem__(*args): return _ModSCREAM.ExcitationEnumeration___setitem__(*args)
    def __delitem__(*args): return _ModSCREAM.ExcitationEnumeration___delitem__(*args)
    def has_key(*args): return _ModSCREAM.ExcitationEnumeration_has_key(*args)
    def keys(*args): return _ModSCREAM.ExcitationEnumeration_keys(*args)
    def values(*args): return _ModSCREAM.ExcitationEnumeration_values(*args)
    def items(*args): return _ModSCREAM.ExcitationEnumeration_items(*args)
    def __contains__(*args): return _ModSCREAM.ExcitationEnumeration___contains__(*args)
    def __iter__(*args): return _ModSCREAM.ExcitationEnumeration___iter__(*args)
    def __del__(self, destroy=_ModSCREAM.delete_ExcitationEnumeration):
        try:
            if self.thisown: destroy(self)
        except: pass


class ExcitationEnumerationPtr(ExcitationEnumeration):
    def __init__(self, this):
        _swig_setattr(self, ExcitationEnumeration, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ExcitationEnumeration, 'thisown', 0)
        _swig_setattr(self, ExcitationEnumeration,self.__class__,ExcitationEnumeration)
_ModSCREAM.ExcitationEnumeration_swigregister(ExcitationEnumerationPtr)

class ExcitedRotamers(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ExcitedRotamers, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ExcitedRotamers, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ std::map<std::string,Rotamer * > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, ExcitedRotamers, 'this', _ModSCREAM.new_ExcitedRotamers(*args))
        _swig_setattr(self, ExcitedRotamers, 'thisown', 1)
    def empty(*args): return _ModSCREAM.ExcitedRotamers_empty(*args)
    def size(*args): return _ModSCREAM.ExcitedRotamers_size(*args)
    def clear(*args): return _ModSCREAM.ExcitedRotamers_clear(*args)
    def swap(*args): return _ModSCREAM.ExcitedRotamers_swap(*args)
    def get_allocator(*args): return _ModSCREAM.ExcitedRotamers_get_allocator(*args)
    def erase(*args): return _ModSCREAM.ExcitedRotamers_erase(*args)
    def count(*args): return _ModSCREAM.ExcitedRotamers_count(*args)
    def __nonzero__(*args): return _ModSCREAM.ExcitedRotamers___nonzero__(*args)
    def __len__(*args): return _ModSCREAM.ExcitedRotamers___len__(*args)
    def __getitem__(*args): return _ModSCREAM.ExcitedRotamers___getitem__(*args)
    def __setitem__(*args): return _ModSCREAM.ExcitedRotamers___setitem__(*args)
    def __delitem__(*args): return _ModSCREAM.ExcitedRotamers___delitem__(*args)
    def has_key(*args): return _ModSCREAM.ExcitedRotamers_has_key(*args)
    def keys(*args): return _ModSCREAM.ExcitedRotamers_keys(*args)
    def values(*args): return _ModSCREAM.ExcitedRotamers_values(*args)
    def items(*args): return _ModSCREAM.ExcitedRotamers_items(*args)
    def __contains__(*args): return _ModSCREAM.ExcitedRotamers___contains__(*args)
    def __iter__(*args): return _ModSCREAM.ExcitedRotamers___iter__(*args)
    def __del__(self, destroy=_ModSCREAM.delete_ExcitedRotamers):
        try:
            if self.thisown: destroy(self)
        except: pass


class ExcitedRotamersPtr(ExcitedRotamers):
    def __init__(self, this):
        _swig_setattr(self, ExcitedRotamers, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ExcitedRotamers, 'thisown', 0)
        _swig_setattr(self, ExcitedRotamers,self.__class__,ExcitedRotamers)
_ModSCREAM.ExcitedRotamers_swigregister(ExcitedRotamersPtr)

class pairds(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, pairds, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, pairds, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ pair<double,string > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    __swig_setmethods__["first"] = _ModSCREAM.pairds_first_set
    __swig_getmethods__["first"] = _ModSCREAM.pairds_first_get
    if _newclass:first = property(_ModSCREAM.pairds_first_get, _ModSCREAM.pairds_first_set)
    __swig_setmethods__["second"] = _ModSCREAM.pairds_second_set
    __swig_getmethods__["second"] = _ModSCREAM.pairds_second_get
    if _newclass:second = property(_ModSCREAM.pairds_second_get, _ModSCREAM.pairds_second_set)
    def __init__(self, *args):
        _swig_setattr(self, pairds, 'this', _ModSCREAM.new_pairds(*args))
        _swig_setattr(self, pairds, 'thisown', 1)
    def __del__(self, destroy=_ModSCREAM.delete_pairds):
        try:
            if self.thisown: destroy(self)
        except: pass


class pairdsPtr(pairds):
    def __init__(self, this):
        _swig_setattr(self, pairds, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, pairds, 'thisown', 0)
        _swig_setattr(self, pairds,self.__class__,pairds)
_ModSCREAM.pairds_swigregister(pairdsPtr)

class ScreamParameters_for_modsim(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ScreamParameters_for_modsim, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ScreamParameters_for_modsim, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ ScreamParameters_for_modsim instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, ScreamParameters_for_modsim, 'this', _ModSCREAM.new_ScreamParameters_for_modsim(*args))
        _swig_setattr(self, ScreamParameters_for_modsim, 'thisown', 1)
    __swig_setmethods__["InputFileName"] = _ModSCREAM.ScreamParameters_for_modsim_InputFileName_set
    __swig_getmethods__["InputFileName"] = _ModSCREAM.ScreamParameters_for_modsim_InputFileName_get
    if _newclass:InputFileName = property(_ModSCREAM.ScreamParameters_for_modsim_InputFileName_get, _ModSCREAM.ScreamParameters_for_modsim_InputFileName_set)
    __swig_setmethods__["MutateResidueInfo"] = _ModSCREAM.ScreamParameters_for_modsim_MutateResidueInfo_set
    __swig_getmethods__["MutateResidueInfo"] = _ModSCREAM.ScreamParameters_for_modsim_MutateResidueInfo_get
    if _newclass:MutateResidueInfo = property(_ModSCREAM.ScreamParameters_for_modsim_MutateResidueInfo_get, _ModSCREAM.ScreamParameters_for_modsim_MutateResidueInfo_set)
    __swig_setmethods__["AdditionalLibraryInfo"] = _ModSCREAM.ScreamParameters_for_modsim_AdditionalLibraryInfo_set
    __swig_getmethods__["AdditionalLibraryInfo"] = _ModSCREAM.ScreamParameters_for_modsim_AdditionalLibraryInfo_get
    if _newclass:AdditionalLibraryInfo = property(_ModSCREAM.ScreamParameters_for_modsim_AdditionalLibraryInfo_get, _ModSCREAM.ScreamParameters_for_modsim_AdditionalLibraryInfo_set)
    __swig_setmethods__["Library"] = _ModSCREAM.ScreamParameters_for_modsim_Library_set
    __swig_getmethods__["Library"] = _ModSCREAM.ScreamParameters_for_modsim_Library_get
    if _newclass:Library = property(_ModSCREAM.ScreamParameters_for_modsim_Library_get, _ModSCREAM.ScreamParameters_for_modsim_Library_set)
    __swig_setmethods__["KeepOriginalRotamer"] = _ModSCREAM.ScreamParameters_for_modsim_KeepOriginalRotamer_set
    __swig_getmethods__["KeepOriginalRotamer"] = _ModSCREAM.ScreamParameters_for_modsim_KeepOriginalRotamer_get
    if _newclass:KeepOriginalRotamer = property(_ModSCREAM.ScreamParameters_for_modsim_KeepOriginalRotamer_get, _ModSCREAM.ScreamParameters_for_modsim_KeepOriginalRotamer_set)
    __swig_setmethods__["UseScreamEnergyFunction"] = _ModSCREAM.ScreamParameters_for_modsim_UseScreamEnergyFunction_set
    __swig_getmethods__["UseScreamEnergyFunction"] = _ModSCREAM.ScreamParameters_for_modsim_UseScreamEnergyFunction_get
    if _newclass:UseScreamEnergyFunction = property(_ModSCREAM.ScreamParameters_for_modsim_UseScreamEnergyFunction_get, _ModSCREAM.ScreamParameters_for_modsim_UseScreamEnergyFunction_set)
    __swig_setmethods__["ScoringFunction"] = _ModSCREAM.ScreamParameters_for_modsim_ScoringFunction_set
    __swig_getmethods__["ScoringFunction"] = _ModSCREAM.ScreamParameters_for_modsim_ScoringFunction_get
    if _newclass:ScoringFunction = property(_ModSCREAM.ScreamParameters_for_modsim_ScoringFunction_get, _ModSCREAM.ScreamParameters_for_modsim_ScoringFunction_set)
    __swig_setmethods__["MultiplePlacementMethod"] = _ModSCREAM.ScreamParameters_for_modsim_MultiplePlacementMethod_set
    __swig_getmethods__["MultiplePlacementMethod"] = _ModSCREAM.ScreamParameters_for_modsim_MultiplePlacementMethod_get
    if _newclass:MultiplePlacementMethod = property(_ModSCREAM.ScreamParameters_for_modsim_MultiplePlacementMethod_get, _ModSCREAM.ScreamParameters_for_modsim_MultiplePlacementMethod_set)
    __swig_setmethods__["CombinatorialRule"] = _ModSCREAM.ScreamParameters_for_modsim_CombinatorialRule_set
    __swig_getmethods__["CombinatorialRule"] = _ModSCREAM.ScreamParameters_for_modsim_CombinatorialRule_get
    if _newclass:CombinatorialRule = property(_ModSCREAM.ScreamParameters_for_modsim_CombinatorialRule_get, _ModSCREAM.ScreamParameters_for_modsim_CombinatorialRule_set)
    __swig_setmethods__["OneEnergyFFParFile"] = _ModSCREAM.ScreamParameters_for_modsim_OneEnergyFFParFile_set
    __swig_getmethods__["OneEnergyFFParFile"] = _ModSCREAM.ScreamParameters_for_modsim_OneEnergyFFParFile_get
    if _newclass:OneEnergyFFParFile = property(_ModSCREAM.ScreamParameters_for_modsim_OneEnergyFFParFile_get, _ModSCREAM.ScreamParameters_for_modsim_OneEnergyFFParFile_set)
    __swig_setmethods__["Selections"] = _ModSCREAM.ScreamParameters_for_modsim_Selections_set
    __swig_getmethods__["Selections"] = _ModSCREAM.ScreamParameters_for_modsim_Selections_get
    if _newclass:Selections = property(_ModSCREAM.ScreamParameters_for_modsim_Selections_get, _ModSCREAM.ScreamParameters_for_modsim_Selections_set)
    __swig_setmethods__["EmptyBackbone"] = _ModSCREAM.ScreamParameters_for_modsim_EmptyBackbone_set
    __swig_getmethods__["EmptyBackbone"] = _ModSCREAM.ScreamParameters_for_modsim_EmptyBackbone_get
    if _newclass:EmptyBackbone = property(_ModSCREAM.ScreamParameters_for_modsim_EmptyBackbone_get, _ModSCREAM.ScreamParameters_for_modsim_EmptyBackbone_set)
    __swig_setmethods__["IterationSetup"] = _ModSCREAM.ScreamParameters_for_modsim_IterationSetup_set
    __swig_getmethods__["IterationSetup"] = _ModSCREAM.ScreamParameters_for_modsim_IterationSetup_get
    if _newclass:IterationSetup = property(_ModSCREAM.ScreamParameters_for_modsim_IterationSetup_get, _ModSCREAM.ScreamParameters_for_modsim_IterationSetup_set)
    __swig_setmethods__["NewLibraryDieSequence"] = _ModSCREAM.ScreamParameters_for_modsim_NewLibraryDieSequence_set
    __swig_getmethods__["NewLibraryDieSequence"] = _ModSCREAM.ScreamParameters_for_modsim_NewLibraryDieSequence_get
    if _newclass:NewLibraryDieSequence = property(_ModSCREAM.ScreamParameters_for_modsim_NewLibraryDieSequence_get, _ModSCREAM.ScreamParameters_for_modsim_NewLibraryDieSequence_set)
    __swig_setmethods__["StericClashCutoffEnergy"] = _ModSCREAM.ScreamParameters_for_modsim_StericClashCutoffEnergy_set
    __swig_getmethods__["StericClashCutoffEnergy"] = _ModSCREAM.ScreamParameters_for_modsim_StericClashCutoffEnergy_get
    if _newclass:StericClashCutoffEnergy = property(_ModSCREAM.ScreamParameters_for_modsim_StericClashCutoffEnergy_get, _ModSCREAM.ScreamParameters_for_modsim_StericClashCutoffEnergy_set)
    __swig_setmethods__["StericClashCutoffDist"] = _ModSCREAM.ScreamParameters_for_modsim_StericClashCutoffDist_set
    __swig_getmethods__["StericClashCutoffDist"] = _ModSCREAM.ScreamParameters_for_modsim_StericClashCutoffDist_get
    if _newclass:StericClashCutoffDist = property(_ModSCREAM.ScreamParameters_for_modsim_StericClashCutoffDist_get, _ModSCREAM.ScreamParameters_for_modsim_StericClashCutoffDist_set)
    __swig_setmethods__["Permutation"] = _ModSCREAM.ScreamParameters_for_modsim_Permutation_set
    __swig_getmethods__["Permutation"] = _ModSCREAM.ScreamParameters_for_modsim_Permutation_get
    if _newclass:Permutation = property(_ModSCREAM.ScreamParameters_for_modsim_Permutation_get, _ModSCREAM.ScreamParameters_for_modsim_Permutation_set)
    __swig_setmethods__["OutputDirectory"] = _ModSCREAM.ScreamParameters_for_modsim_OutputDirectory_set
    __swig_getmethods__["OutputDirectory"] = _ModSCREAM.ScreamParameters_for_modsim_OutputDirectory_get
    if _newclass:OutputDirectory = property(_ModSCREAM.ScreamParameters_for_modsim_OutputDirectory_get, _ModSCREAM.ScreamParameters_for_modsim_OutputDirectory_set)
    __swig_setmethods__["LibPath"] = _ModSCREAM.ScreamParameters_for_modsim_LibPath_set
    __swig_getmethods__["LibPath"] = _ModSCREAM.ScreamParameters_for_modsim_LibPath_get
    if _newclass:LibPath = property(_ModSCREAM.ScreamParameters_for_modsim_LibPath_get, _ModSCREAM.ScreamParameters_for_modsim_LibPath_set)
    def getMutateResidueInfoList(*args): return _ModSCREAM.ScreamParameters_for_modsim_getMutateResidueInfoList(*args)
    def getAdditionalLibraryInfo(*args): return _ModSCREAM.ScreamParameters_for_modsim_getAdditionalLibraryInfo(*args)
    def getKeepOriginalRotamer(*args): return _ModSCREAM.ScreamParameters_for_modsim_getKeepOriginalRotamer(*args)
    def getUseScreamEnergyFunction(*args): return _ModSCREAM.ScreamParameters_for_modsim_getUseScreamEnergyFunction(*args)
    def multiplePlacementMethod(*args): return _ModSCREAM.ScreamParameters_for_modsim_multiplePlacementMethod(*args)
    def read_scream_par_file(*args): return _ModSCREAM.ScreamParameters_for_modsim_read_scream_par_file(*args)
    def print_to_output(*args): return _ModSCREAM.ScreamParameters_for_modsim_print_to_output(*args)
    def minimizationMethod(*args): return _ModSCREAM.ScreamParameters_for_modsim_minimizationMethod(*args)
    def minimizationSteps(*args): return _ModSCREAM.ScreamParameters_for_modsim_minimizationSteps(*args)
    def oneEMethod(*args): return _ModSCREAM.ScreamParameters_for_modsim_oneEMethod(*args)
    def residueToScreamName(*args): return _ModSCREAM.ScreamParameters_for_modsim_residueToScreamName(*args)
    def residueToScreamPstn(*args): return _ModSCREAM.ScreamParameters_for_modsim_residueToScreamPstn(*args)
    def residueToScreamChn(*args): return _ModSCREAM.ScreamParameters_for_modsim_residueToScreamChn(*args)
    def determineLibDirPath(*args): return _ModSCREAM.ScreamParameters_for_modsim_determineLibDirPath(*args)
    def determineLibDirFileNameSuffix(*args): return _ModSCREAM.ScreamParameters_for_modsim_determineLibDirFileNameSuffix(*args)
    def _init_default_params(*args): return _ModSCREAM.ScreamParameters_for_modsim__init_default_params(*args)
    def __del__(self, destroy=_ModSCREAM.delete_ScreamParameters_for_modsim):
        try:
            if self.thisown: destroy(self)
        except: pass


class ScreamParameters_for_modsimPtr(ScreamParameters_for_modsim):
    def __init__(self, this):
        _swig_setattr(self, ScreamParameters_for_modsim, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ScreamParameters_for_modsim, 'thisown', 0)
        _swig_setattr(self, ScreamParameters_for_modsim,self.__class__,ScreamParameters_for_modsim)
_ModSCREAM.ScreamParameters_for_modsim_swigregister(ScreamParameters_for_modsimPtr)

class Rotamer(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Rotamer, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Rotamer, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ Rotamer instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, Rotamer, 'this', _ModSCREAM.new_Rotamer(*args))
        _swig_setattr(self, Rotamer, 'thisown', 1)
    def __del__(self, destroy=_ModSCREAM.delete_Rotamer):
        try:
            if self.thisown: destroy(self)
        except: pass

    def deepcopy(*args): return _ModSCREAM.Rotamer_deepcopy(*args)
    def read_cnn_lines(*args): return _ModSCREAM.Rotamer_read_cnn_lines(*args)
    def print_Me(*args): return _ModSCREAM.Rotamer_print_Me(*args)
    def print_ordered_by_n(*args): return _ModSCREAM.Rotamer_print_ordered_by_n(*args)
    def append_to_filehandle(*args): return _ModSCREAM.Rotamer_append_to_filehandle(*args)
    def pdb_append_to_filehandle(*args): return _ModSCREAM.Rotamer_pdb_append_to_filehandle(*args)
    def append_to_ostream_connect_info(*args): return _ModSCREAM.Rotamer_append_to_ostream_connect_info(*args)
    __swig_setmethods__["self_E"] = _ModSCREAM.Rotamer_self_E_set
    __swig_getmethods__["self_E"] = _ModSCREAM.Rotamer_self_E_get
    if _newclass:self_E = property(_ModSCREAM.Rotamer_self_E_get, _ModSCREAM.Rotamer_self_E_set)
    __swig_setmethods__["is_Original"] = _ModSCREAM.Rotamer_is_Original_set
    __swig_getmethods__["is_Original"] = _ModSCREAM.Rotamer_is_Original_get
    if _newclass:is_Original = property(_ModSCREAM.Rotamer_is_Original_get, _ModSCREAM.Rotamer_is_Original_set)
    __swig_setmethods__["same_backbone"] = _ModSCREAM.Rotamer_same_backbone_set
    __swig_getmethods__["same_backbone"] = _ModSCREAM.Rotamer_same_backbone_get
    if _newclass:same_backbone = property(_ModSCREAM.Rotamer_same_backbone_get, _ModSCREAM.Rotamer_same_backbone_set)
    __swig_setmethods__["library_name"] = _ModSCREAM.Rotamer_library_name_set
    __swig_getmethods__["library_name"] = _ModSCREAM.Rotamer_library_name_get
    if _newclass:library_name = property(_ModSCREAM.Rotamer_library_name_get, _ModSCREAM.Rotamer_library_name_set)
    def get_bb(*args): return _ModSCREAM.Rotamer_get_bb(*args)
    def get_sc(*args): return _ModSCREAM.Rotamer_get_sc(*args)
    def get_sc_atoms(*args): return _ModSCREAM.Rotamer_get_sc_atoms(*args)
    def get_bb_atoms(*args): return _ModSCREAM.Rotamer_get_bb_atoms(*args)
    def getAtom(*args): return _ModSCREAM.Rotamer_getAtom(*args)
    def getTheseAtoms(*args): return _ModSCREAM.Rotamer_getTheseAtoms(*args)
    def fix_toggle(*args): return _ModSCREAM.Rotamer_fix_toggle(*args)
    def fix_sc_toggle(*args): return _ModSCREAM.Rotamer_fix_sc_toggle(*args)
    def fix_bb_toggle(*args): return _ModSCREAM.Rotamer_fix_bb_toggle(*args)
    def number_of_atoms(*args): return _ModSCREAM.Rotamer_number_of_atoms(*args)
    def total_charge(*args): return _ModSCREAM.Rotamer_total_charge(*args)
    def get_rotamer_n(*args): return _ModSCREAM.Rotamer_get_rotamer_n(*args)
    def get_mult_H_n(*args): return _ModSCREAM.Rotamer_get_mult_H_n(*args)
    def get_library_name(*args): return _ModSCREAM.Rotamer_get_library_name(*args)
    def get_empty_lattice_E(*args): return _ModSCREAM.Rotamer_get_empty_lattice_E(*args)
    def get_zeroth_excitation_baseline_E(*args): return _ModSCREAM.Rotamer_get_zeroth_excitation_baseline_E(*args)
    def get_current_baseline_E(*args): return _ModSCREAM.Rotamer_get_current_baseline_E(*args)
    def set_empty_lattice_E(*args): return _ModSCREAM.Rotamer_set_empty_lattice_E(*args)
    def set_zeroth_excitation_baseline_E(*args): return _ModSCREAM.Rotamer_set_zeroth_excitation_baseline_E(*args)
    def set_current_baseline_E(*args): return _ModSCREAM.Rotamer_set_current_baseline_E(*args)
    def get_empty_lattice_E_abs(*args): return _ModSCREAM.Rotamer_get_empty_lattice_E_abs(*args)
    def get_zeroth_excitation_baseline_E_abs(*args): return _ModSCREAM.Rotamer_get_zeroth_excitation_baseline_E_abs(*args)
    def get_current_baseline_E_abs(*args): return _ModSCREAM.Rotamer_get_current_baseline_E_abs(*args)
    def set_empty_lattice_E_abs(*args): return _ModSCREAM.Rotamer_set_empty_lattice_E_abs(*args)
    def set_zeroth_excitation_baseline_E_abs(*args): return _ModSCREAM.Rotamer_set_zeroth_excitation_baseline_E_abs(*args)
    def set_current_baseline_E_abs(*args): return _ModSCREAM.Rotamer_set_current_baseline_E_abs(*args)
    def get_empty_lattice_energy_rank(*args): return _ModSCREAM.Rotamer_get_empty_lattice_energy_rank(*args)
    def set_empty_lattice_energy_rank(*args): return _ModSCREAM.Rotamer_set_empty_lattice_energy_rank(*args)
    def setFailedDistanceCutoff(*args): return _ModSCREAM.Rotamer_setFailedDistanceCutoff(*args)
    def setPassedDistanceCutoff(*args): return _ModSCREAM.Rotamer_setPassedDistanceCutoff(*args)
    def failedDistanceCutoff(*args): return _ModSCREAM.Rotamer_failedDistanceCutoff(*args)
    def get_rotlib_E(*args): return _ModSCREAM.Rotamer_get_rotlib_E(*args)
    def get_sc_valence_E(*args): return _ModSCREAM.Rotamer_get_sc_valence_E(*args)
    def get_sc_coulomb_E(*args): return _ModSCREAM.Rotamer_get_sc_coulomb_E(*args)
    def get_sc_vdw_E(*args): return _ModSCREAM.Rotamer_get_sc_vdw_E(*args)
    def get_sc_hb_E(*args): return _ModSCREAM.Rotamer_get_sc_hb_E(*args)
    def get_sc_total_nb_E(*args): return _ModSCREAM.Rotamer_get_sc_total_nb_E(*args)
    def get_sc_solvation_E(*args): return _ModSCREAM.Rotamer_get_sc_solvation_E(*args)
    def get_sc_total_E(*args): return _ModSCREAM.Rotamer_get_sc_total_E(*args)
    def set_rotamer_n(*args): return _ModSCREAM.Rotamer_set_rotamer_n(*args)
    def set_rotlib_E(*args): return _ModSCREAM.Rotamer_set_rotlib_E(*args)
    def set_sc_valence_E(*args): return _ModSCREAM.Rotamer_set_sc_valence_E(*args)
    def set_sc_coulomb_E(*args): return _ModSCREAM.Rotamer_set_sc_coulomb_E(*args)
    def set_sc_vdw_E(*args): return _ModSCREAM.Rotamer_set_sc_vdw_E(*args)
    def set_sc_hb_E(*args): return _ModSCREAM.Rotamer_set_sc_hb_E(*args)
    def set_sc_total_nb_E(*args): return _ModSCREAM.Rotamer_set_sc_total_nb_E(*args)
    def set_sc_solvation_E(*args): return _ModSCREAM.Rotamer_set_sc_solvation_E(*args)
    def set_sc_total_E(*args): return _ModSCREAM.Rotamer_set_sc_total_E(*args)
    def calc_sc_valence_E(*args): return _ModSCREAM.Rotamer_calc_sc_valence_E(*args)
    def calc_sc_coulomb_E(*args): return _ModSCREAM.Rotamer_calc_sc_coulomb_E(*args)
    def calc_sc_vdw_E(*args): return _ModSCREAM.Rotamer_calc_sc_vdw_E(*args)
    def calc_sc_total_nb_E(*args): return _ModSCREAM.Rotamer_calc_sc_total_nb_E(*args)
    def calc_sc_solvation_E(*args): return _ModSCREAM.Rotamer_calc_sc_solvation_E(*args)
    def calc_sc_total_E(*args): return _ModSCREAM.Rotamer_calc_sc_total_E(*args)
    def match_bb(*args): return _ModSCREAM.Rotamer_match_bb(*args)
    def assign_atom_fftype(*args): return _ModSCREAM.Rotamer_assign_atom_fftype(*args)
    def assign_charges(*args): return _ModSCREAM.Rotamer_assign_charges(*args)
    def assign_lone_pair(*args): return _ModSCREAM.Rotamer_assign_lone_pair(*args)
    def declaredInRotlibScope(*args): return _ModSCREAM.Rotamer_declaredInRotlibScope(*args)
    def setDeclaredInRotlibScope(*args): return _ModSCREAM.Rotamer_setDeclaredInRotlibScope(*args)

class RotamerPtr(Rotamer):
    def __init__(self, this):
        _swig_setattr(self, Rotamer, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, Rotamer, 'thisown', 0)
        _swig_setattr(self, Rotamer,self.__class__,Rotamer)
_ModSCREAM.Rotamer_swigregister(RotamerPtr)

class AARotamer(Rotamer):
    __swig_setmethods__ = {}
    for _s in [Rotamer]: __swig_setmethods__.update(_s.__swig_setmethods__)
    __setattr__ = lambda self, name, value: _swig_setattr(self, AARotamer, name, value)
    __swig_getmethods__ = {}
    for _s in [Rotamer]: __swig_getmethods__.update(_s.__swig_getmethods__)
    __getattr__ = lambda self, name: _swig_getattr(self, AARotamer, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ AARotamer instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, AARotamer, 'this', _ModSCREAM.new_AARotamer(*args))
        _swig_setattr(self, AARotamer, 'thisown', 1)
    def __del__(self, destroy=_ModSCREAM.delete_AARotamer):
        try:
            if self.thisown: destroy(self)
        except: pass

    def deepcopy(*args): return _ModSCREAM.AARotamer_deepcopy(*args)
    def get_resName(*args): return _ModSCREAM.AARotamer_get_resName(*args)
    def set_resName(*args): return _ModSCREAM.AARotamer_set_resName(*args)
    def initRotamerAtomList(*args): return _ModSCREAM.AARotamer_initRotamerAtomList(*args)
    def calc_PHI(*args): return _ModSCREAM.AARotamer_calc_PHI(*args)
    def calc_PSI(*args): return _ModSCREAM.AARotamer_calc_PSI(*args)
    def get_PHI(*args): return _ModSCREAM.AARotamer_get_PHI(*args)
    def get_PSI(*args): return _ModSCREAM.AARotamer_get_PSI(*args)
    def chi1(*args): return _ModSCREAM.AARotamer_chi1(*args)
    def chi2(*args): return _ModSCREAM.AARotamer_chi2(*args)
    def chi3(*args): return _ModSCREAM.AARotamer_chi3(*args)
    def chi4(*args): return _ModSCREAM.AARotamer_chi4(*args)
    def chi5(*args): return _ModSCREAM.AARotamer_chi5(*args)
    def match_bb(*args): return _ModSCREAM.AARotamer_match_bb(*args)
    def assign_atom_fftype(*args): return _ModSCREAM.AARotamer_assign_atom_fftype(*args)
    def assign_charges(*args): return _ModSCREAM.AARotamer_assign_charges(*args)
    def assign_lone_pair(*args): return _ModSCREAM.AARotamer_assign_lone_pair(*args)
    def calc_C_i_minus_one(*args): return _ModSCREAM.AARotamer_calc_C_i_minus_one(*args)
    def center_CA(*args): return _ModSCREAM.AARotamer_center_CA(*args)
    def append_to_filehandle(*args): return _ModSCREAM.AARotamer_append_to_filehandle(*args)
    def pdb_append_to_filehandle(*args): return _ModSCREAM.AARotamer_pdb_append_to_filehandle(*args)
    def append_to_ostream_connect_info(*args): return _ModSCREAM.AARotamer_append_to_ostream_connect_info(*args)
    def print_Me(*args): return _ModSCREAM.AARotamer_print_Me(*args)
    def print_ordered_by_n(*args): return _ModSCREAM.AARotamer_print_ordered_by_n(*args)
    def get_bb(*args): return _ModSCREAM.AARotamer_get_bb(*args)
    def get_sc(*args): return _ModSCREAM.AARotamer_get_sc(*args)
    __swig_setmethods__["PHI"] = _ModSCREAM.AARotamer_PHI_set
    __swig_getmethods__["PHI"] = _ModSCREAM.AARotamer_PHI_get
    if _newclass:PHI = property(_ModSCREAM.AARotamer_PHI_get, _ModSCREAM.AARotamer_PHI_set)
    __swig_setmethods__["PSI"] = _ModSCREAM.AARotamer_PSI_set
    __swig_getmethods__["PSI"] = _ModSCREAM.AARotamer_PSI_get
    if _newclass:PSI = property(_ModSCREAM.AARotamer_PSI_get, _ModSCREAM.AARotamer_PSI_set)
    __swig_setmethods__["resName"] = _ModSCREAM.AARotamer_resName_set
    __swig_getmethods__["resName"] = _ModSCREAM.AARotamer_resName_get
    if _newclass:resName = property(_ModSCREAM.AARotamer_resName_get, _ModSCREAM.AARotamer_resName_set)
    def private_chi(*args): return _ModSCREAM.AARotamer_private_chi(*args)
    def _determine_and_fix_GLY_sidechain_HCA_issue(*args): return _ModSCREAM.AARotamer__determine_and_fix_GLY_sidechain_HCA_issue(*args)

class AARotamerPtr(AARotamer):
    def __init__(self, this):
        _swig_setattr(self, AARotamer, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, AARotamer, 'thisown', 0)
        _swig_setattr(self, AARotamer,self.__class__,AARotamer)
_ModSCREAM.AARotamer_swigregister(AARotamerPtr)

class Protein(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Protein, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Protein, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ Protein instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, Protein, 'this', _ModSCREAM.new_Protein(*args))
        _swig_setattr(self, Protein, 'thisown', 1)
    def __del__(self, destroy=_ModSCREAM.delete_Protein):
        try:
            if self.thisown: destroy(self)
        except: pass

    def get_AAChain(*args): return _ModSCREAM.Protein_get_AAChain(*args)
    def get_Ligand(*args): return _ModSCREAM.Protein_get_Ligand(*args)
    def get_res_type(*args): return _ModSCREAM.Protein_get_res_type(*args)
    def get_sc_atoms(*args): return _ModSCREAM.Protein_get_sc_atoms(*args)
    def get_variable_atoms(*args): return _ModSCREAM.Protein_get_variable_atoms(*args)
    def getAtomList(*args): return _ModSCREAM.Protein_getAtomList(*args)
    def getAtom(*args): return _ModSCREAM.Protein_getAtom(*args)
    def getTheseAtoms(*args): return _ModSCREAM.Protein_getTheseAtoms(*args)
    def totalComponents(*args): return _ModSCREAM.Protein_totalComponents(*args)
    def ntrlRotamerPlacement(*args): return _ModSCREAM.Protein_ntrlRotamerPlacement(*args)
    def getAARotamer(*args): return _ModSCREAM.Protein_getAARotamer(*args)
    def conformerPlacement(*args): return _ModSCREAM.Protein_conformerPlacement(*args)
    def conformerExtraction(*args): return _ModSCREAM.Protein_conformerExtraction(*args)
    def mutation(*args): return _ModSCREAM.Protein_mutation(*args)
    def setSideChainLibraryName(*args): return _ModSCREAM.Protein_setSideChainLibraryName(*args)
    def setProteinLibraryName(*args): return _ModSCREAM.Protein_setProteinLibraryName(*args)
    def sc_clash(*args): return _ModSCREAM.Protein_sc_clash(*args)
    def conformer_clash(*args): return _ModSCREAM.Protein_conformer_clash(*args)
    def sc_CRMS(*args): return _ModSCREAM.Protein_sc_CRMS(*args)
    def conformer_CRMS(*args): return _ModSCREAM.Protein_conformer_CRMS(*args)
    def max_atom_dist_on_SC(*args): return _ModSCREAM.Protein_max_atom_dist_on_SC(*args)
    def sc_atom_CRMS(*args): return _ModSCREAM.Protein_sc_atom_CRMS(*args)
    def fix_entire_atom_list_ordering(*args): return _ModSCREAM.Protein_fix_entire_atom_list_ordering(*args)
    def fix_toggle(*args): return _ModSCREAM.Protein_fix_toggle(*args)
    def fix_sc_toggle(*args): return _ModSCREAM.Protein_fix_sc_toggle(*args)
    def append_to_filehandle(*args): return _ModSCREAM.Protein_append_to_filehandle(*args)
    def pdb_append_to_filehandle(*args): return _ModSCREAM.Protein_pdb_append_to_filehandle(*args)
    def print_bgf_file(*args): return _ModSCREAM.Protein_print_bgf_file(*args)
    def print_Me(*args): return _ModSCREAM.Protein_print_Me(*args)
    def print_ordered_by_n(*args): return _ModSCREAM.Protein_print_ordered_by_n(*args)

class ProteinPtr(Protein):
    def __init__(self, this):
        _swig_setattr(self, Protein, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, Protein, 'thisown', 0)
        _swig_setattr(self, Protein,self.__class__,Protein)
_ModSCREAM.Protein_swigregister(ProteinPtr)


SCREAMMain = _ModSCREAM.SCREAMMain
class ModSimStructs(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ModSimStructs, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ModSimStructs, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ ModSimStructs instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, ModSimStructs, 'this', _ModSCREAM.new_ModSimStructs(*args))
        _swig_setattr(self, ModSimStructs, 'thisown', 1)
    __swig_setmethods__["parameters"] = _ModSCREAM.ModSimStructs_parameters_set
    __swig_getmethods__["parameters"] = _ModSCREAM.ModSimStructs_parameters_get
    if _newclass:parameters = property(_ModSCREAM.ModSimStructs_parameters_get, _ModSCREAM.ModSimStructs_parameters_set)
    __swig_setmethods__["ff_properties"] = _ModSCREAM.ModSimStructs_ff_properties_set
    __swig_getmethods__["ff_properties"] = _ModSCREAM.ModSimStructs_ff_properties_get
    if _newclass:ff_properties = property(_ModSCREAM.ModSimStructs_ff_properties_get, _ModSCREAM.ModSimStructs_ff_properties_set)
    __swig_setmethods__["atom_properties"] = _ModSCREAM.ModSimStructs_atom_properties_set
    __swig_getmethods__["atom_properties"] = _ModSCREAM.ModSimStructs_atom_properties_get
    if _newclass:atom_properties = property(_ModSCREAM.ModSimStructs_atom_properties_get, _ModSCREAM.ModSimStructs_atom_properties_set)
    __swig_setmethods__["unit_cell_properties"] = _ModSCREAM.ModSimStructs_unit_cell_properties_set
    __swig_getmethods__["unit_cell_properties"] = _ModSCREAM.ModSimStructs_unit_cell_properties_get
    if _newclass:unit_cell_properties = property(_ModSCREAM.ModSimStructs_unit_cell_properties_get, _ModSCREAM.ModSimStructs_unit_cell_properties_set)
    __swig_setmethods__["cell_list"] = _ModSCREAM.ModSimStructs_cell_list_set
    __swig_getmethods__["cell_list"] = _ModSCREAM.ModSimStructs_cell_list_get
    if _newclass:cell_list = property(_ModSCREAM.ModSimStructs_cell_list_get, _ModSCREAM.ModSimStructs_cell_list_set)
    __swig_setmethods__["neighbor_list"] = _ModSCREAM.ModSimStructs_neighbor_list_set
    __swig_getmethods__["neighbor_list"] = _ModSCREAM.ModSimStructs_neighbor_list_get
    if _newclass:neighbor_list = property(_ModSCREAM.ModSimStructs_neighbor_list_get, _ModSCREAM.ModSimStructs_neighbor_list_set)
    __swig_setmethods__["neighbor_hbdre_list"] = _ModSCREAM.ModSimStructs_neighbor_hbdre_list_set
    __swig_getmethods__["neighbor_hbdre_list"] = _ModSCREAM.ModSimStructs_neighbor_hbdre_list_get
    if _newclass:neighbor_hbdre_list = property(_ModSCREAM.ModSimStructs_neighbor_hbdre_list_get, _ModSCREAM.ModSimStructs_neighbor_hbdre_list_set)
    __swig_setmethods__["thermo_properties"] = _ModSCREAM.ModSimStructs_thermo_properties_set
    __swig_getmethods__["thermo_properties"] = _ModSCREAM.ModSimStructs_thermo_properties_get
    if _newclass:thermo_properties = property(_ModSCREAM.ModSimStructs_thermo_properties_get, _ModSCREAM.ModSimStructs_thermo_properties_set)
    def __del__(self, destroy=_ModSCREAM.delete_ModSimStructs):
        try:
            if self.thisown: destroy(self)
        except: pass


class ModSimStructsPtr(ModSimStructs):
    def __init__(self, this):
        _swig_setattr(self, ModSimStructs, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ModSimStructs, 'thisown', 0)
        _swig_setattr(self, ModSimStructs,self.__class__,ModSimStructs)
_ModSCREAM.ModSimStructs_swigregister(ModSimStructsPtr)

class ModSimSCREAMInterface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ModSimSCREAMInterface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ModSimSCREAMInterface, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ ModSimSCREAMInterface instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, ModSimSCREAMInterface, 'this', _ModSCREAM.new_ModSimSCREAMInterface(*args))
        _swig_setattr(self, ModSimSCREAMInterface, 'thisown', 1)
    def __del__(self, destroy=_ModSCREAM.delete_ModSimSCREAMInterface):
        try:
            if self.thisown: destroy(self)
        except: pass

    def doSCREAM(*args): return _ModSCREAM.ModSimSCREAMInterface_doSCREAM(*args)
    def calcEnergy(*args): return _ModSCREAM.ModSimSCREAMInterface_calcEnergy(*args)
    def getEnergy(*args): return _ModSCREAM.ModSimSCREAMInterface_getEnergy(*args)
    def printToFile(*args): return _ModSCREAM.ModSimSCREAMInterface_printToFile(*args)
    def placeConformer(*args): return _ModSCREAM.ModSimSCREAMInterface_placeConformer(*args)
    def placeSideChain(*args): return _ModSCREAM.ModSimSCREAMInterface_placeSideChain(*args)
    def sc_clash(*args): return _ModSCREAM.ModSimSCREAMInterface_sc_clash(*args)
    def conformer_clash(*args): return _ModSCREAM.ModSimSCREAMInterface_conformer_clash(*args)
    def remapModSimAtomList(*args): return _ModSCREAM.ModSimSCREAMInterface_remapModSimAtomList(*args)
    def remapModSimOneResidueCoordinates(*args): return _ModSCREAM.ModSimSCREAMInterface_remapModSimOneResidueCoordinates(*args)
    def makeInvisible(*args): return _ModSCREAM.ModSimSCREAMInterface_makeInvisible(*args)
    def makeVisible(*args): return _ModSCREAM.ModSimSCREAMInterface_makeVisible(*args)
    def makeResidueInvisible(*args): return _ModSCREAM.ModSimSCREAMInterface_makeResidueInvisible(*args)
    def makeResidueVisible(*args): return _ModSCREAM.ModSimSCREAMInterface_makeResidueVisible(*args)
    def makeConformerInvisible(*args): return _ModSCREAM.ModSimSCREAMInterface_makeConformerInvisible(*args)
    def makeConformerVisible(*args): return _ModSCREAM.ModSimSCREAMInterface_makeConformerVisible(*args)
    def restoreVisibility(*args): return _ModSCREAM.ModSimSCREAMInterface_restoreVisibility(*args)
    def makeAllImmoveable(*args): return _ModSCREAM.ModSimSCREAMInterface_makeAllImmoveable(*args)
    def makeAllMoveable(*args): return _ModSCREAM.ModSimSCREAMInterface_makeAllMoveable(*args)
    def makeAtomImmoveable(*args): return _ModSCREAM.ModSimSCREAMInterface_makeAtomImmoveable(*args)
    def makeAtomMoveable(*args): return _ModSCREAM.ModSimSCREAMInterface_makeAtomMoveable(*args)
    def makeResidueImmoveable(*args): return _ModSCREAM.ModSimSCREAMInterface_makeResidueImmoveable(*args)
    def makeResidueMoveable(*args): return _ModSCREAM.ModSimSCREAMInterface_makeResidueMoveable(*args)
    def restoreMoveability(*args): return _ModSCREAM.ModSimSCREAMInterface_restoreMoveability(*args)
    def getAARotamer(*args): return _ModSCREAM.ModSimSCREAMInterface_getAARotamer(*args)
    def getProtein(*args): return _ModSCREAM.ModSimSCREAMInterface_getProtein(*args)
    def _determineLibraryPath(*args): return _ModSCREAM.ModSimSCREAMInterface__determineLibraryPath(*args)
    __swig_setmethods__["scream_parameters"] = _ModSCREAM.ModSimSCREAMInterface_scream_parameters_set
    __swig_getmethods__["scream_parameters"] = _ModSCREAM.ModSimSCREAMInterface_scream_parameters_get
    if _newclass:scream_parameters = property(_ModSCREAM.ModSimSCREAMInterface_scream_parameters_get, _ModSCREAM.ModSimSCREAMInterface_scream_parameters_set)

class ModSimSCREAMInterfacePtr(ModSimSCREAMInterface):
    def __init__(self, this):
        _swig_setattr(self, ModSimSCREAMInterface, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ModSimSCREAMInterface, 'thisown', 0)
        _swig_setattr(self, ModSimSCREAMInterface,self.__class__,ModSimSCREAMInterface)
_ModSCREAM.ModSimSCREAMInterface_swigregister(ModSimSCREAMInterfacePtr)

class Rotlib(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Rotlib, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Rotlib, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ Rotlib instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, Rotlib, 'this', _ModSCREAM.new_Rotlib(*args))
        _swig_setattr(self, Rotlib, 'thisown', 1)
    def __del__(self, destroy=_ModSCREAM.delete_Rotlib):
        try:
            if self.thisown: destroy(self)
        except: pass

    def readConnectivityFile(*args): return _ModSCREAM.Rotlib_readConnectivityFile(*args)
    def readRotamerLibrary(*args): return _ModSCREAM.Rotlib_readRotamerLibrary(*args)
    def get_library_name(*args): return _ModSCREAM.Rotlib_get_library_name(*args)
    def getRotConnInfo(*args): return _ModSCREAM.Rotlib_getRotConnInfo(*args)
    def get_next_rot(*args): return _ModSCREAM.Rotlib_get_next_rot(*args)
    def get_current_rot(*args): return _ModSCREAM.Rotlib_get_current_rot(*args)
    def get_next_rot_with_empty_lattice_E_below(*args): return _ModSCREAM.Rotlib_get_next_rot_with_empty_lattice_E_below(*args)
    def get_empty_lattice_E_rot(*args): return _ModSCREAM.Rotlib_get_empty_lattice_E_rot(*args)
    def reset_pstn(*args): return _ModSCREAM.Rotlib_reset_pstn(*args)
    def add_rotamer(*args): return _ModSCREAM.Rotlib_add_rotamer(*args)
    def size(*args): return _ModSCREAM.Rotlib_size(*args)
    def n_rotamers_below_empty_lattice_energy(*args): return _ModSCREAM.Rotlib_n_rotamers_below_empty_lattice_energy(*args)
    def print_Me(*args): return _ModSCREAM.Rotlib_print_Me(*args)
    def print_to_file(*args): return _ModSCREAM.Rotlib_print_to_file(*args)
    def sort_by_rotlib_E(*args): return _ModSCREAM.Rotlib_sort_by_rotlib_E(*args)
    def sort_by_self_E(*args): return _ModSCREAM.Rotlib_sort_by_self_E(*args)
    def sort_by_empty_lattice_E(*args): return _ModSCREAM.Rotlib_sort_by_empty_lattice_E(*args)

class RotlibPtr(Rotlib):
    def __init__(self, this):
        _swig_setattr(self, Rotlib, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, Rotlib, 'thisown', 0)
        _swig_setattr(self, Rotlib,self.__class__,Rotlib)
_ModSCREAM.Rotlib_swigregister(RotlibPtr)

class AARotlib(Rotlib):
    __swig_setmethods__ = {}
    for _s in [Rotlib]: __swig_setmethods__.update(_s.__swig_setmethods__)
    __setattr__ = lambda self, name, value: _swig_setattr(self, AARotlib, name, value)
    __swig_getmethods__ = {}
    for _s in [Rotlib]: __swig_getmethods__.update(_s.__swig_getmethods__)
    __getattr__ = lambda self, name: _swig_getattr(self, AARotlib, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ AARotlib instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, AARotlib, 'this', _ModSCREAM.new_AARotlib(*args))
        _swig_setattr(self, AARotlib, 'thisown', 1)
    def __del__(self, destroy=_ModSCREAM.delete_AARotlib):
        try:
            if self.thisown: destroy(self)
        except: pass

    def get_next_rot(*args): return _ModSCREAM.AARotlib_get_next_rot(*args)
    def get_current_rot(*args): return _ModSCREAM.AARotlib_get_current_rot(*args)
    def get_rot(*args): return _ModSCREAM.AARotlib_get_rot(*args)
    def reset_rot_pstn(*args): return _ModSCREAM.AARotlib_reset_rot_pstn(*args)
    def set_rot_pstn(*args): return _ModSCREAM.AARotlib_set_rot_pstn(*args)
    def get_next_rot_with_empty_lattice_E_below(*args): return _ModSCREAM.AARotlib_get_next_rot_with_empty_lattice_E_below(*args)
    def get_empty_lattice_E_rot(*args): return _ModSCREAM.AARotlib_get_empty_lattice_E_rot(*args)
    def center_CA(*args): return _ModSCREAM.AARotlib_center_CA(*args)
    def calc_all_PHI(*args): return _ModSCREAM.AARotlib_calc_all_PHI(*args)
    def calc_all_PSI(*args): return _ModSCREAM.AARotlib_calc_all_PSI(*args)
    __swig_setmethods__["resName"] = _ModSCREAM.AARotlib_resName_set
    __swig_getmethods__["resName"] = _ModSCREAM.AARotlib_resName_get
    if _newclass:resName = property(_ModSCREAM.AARotlib_resName_get, _ModSCREAM.AARotlib_resName_set)

class AARotlibPtr(AARotlib):
    def __init__(self, this):
        _swig_setattr(self, AARotlib, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, AARotlib, 'thisown', 0)
        _swig_setattr(self, AARotlib,self.__class__,AARotlib)
_ModSCREAM.AARotlib_swigregister(AARotlibPtr)

class NtrlAARotlib(AARotlib):
    __swig_setmethods__ = {}
    for _s in [AARotlib]: __swig_setmethods__.update(_s.__swig_setmethods__)
    __setattr__ = lambda self, name, value: _swig_setattr(self, NtrlAARotlib, name, value)
    __swig_getmethods__ = {}
    for _s in [AARotlib]: __swig_getmethods__.update(_s.__swig_getmethods__)
    __getattr__ = lambda self, name: _swig_getattr(self, NtrlAARotlib, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ NtrlAARotlib instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, NtrlAARotlib, 'this', _ModSCREAM.new_NtrlAARotlib(*args))
        _swig_setattr(self, NtrlAARotlib, 'thisown', 1)
    def setup_library(*args): return _ModSCREAM.NtrlAARotlib_setup_library(*args)
    def __del__(self, destroy=_ModSCREAM.delete_NtrlAARotlib):
        try:
            if self.thisown: destroy(self)
        except: pass

    def assign_atom_fftype(*args): return _ModSCREAM.NtrlAARotlib_assign_atom_fftype(*args)
    def assign_charges(*args): return _ModSCREAM.NtrlAARotlib_assign_charges(*args)
    def assign_lone_pair(*args): return _ModSCREAM.NtrlAARotlib_assign_lone_pair(*args)
    def append_to_filehandle(*args): return _ModSCREAM.NtrlAARotlib_append_to_filehandle(*args)

class NtrlAARotlibPtr(NtrlAARotlib):
    def __init__(self, this):
        _swig_setattr(self, NtrlAARotlib, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, NtrlAARotlib, 'thisown', 0)
        _swig_setattr(self, NtrlAARotlib,self.__class__,NtrlAARotlib)
_ModSCREAM.NtrlAARotlib_swigregister(NtrlAARotlibPtr)

class Multiple_NtrlAARotlib(NtrlAARotlib):
    __swig_setmethods__ = {}
    for _s in [NtrlAARotlib]: __swig_setmethods__.update(_s.__swig_setmethods__)
    __setattr__ = lambda self, name, value: _swig_setattr(self, Multiple_NtrlAARotlib, name, value)
    __swig_getmethods__ = {}
    for _s in [NtrlAARotlib]: __swig_getmethods__.update(_s.__swig_getmethods__)
    __getattr__ = lambda self, name: _swig_getattr(self, Multiple_NtrlAARotlib, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ Multiple_NtrlAARotlib instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, Multiple_NtrlAARotlib, 'this', _ModSCREAM.new_Multiple_NtrlAARotlib(*args))
        _swig_setattr(self, Multiple_NtrlAARotlib, 'thisown', 1)
    def __del__(self, destroy=_ModSCREAM.delete_Multiple_NtrlAARotlib):
        try:
            if self.thisown: destroy(self)
        except: pass

    def getRotConnInfo(*args): return _ModSCREAM.Multiple_NtrlAARotlib_getRotConnInfo(*args)
    def add_library(*args): return _ModSCREAM.Multiple_NtrlAARotlib_add_library(*args)

class Multiple_NtrlAARotlibPtr(Multiple_NtrlAARotlib):
    def __init__(self, this):
        _swig_setattr(self, Multiple_NtrlAARotlib, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, Multiple_NtrlAARotlib, 'thisown', 0)
        _swig_setattr(self, Multiple_NtrlAARotlib,self.__class__,Multiple_NtrlAARotlib)
_ModSCREAM.Multiple_NtrlAARotlib_swigregister(Multiple_NtrlAARotlibPtr)

class HIS_NtrlAARotlib(NtrlAARotlib):
    __swig_setmethods__ = {}
    for _s in [NtrlAARotlib]: __swig_setmethods__.update(_s.__swig_setmethods__)
    __setattr__ = lambda self, name, value: _swig_setattr(self, HIS_NtrlAARotlib, name, value)
    __swig_getmethods__ = {}
    for _s in [NtrlAARotlib]: __swig_getmethods__.update(_s.__swig_getmethods__)
    __getattr__ = lambda self, name: _swig_getattr(self, HIS_NtrlAARotlib, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ HIS_NtrlAARotlib instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, HIS_NtrlAARotlib, 'this', _ModSCREAM.new_HIS_NtrlAARotlib(*args))
        _swig_setattr(self, HIS_NtrlAARotlib, 'thisown', 1)
    def __del__(self, destroy=_ModSCREAM.delete_HIS_NtrlAARotlib):
        try:
            if self.thisown: destroy(self)
        except: pass

    def add_rotamer(*args): return _ModSCREAM.HIS_NtrlAARotlib_add_rotamer(*args)

class HIS_NtrlAARotlibPtr(HIS_NtrlAARotlib):
    def __init__(self, this):
        _swig_setattr(self, HIS_NtrlAARotlib, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, HIS_NtrlAARotlib, 'thisown', 0)
        _swig_setattr(self, HIS_NtrlAARotlib,self.__class__,HIS_NtrlAARotlib)
_ModSCREAM.HIS_NtrlAARotlib_swigregister(HIS_NtrlAARotlibPtr)

class RotlibCollection(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, RotlibCollection, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, RotlibCollection, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ RotlibCollection instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, RotlibCollection, 'this', _ModSCREAM.new_RotlibCollection(*args))
        _swig_setattr(self, RotlibCollection, 'thisown', 1)
    def __del__(self, destroy=_ModSCREAM.delete_RotlibCollection):
        try:
            if self.thisown: destroy(self)
        except: pass

    def addRotlib(*args): return _ModSCREAM.RotlibCollection_addRotlib(*args)
    def initEmptyLatticeDataStructures(*args): return _ModSCREAM.RotlibCollection_initEmptyLatticeDataStructures(*args)
    def initDynamicMemoryDataStructures(*args): return _ModSCREAM.RotlibCollection_initDynamicMemoryDataStructures(*args)
    def resetEmptyLatticeCrntPstn(*args): return _ModSCREAM.RotlibCollection_resetEmptyLatticeCrntPstn(*args)
    def resetTotalEnergyCrntPstn(*args): return _ModSCREAM.RotlibCollection_resetTotalEnergyCrntPstn(*args)
    def getNextEmptyLatticeExcitationRotamers(*args): return _ModSCREAM.RotlibCollection_getNextEmptyLatticeExcitationRotamers(*args)
    def getNextTotalEnergyExcitationRotamers(*args): return _ModSCREAM.RotlibCollection_getNextTotalEnergyExcitationRotamers(*args)
    def getNthEmptyLatticeExcitationRotamers(*args): return _ModSCREAM.RotlibCollection_getNthEmptyLatticeExcitationRotamers(*args)
    def getELExcitedRotamerFromEnumeration(*args): return _ModSCREAM.RotlibCollection_getELExcitedRotamerFromEnumeration(*args)
    def getELEnumerationFromExcitedRotamer(*args): return _ModSCREAM.RotlibCollection_getELEnumerationFromExcitedRotamer(*args)
    def getMutInfoRotlibMap(*args): return _ModSCREAM.RotlibCollection_getMutInfoRotlibMap(*args)
    def getMutInfoRotlibDict(*args): return _ModSCREAM.RotlibCollection_getMutInfoRotlibDict(*args)
    def getNextDynamicMemoryRotamers_And_Expand(*args): return _ModSCREAM.RotlibCollection_getNextDynamicMemoryRotamers_And_Expand(*args)
    def setExcitationEnergy(*args): return _ModSCREAM.RotlibCollection_setExcitationEnergy(*args)
    def getExcitationEnergy(*args): return _ModSCREAM.RotlibCollection_getExcitationEnergy(*args)
    def printEmptyLatticeLinearEnergyTable(*args): return _ModSCREAM.RotlibCollection_printEmptyLatticeLinearEnergyTable(*args)
    def printExcitationEnergyTable(*args): return _ModSCREAM.RotlibCollection_printExcitationEnergyTable(*args)
    def printEmptyLatticeTable(*args): return _ModSCREAM.RotlibCollection_printEmptyLatticeTable(*args)
    def sizeOfSystem(*args): return _ModSCREAM.RotlibCollection_sizeOfSystem(*args)
    def getHighestAllowedRotamerE(*args): return _ModSCREAM.RotlibCollection_getHighestAllowedRotamerE(*args)
    def setHighestAllowedRotamerE(*args): return _ModSCREAM.RotlibCollection_setHighestAllowedRotamerE(*args)
    __swig_setmethods__["maxRotamerConfigurations"] = _ModSCREAM.RotlibCollection_maxRotamerConfigurations_set
    __swig_getmethods__["maxRotamerConfigurations"] = _ModSCREAM.RotlibCollection_maxRotamerConfigurations_get
    if _newclass:maxRotamerConfigurations = property(_ModSCREAM.RotlibCollection_maxRotamerConfigurations_get, _ModSCREAM.RotlibCollection_maxRotamerConfigurations_set)

class RotlibCollectionPtr(RotlibCollection):
    def __init__(self, this):
        _swig_setattr(self, RotlibCollection, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, RotlibCollection, 'thisown', 0)
        _swig_setattr(self, RotlibCollection,self.__class__,RotlibCollection)
_ModSCREAM.RotlibCollection_swigregister(RotlibCollectionPtr)

class bgf_handler(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, bgf_handler, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, bgf_handler, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ bgf_handler instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, bgf_handler, 'this', _ModSCREAM.new_bgf_handler(*args))
        _swig_setattr(self, bgf_handler, 'thisown', 1)
    def __del__(self, destroy=_ModSCREAM.delete_bgf_handler):
        try:
            if self.thisown: destroy(self)
        except: pass

    def readfile(*args): return _ModSCREAM.bgf_handler_readfile(*args)
    def printToFile(*args): return _ModSCREAM.bgf_handler_printToFile(*args)
    __swig_getmethods__["printfile"] = lambda x: _ModSCREAM.bgf_handler_printfile
    if _newclass:printfile = staticmethod(_ModSCREAM.bgf_handler_printfile)
    def printPDB(*args): return _ModSCREAM.bgf_handler_printPDB(*args)
    __swig_getmethods__["printToPDB"] = lambda x: _ModSCREAM.bgf_handler_printToPDB
    if _newclass:printToPDB = staticmethod(_ModSCREAM.bgf_handler_printToPDB)
    def pass_atomlist(*args): return _ModSCREAM.bgf_handler_pass_atomlist(*args)
    __swig_setmethods__["atom_list"] = _ModSCREAM.bgf_handler_atom_list_set
    __swig_getmethods__["atom_list"] = _ModSCREAM.bgf_handler_atom_list_get
    if _newclass:atom_list = property(_ModSCREAM.bgf_handler_atom_list_get, _ModSCREAM.bgf_handler_atom_list_set)
    __swig_setmethods__["header_lines"] = _ModSCREAM.bgf_handler_header_lines_set
    __swig_getmethods__["header_lines"] = _ModSCREAM.bgf_handler_header_lines_get
    if _newclass:header_lines = property(_ModSCREAM.bgf_handler_header_lines_get, _ModSCREAM.bgf_handler_header_lines_set)
    __swig_setmethods__["atom_lines"] = _ModSCREAM.bgf_handler_atom_lines_set
    __swig_getmethods__["atom_lines"] = _ModSCREAM.bgf_handler_atom_lines_get
    if _newclass:atom_lines = property(_ModSCREAM.bgf_handler_atom_lines_get, _ModSCREAM.bgf_handler_atom_lines_set)
    __swig_setmethods__["conect_format_lines"] = _ModSCREAM.bgf_handler_conect_format_lines_set
    __swig_getmethods__["conect_format_lines"] = _ModSCREAM.bgf_handler_conect_format_lines_get
    if _newclass:conect_format_lines = property(_ModSCREAM.bgf_handler_conect_format_lines_get, _ModSCREAM.bgf_handler_conect_format_lines_set)
    __swig_setmethods__["connectivity_record_lines"] = _ModSCREAM.bgf_handler_connectivity_record_lines_set
    __swig_getmethods__["connectivity_record_lines"] = _ModSCREAM.bgf_handler_connectivity_record_lines_get
    if _newclass:connectivity_record_lines = property(_ModSCREAM.bgf_handler_connectivity_record_lines_get, _ModSCREAM.bgf_handler_connectivity_record_lines_set)

class bgf_handlerPtr(bgf_handler):
    def __init__(self, this):
        _swig_setattr(self, bgf_handler, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, bgf_handler, 'thisown', 0)
        _swig_setattr(self, bgf_handler,self.__class__,bgf_handler)
_ModSCREAM.bgf_handler_swigregister(bgf_handlerPtr)

bgf_handler_printfile = _ModSCREAM.bgf_handler_printfile

bgf_handler_printToPDB = _ModSCREAM.bgf_handler_printToPDB


derefString = _ModSCREAM.derefString

derefRotamer = _ModSCREAM.derefRotamer

derefAARotamer = _ModSCREAM.derefAARotamer

