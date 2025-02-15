# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _Py_Scream_EE

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


class ScreamModel(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ScreamModel, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ScreamModel, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ ScreamModel instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, ScreamModel, 'this', _Py_Scream_EE.new_ScreamModel(*args))
        _swig_setattr(self, ScreamModel, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_ScreamModel):
        try:
            if self.thisown: destroy(self)
        except: pass

    __swig_setmethods__["scream_parameters"] = _Py_Scream_EE.ScreamModel_scream_parameters_set
    __swig_getmethods__["scream_parameters"] = _Py_Scream_EE.ScreamModel_scream_parameters_get
    if _newclass:scream_parameters = property(_Py_Scream_EE.ScreamModel_scream_parameters_get, _Py_Scream_EE.ScreamModel_scream_parameters_set)
    __swig_setmethods__["HANDLER"] = _Py_Scream_EE.ScreamModel_HANDLER_set
    __swig_getmethods__["HANDLER"] = _Py_Scream_EE.ScreamModel_HANDLER_get
    if _newclass:HANDLER = property(_Py_Scream_EE.ScreamModel_HANDLER_get, _Py_Scream_EE.ScreamModel_HANDLER_set)
    __swig_setmethods__["ptn"] = _Py_Scream_EE.ScreamModel_ptn_set
    __swig_getmethods__["ptn"] = _Py_Scream_EE.ScreamModel_ptn_get
    if _newclass:ptn = property(_Py_Scream_EE.ScreamModel_ptn_get, _Py_Scream_EE.ScreamModel_ptn_set)
    __swig_setmethods__["scream_EE"] = _Py_Scream_EE.ScreamModel_scream_EE_set
    __swig_getmethods__["scream_EE"] = _Py_Scream_EE.ScreamModel_scream_EE_get
    if _newclass:scream_EE = property(_Py_Scream_EE.ScreamModel_scream_EE_get, _Py_Scream_EE.ScreamModel_scream_EE_set)
    def new_ScreamEE(*args): return _Py_Scream_EE.ScreamModel_new_ScreamEE(*args)
    def new_Rotlib(*args): return _Py_Scream_EE.ScreamModel_new_Rotlib(*args)
    __swig_setmethods__["scream_EE_list"] = _Py_Scream_EE.ScreamModel_scream_EE_list_set
    __swig_getmethods__["scream_EE_list"] = _Py_Scream_EE.ScreamModel_scream_EE_list_get
    if _newclass:scream_EE_list = property(_Py_Scream_EE.ScreamModel_scream_EE_list_get, _Py_Scream_EE.ScreamModel_scream_EE_list_set)
    __swig_setmethods__["rotlib_list"] = _Py_Scream_EE.ScreamModel_rotlib_list_set
    __swig_getmethods__["rotlib_list"] = _Py_Scream_EE.ScreamModel_rotlib_list_get
    if _newclass:rotlib_list = property(_Py_Scream_EE.ScreamModel_rotlib_list_get, _Py_Scream_EE.ScreamModel_rotlib_list_set)

class ScreamModelPtr(ScreamModel):
    def __init__(self, this):
        _swig_setattr(self, ScreamModel, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ScreamModel, 'thisown', 0)
        _swig_setattr(self, ScreamModel,self.__class__,ScreamModel)
_Py_Scream_EE.ScreamModel_swigregister(ScreamModelPtr)

class ScreamParameters(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ScreamParameters, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ScreamParameters, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ ScreamParameters instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, ScreamParameters, 'this', _Py_Scream_EE.new_ScreamParameters(*args))
        _swig_setattr(self, ScreamParameters, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_ScreamParameters):
        try:
            if self.thisown: destroy(self)
        except: pass

    __swig_setmethods__["InputFileName"] = _Py_Scream_EE.ScreamParameters_InputFileName_set
    __swig_getmethods__["InputFileName"] = _Py_Scream_EE.ScreamParameters_InputFileName_get
    if _newclass:InputFileName = property(_Py_Scream_EE.ScreamParameters_InputFileName_get, _Py_Scream_EE.ScreamParameters_InputFileName_set)
    __swig_setmethods__["MutateResidueInfo"] = _Py_Scream_EE.ScreamParameters_MutateResidueInfo_set
    __swig_getmethods__["MutateResidueInfo"] = _Py_Scream_EE.ScreamParameters_MutateResidueInfo_get
    if _newclass:MutateResidueInfo = property(_Py_Scream_EE.ScreamParameters_MutateResidueInfo_get, _Py_Scream_EE.ScreamParameters_MutateResidueInfo_set)
    __swig_setmethods__["AdditionalLibraryInfo"] = _Py_Scream_EE.ScreamParameters_AdditionalLibraryInfo_set
    __swig_getmethods__["AdditionalLibraryInfo"] = _Py_Scream_EE.ScreamParameters_AdditionalLibraryInfo_get
    if _newclass:AdditionalLibraryInfo = property(_Py_Scream_EE.ScreamParameters_AdditionalLibraryInfo_get, _Py_Scream_EE.ScreamParameters_AdditionalLibraryInfo_set)
    __swig_setmethods__["Library"] = _Py_Scream_EE.ScreamParameters_Library_set
    __swig_getmethods__["Library"] = _Py_Scream_EE.ScreamParameters_Library_get
    if _newclass:Library = property(_Py_Scream_EE.ScreamParameters_Library_get, _Py_Scream_EE.ScreamParameters_Library_set)
    __swig_setmethods__["PlacementMethod"] = _Py_Scream_EE.ScreamParameters_PlacementMethod_set
    __swig_getmethods__["PlacementMethod"] = _Py_Scream_EE.ScreamParameters_PlacementMethod_get
    if _newclass:PlacementMethod = property(_Py_Scream_EE.ScreamParameters_PlacementMethod_get, _Py_Scream_EE.ScreamParameters_PlacementMethod_set)
    __swig_setmethods__["CreateCBParameters"] = _Py_Scream_EE.ScreamParameters_CreateCBParameters_set
    __swig_getmethods__["CreateCBParameters"] = _Py_Scream_EE.ScreamParameters_CreateCBParameters_get
    if _newclass:CreateCBParameters = property(_Py_Scream_EE.ScreamParameters_CreateCBParameters_get, _Py_Scream_EE.ScreamParameters_CreateCBParameters_set)
    __swig_setmethods__["KeepOriginalRotamer"] = _Py_Scream_EE.ScreamParameters_KeepOriginalRotamer_set
    __swig_getmethods__["KeepOriginalRotamer"] = _Py_Scream_EE.ScreamParameters_KeepOriginalRotamer_get
    if _newclass:KeepOriginalRotamer = property(_Py_Scream_EE.ScreamParameters_KeepOriginalRotamer_get, _Py_Scream_EE.ScreamParameters_KeepOriginalRotamer_set)
    __swig_setmethods__["UseScreamEnergyFunction"] = _Py_Scream_EE.ScreamParameters_UseScreamEnergyFunction_set
    __swig_getmethods__["UseScreamEnergyFunction"] = _Py_Scream_EE.ScreamParameters_UseScreamEnergyFunction_get
    if _newclass:UseScreamEnergyFunction = property(_Py_Scream_EE.ScreamParameters_UseScreamEnergyFunction_get, _Py_Scream_EE.ScreamParameters_UseScreamEnergyFunction_set)
    __swig_setmethods__["UseDeltaMethod"] = _Py_Scream_EE.ScreamParameters_UseDeltaMethod_set
    __swig_getmethods__["UseDeltaMethod"] = _Py_Scream_EE.ScreamParameters_UseDeltaMethod_get
    if _newclass:UseDeltaMethod = property(_Py_Scream_EE.ScreamParameters_UseDeltaMethod_get, _Py_Scream_EE.ScreamParameters_UseDeltaMethod_set)
    __swig_setmethods__["UseRotamerNeighborList"] = _Py_Scream_EE.ScreamParameters_UseRotamerNeighborList_set
    __swig_getmethods__["UseRotamerNeighborList"] = _Py_Scream_EE.ScreamParameters_UseRotamerNeighborList_get
    if _newclass:UseRotamerNeighborList = property(_Py_Scream_EE.ScreamParameters_UseRotamerNeighborList_get, _Py_Scream_EE.ScreamParameters_UseRotamerNeighborList_set)
    __swig_setmethods__["UseAsymmetricDelta"] = _Py_Scream_EE.ScreamParameters_UseAsymmetricDelta_set
    __swig_getmethods__["UseAsymmetricDelta"] = _Py_Scream_EE.ScreamParameters_UseAsymmetricDelta_get
    if _newclass:UseAsymmetricDelta = property(_Py_Scream_EE.ScreamParameters_UseAsymmetricDelta_get, _Py_Scream_EE.ScreamParameters_UseAsymmetricDelta_set)
    __swig_setmethods__["UseDeltaForInterResiE"] = _Py_Scream_EE.ScreamParameters_UseDeltaForInterResiE_set
    __swig_getmethods__["UseDeltaForInterResiE"] = _Py_Scream_EE.ScreamParameters_UseDeltaForInterResiE_get
    if _newclass:UseDeltaForInterResiE = property(_Py_Scream_EE.ScreamParameters_UseDeltaForInterResiE_get, _Py_Scream_EE.ScreamParameters_UseDeltaForInterResiE_set)
    __swig_setmethods__["FlatDeltaValue"] = _Py_Scream_EE.ScreamParameters_FlatDeltaValue_set
    __swig_getmethods__["FlatDeltaValue"] = _Py_Scream_EE.ScreamParameters_FlatDeltaValue_get
    if _newclass:FlatDeltaValue = property(_Py_Scream_EE.ScreamParameters_FlatDeltaValue_get, _Py_Scream_EE.ScreamParameters_FlatDeltaValue_set)
    __swig_setmethods__["DeltaStandardDevs"] = _Py_Scream_EE.ScreamParameters_DeltaStandardDevs_set
    __swig_getmethods__["DeltaStandardDevs"] = _Py_Scream_EE.ScreamParameters_DeltaStandardDevs_get
    if _newclass:DeltaStandardDevs = property(_Py_Scream_EE.ScreamParameters_DeltaStandardDevs_get, _Py_Scream_EE.ScreamParameters_DeltaStandardDevs_set)
    __swig_setmethods__["InnerWallScalingFactor"] = _Py_Scream_EE.ScreamParameters_InnerWallScalingFactor_set
    __swig_getmethods__["InnerWallScalingFactor"] = _Py_Scream_EE.ScreamParameters_InnerWallScalingFactor_get
    if _newclass:InnerWallScalingFactor = property(_Py_Scream_EE.ScreamParameters_InnerWallScalingFactor_get, _Py_Scream_EE.ScreamParameters_InnerWallScalingFactor_set)
    __swig_setmethods__["NonPolarHCalc"] = _Py_Scream_EE.ScreamParameters_NonPolarHCalc_set
    __swig_getmethods__["NonPolarHCalc"] = _Py_Scream_EE.ScreamParameters_NonPolarHCalc_get
    if _newclass:NonPolarHCalc = property(_Py_Scream_EE.ScreamParameters_NonPolarHCalc_get, _Py_Scream_EE.ScreamParameters_NonPolarHCalc_set)
    __swig_setmethods__["ScoringFunction"] = _Py_Scream_EE.ScreamParameters_ScoringFunction_set
    __swig_getmethods__["ScoringFunction"] = _Py_Scream_EE.ScreamParameters_ScoringFunction_get
    if _newclass:ScoringFunction = property(_Py_Scream_EE.ScreamParameters_ScoringFunction_get, _Py_Scream_EE.ScreamParameters_ScoringFunction_set)
    __swig_setmethods__["MultiplePlacementMethod"] = _Py_Scream_EE.ScreamParameters_MultiplePlacementMethod_set
    __swig_getmethods__["MultiplePlacementMethod"] = _Py_Scream_EE.ScreamParameters_MultiplePlacementMethod_get
    if _newclass:MultiplePlacementMethod = property(_Py_Scream_EE.ScreamParameters_MultiplePlacementMethod_get, _Py_Scream_EE.ScreamParameters_MultiplePlacementMethod_set)
    __swig_setmethods__["CBGroundSpectrumCalc"] = _Py_Scream_EE.ScreamParameters_CBGroundSpectrumCalc_set
    __swig_getmethods__["CBGroundSpectrumCalc"] = _Py_Scream_EE.ScreamParameters_CBGroundSpectrumCalc_get
    if _newclass:CBGroundSpectrumCalc = property(_Py_Scream_EE.ScreamParameters_CBGroundSpectrumCalc_get, _Py_Scream_EE.ScreamParameters_CBGroundSpectrumCalc_set)
    __swig_setmethods__["OneEnergyFFParFile"] = _Py_Scream_EE.ScreamParameters_OneEnergyFFParFile_set
    __swig_getmethods__["OneEnergyFFParFile"] = _Py_Scream_EE.ScreamParameters_OneEnergyFFParFile_get
    if _newclass:OneEnergyFFParFile = property(_Py_Scream_EE.ScreamParameters_OneEnergyFFParFile_get, _Py_Scream_EE.ScreamParameters_OneEnergyFFParFile_set)
    __swig_setmethods__["DeltaParFile"] = _Py_Scream_EE.ScreamParameters_DeltaParFile_set
    __swig_getmethods__["DeltaParFile"] = _Py_Scream_EE.ScreamParameters_DeltaParFile_get
    if _newclass:DeltaParFile = property(_Py_Scream_EE.ScreamParameters_DeltaParFile_get, _Py_Scream_EE.ScreamParameters_DeltaParFile_set)
    __swig_setmethods__["EachAtomDeltaFile"] = _Py_Scream_EE.ScreamParameters_EachAtomDeltaFile_set
    __swig_getmethods__["EachAtomDeltaFile"] = _Py_Scream_EE.ScreamParameters_EachAtomDeltaFile_get
    if _newclass:EachAtomDeltaFile = property(_Py_Scream_EE.ScreamParameters_EachAtomDeltaFile_get, _Py_Scream_EE.ScreamParameters_EachAtomDeltaFile_set)
    __swig_setmethods__["PolarOptimizationExclusions"] = _Py_Scream_EE.ScreamParameters_PolarOptimizationExclusions_set
    __swig_getmethods__["PolarOptimizationExclusions"] = _Py_Scream_EE.ScreamParameters_PolarOptimizationExclusions_get
    if _newclass:PolarOptimizationExclusions = property(_Py_Scream_EE.ScreamParameters_PolarOptimizationExclusions_get, _Py_Scream_EE.ScreamParameters_PolarOptimizationExclusions_set)
    __swig_setmethods__["LJOption"] = _Py_Scream_EE.ScreamParameters_LJOption_set
    __swig_getmethods__["LJOption"] = _Py_Scream_EE.ScreamParameters_LJOption_get
    if _newclass:LJOption = property(_Py_Scream_EE.ScreamParameters_LJOption_get, _Py_Scream_EE.ScreamParameters_LJOption_set)
    __swig_setmethods__["CoulombMode"] = _Py_Scream_EE.ScreamParameters_CoulombMode_set
    __swig_getmethods__["CoulombMode"] = _Py_Scream_EE.ScreamParameters_CoulombMode_get
    if _newclass:CoulombMode = property(_Py_Scream_EE.ScreamParameters_CoulombMode_get, _Py_Scream_EE.ScreamParameters_CoulombMode_set)
    __swig_setmethods__["Dielectric"] = _Py_Scream_EE.ScreamParameters_Dielectric_set
    __swig_getmethods__["Dielectric"] = _Py_Scream_EE.ScreamParameters_Dielectric_get
    if _newclass:Dielectric = property(_Py_Scream_EE.ScreamParameters_Dielectric_get, _Py_Scream_EE.ScreamParameters_Dielectric_set)
    __swig_setmethods__["Selections"] = _Py_Scream_EE.ScreamParameters_Selections_set
    __swig_getmethods__["Selections"] = _Py_Scream_EE.ScreamParameters_Selections_get
    if _newclass:Selections = property(_Py_Scream_EE.ScreamParameters_Selections_get, _Py_Scream_EE.ScreamParameters_Selections_set)
    __swig_setmethods__["MaxSearchNumber"] = _Py_Scream_EE.ScreamParameters_MaxSearchNumber_set
    __swig_getmethods__["MaxSearchNumber"] = _Py_Scream_EE.ScreamParameters_MaxSearchNumber_get
    if _newclass:MaxSearchNumber = property(_Py_Scream_EE.ScreamParameters_MaxSearchNumber_get, _Py_Scream_EE.ScreamParameters_MaxSearchNumber_set)
    __swig_setmethods__["AbsStericClashCutoffEL"] = _Py_Scream_EE.ScreamParameters_AbsStericClashCutoffEL_set
    __swig_getmethods__["AbsStericClashCutoffEL"] = _Py_Scream_EE.ScreamParameters_AbsStericClashCutoffEL_get
    if _newclass:AbsStericClashCutoffEL = property(_Py_Scream_EE.ScreamParameters_AbsStericClashCutoffEL_get, _Py_Scream_EE.ScreamParameters_AbsStericClashCutoffEL_set)
    __swig_setmethods__["StericClashCutoffEnergy"] = _Py_Scream_EE.ScreamParameters_StericClashCutoffEnergy_set
    __swig_getmethods__["StericClashCutoffEnergy"] = _Py_Scream_EE.ScreamParameters_StericClashCutoffEnergy_get
    if _newclass:StericClashCutoffEnergy = property(_Py_Scream_EE.ScreamParameters_StericClashCutoffEnergy_get, _Py_Scream_EE.ScreamParameters_StericClashCutoffEnergy_set)
    __swig_setmethods__["StericClashCutoffDist"] = _Py_Scream_EE.ScreamParameters_StericClashCutoffDist_set
    __swig_getmethods__["StericClashCutoffDist"] = _Py_Scream_EE.ScreamParameters_StericClashCutoffDist_get
    if _newclass:StericClashCutoffDist = property(_Py_Scream_EE.ScreamParameters_StericClashCutoffDist_get, _Py_Scream_EE.ScreamParameters_StericClashCutoffDist_set)
    __swig_setmethods__["MaxFinalStepRunTime"] = _Py_Scream_EE.ScreamParameters_MaxFinalStepRunTime_set
    __swig_getmethods__["MaxFinalStepRunTime"] = _Py_Scream_EE.ScreamParameters_MaxFinalStepRunTime_get
    if _newclass:MaxFinalStepRunTime = property(_Py_Scream_EE.ScreamParameters_MaxFinalStepRunTime_get, _Py_Scream_EE.ScreamParameters_MaxFinalStepRunTime_set)
    __swig_setmethods__["LibPath"] = _Py_Scream_EE.ScreamParameters_LibPath_set
    __swig_getmethods__["LibPath"] = _Py_Scream_EE.ScreamParameters_LibPath_get
    if _newclass:LibPath = property(_Py_Scream_EE.ScreamParameters_LibPath_get, _Py_Scream_EE.ScreamParameters_LibPath_set)
    __swig_setmethods__["Verbosity"] = _Py_Scream_EE.ScreamParameters_Verbosity_set
    __swig_getmethods__["Verbosity"] = _Py_Scream_EE.ScreamParameters_Verbosity_get
    if _newclass:Verbosity = property(_Py_Scream_EE.ScreamParameters_Verbosity_get, _Py_Scream_EE.ScreamParameters_Verbosity_set)
    __swig_setmethods__["DesignPositionAndClass"] = _Py_Scream_EE.ScreamParameters_DesignPositionAndClass_set
    __swig_getmethods__["DesignPositionAndClass"] = _Py_Scream_EE.ScreamParameters_DesignPositionAndClass_get
    if _newclass:DesignPositionAndClass = property(_Py_Scream_EE.ScreamParameters_DesignPositionAndClass_get, _Py_Scream_EE.ScreamParameters_DesignPositionAndClass_set)
    __swig_setmethods__["DesignAAClassDefns"] = _Py_Scream_EE.ScreamParameters_DesignAAClassDefns_set
    __swig_getmethods__["DesignAAClassDefns"] = _Py_Scream_EE.ScreamParameters_DesignAAClassDefns_get
    if _newclass:DesignAAClassDefns = property(_Py_Scream_EE.ScreamParameters_DesignAAClassDefns_get, _Py_Scream_EE.ScreamParameters_DesignAAClassDefns_set)
    __swig_setmethods__["JustOutputSequence"] = _Py_Scream_EE.ScreamParameters_JustOutputSequence_set
    __swig_getmethods__["JustOutputSequence"] = _Py_Scream_EE.ScreamParameters_JustOutputSequence_get
    if _newclass:JustOutputSequence = property(_Py_Scream_EE.ScreamParameters_JustOutputSequence_get, _Py_Scream_EE.ScreamParameters_JustOutputSequence_set)
    __swig_setmethods__["StructuresPerSequence"] = _Py_Scream_EE.ScreamParameters_StructuresPerSequence_set
    __swig_getmethods__["StructuresPerSequence"] = _Py_Scream_EE.ScreamParameters_StructuresPerSequence_get
    if _newclass:StructuresPerSequence = property(_Py_Scream_EE.ScreamParameters_StructuresPerSequence_get, _Py_Scream_EE.ScreamParameters_StructuresPerSequence_set)
    __swig_setmethods__["BindingSiteMode"] = _Py_Scream_EE.ScreamParameters_BindingSiteMode_set
    __swig_getmethods__["BindingSiteMode"] = _Py_Scream_EE.ScreamParameters_BindingSiteMode_get
    if _newclass:BindingSiteMode = property(_Py_Scream_EE.ScreamParameters_BindingSiteMode_get, _Py_Scream_EE.ScreamParameters_BindingSiteMode_set)
    __swig_setmethods__["FixedResidues"] = _Py_Scream_EE.ScreamParameters_FixedResidues_set
    __swig_getmethods__["FixedResidues"] = _Py_Scream_EE.ScreamParameters_FixedResidues_get
    if _newclass:FixedResidues = property(_Py_Scream_EE.ScreamParameters_FixedResidues_get, _Py_Scream_EE.ScreamParameters_FixedResidues_set)
    __swig_setmethods__["AroundAtom"] = _Py_Scream_EE.ScreamParameters_AroundAtom_set
    __swig_getmethods__["AroundAtom"] = _Py_Scream_EE.ScreamParameters_AroundAtom_get
    if _newclass:AroundAtom = property(_Py_Scream_EE.ScreamParameters_AroundAtom_get, _Py_Scream_EE.ScreamParameters_AroundAtom_set)
    __swig_setmethods__["AroundResidue"] = _Py_Scream_EE.ScreamParameters_AroundResidue_set
    __swig_getmethods__["AroundResidue"] = _Py_Scream_EE.ScreamParameters_AroundResidue_get
    if _newclass:AroundResidue = property(_Py_Scream_EE.ScreamParameters_AroundResidue_get, _Py_Scream_EE.ScreamParameters_AroundResidue_set)
    __swig_setmethods__["AroundChain"] = _Py_Scream_EE.ScreamParameters_AroundChain_set
    __swig_getmethods__["AroundChain"] = _Py_Scream_EE.ScreamParameters_AroundChain_get
    if _newclass:AroundChain = property(_Py_Scream_EE.ScreamParameters_AroundChain_get, _Py_Scream_EE.ScreamParameters_AroundChain_set)
    __swig_setmethods__["AroundDistance"] = _Py_Scream_EE.ScreamParameters_AroundDistance_set
    __swig_getmethods__["AroundDistance"] = _Py_Scream_EE.ScreamParameters_AroundDistance_get
    if _newclass:AroundDistance = property(_Py_Scream_EE.ScreamParameters_AroundDistance_get, _Py_Scream_EE.ScreamParameters_AroundDistance_set)
    __swig_setmethods__["AroundDistanceDefn"] = _Py_Scream_EE.ScreamParameters_AroundDistanceDefn_set
    __swig_getmethods__["AroundDistanceDefn"] = _Py_Scream_EE.ScreamParameters_AroundDistanceDefn_get
    if _newclass:AroundDistanceDefn = property(_Py_Scream_EE.ScreamParameters_AroundDistanceDefn_get, _Py_Scream_EE.ScreamParameters_AroundDistanceDefn_set)
    def getMutateResidueInfoList(*args): return _Py_Scream_EE.ScreamParameters_getMutateResidueInfoList(*args)
    def getAdditionalLibraryInfo(*args): return _Py_Scream_EE.ScreamParameters_getAdditionalLibraryInfo(*args)
    def getKeepOriginalRotamer(*args): return _Py_Scream_EE.ScreamParameters_getKeepOriginalRotamer(*args)
    def getUseScreamEnergyFunction(*args): return _Py_Scream_EE.ScreamParameters_getUseScreamEnergyFunction(*args)
    def getPlacementMethod(*args): return _Py_Scream_EE.ScreamParameters_getPlacementMethod(*args)
    def getCreateCBParameters(*args): return _Py_Scream_EE.ScreamParameters_getCreateCBParameters(*args)
    def getUseDeltaMethod(*args): return _Py_Scream_EE.ScreamParameters_getUseDeltaMethod(*args)
    def getUseRotamerNeighborList(*args): return _Py_Scream_EE.ScreamParameters_getUseRotamerNeighborList(*args)
    def getUseAsymmetricDelta(*args): return _Py_Scream_EE.ScreamParameters_getUseAsymmetricDelta(*args)
    def getUseDeltaForInterResiE(*args): return _Py_Scream_EE.ScreamParameters_getUseDeltaForInterResiE(*args)
    def getFlatDeltaValue(*args): return _Py_Scream_EE.ScreamParameters_getFlatDeltaValue(*args)
    def getDeltaStandardDevs(*args): return _Py_Scream_EE.ScreamParameters_getDeltaStandardDevs(*args)
    def getInnerWallScalingFactor(*args): return _Py_Scream_EE.ScreamParameters_getInnerWallScalingFactor(*args)
    def getNonPolarHCalc(*args): return _Py_Scream_EE.ScreamParameters_getNonPolarHCalc(*args)
    def getOneEnergyFFParFile(*args): return _Py_Scream_EE.ScreamParameters_getOneEnergyFFParFile(*args)
    def getDeltaParFile(*args): return _Py_Scream_EE.ScreamParameters_getDeltaParFile(*args)
    def getEachAtomDeltaFile(*args): return _Py_Scream_EE.ScreamParameters_getEachAtomDeltaFile(*args)
    def getPolarOptimizationExclusions(*args): return _Py_Scream_EE.ScreamParameters_getPolarOptimizationExclusions(*args)
    def getSelections(*args): return _Py_Scream_EE.ScreamParameters_getSelections(*args)
    def getMaxSearchNumber(*args): return _Py_Scream_EE.ScreamParameters_getMaxSearchNumber(*args)
    def getAbsStericClashCutoffEL(*args): return _Py_Scream_EE.ScreamParameters_getAbsStericClashCutoffEL(*args)
    def getStericClashCutoffEnergy(*args): return _Py_Scream_EE.ScreamParameters_getStericClashCutoffEnergy(*args)
    def getStericClashCutoffDist(*args): return _Py_Scream_EE.ScreamParameters_getStericClashCutoffDist(*args)
    def getMaxFinalStepRunTime(*args): return _Py_Scream_EE.ScreamParameters_getMaxFinalStepRunTime(*args)
    def getDesignPositionAndClass(*args): return _Py_Scream_EE.ScreamParameters_getDesignPositionAndClass(*args)
    def getDesignAAClassDefns(*args): return _Py_Scream_EE.ScreamParameters_getDesignAAClassDefns(*args)
    def getJustOutputSequence(*args): return _Py_Scream_EE.ScreamParameters_getJustOutputSequence(*args)
    def getLJOption(*args): return _Py_Scream_EE.ScreamParameters_getLJOption(*args)
    def getCoulombMode(*args): return _Py_Scream_EE.ScreamParameters_getCoulombMode(*args)
    def getDielectric(*args): return _Py_Scream_EE.ScreamParameters_getDielectric(*args)
    def getBindingSiteMode(*args): return _Py_Scream_EE.ScreamParameters_getBindingSiteMode(*args)
    def getFixedResidues(*args): return _Py_Scream_EE.ScreamParameters_getFixedResidues(*args)
    def getAroundAtom(*args): return _Py_Scream_EE.ScreamParameters_getAroundAtom(*args)
    def getAroundResidue(*args): return _Py_Scream_EE.ScreamParameters_getAroundResidue(*args)
    def getAroundChain(*args): return _Py_Scream_EE.ScreamParameters_getAroundChain(*args)
    def getAroundDistance(*args): return _Py_Scream_EE.ScreamParameters_getAroundDistance(*args)
    def getAroundDistanceDefn(*args): return _Py_Scream_EE.ScreamParameters_getAroundDistanceDefn(*args)
    def getDesignPositions(*args): return _Py_Scream_EE.ScreamParameters_getDesignPositions(*args)
    def getDesignClassFromPosition(*args): return _Py_Scream_EE.ScreamParameters_getDesignClassFromPosition(*args)
    def getDesignClassAAs(*args): return _Py_Scream_EE.ScreamParameters_getDesignClassAAs(*args)
    def multiplePlacementMethod(*args): return _Py_Scream_EE.ScreamParameters_multiplePlacementMethod(*args)
    def getCBGroundSpectrumCalc(*args): return _Py_Scream_EE.ScreamParameters_getCBGroundSpectrumCalc(*args)
    def read_scream_par_file(*args): return _Py_Scream_EE.ScreamParameters_read_scream_par_file(*args)
    def print_to_output(*args): return _Py_Scream_EE.ScreamParameters_print_to_output(*args)
    def minimizationMethod(*args): return _Py_Scream_EE.ScreamParameters_minimizationMethod(*args)
    def minimizationSteps(*args): return _Py_Scream_EE.ScreamParameters_minimizationSteps(*args)
    def oneEMethod(*args): return _Py_Scream_EE.ScreamParameters_oneEMethod(*args)
    def residueToScreamName(*args): return _Py_Scream_EE.ScreamParameters_residueToScreamName(*args)
    def residueToScreamPstn(*args): return _Py_Scream_EE.ScreamParameters_residueToScreamPstn(*args)
    def residueToScreamChn(*args): return _Py_Scream_EE.ScreamParameters_residueToScreamChn(*args)
    def determineLibDirPath(*args): return _Py_Scream_EE.ScreamParameters_determineLibDirPath(*args)
    def determineLibDirFileNameSuffix(*args): return _Py_Scream_EE.ScreamParameters_determineLibDirFileNameSuffix(*args)
    def determineCnnDirPath(*args): return _Py_Scream_EE.ScreamParameters_determineCnnDirPath(*args)
    def getLibResolution(*args): return _Py_Scream_EE.ScreamParameters_getLibResolution(*args)
    def returnEnergyMethod(*args): return _Py_Scream_EE.ScreamParameters_returnEnergyMethod(*args)
    def returnEnergyMethodTValue(*args): return _Py_Scream_EE.ScreamParameters_returnEnergyMethodTValue(*args)
    def getVerbosity(*args): return _Py_Scream_EE.ScreamParameters_getVerbosity(*args)
    def _init_default_params(*args): return _Py_Scream_EE.ScreamParameters__init_default_params(*args)

class ScreamParametersPtr(ScreamParameters):
    def __init__(self, this):
        _swig_setattr(self, ScreamParameters, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ScreamParameters, 'thisown', 0)
        _swig_setattr(self, ScreamParameters,self.__class__,ScreamParameters)
_Py_Scream_EE.ScreamParameters_swigregister(ScreamParametersPtr)

class SCREAM_ATOM(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SCREAM_ATOM, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SCREAM_ATOM, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ SCREAM_ATOM instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, SCREAM_ATOM, 'this', _Py_Scream_EE.new_SCREAM_ATOM(*args))
        _swig_setattr(self, SCREAM_ATOM, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_SCREAM_ATOM):
        try:
            if self.thisown: destroy(self)
        except: pass

    def pdb_init(*args): return _Py_Scream_EE.SCREAM_ATOM_pdb_init(*args)
    def set_x(*args): return _Py_Scream_EE.SCREAM_ATOM_set_x(*args)
    def set_y(*args): return _Py_Scream_EE.SCREAM_ATOM_set_y(*args)
    def set_z(*args): return _Py_Scream_EE.SCREAM_ATOM_set_z(*args)
    def getAtomLabel(*args): return _Py_Scream_EE.SCREAM_ATOM_getAtomLabel(*args)
    def setAtomLabel(*args): return _Py_Scream_EE.SCREAM_ATOM_setAtomLabel(*args)
    def getAtomType(*args): return _Py_Scream_EE.SCREAM_ATOM_getAtomType(*args)
    def setAtomType(*args): return _Py_Scream_EE.SCREAM_ATOM_setAtomType(*args)
    def getX(*args): return _Py_Scream_EE.SCREAM_ATOM_getX(*args)
    def setX(*args): return _Py_Scream_EE.SCREAM_ATOM_setX(*args)
    def getY(*args): return _Py_Scream_EE.SCREAM_ATOM_getY(*args)
    def setY(*args): return _Py_Scream_EE.SCREAM_ATOM_setY(*args)
    def getZ(*args): return _Py_Scream_EE.SCREAM_ATOM_getZ(*args)
    def setZ(*args): return _Py_Scream_EE.SCREAM_ATOM_setZ(*args)
    def getCharge(*args): return _Py_Scream_EE.SCREAM_ATOM_getCharge(*args)
    def setCharge(*args): return _Py_Scream_EE.SCREAM_ATOM_setCharge(*args)
    def getResName(*args): return _Py_Scream_EE.SCREAM_ATOM_getResName(*args)
    def setResName(*args): return _Py_Scream_EE.SCREAM_ATOM_setResName(*args)
    def getChain(*args): return _Py_Scream_EE.SCREAM_ATOM_getChain(*args)
    def setChain(*args): return _Py_Scream_EE.SCREAM_ATOM_setChain(*args)
    def getResNum(*args): return _Py_Scream_EE.SCREAM_ATOM_getResNum(*args)
    def setResNum(*args): return _Py_Scream_EE.SCREAM_ATOM_setResNum(*args)
    __swig_setmethods__["GLOBAL_ATOM_N"] = _Py_Scream_EE.SCREAM_ATOM_GLOBAL_ATOM_N_set
    __swig_getmethods__["GLOBAL_ATOM_N"] = _Py_Scream_EE.SCREAM_ATOM_GLOBAL_ATOM_N_get
    if _newclass:GLOBAL_ATOM_N = property(_Py_Scream_EE.SCREAM_ATOM_GLOBAL_ATOM_N_get, _Py_Scream_EE.SCREAM_ATOM_GLOBAL_ATOM_N_set)
    __swig_setmethods__["keyw"] = _Py_Scream_EE.SCREAM_ATOM_keyw_set
    __swig_getmethods__["keyw"] = _Py_Scream_EE.SCREAM_ATOM_keyw_get
    if _newclass:keyw = property(_Py_Scream_EE.SCREAM_ATOM_keyw_get, _Py_Scream_EE.SCREAM_ATOM_keyw_set)
    __swig_setmethods__["atomLabel"] = _Py_Scream_EE.SCREAM_ATOM_atomLabel_set
    __swig_getmethods__["atomLabel"] = _Py_Scream_EE.SCREAM_ATOM_atomLabel_get
    if _newclass:atomLabel = property(_Py_Scream_EE.SCREAM_ATOM_atomLabel_get, _Py_Scream_EE.SCREAM_ATOM_atomLabel_set)
    __swig_setmethods__["stripped_atomLabel"] = _Py_Scream_EE.SCREAM_ATOM_stripped_atomLabel_set
    __swig_getmethods__["stripped_atomLabel"] = _Py_Scream_EE.SCREAM_ATOM_stripped_atomLabel_get
    if _newclass:stripped_atomLabel = property(_Py_Scream_EE.SCREAM_ATOM_stripped_atomLabel_get, _Py_Scream_EE.SCREAM_ATOM_stripped_atomLabel_set)
    __swig_setmethods__["isSC_Flag"] = _Py_Scream_EE.SCREAM_ATOM_isSC_Flag_set
    __swig_getmethods__["isSC_Flag"] = _Py_Scream_EE.SCREAM_ATOM_isSC_Flag_get
    if _newclass:isSC_Flag = property(_Py_Scream_EE.SCREAM_ATOM_isSC_Flag_get, _Py_Scream_EE.SCREAM_ATOM_isSC_Flag_set)
    __swig_setmethods__["isAAResAtom"] = _Py_Scream_EE.SCREAM_ATOM_isAAResAtom_set
    __swig_getmethods__["isAAResAtom"] = _Py_Scream_EE.SCREAM_ATOM_isAAResAtom_get
    if _newclass:isAAResAtom = property(_Py_Scream_EE.SCREAM_ATOM_isAAResAtom_get, _Py_Scream_EE.SCREAM_ATOM_isAAResAtom_set)
    __swig_setmethods__["atomType"] = _Py_Scream_EE.SCREAM_ATOM_atomType_set
    __swig_getmethods__["atomType"] = _Py_Scream_EE.SCREAM_ATOM_atomType_get
    if _newclass:atomType = property(_Py_Scream_EE.SCREAM_ATOM_atomType_get, _Py_Scream_EE.SCREAM_ATOM_atomType_set)
    __swig_setmethods__["stripped_atomType"] = _Py_Scream_EE.SCREAM_ATOM_stripped_atomType_set
    __swig_getmethods__["stripped_atomType"] = _Py_Scream_EE.SCREAM_ATOM_stripped_atomType_get
    if _newclass:stripped_atomType = property(_Py_Scream_EE.SCREAM_ATOM_stripped_atomType_get, _Py_Scream_EE.SCREAM_ATOM_stripped_atomType_set)
    __swig_setmethods__["occupancy"] = _Py_Scream_EE.SCREAM_ATOM_occupancy_set
    __swig_getmethods__["occupancy"] = _Py_Scream_EE.SCREAM_ATOM_occupancy_get
    if _newclass:occupancy = property(_Py_Scream_EE.SCREAM_ATOM_occupancy_get, _Py_Scream_EE.SCREAM_ATOM_occupancy_set)
    __swig_setmethods__["BFactor"] = _Py_Scream_EE.SCREAM_ATOM_BFactor_set
    __swig_getmethods__["BFactor"] = _Py_Scream_EE.SCREAM_ATOM_BFactor_get
    if _newclass:BFactor = property(_Py_Scream_EE.SCREAM_ATOM_BFactor_get, _Py_Scream_EE.SCREAM_ATOM_BFactor_set)
    __swig_setmethods__["resName"] = _Py_Scream_EE.SCREAM_ATOM_resName_set
    __swig_getmethods__["resName"] = _Py_Scream_EE.SCREAM_ATOM_resName_get
    if _newclass:resName = property(_Py_Scream_EE.SCREAM_ATOM_resName_get, _Py_Scream_EE.SCREAM_ATOM_resName_set)
    __swig_setmethods__["oneLetterResName"] = _Py_Scream_EE.SCREAM_ATOM_oneLetterResName_set
    __swig_getmethods__["oneLetterResName"] = _Py_Scream_EE.SCREAM_ATOM_oneLetterResName_get
    if _newclass:oneLetterResName = property(_Py_Scream_EE.SCREAM_ATOM_oneLetterResName_get, _Py_Scream_EE.SCREAM_ATOM_oneLetterResName_set)
    __swig_setmethods__["chain"] = _Py_Scream_EE.SCREAM_ATOM_chain_set
    __swig_getmethods__["chain"] = _Py_Scream_EE.SCREAM_ATOM_chain_get
    if _newclass:chain = property(_Py_Scream_EE.SCREAM_ATOM_chain_get, _Py_Scream_EE.SCREAM_ATOM_chain_set)
    __swig_setmethods__["resNum"] = _Py_Scream_EE.SCREAM_ATOM_resNum_set
    __swig_getmethods__["resNum"] = _Py_Scream_EE.SCREAM_ATOM_resNum_get
    if _newclass:resNum = property(_Py_Scream_EE.SCREAM_ATOM_resNum_get, _Py_Scream_EE.SCREAM_ATOM_resNum_set)
    __swig_setmethods__["atoms_connected"] = _Py_Scream_EE.SCREAM_ATOM_atoms_connected_set
    __swig_getmethods__["atoms_connected"] = _Py_Scream_EE.SCREAM_ATOM_atoms_connected_get
    if _newclass:atoms_connected = property(_Py_Scream_EE.SCREAM_ATOM_atoms_connected_get, _Py_Scream_EE.SCREAM_ATOM_atoms_connected_set)
    __swig_setmethods__["lone_pair"] = _Py_Scream_EE.SCREAM_ATOM_lone_pair_set
    __swig_getmethods__["lone_pair"] = _Py_Scream_EE.SCREAM_ATOM_lone_pair_get
    if _newclass:lone_pair = property(_Py_Scream_EE.SCREAM_ATOM_lone_pair_get, _Py_Scream_EE.SCREAM_ATOM_lone_pair_set)
    __swig_setmethods__["x"] = _Py_Scream_EE.SCREAM_ATOM_x_set
    __swig_getmethods__["x"] = _Py_Scream_EE.SCREAM_ATOM_x_get
    if _newclass:x = property(_Py_Scream_EE.SCREAM_ATOM_x_get, _Py_Scream_EE.SCREAM_ATOM_x_set)
    __swig_setmethods__["q"] = _Py_Scream_EE.SCREAM_ATOM_q_set
    __swig_getmethods__["q"] = _Py_Scream_EE.SCREAM_ATOM_q_get
    if _newclass:q = property(_Py_Scream_EE.SCREAM_ATOM_q_get, _Py_Scream_EE.SCREAM_ATOM_q_set)
    __swig_setmethods__["n"] = _Py_Scream_EE.SCREAM_ATOM_n_set
    __swig_getmethods__["n"] = _Py_Scream_EE.SCREAM_ATOM_n_get
    if _newclass:n = property(_Py_Scream_EE.SCREAM_ATOM_n_get, _Py_Scream_EE.SCREAM_ATOM_n_set)
    __swig_setmethods__["type"] = _Py_Scream_EE.SCREAM_ATOM_type_set
    __swig_getmethods__["type"] = _Py_Scream_EE.SCREAM_ATOM_type_get
    if _newclass:type = property(_Py_Scream_EE.SCREAM_ATOM_type_get, _Py_Scream_EE.SCREAM_ATOM_type_set)
    __swig_setmethods__["flags"] = _Py_Scream_EE.SCREAM_ATOM_flags_set
    __swig_getmethods__["flags"] = _Py_Scream_EE.SCREAM_ATOM_flags_get
    if _newclass:flags = property(_Py_Scream_EE.SCREAM_ATOM_flags_get, _Py_Scream_EE.SCREAM_ATOM_flags_set)
    __swig_setmethods__["m"] = _Py_Scream_EE.SCREAM_ATOM_m_set
    __swig_getmethods__["m"] = _Py_Scream_EE.SCREAM_ATOM_m_get
    if _newclass:m = property(_Py_Scream_EE.SCREAM_ATOM_m_get, _Py_Scream_EE.SCREAM_ATOM_m_set)
    __swig_setmethods__["vchg2"] = _Py_Scream_EE.SCREAM_ATOM_vchg2_set
    __swig_getmethods__["vchg2"] = _Py_Scream_EE.SCREAM_ATOM_vchg2_get
    if _newclass:vchg2 = property(_Py_Scream_EE.SCREAM_ATOM_vchg2_get, _Py_Scream_EE.SCREAM_ATOM_vchg2_set)
    __swig_setmethods__["library_name"] = _Py_Scream_EE.SCREAM_ATOM_library_name_set
    __swig_getmethods__["library_name"] = _Py_Scream_EE.SCREAM_ATOM_library_name_get
    if _newclass:library_name = property(_Py_Scream_EE.SCREAM_ATOM_library_name_get, _Py_Scream_EE.SCREAM_ATOM_library_name_set)
    __swig_setmethods__["vdw_r"] = _Py_Scream_EE.SCREAM_ATOM_vdw_r_set
    __swig_getmethods__["vdw_r"] = _Py_Scream_EE.SCREAM_ATOM_vdw_r_get
    if _newclass:vdw_r = property(_Py_Scream_EE.SCREAM_ATOM_vdw_r_get, _Py_Scream_EE.SCREAM_ATOM_vdw_r_set)
    __swig_setmethods__["vdw_d"] = _Py_Scream_EE.SCREAM_ATOM_vdw_d_set
    __swig_getmethods__["vdw_d"] = _Py_Scream_EE.SCREAM_ATOM_vdw_d_get
    if _newclass:vdw_d = property(_Py_Scream_EE.SCREAM_ATOM_vdw_d_get, _Py_Scream_EE.SCREAM_ATOM_vdw_d_set)
    __swig_setmethods__["vdw_s"] = _Py_Scream_EE.SCREAM_ATOM_vdw_s_set
    __swig_getmethods__["vdw_s"] = _Py_Scream_EE.SCREAM_ATOM_vdw_s_get
    if _newclass:vdw_s = property(_Py_Scream_EE.SCREAM_ATOM_vdw_s_get, _Py_Scream_EE.SCREAM_ATOM_vdw_s_set)
    __swig_setmethods__["vachg"] = _Py_Scream_EE.SCREAM_ATOM_vachg_set
    __swig_getmethods__["vachg"] = _Py_Scream_EE.SCREAM_ATOM_vachg_get
    if _newclass:vachg = property(_Py_Scream_EE.SCREAM_ATOM_vachg_get, _Py_Scream_EE.SCREAM_ATOM_vachg_set)
    __swig_setmethods__["vrchg"] = _Py_Scream_EE.SCREAM_ATOM_vrchg_set
    __swig_getmethods__["vrchg"] = _Py_Scream_EE.SCREAM_ATOM_vrchg_get
    if _newclass:vrchg = property(_Py_Scream_EE.SCREAM_ATOM_vrchg_get, _Py_Scream_EE.SCREAM_ATOM_vrchg_set)
    __swig_setmethods__["hb_da"] = _Py_Scream_EE.SCREAM_ATOM_hb_da_set
    __swig_getmethods__["hb_da"] = _Py_Scream_EE.SCREAM_ATOM_hb_da_get
    if _newclass:hb_da = property(_Py_Scream_EE.SCREAM_ATOM_hb_da_get, _Py_Scream_EE.SCREAM_ATOM_hb_da_set)
    __swig_setmethods__["a"] = _Py_Scream_EE.SCREAM_ATOM_a_set
    __swig_getmethods__["a"] = _Py_Scream_EE.SCREAM_ATOM_a_get
    if _newclass:a = property(_Py_Scream_EE.SCREAM_ATOM_a_get, _Py_Scream_EE.SCREAM_ATOM_a_set)
    __swig_setmethods__["delta"] = _Py_Scream_EE.SCREAM_ATOM_delta_set
    __swig_getmethods__["delta"] = _Py_Scream_EE.SCREAM_ATOM_delta_get
    if _newclass:delta = property(_Py_Scream_EE.SCREAM_ATOM_delta_get, _Py_Scream_EE.SCREAM_ATOM_delta_set)
    __swig_setmethods__["connectivity_m"] = _Py_Scream_EE.SCREAM_ATOM_connectivity_m_set
    __swig_getmethods__["connectivity_m"] = _Py_Scream_EE.SCREAM_ATOM_connectivity_m_get
    if _newclass:connectivity_m = property(_Py_Scream_EE.SCREAM_ATOM_connectivity_m_get, _Py_Scream_EE.SCREAM_ATOM_connectivity_m_set)
    def initFlag(*args): return _Py_Scream_EE.SCREAM_ATOM_initFlag(*args)
    def resetFlag(*args): return _Py_Scream_EE.SCREAM_ATOM_resetFlag(*args)
    def make_atom_moveable(*args): return _Py_Scream_EE.SCREAM_ATOM_make_atom_moveable(*args)
    def make_atom_fixed(*args): return _Py_Scream_EE.SCREAM_ATOM_make_atom_fixed(*args)
    def make_atom_invisible(*args): return _Py_Scream_EE.SCREAM_ATOM_make_atom_invisible(*args)
    def make_atom_visible(*args): return _Py_Scream_EE.SCREAM_ATOM_make_atom_visible(*args)
    def make_atom_EL_invisible(*args): return _Py_Scream_EE.SCREAM_ATOM_make_atom_EL_invisible(*args)
    def make_atom_EL_visible(*args): return _Py_Scream_EE.SCREAM_ATOM_make_atom_EL_visible(*args)
    def is_part_of_EE(*args): return _Py_Scream_EE.SCREAM_ATOM_is_part_of_EE(*args)
    def fix_atom(*args): return _Py_Scream_EE.SCREAM_ATOM_fix_atom(*args)
    def distance(*args): return _Py_Scream_EE.SCREAM_ATOM_distance(*args)
    def distance_squared(*args): return _Py_Scream_EE.SCREAM_ATOM_distance_squared(*args)
    def worst_clash_dist(*args): return _Py_Scream_EE.SCREAM_ATOM_worst_clash_dist(*args)
    def feed_me(*args): return _Py_Scream_EE.SCREAM_ATOM_feed_me(*args)
    def feed_me_pdb(*args): return _Py_Scream_EE.SCREAM_ATOM_feed_me_pdb(*args)
    def make_bond(*args): return _Py_Scream_EE.SCREAM_ATOM_make_bond(*args)
    def delete_bond(*args): return _Py_Scream_EE.SCREAM_ATOM_delete_bond(*args)
    def copy(*args): return _Py_Scream_EE.SCREAM_ATOM_copy(*args)
    def copyJustCoords(*args): return _Py_Scream_EE.SCREAM_ATOM_copyJustCoords(*args)
    def dump(*args): return _Py_Scream_EE.SCREAM_ATOM_dump(*args)
    def pdb_dump(*args): return _Py_Scream_EE.SCREAM_ATOM_pdb_dump(*args)
    def return_bgf_line(*args): return _Py_Scream_EE.SCREAM_ATOM_return_bgf_line(*args)
    def return_pdb_line(*args): return _Py_Scream_EE.SCREAM_ATOM_return_pdb_line(*args)
    def append_to_filehandle(*args): return _Py_Scream_EE.SCREAM_ATOM_append_to_filehandle(*args)
    def pdb_append_to_filehandle(*args): return _Py_Scream_EE.SCREAM_ATOM_pdb_append_to_filehandle(*args)
    def pdb_append_to_ostream_connect_info(*args): return _Py_Scream_EE.SCREAM_ATOM_pdb_append_to_ostream_connect_info(*args)
    def append_to_ostream_connect_info(*args): return _Py_Scream_EE.SCREAM_ATOM_append_to_ostream_connect_info(*args)

class SCREAM_ATOMPtr(SCREAM_ATOM):
    def __init__(self, this):
        _swig_setattr(self, SCREAM_ATOM, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, SCREAM_ATOM, 'thisown', 0)
        _swig_setattr(self, SCREAM_ATOM,self.__class__,SCREAM_ATOM)
_Py_Scream_EE.SCREAM_ATOM_swigregister(SCREAM_ATOMPtr)

class Rotamer(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Rotamer, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Rotamer, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ Rotamer instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, Rotamer, 'this', _Py_Scream_EE.new_Rotamer(*args))
        _swig_setattr(self, Rotamer, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_Rotamer):
        try:
            if self.thisown: destroy(self)
        except: pass

    def deepcopy(*args): return _Py_Scream_EE.Rotamer_deepcopy(*args)
    def read_cnn_lines(*args): return _Py_Scream_EE.Rotamer_read_cnn_lines(*args)
    def print_Me(*args): return _Py_Scream_EE.Rotamer_print_Me(*args)
    def print_ordered_by_n(*args): return _Py_Scream_EE.Rotamer_print_ordered_by_n(*args)
    def append_to_filehandle(*args): return _Py_Scream_EE.Rotamer_append_to_filehandle(*args)
    def pdb_append_to_filehandle(*args): return _Py_Scream_EE.Rotamer_pdb_append_to_filehandle(*args)
    def append_to_ostream_connect_info(*args): return _Py_Scream_EE.Rotamer_append_to_ostream_connect_info(*args)
    def printEnergies(*args): return _Py_Scream_EE.Rotamer_printEnergies(*args)
    __swig_setmethods__["self_E"] = _Py_Scream_EE.Rotamer_self_E_set
    __swig_getmethods__["self_E"] = _Py_Scream_EE.Rotamer_self_E_get
    if _newclass:self_E = property(_Py_Scream_EE.Rotamer_self_E_get, _Py_Scream_EE.Rotamer_self_E_set)
    __swig_setmethods__["is_Original"] = _Py_Scream_EE.Rotamer_is_Original_set
    __swig_getmethods__["is_Original"] = _Py_Scream_EE.Rotamer_is_Original_get
    if _newclass:is_Original = property(_Py_Scream_EE.Rotamer_is_Original_get, _Py_Scream_EE.Rotamer_is_Original_set)
    def get_is_Original_flag(*args): return _Py_Scream_EE.Rotamer_get_is_Original_flag(*args)
    def set_is_Original_flag(*args): return _Py_Scream_EE.Rotamer_set_is_Original_flag(*args)
    __swig_setmethods__["same_backbone"] = _Py_Scream_EE.Rotamer_same_backbone_set
    __swig_getmethods__["same_backbone"] = _Py_Scream_EE.Rotamer_same_backbone_get
    if _newclass:same_backbone = property(_Py_Scream_EE.Rotamer_same_backbone_get, _Py_Scream_EE.Rotamer_same_backbone_set)
    __swig_setmethods__["library_name"] = _Py_Scream_EE.Rotamer_library_name_set
    __swig_getmethods__["library_name"] = _Py_Scream_EE.Rotamer_library_name_get
    if _newclass:library_name = property(_Py_Scream_EE.Rotamer_library_name_get, _Py_Scream_EE.Rotamer_library_name_set)
    def get_bb(*args): return _Py_Scream_EE.Rotamer_get_bb(*args)
    def get_sc(*args): return _Py_Scream_EE.Rotamer_get_sc(*args)
    def get_sc_atoms(*args): return _Py_Scream_EE.Rotamer_get_sc_atoms(*args)
    def get_bb_atoms(*args): return _Py_Scream_EE.Rotamer_get_bb_atoms(*args)
    def getAtom(*args): return _Py_Scream_EE.Rotamer_getAtom(*args)
    def getTheseAtoms(*args): return _Py_Scream_EE.Rotamer_getTheseAtoms(*args)
    def getAllRotamers(*args): return _Py_Scream_EE.Rotamer_getAllRotamers(*args)
    def fix_toggle(*args): return _Py_Scream_EE.Rotamer_fix_toggle(*args)
    def fix_sc_toggle(*args): return _Py_Scream_EE.Rotamer_fix_sc_toggle(*args)
    def fix_bb_toggle(*args): return _Py_Scream_EE.Rotamer_fix_bb_toggle(*args)
    def number_of_atoms(*args): return _Py_Scream_EE.Rotamer_number_of_atoms(*args)
    def total_charge(*args): return _Py_Scream_EE.Rotamer_total_charge(*args)
    def get_rotamer_n(*args): return _Py_Scream_EE.Rotamer_get_rotamer_n(*args)
    def get_mult_H_n(*args): return _Py_Scream_EE.Rotamer_get_mult_H_n(*args)
    def get_library_name(*args): return _Py_Scream_EE.Rotamer_get_library_name(*args)
    def get_empty_lattice_E(*args): return _Py_Scream_EE.Rotamer_get_empty_lattice_E(*args)
    def set_empty_lattice_E(*args): return _Py_Scream_EE.Rotamer_set_empty_lattice_E(*args)
    def get_empty_lattice_E_abs(*args): return _Py_Scream_EE.Rotamer_get_empty_lattice_E_abs(*args)
    def set_empty_lattice_E_abs(*args): return _Py_Scream_EE.Rotamer_set_empty_lattice_E_abs(*args)
    def get_empty_lattice_energy_rank(*args): return _Py_Scream_EE.Rotamer_get_empty_lattice_energy_rank(*args)
    def set_empty_lattice_energy_rank(*args): return _Py_Scream_EE.Rotamer_set_empty_lattice_energy_rank(*args)
    def setFailedDistanceCutoff(*args): return _Py_Scream_EE.Rotamer_setFailedDistanceCutoff(*args)
    def setPassedDistanceCutoff(*args): return _Py_Scream_EE.Rotamer_setPassedDistanceCutoff(*args)
    def failedDistanceCutoff(*args): return _Py_Scream_EE.Rotamer_failedDistanceCutoff(*args)
    def sameResidueTypeAs(*args): return _Py_Scream_EE.Rotamer_sameResidueTypeAs(*args)
    def get_preCalc_Energy_Line(*args): return _Py_Scream_EE.Rotamer_get_preCalc_Energy_Line(*args)
    def populate_preCalc_Terms(*args): return _Py_Scream_EE.Rotamer_populate_preCalc_Terms(*args)
    def get_preCalc_TotE(*args): return _Py_Scream_EE.Rotamer_get_preCalc_TotE(*args)
    def get_preCalc_BondsE(*args): return _Py_Scream_EE.Rotamer_get_preCalc_BondsE(*args)
    def get_preCalc_AnglesE(*args): return _Py_Scream_EE.Rotamer_get_preCalc_AnglesE(*args)
    def get_preCalc_TorsionsE(*args): return _Py_Scream_EE.Rotamer_get_preCalc_TorsionsE(*args)
    def get_preCalc_InversionsE(*args): return _Py_Scream_EE.Rotamer_get_preCalc_InversionsE(*args)
    def get_preCalc_CoulombE(*args): return _Py_Scream_EE.Rotamer_get_preCalc_CoulombE(*args)
    def get_preCalc_vdwE(*args): return _Py_Scream_EE.Rotamer_get_preCalc_vdwE(*args)
    def get_preCalc_HBondE(*args): return _Py_Scream_EE.Rotamer_get_preCalc_HBondE(*args)
    def get_preCalc_SolvE(*args): return _Py_Scream_EE.Rotamer_get_preCalc_SolvE(*args)
    def set_preCalc_TotE(*args): return _Py_Scream_EE.Rotamer_set_preCalc_TotE(*args)
    def set_preCalc_BondsE(*args): return _Py_Scream_EE.Rotamer_set_preCalc_BondsE(*args)
    def set_preCalc_AnglesE(*args): return _Py_Scream_EE.Rotamer_set_preCalc_AnglesE(*args)
    def set_preCalc_TorsionsE(*args): return _Py_Scream_EE.Rotamer_set_preCalc_TorsionsE(*args)
    def set_preCalc_InversionsE(*args): return _Py_Scream_EE.Rotamer_set_preCalc_InversionsE(*args)
    def set_preCalc_CoulombE(*args): return _Py_Scream_EE.Rotamer_set_preCalc_CoulombE(*args)
    def set_preCalc_vdwE(*args): return _Py_Scream_EE.Rotamer_set_preCalc_vdwE(*args)
    def set_preCalc_HBondE(*args): return _Py_Scream_EE.Rotamer_set_preCalc_HBondE(*args)
    def set_preCalc_SolvE(*args): return _Py_Scream_EE.Rotamer_set_preCalc_SolvE(*args)
    def get_rotlib_E(*args): return _Py_Scream_EE.Rotamer_get_rotlib_E(*args)
    def get_sc_valence_E(*args): return _Py_Scream_EE.Rotamer_get_sc_valence_E(*args)
    def get_sc_coulomb_E(*args): return _Py_Scream_EE.Rotamer_get_sc_coulomb_E(*args)
    def get_sc_vdw_E(*args): return _Py_Scream_EE.Rotamer_get_sc_vdw_E(*args)
    def get_sc_hb_E(*args): return _Py_Scream_EE.Rotamer_get_sc_hb_E(*args)
    def get_sc_total_nb_E(*args): return _Py_Scream_EE.Rotamer_get_sc_total_nb_E(*args)
    def get_sc_solvation_E(*args): return _Py_Scream_EE.Rotamer_get_sc_solvation_E(*args)
    def get_sc_total_E(*args): return _Py_Scream_EE.Rotamer_get_sc_total_E(*args)
    def set_rotamer_n(*args): return _Py_Scream_EE.Rotamer_set_rotamer_n(*args)
    def set_rotlib_E(*args): return _Py_Scream_EE.Rotamer_set_rotlib_E(*args)
    def set_sc_valence_E(*args): return _Py_Scream_EE.Rotamer_set_sc_valence_E(*args)
    def set_sc_coulomb_E(*args): return _Py_Scream_EE.Rotamer_set_sc_coulomb_E(*args)
    def set_sc_vdw_E(*args): return _Py_Scream_EE.Rotamer_set_sc_vdw_E(*args)
    def set_sc_hb_E(*args): return _Py_Scream_EE.Rotamer_set_sc_hb_E(*args)
    def set_sc_total_nb_E(*args): return _Py_Scream_EE.Rotamer_set_sc_total_nb_E(*args)
    def set_sc_solvation_E(*args): return _Py_Scream_EE.Rotamer_set_sc_solvation_E(*args)
    def set_sc_total_E(*args): return _Py_Scream_EE.Rotamer_set_sc_total_E(*args)
    def match_bb(*args): return _Py_Scream_EE.Rotamer_match_bb(*args)
    def match_CB(*args): return _Py_Scream_EE.Rotamer_match_CB(*args)
    def assign_atom_fftype(*args): return _Py_Scream_EE.Rotamer_assign_atom_fftype(*args)
    def assign_charges(*args): return _Py_Scream_EE.Rotamer_assign_charges(*args)
    def assign_lone_pair(*args): return _Py_Scream_EE.Rotamer_assign_lone_pair(*args)
    def declaredInRotlibScope(*args): return _Py_Scream_EE.Rotamer_declaredInRotlibScope(*args)
    def setDeclaredInRotlibScope(*args): return _Py_Scream_EE.Rotamer_setDeclaredInRotlibScope(*args)

class RotamerPtr(Rotamer):
    def __init__(self, this):
        _swig_setattr(self, Rotamer, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, Rotamer, 'thisown', 0)
        _swig_setattr(self, Rotamer,self.__class__,Rotamer)
_Py_Scream_EE.Rotamer_swigregister(RotamerPtr)

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
        _swig_setattr(self, AARotamer, 'this', _Py_Scream_EE.new_AARotamer(*args))
        _swig_setattr(self, AARotamer, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_AARotamer):
        try:
            if self.thisown: destroy(self)
        except: pass

    def deepcopy(*args): return _Py_Scream_EE.AARotamer_deepcopy(*args)
    def get_resName(*args): return _Py_Scream_EE.AARotamer_get_resName(*args)
    def set_resName(*args): return _Py_Scream_EE.AARotamer_set_resName(*args)
    def initRotamerAtomList(*args): return _Py_Scream_EE.AARotamer_initRotamerAtomList(*args)
    def calc_PHI(*args): return _Py_Scream_EE.AARotamer_calc_PHI(*args)
    def calc_PSI(*args): return _Py_Scream_EE.AARotamer_calc_PSI(*args)
    def get_PHI(*args): return _Py_Scream_EE.AARotamer_get_PHI(*args)
    def get_PSI(*args): return _Py_Scream_EE.AARotamer_get_PSI(*args)
    def chi1(*args): return _Py_Scream_EE.AARotamer_chi1(*args)
    def chi2(*args): return _Py_Scream_EE.AARotamer_chi2(*args)
    def chi3(*args): return _Py_Scream_EE.AARotamer_chi3(*args)
    def chi4(*args): return _Py_Scream_EE.AARotamer_chi4(*args)
    def chi5(*args): return _Py_Scream_EE.AARotamer_chi5(*args)
    def match_bb(*args): return _Py_Scream_EE.AARotamer_match_bb(*args)
    def match_CB(*args): return _Py_Scream_EE.AARotamer_match_CB(*args)
    def create_CB(*args): return _Py_Scream_EE.AARotamer_create_CB(*args)
    def assign_atom_fftype(*args): return _Py_Scream_EE.AARotamer_assign_atom_fftype(*args)
    def assign_charges(*args): return _Py_Scream_EE.AARotamer_assign_charges(*args)
    def assign_lone_pair(*args): return _Py_Scream_EE.AARotamer_assign_lone_pair(*args)
    def calc_C_i_minus_one(*args): return _Py_Scream_EE.AARotamer_calc_C_i_minus_one(*args)
    def center_CA(*args): return _Py_Scream_EE.AARotamer_center_CA(*args)
    def append_to_filehandle(*args): return _Py_Scream_EE.AARotamer_append_to_filehandle(*args)
    def pdb_append_to_filehandle(*args): return _Py_Scream_EE.AARotamer_pdb_append_to_filehandle(*args)
    def append_to_ostream_connect_info(*args): return _Py_Scream_EE.AARotamer_append_to_ostream_connect_info(*args)
    def print_Me(*args): return _Py_Scream_EE.AARotamer_print_Me(*args)
    def print_ordered_by_n(*args): return _Py_Scream_EE.AARotamer_print_ordered_by_n(*args)
    def get_bb(*args): return _Py_Scream_EE.AARotamer_get_bb(*args)
    def get_sc(*args): return _Py_Scream_EE.AARotamer_get_sc(*args)
    __swig_setmethods__["PHI"] = _Py_Scream_EE.AARotamer_PHI_set
    __swig_getmethods__["PHI"] = _Py_Scream_EE.AARotamer_PHI_get
    if _newclass:PHI = property(_Py_Scream_EE.AARotamer_PHI_get, _Py_Scream_EE.AARotamer_PHI_set)
    __swig_setmethods__["PSI"] = _Py_Scream_EE.AARotamer_PSI_set
    __swig_getmethods__["PSI"] = _Py_Scream_EE.AARotamer_PSI_get
    if _newclass:PSI = property(_Py_Scream_EE.AARotamer_PSI_get, _Py_Scream_EE.AARotamer_PSI_set)
    __swig_setmethods__["resName"] = _Py_Scream_EE.AARotamer_resName_set
    __swig_getmethods__["resName"] = _Py_Scream_EE.AARotamer_resName_get
    if _newclass:resName = property(_Py_Scream_EE.AARotamer_resName_get, _Py_Scream_EE.AARotamer_resName_set)
    def private_chi(*args): return _Py_Scream_EE.AARotamer_private_chi(*args)
    def _determine_and_fix_GLY_sidechain_HCA_issue(*args): return _Py_Scream_EE.AARotamer__determine_and_fix_GLY_sidechain_HCA_issue(*args)

class AARotamerPtr(AARotamer):
    def __init__(self, this):
        _swig_setattr(self, AARotamer, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, AARotamer, 'thisown', 0)
        _swig_setattr(self, AARotamer,self.__class__,AARotamer)
_Py_Scream_EE.AARotamer_swigregister(AARotamerPtr)

class Protein(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Protein, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Protein, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ Protein instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, Protein, 'this', _Py_Scream_EE.new_Protein(*args))
        _swig_setattr(self, Protein, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_Protein):
        try:
            if self.thisown: destroy(self)
        except: pass

    def get_AAChain(*args): return _Py_Scream_EE.Protein_get_AAChain(*args)
    def get_Ligand(*args): return _Py_Scream_EE.Protein_get_Ligand(*args)
    def get_Component_with_ChainName(*args): return _Py_Scream_EE.Protein_get_Component_with_ChainName(*args)
    def get_res_type(*args): return _Py_Scream_EE.Protein_get_res_type(*args)
    def get_sc_atoms(*args): return _Py_Scream_EE.Protein_get_sc_atoms(*args)
    def get_variable_atoms(*args): return _Py_Scream_EE.Protein_get_variable_atoms(*args)
    def get_visible_in_EL_mutInfo_atoms(*args): return _Py_Scream_EE.Protein_get_visible_in_EL_mutInfo_atoms(*args)
    def getAtomList(*args): return _Py_Scream_EE.Protein_getAtomList(*args)
    def getNewAtomList(*args): return _Py_Scream_EE.Protein_getNewAtomList(*args)
    def getAtom(*args): return _Py_Scream_EE.Protein_getAtom(*args)
    def getTheseAtoms(*args): return _Py_Scream_EE.Protein_getTheseAtoms(*args)
    def addHydrogens(*args): return _Py_Scream_EE.Protein_addHydrogens(*args)
    def addConnectivity(*args): return _Py_Scream_EE.Protein_addConnectivity(*args)
    def assignFFType(*args): return _Py_Scream_EE.Protein_assignFFType(*args)
    def residuesAroundAtomN(*args): return _Py_Scream_EE.Protein_residuesAroundAtomN(*args)
    def residuesAroundResidue(*args): return _Py_Scream_EE.Protein_residuesAroundResidue(*args)
    def residuesAroundChain(*args): return _Py_Scream_EE.Protein_residuesAroundChain(*args)
    def residuesAroundAtom(*args): return _Py_Scream_EE.Protein_residuesAroundAtom(*args)
    def totalComponents(*args): return _Py_Scream_EE.Protein_totalComponents(*args)
    def mutationDone(*args): return _Py_Scream_EE.Protein_mutationDone(*args)
    def setMutInfoStrainEnergy(*args): return _Py_Scream_EE.Protein_setMutInfoStrainEnergy(*args)
    def getMutInfoStrainEnergy(*args): return _Py_Scream_EE.Protein_getMutInfoStrainEnergy(*args)
    def printAtomFlagStates(*args): return _Py_Scream_EE.Protein_printAtomFlagStates(*args)
    def getPlacementMethod(*args): return _Py_Scream_EE.Protein_getPlacementMethod(*args)
    def setPlacementMethod(*args): return _Py_Scream_EE.Protein_setPlacementMethod(*args)
    def getOffBisectorAngle(*args): return _Py_Scream_EE.Protein_getOffBisectorAngle(*args)
    def getOffPlaneAngle(*args): return _Py_Scream_EE.Protein_getOffPlaneAngle(*args)
    def getBondLength(*args): return _Py_Scream_EE.Protein_getBondLength(*args)
    def getRotamerMatchVectorLamdba(*args): return _Py_Scream_EE.Protein_getRotamerMatchVectorLamdba(*args)
    def setOffBisectorAngle(*args): return _Py_Scream_EE.Protein_setOffBisectorAngle(*args)
    def setOffPlaneAngle(*args): return _Py_Scream_EE.Protein_setOffPlaneAngle(*args)
    def setBondLength(*args): return _Py_Scream_EE.Protein_setBondLength(*args)
    def setRotamerMatchVectorLamdba(*args): return _Py_Scream_EE.Protein_setRotamerMatchVectorLamdba(*args)
    def ntrlRotamerPlacement(*args): return _Py_Scream_EE.Protein_ntrlRotamerPlacement(*args)
    def getAARotamer(*args): return _Py_Scream_EE.Protein_getAARotamer(*args)
    def conformerPlacement(*args): return _Py_Scream_EE.Protein_conformerPlacement(*args)
    def conformerExtraction(*args): return _Py_Scream_EE.Protein_conformerExtraction(*args)
    def rotamerClusterPlacement(*args): return _Py_Scream_EE.Protein_rotamerClusterPlacement(*args)
    def setRotamerClusterEmptyLatticeEnergy(*args): return _Py_Scream_EE.Protein_setRotamerClusterEmptyLatticeEnergy(*args)
    def getRotamerClusterEmptyLatticeEnergy(*args): return _Py_Scream_EE.Protein_getRotamerClusterEmptyLatticeEnergy(*args)
    def mutation(*args): return _Py_Scream_EE.Protein_mutation(*args)
    def setPreCalcEnergy(*args): return _Py_Scream_EE.Protein_setPreCalcEnergy(*args)
    def getPreCalcEnergy(*args): return _Py_Scream_EE.Protein_getPreCalcEnergy(*args)
    def setEmptyLatticeEnergy(*args): return _Py_Scream_EE.Protein_setEmptyLatticeEnergy(*args)
    def getEmptyLatticeEnergy(*args): return _Py_Scream_EE.Protein_getEmptyLatticeEnergy(*args)
    def setSideChainLibraryName(*args): return _Py_Scream_EE.Protein_setSideChainLibraryName(*args)
    def setProteinLibraryName(*args): return _Py_Scream_EE.Protein_setProteinLibraryName(*args)
    def resetFlags(*args): return _Py_Scream_EE.Protein_resetFlags(*args)
    def getNewMapping(*args): return _Py_Scream_EE.Protein_getNewMapping(*args)
    def sc_clash(*args): return _Py_Scream_EE.Protein_sc_clash(*args)
    def conformer_clash(*args): return _Py_Scream_EE.Protein_conformer_clash(*args)
    def sc_CRMS(*args): return _Py_Scream_EE.Protein_sc_CRMS(*args)
    def conformer_CRMS(*args): return _Py_Scream_EE.Protein_conformer_CRMS(*args)
    def max_atom_dist_on_SC(*args): return _Py_Scream_EE.Protein_max_atom_dist_on_SC(*args)
    def sc_atom_CRMS(*args): return _Py_Scream_EE.Protein_sc_atom_CRMS(*args)
    def fix_entire_atom_list_ordering(*args): return _Py_Scream_EE.Protein_fix_entire_atom_list_ordering(*args)
    def fix_toggle(*args): return _Py_Scream_EE.Protein_fix_toggle(*args)
    def fix_sc_toggle(*args): return _Py_Scream_EE.Protein_fix_sc_toggle(*args)
    def append_to_filehandle(*args): return _Py_Scream_EE.Protein_append_to_filehandle(*args)
    def pdb_append_to_filehandle(*args): return _Py_Scream_EE.Protein_pdb_append_to_filehandle(*args)
    def print_bgf_file(*args): return _Py_Scream_EE.Protein_print_bgf_file(*args)
    def print_Me(*args): return _Py_Scream_EE.Protein_print_Me(*args)
    def print_ordered_by_n(*args): return _Py_Scream_EE.Protein_print_ordered_by_n(*args)

class ProteinPtr(Protein):
    def __init__(self, this):
        _swig_setattr(self, Protein, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, Protein, 'thisown', 0)
        _swig_setattr(self, Protein,self.__class__,Protein)
_Py_Scream_EE.Protein_swigregister(ProteinPtr)

class Rotlib(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Rotlib, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Rotlib, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ Rotlib instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, Rotlib, 'this', _Py_Scream_EE.new_Rotlib(*args))
        _swig_setattr(self, Rotlib, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_Rotlib):
        try:
            if self.thisown: destroy(self)
        except: pass

    def readConnectivityFile(*args): return _Py_Scream_EE.Rotlib_readConnectivityFile(*args)
    def readRotamerLibrary(*args): return _Py_Scream_EE.Rotlib_readRotamerLibrary(*args)
    def get_library_name(*args): return _Py_Scream_EE.Rotlib_get_library_name(*args)
    def getRotConnInfo(*args): return _Py_Scream_EE.Rotlib_getRotConnInfo(*args)
    def get_next_rot(*args): return _Py_Scream_EE.Rotlib_get_next_rot(*args)
    def get_current_rot(*args): return _Py_Scream_EE.Rotlib_get_current_rot(*args)
    def get_next_rot_with_empty_lattice_E_below(*args): return _Py_Scream_EE.Rotlib_get_next_rot_with_empty_lattice_E_below(*args)
    def get_empty_lattice_E_rot(*args): return _Py_Scream_EE.Rotlib_get_empty_lattice_E_rot(*args)
    def get_empty_lattice_E_rot_after_sorted_by_empty_lattice_E(*args): return _Py_Scream_EE.Rotlib_get_empty_lattice_E_rot_after_sorted_by_empty_lattice_E(*args)
    def reset_pstn(*args): return _Py_Scream_EE.Rotlib_reset_pstn(*args)
    def size(*args): return _Py_Scream_EE.Rotlib_size(*args)
    def n_rotamers_below_empty_lattice_energy(*args): return _Py_Scream_EE.Rotlib_n_rotamers_below_empty_lattice_energy(*args)
    def add_rotamer(*args): return _Py_Scream_EE.Rotlib_add_rotamer(*args)
    def new_rotamer(*args): return _Py_Scream_EE.Rotlib_new_rotamer(*args)
    def new_rotamer_cluster(*args): return _Py_Scream_EE.Rotlib_new_rotamer_cluster(*args)
    def print_Me(*args): return _Py_Scream_EE.Rotlib_print_Me(*args)
    def print_to_file(*args): return _Py_Scream_EE.Rotlib_print_to_file(*args)
    def sort_by_rotlib_E(*args): return _Py_Scream_EE.Rotlib_sort_by_rotlib_E(*args)
    def sort_by_self_E(*args): return _Py_Scream_EE.Rotlib_sort_by_self_E(*args)
    def sort_by_empty_lattice_E(*args): return _Py_Scream_EE.Rotlib_sort_by_empty_lattice_E(*args)
    def get_best_preCalc_E(*args): return _Py_Scream_EE.Rotlib_get_best_preCalc_E(*args)

class RotlibPtr(Rotlib):
    def __init__(self, this):
        _swig_setattr(self, Rotlib, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, Rotlib, 'thisown', 0)
        _swig_setattr(self, Rotlib,self.__class__,Rotlib)
_Py_Scream_EE.Rotlib_swigregister(RotlibPtr)

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
        _swig_setattr(self, AARotlib, 'this', _Py_Scream_EE.new_AARotlib(*args))
        _swig_setattr(self, AARotlib, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_AARotlib):
        try:
            if self.thisown: destroy(self)
        except: pass

    def get_next_rot(*args): return _Py_Scream_EE.AARotlib_get_next_rot(*args)
    def get_current_rot(*args): return _Py_Scream_EE.AARotlib_get_current_rot(*args)
    def get_rot(*args): return _Py_Scream_EE.AARotlib_get_rot(*args)
    def reset_rot_pstn(*args): return _Py_Scream_EE.AARotlib_reset_rot_pstn(*args)
    def set_rot_pstn(*args): return _Py_Scream_EE.AARotlib_set_rot_pstn(*args)
    def get_next_rot_with_empty_lattice_E_below(*args): return _Py_Scream_EE.AARotlib_get_next_rot_with_empty_lattice_E_below(*args)
    def get_empty_lattice_E_rot(*args): return _Py_Scream_EE.AARotlib_get_empty_lattice_E_rot(*args)
    def center_CA(*args): return _Py_Scream_EE.AARotlib_center_CA(*args)
    def calc_all_PHI(*args): return _Py_Scream_EE.AARotlib_calc_all_PHI(*args)
    def calc_all_PSI(*args): return _Py_Scream_EE.AARotlib_calc_all_PSI(*args)
    __swig_setmethods__["resName"] = _Py_Scream_EE.AARotlib_resName_set
    __swig_getmethods__["resName"] = _Py_Scream_EE.AARotlib_resName_get
    if _newclass:resName = property(_Py_Scream_EE.AARotlib_resName_get, _Py_Scream_EE.AARotlib_resName_set)

class AARotlibPtr(AARotlib):
    def __init__(self, this):
        _swig_setattr(self, AARotlib, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, AARotlib, 'thisown', 0)
        _swig_setattr(self, AARotlib,self.__class__,AARotlib)
_Py_Scream_EE.AARotlib_swigregister(AARotlibPtr)

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
        _swig_setattr(self, NtrlAARotlib, 'this', _Py_Scream_EE.new_NtrlAARotlib(*args))
        _swig_setattr(self, NtrlAARotlib, 'thisown', 1)
    def setup_library(*args): return _Py_Scream_EE.NtrlAARotlib_setup_library(*args)
    def __del__(self, destroy=_Py_Scream_EE.delete_NtrlAARotlib):
        try:
            if self.thisown: destroy(self)
        except: pass

    def assign_atom_fftype(*args): return _Py_Scream_EE.NtrlAARotlib_assign_atom_fftype(*args)
    def assign_charges(*args): return _Py_Scream_EE.NtrlAARotlib_assign_charges(*args)
    def assign_lone_pair(*args): return _Py_Scream_EE.NtrlAARotlib_assign_lone_pair(*args)
    def append_to_filehandle(*args): return _Py_Scream_EE.NtrlAARotlib_append_to_filehandle(*args)

class NtrlAARotlibPtr(NtrlAARotlib):
    def __init__(self, this):
        _swig_setattr(self, NtrlAARotlib, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, NtrlAARotlib, 'thisown', 0)
        _swig_setattr(self, NtrlAARotlib,self.__class__,NtrlAARotlib)
_Py_Scream_EE.NtrlAARotlib_swigregister(NtrlAARotlibPtr)

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
        _swig_setattr(self, Multiple_NtrlAARotlib, 'this', _Py_Scream_EE.new_Multiple_NtrlAARotlib(*args))
        _swig_setattr(self, Multiple_NtrlAARotlib, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_Multiple_NtrlAARotlib):
        try:
            if self.thisown: destroy(self)
        except: pass

    def getRotConnInfo(*args): return _Py_Scream_EE.Multiple_NtrlAARotlib_getRotConnInfo(*args)
    def add_library(*args): return _Py_Scream_EE.Multiple_NtrlAARotlib_add_library(*args)

class Multiple_NtrlAARotlibPtr(Multiple_NtrlAARotlib):
    def __init__(self, this):
        _swig_setattr(self, Multiple_NtrlAARotlib, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, Multiple_NtrlAARotlib, 'thisown', 0)
        _swig_setattr(self, Multiple_NtrlAARotlib,self.__class__,Multiple_NtrlAARotlib)
_Py_Scream_EE.Multiple_NtrlAARotlib_swigregister(Multiple_NtrlAARotlibPtr)

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
        _swig_setattr(self, HIS_NtrlAARotlib, 'this', _Py_Scream_EE.new_HIS_NtrlAARotlib(*args))
        _swig_setattr(self, HIS_NtrlAARotlib, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_HIS_NtrlAARotlib):
        try:
            if self.thisown: destroy(self)
        except: pass

    def add_rotamer(*args): return _Py_Scream_EE.HIS_NtrlAARotlib_add_rotamer(*args)

class HIS_NtrlAARotlibPtr(HIS_NtrlAARotlib):
    def __init__(self, this):
        _swig_setattr(self, HIS_NtrlAARotlib, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, HIS_NtrlAARotlib, 'thisown', 0)
        _swig_setattr(self, HIS_NtrlAARotlib,self.__class__,HIS_NtrlAARotlib)
_Py_Scream_EE.HIS_NtrlAARotlib_swigregister(HIS_NtrlAARotlibPtr)

class RotlibCollection(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, RotlibCollection, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, RotlibCollection, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ RotlibCollection instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, RotlibCollection, 'this', _Py_Scream_EE.new_RotlibCollection(*args))
        _swig_setattr(self, RotlibCollection, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_RotlibCollection):
        try:
            if self.thisown: destroy(self)
        except: pass

    def addRotlib(*args): return _Py_Scream_EE.RotlibCollection_addRotlib(*args)
    def addClashCollection(*args): return _Py_Scream_EE.RotlibCollection_addClashCollection(*args)
    def initEmptyLatticeDataStructures(*args): return _Py_Scream_EE.RotlibCollection_initEmptyLatticeDataStructures(*args)
    def initDynamicMemoryDataStructures(*args): return _Py_Scream_EE.RotlibCollection_initDynamicMemoryDataStructures(*args)
    def initAllocationUnderEnergyThreshold(*args): return _Py_Scream_EE.RotlibCollection_initAllocationUnderEnergyThreshold(*args)
    def getNextRotamersByELEnergy(*args): return _Py_Scream_EE.RotlibCollection_getNextRotamersByELEnergy(*args)
    def resetEmptyLatticeCrntPstn(*args): return _Py_Scream_EE.RotlibCollection_resetEmptyLatticeCrntPstn(*args)
    def resetTotalEnergyCrntPstn(*args): return _Py_Scream_EE.RotlibCollection_resetTotalEnergyCrntPstn(*args)
    def getNextEmptyLatticeExcitationRotamers(*args): return _Py_Scream_EE.RotlibCollection_getNextEmptyLatticeExcitationRotamers(*args)
    def getNextTotalEnergyExcitationRotamers(*args): return _Py_Scream_EE.RotlibCollection_getNextTotalEnergyExcitationRotamers(*args)
    def getNthEmptyLatticeExcitationRotamers(*args): return _Py_Scream_EE.RotlibCollection_getNthEmptyLatticeExcitationRotamers(*args)
    def getELExcitedRotamerFromEnumeration(*args): return _Py_Scream_EE.RotlibCollection_getELExcitedRotamerFromEnumeration(*args)
    def getELExcitedRotamer_nFromEnumeration_n(*args): return _Py_Scream_EE.RotlibCollection_getELExcitedRotamer_nFromEnumeration_n(*args)
    def getELEnumerationFromExcitedRotamer(*args): return _Py_Scream_EE.RotlibCollection_getELEnumerationFromExcitedRotamer(*args)
    def getELEnumeration_nFromExcitedRotamer_n(*args): return _Py_Scream_EE.RotlibCollection_getELEnumeration_nFromExcitedRotamer_n(*args)
    def _ExcitationEnumerationToExcitationEnumeration_n(*args): return _Py_Scream_EE.RotlibCollection__ExcitationEnumerationToExcitationEnumeration_n(*args)
    def _ExcitedRotamers_nToExcitedRotamers(*args): return _Py_Scream_EE.RotlibCollection__ExcitedRotamers_nToExcitedRotamers(*args)
    def getClashCollection(*args): return _Py_Scream_EE.RotlibCollection_getClashCollection(*args)
    def cleanClashCollection(*args): return _Py_Scream_EE.RotlibCollection_cleanClashCollection(*args)
    def getMutInfoRotlibMap(*args): return _Py_Scream_EE.RotlibCollection_getMutInfoRotlibMap(*args)
    def getMutInfoRotlibDict(*args): return _Py_Scream_EE.RotlibCollection_getMutInfoRotlibDict(*args)
    def getNextDynamicMemoryRotamers_And_Expand(*args): return _Py_Scream_EE.RotlibCollection_getNextDynamicMemoryRotamers_And_Expand(*args)
    def getNextDynamicClashEliminatedRotamers_And_Expand(*args): return _Py_Scream_EE.RotlibCollection_getNextDynamicClashEliminatedRotamers_And_Expand(*args)
    def increaseConfigurationsUnderEnergyThreshold(*args): return _Py_Scream_EE.RotlibCollection_increaseConfigurationsUnderEnergyThreshold(*args)
    def getNextUnderEnergyThresholdRotamers(*args): return _Py_Scream_EE.RotlibCollection_getNextUnderEnergyThresholdRotamers(*args)
    def setExcitationEnergy(*args): return _Py_Scream_EE.RotlibCollection_setExcitationEnergy(*args)
    def getExcitationEnergy(*args): return _Py_Scream_EE.RotlibCollection_getExcitationEnergy(*args)
    def printEmptyLatticeLinearEnergyTable(*args): return _Py_Scream_EE.RotlibCollection_printEmptyLatticeLinearEnergyTable(*args)
    def printExcitationEnergyTable(*args): return _Py_Scream_EE.RotlibCollection_printExcitationEnergyTable(*args)
    def printEmptyLatticeTable(*args): return _Py_Scream_EE.RotlibCollection_printEmptyLatticeTable(*args)
    def getInitMethod(*args): return _Py_Scream_EE.RotlibCollection_getInitMethod(*args)
    def sizeOfSystem(*args): return _Py_Scream_EE.RotlibCollection_sizeOfSystem(*args)
    def getHighestAllowedRotamerE(*args): return _Py_Scream_EE.RotlibCollection_getHighestAllowedRotamerE(*args)
    def setHighestAllowedRotamerE(*args): return _Py_Scream_EE.RotlibCollection_setHighestAllowedRotamerE(*args)
    __swig_setmethods__["maxRotamerConfigurations"] = _Py_Scream_EE.RotlibCollection_maxRotamerConfigurations_set
    __swig_getmethods__["maxRotamerConfigurations"] = _Py_Scream_EE.RotlibCollection_maxRotamerConfigurations_get
    if _newclass:maxRotamerConfigurations = property(_Py_Scream_EE.RotlibCollection_maxRotamerConfigurations_get, _Py_Scream_EE.RotlibCollection_maxRotamerConfigurations_set)
    def cmpMaxRotamerConfigurations(*args): return _Py_Scream_EE.RotlibCollection_cmpMaxRotamerConfigurations(*args)

class RotlibCollectionPtr(RotlibCollection):
    def __init__(self, this):
        _swig_setattr(self, RotlibCollection, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, RotlibCollection, 'thisown', 0)
        _swig_setattr(self, RotlibCollection,self.__class__,RotlibCollection)
_Py_Scream_EE.RotlibCollection_swigregister(RotlibCollectionPtr)

class ClashCollection(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ClashCollection, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ClashCollection, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ ClashCollection instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, ClashCollection, 'this', _Py_Scream_EE.new_ClashCollection(*args))
        _swig_setattr(self, ClashCollection, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_ClashCollection):
        try:
            if self.thisown: destroy(self)
        except: pass

    def setThresholdE(*args): return _Py_Scream_EE.ClashCollection_setThresholdE(*args)
    def addClashPair(*args): return _Py_Scream_EE.ClashCollection_addClashPair(*args)
    def checkClash(*args): return _Py_Scream_EE.ClashCollection_checkClash(*args)
    def getThresholdE(*args): return _Py_Scream_EE.ClashCollection_getThresholdE(*args)
    def getNumberOfClashes(*args): return _Py_Scream_EE.ClashCollection_getNumberOfClashes(*args)
    def storeCurrentRotamerConfiguration(*args): return _Py_Scream_EE.ClashCollection_storeCurrentRotamerConfiguration(*args)
    def increment_total_clashing_rotamers_eliminated(*args): return _Py_Scream_EE.ClashCollection_increment_total_clashing_rotamers_eliminated(*args)
    def set_total_clashing_rotamers_eliminated(*args): return _Py_Scream_EE.ClashCollection_set_total_clashing_rotamers_eliminated(*args)
    def get_total_clashing_rotamers_eliminated(*args): return _Py_Scream_EE.ClashCollection_get_total_clashing_rotamers_eliminated(*args)
    def getClashList(*args): return _Py_Scream_EE.ClashCollection_getClashList(*args)
    def getDiscreteClashPairList(*args): return _Py_Scream_EE.ClashCollection_getDiscreteClashPairList(*args)

class ClashCollectionPtr(ClashCollection):
    def __init__(self, this):
        _swig_setattr(self, ClashCollection, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ClashCollection, 'thisown', 0)
        _swig_setattr(self, ClashCollection,self.__class__,ClashCollection)
_Py_Scream_EE.ClashCollection_swigregister(ClashCollectionPtr)

class RotamerNeighborList(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, RotamerNeighborList, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, RotamerNeighborList, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ RotamerNeighborList instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, RotamerNeighborList, 'this', _Py_Scream_EE.new_RotamerNeighborList(*args))
        _swig_setattr(self, RotamerNeighborList, 'thisown', 1)
    def setCutoff(*args): return _Py_Scream_EE.RotamerNeighborList_setCutoff(*args)
    def getCutoff(*args): return _Py_Scream_EE.RotamerNeighborList_getCutoff(*args)
    def setProtein(*args): return _Py_Scream_EE.RotamerNeighborList_setProtein(*args)
    def getProtein(*args): return _Py_Scream_EE.RotamerNeighborList_getProtein(*args)
    def addMutInfoRotConnInfo(*args): return _Py_Scream_EE.RotamerNeighborList_addMutInfoRotConnInfo(*args)
    def initRotamerNeighborList(*args): return _Py_Scream_EE.RotamerNeighborList_initRotamerNeighborList(*args)
    def returnEmptyLatticeNeighborList(*args): return _Py_Scream_EE.RotamerNeighborList_returnEmptyLatticeNeighborList(*args)
    def __del__(self, destroy=_Py_Scream_EE.delete_RotamerNeighborList):
        try:
            if self.thisown: destroy(self)
        except: pass


class RotamerNeighborListPtr(RotamerNeighborList):
    def __init__(self, this):
        _swig_setattr(self, RotamerNeighborList, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, RotamerNeighborList, 'thisown', 0)
        _swig_setattr(self, RotamerNeighborList,self.__class__,RotamerNeighborList)
_Py_Scream_EE.RotamerNeighborList_swigregister(RotamerNeighborListPtr)

class RotamerCluster(Rotamer):
    __swig_setmethods__ = {}
    for _s in [Rotamer]: __swig_setmethods__.update(_s.__swig_setmethods__)
    __setattr__ = lambda self, name, value: _swig_setattr(self, RotamerCluster, name, value)
    __swig_getmethods__ = {}
    for _s in [Rotamer]: __swig_getmethods__.update(_s.__swig_getmethods__)
    __getattr__ = lambda self, name: _swig_getattr(self, RotamerCluster, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ RotamerCluster instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, RotamerCluster, 'this', _Py_Scream_EE.new_RotamerCluster(*args))
        _swig_setattr(self, RotamerCluster, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_RotamerCluster):
        try:
            if self.thisown: destroy(self)
        except: pass

    def addRotamerCluster(*args): return _Py_Scream_EE.RotamerCluster_addRotamerCluster(*args)
    def getAllRotamers(*args): return _Py_Scream_EE.RotamerCluster_getAllRotamers(*args)
    def print_Me(*args): return _Py_Scream_EE.RotamerCluster_print_Me(*args)
    def append_to_filehandle(*args): return _Py_Scream_EE.RotamerCluster_append_to_filehandle(*args)
    def pdb_append_to_filehandle(*args): return _Py_Scream_EE.RotamerCluster_pdb_append_to_filehandle(*args)
    def append_to_ostream_connect_info(*args): return _Py_Scream_EE.RotamerCluster_append_to_ostream_connect_info(*args)
    def get_sc_atoms(*args): return _Py_Scream_EE.RotamerCluster_get_sc_atoms(*args)
    def get_bb_atoms(*args): return _Py_Scream_EE.RotamerCluster_get_bb_atoms(*args)

class RotamerClusterPtr(RotamerCluster):
    def __init__(self, this):
        _swig_setattr(self, RotamerCluster, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, RotamerCluster, 'thisown', 0)
        _swig_setattr(self, RotamerCluster,self.__class__,RotamerCluster)
_Py_Scream_EE.RotamerCluster_swigregister(RotamerClusterPtr)

class RotConnInfo(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, RotConnInfo, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, RotConnInfo, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ RotConnInfo instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    __swig_setmethods__["targetRotamerLibFile"] = _Py_Scream_EE.RotConnInfo_targetRotamerLibFile_set
    __swig_getmethods__["targetRotamerLibFile"] = _Py_Scream_EE.RotConnInfo_targetRotamerLibFile_get
    if _newclass:targetRotamerLibFile = property(_Py_Scream_EE.RotConnInfo_targetRotamerLibFile_get, _Py_Scream_EE.RotConnInfo_targetRotamerLibFile_set)
    __swig_setmethods__["anchor_pts"] = _Py_Scream_EE.RotConnInfo_anchor_pts_set
    __swig_getmethods__["anchor_pts"] = _Py_Scream_EE.RotConnInfo_anchor_pts_get
    if _newclass:anchor_pts = property(_Py_Scream_EE.RotConnInfo_anchor_pts_get, _Py_Scream_EE.RotConnInfo_anchor_pts_set)
    __swig_setmethods__["atoms_of_exact_match"] = _Py_Scream_EE.RotConnInfo_atoms_of_exact_match_set
    __swig_getmethods__["atoms_of_exact_match"] = _Py_Scream_EE.RotConnInfo_atoms_of_exact_match_get
    if _newclass:atoms_of_exact_match = property(_Py_Scream_EE.RotConnInfo_atoms_of_exact_match_get, _Py_Scream_EE.RotConnInfo_atoms_of_exact_match_set)
    __swig_setmethods__["atom_n_map"] = _Py_Scream_EE.RotConnInfo_atom_n_map_set
    __swig_getmethods__["atom_n_map"] = _Py_Scream_EE.RotConnInfo_atom_n_map_get
    if _newclass:atom_n_map = property(_Py_Scream_EE.RotConnInfo_atom_n_map_get, _Py_Scream_EE.RotConnInfo_atom_n_map_set)
    __swig_setmethods__["atom_n_label_map"] = _Py_Scream_EE.RotConnInfo_atom_n_label_map_set
    __swig_getmethods__["atom_n_label_map"] = _Py_Scream_EE.RotConnInfo_atom_n_label_map_get
    if _newclass:atom_n_label_map = property(_Py_Scream_EE.RotConnInfo_atom_n_label_map_get, _Py_Scream_EE.RotConnInfo_atom_n_label_map_set)
    __swig_setmethods__["side_chain_atoms"] = _Py_Scream_EE.RotConnInfo_side_chain_atoms_set
    __swig_getmethods__["side_chain_atoms"] = _Py_Scream_EE.RotConnInfo_side_chain_atoms_get
    if _newclass:side_chain_atoms = property(_Py_Scream_EE.RotConnInfo_side_chain_atoms_get, _Py_Scream_EE.RotConnInfo_side_chain_atoms_set)
    __swig_setmethods__["atom_connectivity_info"] = _Py_Scream_EE.RotConnInfo_atom_connectivity_info_set
    __swig_getmethods__["atom_connectivity_info"] = _Py_Scream_EE.RotConnInfo_atom_connectivity_info_get
    if _newclass:atom_connectivity_info = property(_Py_Scream_EE.RotConnInfo_atom_connectivity_info_get, _Py_Scream_EE.RotConnInfo_atom_connectivity_info_set)
    __swig_setmethods__["connection_point_atoms"] = _Py_Scream_EE.RotConnInfo_connection_point_atoms_set
    __swig_getmethods__["connection_point_atoms"] = _Py_Scream_EE.RotConnInfo_connection_point_atoms_get
    if _newclass:connection_point_atoms = property(_Py_Scream_EE.RotConnInfo_connection_point_atoms_get, _Py_Scream_EE.RotConnInfo_connection_point_atoms_set)
    def modifyMappingInProteinAtoms(*args): return _Py_Scream_EE.RotConnInfo_modifyMappingInProteinAtoms(*args)
    def clear(*args): return _Py_Scream_EE.RotConnInfo_clear(*args)
    def __init__(self, *args):
        _swig_setattr(self, RotConnInfo, 'this', _Py_Scream_EE.new_RotConnInfo(*args))
        _swig_setattr(self, RotConnInfo, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_RotConnInfo):
        try:
            if self.thisown: destroy(self)
        except: pass


class RotConnInfoPtr(RotConnInfo):
    def __init__(self, this):
        _swig_setattr(self, RotConnInfo, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, RotConnInfo, 'thisown', 0)
        _swig_setattr(self, RotConnInfo,self.__class__,RotConnInfo)
_Py_Scream_EE.RotConnInfo_swigregister(RotConnInfoPtr)

class bgf_handler(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, bgf_handler, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, bgf_handler, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ bgf_handler instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, bgf_handler, 'this', _Py_Scream_EE.new_bgf_handler(*args))
        _swig_setattr(self, bgf_handler, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_bgf_handler):
        try:
            if self.thisown: destroy(self)
        except: pass

    def readfile(*args): return _Py_Scream_EE.bgf_handler_readfile(*args)
    def readPDB(*args): return _Py_Scream_EE.bgf_handler_readPDB(*args)
    def printToFile(*args): return _Py_Scream_EE.bgf_handler_printToFile(*args)
    def printfile(*args): return _Py_Scream_EE.bgf_handler_printfile(*args)
    def printPDB(*args): return _Py_Scream_EE.bgf_handler_printPDB(*args)
    def printToPDB(*args): return _Py_Scream_EE.bgf_handler_printToPDB(*args)
    def printSequenceToFile(*args): return _Py_Scream_EE.bgf_handler_printSequenceToFile(*args)
    def returnSequence(*args): return _Py_Scream_EE.bgf_handler_returnSequence(*args)
    __swig_getmethods__["printSequence"] = lambda x: _Py_Scream_EE.bgf_handler_printSequence
    if _newclass:printSequence = staticmethod(_Py_Scream_EE.bgf_handler_printSequence)
    def pass_atomlist(*args): return _Py_Scream_EE.bgf_handler_pass_atomlist(*args)
    def getAtomList(*args): return _Py_Scream_EE.bgf_handler_getAtomList(*args)
    __swig_setmethods__["atom_list"] = _Py_Scream_EE.bgf_handler_atom_list_set
    __swig_getmethods__["atom_list"] = _Py_Scream_EE.bgf_handler_atom_list_get
    if _newclass:atom_list = property(_Py_Scream_EE.bgf_handler_atom_list_get, _Py_Scream_EE.bgf_handler_atom_list_set)
    __swig_setmethods__["header_lines"] = _Py_Scream_EE.bgf_handler_header_lines_set
    __swig_getmethods__["header_lines"] = _Py_Scream_EE.bgf_handler_header_lines_get
    if _newclass:header_lines = property(_Py_Scream_EE.bgf_handler_header_lines_get, _Py_Scream_EE.bgf_handler_header_lines_set)
    __swig_setmethods__["atom_lines"] = _Py_Scream_EE.bgf_handler_atom_lines_set
    __swig_getmethods__["atom_lines"] = _Py_Scream_EE.bgf_handler_atom_lines_get
    if _newclass:atom_lines = property(_Py_Scream_EE.bgf_handler_atom_lines_get, _Py_Scream_EE.bgf_handler_atom_lines_set)
    __swig_setmethods__["conect_format_lines"] = _Py_Scream_EE.bgf_handler_conect_format_lines_set
    __swig_getmethods__["conect_format_lines"] = _Py_Scream_EE.bgf_handler_conect_format_lines_get
    if _newclass:conect_format_lines = property(_Py_Scream_EE.bgf_handler_conect_format_lines_get, _Py_Scream_EE.bgf_handler_conect_format_lines_set)
    __swig_setmethods__["connectivity_record_lines"] = _Py_Scream_EE.bgf_handler_connectivity_record_lines_set
    __swig_getmethods__["connectivity_record_lines"] = _Py_Scream_EE.bgf_handler_connectivity_record_lines_get
    if _newclass:connectivity_record_lines = property(_Py_Scream_EE.bgf_handler_connectivity_record_lines_get, _Py_Scream_EE.bgf_handler_connectivity_record_lines_set)

class bgf_handlerPtr(bgf_handler):
    def __init__(self, this):
        _swig_setattr(self, bgf_handler, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, bgf_handler, 'thisown', 0)
        _swig_setattr(self, bgf_handler,self.__class__,bgf_handler)
_Py_Scream_EE.bgf_handler_swigregister(bgf_handlerPtr)

bgf_handler_printSequence = _Py_Scream_EE.bgf_handler_printSequence

class AminoAcid_RTF(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, AminoAcid_RTF, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, AminoAcid_RTF, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ AminoAcid_RTF instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, AminoAcid_RTF, 'this', _Py_Scream_EE.new_AminoAcid_RTF(*args))
        _swig_setattr(self, AminoAcid_RTF, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_AminoAcid_RTF):
        try:
            if self.thisown: destroy(self)
        except: pass

    def get_ff_type(*args): return _Py_Scream_EE.AminoAcid_RTF_get_ff_type(*args)
    def return_bonds_table(*args): return _Py_Scream_EE.AminoAcid_RTF_return_bonds_table(*args)

class AminoAcid_RTFPtr(AminoAcid_RTF):
    def __init__(self, this):
        _swig_setattr(self, AminoAcid_RTF, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, AminoAcid_RTF, 'thisown', 0)
        _swig_setattr(self, AminoAcid_RTF,self.__class__,AminoAcid_RTF)
_Py_Scream_EE.AminoAcid_RTF_swigregister(AminoAcid_RTFPtr)

class SCREAM_RTF(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SCREAM_RTF, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SCREAM_RTF, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ SCREAM_RTF instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, SCREAM_RTF, 'this', _Py_Scream_EE.new_SCREAM_RTF(*args))
        _swig_setattr(self, SCREAM_RTF, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_SCREAM_RTF):
        try:
            if self.thisown: destroy(self)
        except: pass

    def get_AminoAcid_RTF(*args): return _Py_Scream_EE.SCREAM_RTF_get_AminoAcid_RTF(*args)
    def get_ff_type(*args): return _Py_Scream_EE.SCREAM_RTF_get_ff_type(*args)

class SCREAM_RTFPtr(SCREAM_RTF):
    def __init__(self, this):
        _swig_setattr(self, SCREAM_RTF, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, SCREAM_RTF, 'thisown', 0)
        _swig_setattr(self, SCREAM_RTF,self.__class__,SCREAM_RTF)
_Py_Scream_EE.SCREAM_RTF_swigregister(SCREAM_RTFPtr)

class Scream_EE(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Scream_EE, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Scream_EE, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ Scream_EE instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, Scream_EE, 'this', _Py_Scream_EE.new_Scream_EE(*args))
        _swig_setattr(self, Scream_EE, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_Scream_EE):
        try:
            if self.thisown: destroy(self)
        except: pass

    def init(*args): return _Py_Scream_EE.Scream_EE_init(*args)
    def setCalcNonPolarHydrogen_flag(*args): return _Py_Scream_EE.Scream_EE_setCalcNonPolarHydrogen_flag(*args)
    def getCalcNonPolarHydrogen_flag(*args): return _Py_Scream_EE.Scream_EE_getCalcNonPolarHydrogen_flag(*args)
    def addMutInfoRotConnInfo(*args): return _Py_Scream_EE.Scream_EE_addMutInfoRotConnInfo(*args)
    def init_after_addedMutInfoRotConnInfo(*args): return _Py_Scream_EE.Scream_EE_init_after_addedMutInfoRotConnInfo(*args)
    def init_after_addedMutInfoRotConnInfo_on_the_fly_E(*args): return _Py_Scream_EE.Scream_EE_init_after_addedMutInfoRotConnInfo_on_the_fly_E(*args)
    def init_after_addedMutInfoRotConnInfo_neighbor_list(*args): return _Py_Scream_EE.Scream_EE_init_after_addedMutInfoRotConnInfo_neighbor_list(*args)
    def fix_mutInfo(*args): return _Py_Scream_EE.Scream_EE_fix_mutInfo(*args)
    def moveable_mutInfo(*args): return _Py_Scream_EE.Scream_EE_moveable_mutInfo(*args)
    def fix_all(*args): return _Py_Scream_EE.Scream_EE_fix_all(*args)
    def visible_mutInfo(*args): return _Py_Scream_EE.Scream_EE_visible_mutInfo(*args)
    def invisible_mutInfo(*args): return _Py_Scream_EE.Scream_EE_invisible_mutInfo(*args)
    def visible_EL_mutInfo(*args): return _Py_Scream_EE.Scream_EE_visible_EL_mutInfo(*args)
    def invisible_EL_mutInfo(*args): return _Py_Scream_EE.Scream_EE_invisible_EL_mutInfo(*args)
    def visible_all(*args): return _Py_Scream_EE.Scream_EE_visible_all(*args)
    def invisible_all(*args): return _Py_Scream_EE.Scream_EE_invisible_all(*args)
    def visible_EL_all(*args): return _Py_Scream_EE.Scream_EE_visible_EL_all(*args)
    def invisible_EL_all(*args): return _Py_Scream_EE.Scream_EE_invisible_EL_all(*args)
    def make_chain_invisible(*args): return _Py_Scream_EE.Scream_EE_make_chain_invisible(*args)
    def make_chain_EL_invisible(*args): return _Py_Scream_EE.Scream_EE_make_chain_EL_invisible(*args)
    def resetFlags(*args): return _Py_Scream_EE.Scream_EE_resetFlags(*args)
    def setup_variableAtomsOnEachSidechain(*args): return _Py_Scream_EE.Scream_EE_setup_variableAtomsOnEachSidechain(*args)
    def initScreamAtomDeltaValue(*args): return _Py_Scream_EE.Scream_EE_initScreamAtomDeltaValue(*args)
    def initScreamAtomVdwHbFields(*args): return _Py_Scream_EE.Scream_EE_initScreamAtomVdwHbFields(*args)
    def addClashCollection(*args): return _Py_Scream_EE.Scream_EE_addClashCollection(*args)
    def cleanClashCollection(*args): return _Py_Scream_EE.Scream_EE_cleanClashCollection(*args)
    def getDistanceDielectricPrefactor(*args): return _Py_Scream_EE.Scream_EE_getDistanceDielectricPrefactor(*args)
    def setDistanceDielectricPrefactor(*args): return _Py_Scream_EE.Scream_EE_setDistanceDielectricPrefactor(*args)
    def setNormalDielectric(*args): return _Py_Scream_EE.Scream_EE_setNormalDielectric(*args)
    def ntrlRotamerPlacement(*args): return _Py_Scream_EE.Scream_EE_ntrlRotamerPlacement(*args)
    __swig_setmethods__["coulomb_obj"] = _Py_Scream_EE.Scream_EE_coulomb_obj_set
    __swig_getmethods__["coulomb_obj"] = _Py_Scream_EE.Scream_EE_coulomb_obj_get
    if _newclass:coulomb_obj = property(_Py_Scream_EE.Scream_EE_coulomb_obj_get, _Py_Scream_EE.Scream_EE_coulomb_obj_set)
    __swig_setmethods__["vdw_obj"] = _Py_Scream_EE.Scream_EE_vdw_obj_set
    __swig_getmethods__["vdw_obj"] = _Py_Scream_EE.Scream_EE_vdw_obj_get
    if _newclass:vdw_obj = property(_Py_Scream_EE.Scream_EE_vdw_obj_get, _Py_Scream_EE.Scream_EE_vdw_obj_set)
    __swig_setmethods__["hb_obj"] = _Py_Scream_EE.Scream_EE_hb_obj_set
    __swig_getmethods__["hb_obj"] = _Py_Scream_EE.Scream_EE_hb_obj_get
    if _newclass:hb_obj = property(_Py_Scream_EE.Scream_EE_hb_obj_get, _Py_Scream_EE.Scream_EE_hb_obj_set)
    __swig_setmethods__["coulomb_EE"] = _Py_Scream_EE.Scream_EE_coulomb_EE_set
    __swig_getmethods__["coulomb_EE"] = _Py_Scream_EE.Scream_EE_coulomb_EE_get
    if _newclass:coulomb_EE = property(_Py_Scream_EE.Scream_EE_coulomb_EE_get, _Py_Scream_EE.Scream_EE_coulomb_EE_set)
    __swig_setmethods__["vdw_EE"] = _Py_Scream_EE.Scream_EE_vdw_EE_set
    __swig_getmethods__["vdw_EE"] = _Py_Scream_EE.Scream_EE_vdw_EE_get
    if _newclass:vdw_EE = property(_Py_Scream_EE.Scream_EE_vdw_EE_get, _Py_Scream_EE.Scream_EE_vdw_EE_set)
    __swig_setmethods__["hb_EE"] = _Py_Scream_EE.Scream_EE_hb_EE_set
    __swig_getmethods__["hb_EE"] = _Py_Scream_EE.Scream_EE_hb_EE_get
    if _newclass:hb_EE = property(_Py_Scream_EE.Scream_EE_hb_EE_get, _Py_Scream_EE.Scream_EE_hb_EE_set)
    __swig_setmethods__["vdw_hb_exclusion_EE"] = _Py_Scream_EE.Scream_EE_vdw_hb_exclusion_EE_set
    __swig_getmethods__["vdw_hb_exclusion_EE"] = _Py_Scream_EE.Scream_EE_vdw_hb_exclusion_EE_get
    if _newclass:vdw_hb_exclusion_EE = property(_Py_Scream_EE.Scream_EE_vdw_hb_exclusion_EE_get, _Py_Scream_EE.Scream_EE_vdw_hb_exclusion_EE_set)
    def calc_empty_lattice_E(*args): return _Py_Scream_EE.Scream_EE_calc_empty_lattice_E(*args)
    def calc_empty_lattice_E_full_delta(*args): return _Py_Scream_EE.Scream_EE_calc_empty_lattice_E_full_delta(*args)
    def calc_empty_lattice_E_flat_delta(*args): return _Py_Scream_EE.Scream_EE_calc_empty_lattice_E_flat_delta(*args)
    def calc_empty_lattice_E_scaled_inner_wall(*args): return _Py_Scream_EE.Scream_EE_calc_empty_lattice_E_scaled_inner_wall(*args)
    def calc_empty_lattice_coulomb_E_delta(*args): return _Py_Scream_EE.Scream_EE_calc_empty_lattice_coulomb_E_delta(*args)
    def calc_empty_lattice_vdw_E_delta(*args): return _Py_Scream_EE.Scream_EE_calc_empty_lattice_vdw_E_delta(*args)
    def calc_empty_lattice_hb_E_delta(*args): return _Py_Scream_EE.Scream_EE_calc_empty_lattice_hb_E_delta(*args)
    def calc_empty_lattice_vdw_hb_exclusion_E_delta(*args): return _Py_Scream_EE.Scream_EE_calc_empty_lattice_vdw_hb_exclusion_E_delta(*args)
    def calc_EL_vdw_rot_selfBB(*args): return _Py_Scream_EE.Scream_EE_calc_EL_vdw_rot_selfBB(*args)
    def calc_EL_vdw_rot_otherBB(*args): return _Py_Scream_EE.Scream_EE_calc_EL_vdw_rot_otherBB(*args)
    def calc_EL_vdw_rot_fixedSC(*args): return _Py_Scream_EE.Scream_EE_calc_EL_vdw_rot_fixedSC(*args)
    def calc_EL_vdw_rot_fixedHET(*args): return _Py_Scream_EE.Scream_EE_calc_EL_vdw_rot_fixedHET(*args)
    def calc_EL_vdw_rot_moveableHET(*args): return _Py_Scream_EE.Scream_EE_calc_EL_vdw_rot_moveableHET(*args)
    def calc_EL_coulomb_rot_selfBB(*args): return _Py_Scream_EE.Scream_EE_calc_EL_coulomb_rot_selfBB(*args)
    def calc_EL_coulomb_rot_otherBB(*args): return _Py_Scream_EE.Scream_EE_calc_EL_coulomb_rot_otherBB(*args)
    def calc_EL_coulomb_rot_fixedSC(*args): return _Py_Scream_EE.Scream_EE_calc_EL_coulomb_rot_fixedSC(*args)
    def calc_EL_coulomb_rot_fixedHET(*args): return _Py_Scream_EE.Scream_EE_calc_EL_coulomb_rot_fixedHET(*args)
    def calc_EL_coulomb_rot_moveableHET(*args): return _Py_Scream_EE.Scream_EE_calc_EL_coulomb_rot_moveableHET(*args)
    def calc_EL_hb_rot_selfBB(*args): return _Py_Scream_EE.Scream_EE_calc_EL_hb_rot_selfBB(*args)
    def calc_EL_hb_rot_otherBB(*args): return _Py_Scream_EE.Scream_EE_calc_EL_hb_rot_otherBB(*args)
    def calc_EL_hb_rot_fixedSC(*args): return _Py_Scream_EE.Scream_EE_calc_EL_hb_rot_fixedSC(*args)
    def calc_EL_hb_rot_fixedHET(*args): return _Py_Scream_EE.Scream_EE_calc_EL_hb_rot_fixedHET(*args)
    def calc_EL_hb_rot_moveableHET(*args): return _Py_Scream_EE.Scream_EE_calc_EL_hb_rot_moveableHET(*args)
    def calc_all_interaction_E(*args): return _Py_Scream_EE.Scream_EE_calc_all_interaction_E(*args)
    def calc_all_interaction_E_full_delta(*args): return _Py_Scream_EE.Scream_EE_calc_all_interaction_E_full_delta(*args)
    def calc_all_interaction_E_flat_delta(*args): return _Py_Scream_EE.Scream_EE_calc_all_interaction_E_flat_delta(*args)
    def calc_all_interaction_coulomb_E_delta(*args): return _Py_Scream_EE.Scream_EE_calc_all_interaction_coulomb_E_delta(*args)
    def calc_all_interaction_vdw_E_delta(*args): return _Py_Scream_EE.Scream_EE_calc_all_interaction_vdw_E_delta(*args)
    def calc_all_interaction_hb_E_delta(*args): return _Py_Scream_EE.Scream_EE_calc_all_interaction_hb_E_delta(*args)
    def calc_all_interaction_vdw_hb_exclusion_E_delta(*args): return _Py_Scream_EE.Scream_EE_calc_all_interaction_vdw_hb_exclusion_E_delta(*args)
    def calc_residue_interaction_E(*args): return _Py_Scream_EE.Scream_EE_calc_residue_interaction_E(*args)
    def calc_residue_interaction_vdw_E(*args): return _Py_Scream_EE.Scream_EE_calc_residue_interaction_vdw_E(*args)
    def calc_residue_interaction_hb_E(*args): return _Py_Scream_EE.Scream_EE_calc_residue_interaction_hb_E(*args)
    def calc_residue_interaction_coulumb_E(*args): return _Py_Scream_EE.Scream_EE_calc_residue_interaction_coulumb_E(*args)
    def setProtein(*args): return _Py_Scream_EE.Scream_EE_setProtein(*args)
    def getProtein(*args): return _Py_Scream_EE.Scream_EE_getProtein(*args)
    __swig_setmethods__["ptn"] = _Py_Scream_EE.Scream_EE_ptn_set
    __swig_getmethods__["ptn"] = _Py_Scream_EE.Scream_EE_ptn_get
    if _newclass:ptn = property(_Py_Scream_EE.Scream_EE_ptn_get, _Py_Scream_EE.Scream_EE_ptn_set)
    __swig_setmethods__["mutInfoV"] = _Py_Scream_EE.Scream_EE_mutInfoV_set
    __swig_getmethods__["mutInfoV"] = _Py_Scream_EE.Scream_EE_mutInfoV_get
    if _newclass:mutInfoV = property(_Py_Scream_EE.Scream_EE_mutInfoV_get, _Py_Scream_EE.Scream_EE_mutInfoV_set)

class Scream_EEPtr(Scream_EE):
    def __init__(self, this):
        _swig_setattr(self, Scream_EE, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, Scream_EE, 'thisown', 0)
        _swig_setattr(self, Scream_EE,self.__class__,Scream_EE)
_Py_Scream_EE.Scream_EE_swigregister(Scream_EEPtr)

class MutInfo(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MutInfo, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MutInfo, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ MutInfo instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, MutInfo, 'this', _Py_Scream_EE.new_MutInfo(*args))
        _swig_setattr(self, MutInfo, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_MutInfo):
        try:
            if self.thisown: destroy(self)
        except: pass

    def init(*args): return _Py_Scream_EE.MutInfo_init(*args)
    def addMutInfo(*args): return _Py_Scream_EE.MutInfo_addMutInfo(*args)
    def __eq__(*args): return _Py_Scream_EE.MutInfo___eq__(*args)
    def __lt__(*args): return _Py_Scream_EE.MutInfo___lt__(*args)
    def getChn(*args): return _Py_Scream_EE.MutInfo_getChn(*args)
    def getPstn(*args): return _Py_Scream_EE.MutInfo_getPstn(*args)
    def getAA(*args): return _Py_Scream_EE.MutInfo_getAA(*args)
    __swig_setmethods__["chn"] = _Py_Scream_EE.MutInfo_chn_set
    __swig_getmethods__["chn"] = _Py_Scream_EE.MutInfo_chn_get
    if _newclass:chn = property(_Py_Scream_EE.MutInfo_chn_get, _Py_Scream_EE.MutInfo_chn_set)
    __swig_setmethods__["pstn"] = _Py_Scream_EE.MutInfo_pstn_set
    __swig_getmethods__["pstn"] = _Py_Scream_EE.MutInfo_pstn_get
    if _newclass:pstn = property(_Py_Scream_EE.MutInfo_pstn_get, _Py_Scream_EE.MutInfo_pstn_set)
    __swig_setmethods__["AA"] = _Py_Scream_EE.MutInfo_AA_set
    __swig_getmethods__["AA"] = _Py_Scream_EE.MutInfo_AA_get
    if _newclass:AA = property(_Py_Scream_EE.MutInfo_AA_get, _Py_Scream_EE.MutInfo_AA_set)
    __swig_setmethods__["str"] = _Py_Scream_EE.MutInfo_str_set
    __swig_getmethods__["str"] = _Py_Scream_EE.MutInfo_str_get
    if _newclass:str = property(_Py_Scream_EE.MutInfo_str_get, _Py_Scream_EE.MutInfo_str_set)
    __swig_setmethods__["mIInt"] = _Py_Scream_EE.MutInfo_mIInt_set
    __swig_getmethods__["mIInt"] = _Py_Scream_EE.MutInfo_mIInt_get
    if _newclass:mIInt = property(_Py_Scream_EE.MutInfo_mIInt_get, _Py_Scream_EE.MutInfo_mIInt_set)
    def print_Me(*args): return _Py_Scream_EE.MutInfo_print_Me(*args)
    def getString(*args): return _Py_Scream_EE.MutInfo_getString(*args)
    def getAllMutInfos(*args): return _Py_Scream_EE.MutInfo_getAllMutInfos(*args)
    def setIndex(*args): return _Py_Scream_EE.MutInfo_setIndex(*args)
    def getIndex(*args): return _Py_Scream_EE.MutInfo_getIndex(*args)
    def setRotConnInfo(*args): return _Py_Scream_EE.MutInfo_setRotConnInfo(*args)
    def getRotConnInfo(*args): return _Py_Scream_EE.MutInfo_getRotConnInfo(*args)
    def getMutInfoStringWithRotConnInfo(*args): return _Py_Scream_EE.MutInfo_getMutInfoStringWithRotConnInfo(*args)
    def searchAndAddRotConnInfo(*args): return _Py_Scream_EE.MutInfo_searchAndAddRotConnInfo(*args)
    def isClusterMutInfo(*args): return _Py_Scream_EE.MutInfo_isClusterMutInfo(*args)

class MutInfoPtr(MutInfo):
    def __init__(self, this):
        _swig_setattr(self, MutInfo, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, MutInfo, 'thisown', 0)
        _swig_setattr(self, MutInfo,self.__class__,MutInfo)
_Py_Scream_EE.MutInfo_swigregister(MutInfoPtr)

class MutInfoPair(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MutInfoPair, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MutInfoPair, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ MutInfoPair instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, MutInfoPair, 'this', _Py_Scream_EE.new_MutInfoPair(*args))
        _swig_setattr(self, MutInfoPair, 'thisown', 1)
    def __del__(self, destroy=_Py_Scream_EE.delete_MutInfoPair):
        try:
            if self.thisown: destroy(self)
        except: pass

    def init(*args): return _Py_Scream_EE.MutInfoPair_init(*args)
    def __eq__(*args): return _Py_Scream_EE.MutInfoPair___eq__(*args)
    def __lt__(*args): return _Py_Scream_EE.MutInfoPair___lt__(*args)
    def getString(*args): return _Py_Scream_EE.MutInfoPair_getString(*args)
    __swig_setmethods__["mutInfo1"] = _Py_Scream_EE.MutInfoPair_mutInfo1_set
    __swig_getmethods__["mutInfo1"] = _Py_Scream_EE.MutInfoPair_mutInfo1_get
    if _newclass:mutInfo1 = property(_Py_Scream_EE.MutInfoPair_mutInfo1_get, _Py_Scream_EE.MutInfoPair_mutInfo1_set)
    __swig_setmethods__["mutInfo2"] = _Py_Scream_EE.MutInfoPair_mutInfo2_set
    __swig_getmethods__["mutInfo2"] = _Py_Scream_EE.MutInfoPair_mutInfo2_get
    if _newclass:mutInfo2 = property(_Py_Scream_EE.MutInfoPair_mutInfo2_get, _Py_Scream_EE.MutInfoPair_mutInfo2_set)
    def getMutInfo1(*args): return _Py_Scream_EE.MutInfoPair_getMutInfo1(*args)
    def getMutInfo2(*args): return _Py_Scream_EE.MutInfoPair_getMutInfo2(*args)
    def setClashE(*args): return _Py_Scream_EE.MutInfoPair_setClashE(*args)
    def getClashE(*args): return _Py_Scream_EE.MutInfoPair_getClashE(*args)

class MutInfoPairPtr(MutInfoPair):
    def __init__(self, this):
        _swig_setattr(self, MutInfoPair, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, MutInfoPair, 'thisown', 0)
        _swig_setattr(self, MutInfoPair,self.__class__,MutInfoPair)
_Py_Scream_EE.MutInfoPair_swigregister(MutInfoPairPtr)

class ConnectivityMap(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ConnectivityMap, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ConnectivityMap, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ std::map<SCREAM_ATOM *,int > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, ConnectivityMap, 'this', _Py_Scream_EE.new_ConnectivityMap(*args))
        _swig_setattr(self, ConnectivityMap, 'thisown', 1)
    def empty(*args): return _Py_Scream_EE.ConnectivityMap_empty(*args)
    def size(*args): return _Py_Scream_EE.ConnectivityMap_size(*args)
    def clear(*args): return _Py_Scream_EE.ConnectivityMap_clear(*args)
    def swap(*args): return _Py_Scream_EE.ConnectivityMap_swap(*args)
    def get_allocator(*args): return _Py_Scream_EE.ConnectivityMap_get_allocator(*args)
    def erase(*args): return _Py_Scream_EE.ConnectivityMap_erase(*args)
    def count(*args): return _Py_Scream_EE.ConnectivityMap_count(*args)
    def __nonzero__(*args): return _Py_Scream_EE.ConnectivityMap___nonzero__(*args)
    def __len__(*args): return _Py_Scream_EE.ConnectivityMap___len__(*args)
    def __getitem__(*args): return _Py_Scream_EE.ConnectivityMap___getitem__(*args)
    def __setitem__(*args): return _Py_Scream_EE.ConnectivityMap___setitem__(*args)
    def __delitem__(*args): return _Py_Scream_EE.ConnectivityMap___delitem__(*args)
    def has_key(*args): return _Py_Scream_EE.ConnectivityMap_has_key(*args)
    def keys(*args): return _Py_Scream_EE.ConnectivityMap_keys(*args)
    def values(*args): return _Py_Scream_EE.ConnectivityMap_values(*args)
    def items(*args): return _Py_Scream_EE.ConnectivityMap_items(*args)
    def __contains__(*args): return _Py_Scream_EE.ConnectivityMap___contains__(*args)
    def __iter__(*args): return _Py_Scream_EE.ConnectivityMap___iter__(*args)
    def __del__(self, destroy=_Py_Scream_EE.delete_ConnectivityMap):
        try:
            if self.thisown: destroy(self)
        except: pass


class ConnectivityMapPtr(ConnectivityMap):
    def __init__(self, this):
        _swig_setattr(self, ConnectivityMap, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ConnectivityMap, 'thisown', 0)
        _swig_setattr(self, ConnectivityMap,self.__class__,ConnectivityMap)
_Py_Scream_EE.ConnectivityMap_swigregister(ConnectivityMapPtr)

class stringV(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, stringV, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, stringV, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ std::vector<std::string > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def empty(*args): return _Py_Scream_EE.stringV_empty(*args)
    def size(*args): return _Py_Scream_EE.stringV_size(*args)
    def clear(*args): return _Py_Scream_EE.stringV_clear(*args)
    def swap(*args): return _Py_Scream_EE.stringV_swap(*args)
    def get_allocator(*args): return _Py_Scream_EE.stringV_get_allocator(*args)
    def pop_back(*args): return _Py_Scream_EE.stringV_pop_back(*args)
    def __init__(self, *args):
        _swig_setattr(self, stringV, 'this', _Py_Scream_EE.new_stringV(*args))
        _swig_setattr(self, stringV, 'thisown', 1)
    def push_back(*args): return _Py_Scream_EE.stringV_push_back(*args)
    def front(*args): return _Py_Scream_EE.stringV_front(*args)
    def back(*args): return _Py_Scream_EE.stringV_back(*args)
    def assign(*args): return _Py_Scream_EE.stringV_assign(*args)
    def resize(*args): return _Py_Scream_EE.stringV_resize(*args)
    def reserve(*args): return _Py_Scream_EE.stringV_reserve(*args)
    def capacity(*args): return _Py_Scream_EE.stringV_capacity(*args)
    def __nonzero__(*args): return _Py_Scream_EE.stringV___nonzero__(*args)
    def __len__(*args): return _Py_Scream_EE.stringV___len__(*args)
    def pop(*args): return _Py_Scream_EE.stringV_pop(*args)
    def __getslice__(*args): return _Py_Scream_EE.stringV___getslice__(*args)
    def __setslice__(*args): return _Py_Scream_EE.stringV___setslice__(*args)
    def __delslice__(*args): return _Py_Scream_EE.stringV___delslice__(*args)
    def __delitem__(*args): return _Py_Scream_EE.stringV___delitem__(*args)
    def __getitem__(*args): return _Py_Scream_EE.stringV___getitem__(*args)
    def __setitem__(*args): return _Py_Scream_EE.stringV___setitem__(*args)
    def append(*args): return _Py_Scream_EE.stringV_append(*args)
    def __del__(self, destroy=_Py_Scream_EE.delete_stringV):
        try:
            if self.thisown: destroy(self)
        except: pass


class stringVPtr(stringV):
    def __init__(self, this):
        _swig_setattr(self, stringV, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, stringV, 'thisown', 0)
        _swig_setattr(self, stringV,self.__class__,stringV)
_Py_Scream_EE.stringV_swigregister(stringVPtr)

class ExcitationEnumeration(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ExcitationEnumeration, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ExcitationEnumeration, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ std::map<std::string,unsigned short > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, ExcitationEnumeration, 'this', _Py_Scream_EE.new_ExcitationEnumeration(*args))
        _swig_setattr(self, ExcitationEnumeration, 'thisown', 1)
    def empty(*args): return _Py_Scream_EE.ExcitationEnumeration_empty(*args)
    def size(*args): return _Py_Scream_EE.ExcitationEnumeration_size(*args)
    def clear(*args): return _Py_Scream_EE.ExcitationEnumeration_clear(*args)
    def swap(*args): return _Py_Scream_EE.ExcitationEnumeration_swap(*args)
    def get_allocator(*args): return _Py_Scream_EE.ExcitationEnumeration_get_allocator(*args)
    def erase(*args): return _Py_Scream_EE.ExcitationEnumeration_erase(*args)
    def count(*args): return _Py_Scream_EE.ExcitationEnumeration_count(*args)
    def __nonzero__(*args): return _Py_Scream_EE.ExcitationEnumeration___nonzero__(*args)
    def __len__(*args): return _Py_Scream_EE.ExcitationEnumeration___len__(*args)
    def __getitem__(*args): return _Py_Scream_EE.ExcitationEnumeration___getitem__(*args)
    def __setitem__(*args): return _Py_Scream_EE.ExcitationEnumeration___setitem__(*args)
    def __delitem__(*args): return _Py_Scream_EE.ExcitationEnumeration___delitem__(*args)
    def has_key(*args): return _Py_Scream_EE.ExcitationEnumeration_has_key(*args)
    def keys(*args): return _Py_Scream_EE.ExcitationEnumeration_keys(*args)
    def values(*args): return _Py_Scream_EE.ExcitationEnumeration_values(*args)
    def items(*args): return _Py_Scream_EE.ExcitationEnumeration_items(*args)
    def __contains__(*args): return _Py_Scream_EE.ExcitationEnumeration___contains__(*args)
    def __iter__(*args): return _Py_Scream_EE.ExcitationEnumeration___iter__(*args)
    def __del__(self, destroy=_Py_Scream_EE.delete_ExcitationEnumeration):
        try:
            if self.thisown: destroy(self)
        except: pass


class ExcitationEnumerationPtr(ExcitationEnumeration):
    def __init__(self, this):
        _swig_setattr(self, ExcitationEnumeration, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ExcitationEnumeration, 'thisown', 0)
        _swig_setattr(self, ExcitationEnumeration,self.__class__,ExcitationEnumeration)
_Py_Scream_EE.ExcitationEnumeration_swigregister(ExcitationEnumerationPtr)

class ExcitedRotamers(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ExcitedRotamers, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ExcitedRotamers, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ std::map<std::string,Rotamer * > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, ExcitedRotamers, 'this', _Py_Scream_EE.new_ExcitedRotamers(*args))
        _swig_setattr(self, ExcitedRotamers, 'thisown', 1)
    def empty(*args): return _Py_Scream_EE.ExcitedRotamers_empty(*args)
    def size(*args): return _Py_Scream_EE.ExcitedRotamers_size(*args)
    def clear(*args): return _Py_Scream_EE.ExcitedRotamers_clear(*args)
    def swap(*args): return _Py_Scream_EE.ExcitedRotamers_swap(*args)
    def get_allocator(*args): return _Py_Scream_EE.ExcitedRotamers_get_allocator(*args)
    def erase(*args): return _Py_Scream_EE.ExcitedRotamers_erase(*args)
    def count(*args): return _Py_Scream_EE.ExcitedRotamers_count(*args)
    def __nonzero__(*args): return _Py_Scream_EE.ExcitedRotamers___nonzero__(*args)
    def __len__(*args): return _Py_Scream_EE.ExcitedRotamers___len__(*args)
    def __getitem__(*args): return _Py_Scream_EE.ExcitedRotamers___getitem__(*args)
    def __setitem__(*args): return _Py_Scream_EE.ExcitedRotamers___setitem__(*args)
    def __delitem__(*args): return _Py_Scream_EE.ExcitedRotamers___delitem__(*args)
    def has_key(*args): return _Py_Scream_EE.ExcitedRotamers_has_key(*args)
    def keys(*args): return _Py_Scream_EE.ExcitedRotamers_keys(*args)
    def values(*args): return _Py_Scream_EE.ExcitedRotamers_values(*args)
    def items(*args): return _Py_Scream_EE.ExcitedRotamers_items(*args)
    def __contains__(*args): return _Py_Scream_EE.ExcitedRotamers___contains__(*args)
    def __iter__(*args): return _Py_Scream_EE.ExcitedRotamers___iter__(*args)
    def __del__(self, destroy=_Py_Scream_EE.delete_ExcitedRotamers):
        try:
            if self.thisown: destroy(self)
        except: pass


class ExcitedRotamersPtr(ExcitedRotamers):
    def __init__(self, this):
        _swig_setattr(self, ExcitedRotamers, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ExcitedRotamers, 'thisown', 0)
        _swig_setattr(self, ExcitedRotamers,self.__class__,ExcitedRotamers)
_Py_Scream_EE.ExcitedRotamers_swigregister(ExcitedRotamersPtr)

class RotamerV(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, RotamerV, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, RotamerV, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ std::vector<Rotamer * > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def empty(*args): return _Py_Scream_EE.RotamerV_empty(*args)
    def size(*args): return _Py_Scream_EE.RotamerV_size(*args)
    def clear(*args): return _Py_Scream_EE.RotamerV_clear(*args)
    def swap(*args): return _Py_Scream_EE.RotamerV_swap(*args)
    def get_allocator(*args): return _Py_Scream_EE.RotamerV_get_allocator(*args)
    def pop_back(*args): return _Py_Scream_EE.RotamerV_pop_back(*args)
    def __init__(self, *args):
        _swig_setattr(self, RotamerV, 'this', _Py_Scream_EE.new_RotamerV(*args))
        _swig_setattr(self, RotamerV, 'thisown', 1)
    def push_back(*args): return _Py_Scream_EE.RotamerV_push_back(*args)
    def front(*args): return _Py_Scream_EE.RotamerV_front(*args)
    def back(*args): return _Py_Scream_EE.RotamerV_back(*args)
    def assign(*args): return _Py_Scream_EE.RotamerV_assign(*args)
    def resize(*args): return _Py_Scream_EE.RotamerV_resize(*args)
    def reserve(*args): return _Py_Scream_EE.RotamerV_reserve(*args)
    def capacity(*args): return _Py_Scream_EE.RotamerV_capacity(*args)
    def __nonzero__(*args): return _Py_Scream_EE.RotamerV___nonzero__(*args)
    def __len__(*args): return _Py_Scream_EE.RotamerV___len__(*args)
    def pop(*args): return _Py_Scream_EE.RotamerV_pop(*args)
    def __getslice__(*args): return _Py_Scream_EE.RotamerV___getslice__(*args)
    def __setslice__(*args): return _Py_Scream_EE.RotamerV___setslice__(*args)
    def __delslice__(*args): return _Py_Scream_EE.RotamerV___delslice__(*args)
    def __delitem__(*args): return _Py_Scream_EE.RotamerV___delitem__(*args)
    def __getitem__(*args): return _Py_Scream_EE.RotamerV___getitem__(*args)
    def __setitem__(*args): return _Py_Scream_EE.RotamerV___setitem__(*args)
    def append(*args): return _Py_Scream_EE.RotamerV_append(*args)
    def __del__(self, destroy=_Py_Scream_EE.delete_RotamerV):
        try:
            if self.thisown: destroy(self)
        except: pass


class RotamerVPtr(RotamerV):
    def __init__(self, this):
        _swig_setattr(self, RotamerV, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, RotamerV, 'thisown', 0)
        _swig_setattr(self, RotamerV,self.__class__,RotamerV)
_Py_Scream_EE.RotamerV_swigregister(RotamerVPtr)

class pairds(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, pairds, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, pairds, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ std::pair<double,std::string > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, pairds, 'this', _Py_Scream_EE.new_pairds(*args))
        _swig_setattr(self, pairds, 'thisown', 1)
    __swig_setmethods__["first"] = _Py_Scream_EE.pairds_first_set
    __swig_getmethods__["first"] = _Py_Scream_EE.pairds_first_get
    if _newclass:first = property(_Py_Scream_EE.pairds_first_get, _Py_Scream_EE.pairds_first_set)
    __swig_setmethods__["second"] = _Py_Scream_EE.pairds_second_set
    __swig_getmethods__["second"] = _Py_Scream_EE.pairds_second_get
    if _newclass:second = property(_Py_Scream_EE.pairds_second_get, _Py_Scream_EE.pairds_second_set)
    def __len__(self):
      return 2
    def __getitem__(self, index):
      if not (index % 2): 
        return self.first
      else:
        return self.second
    def __setitem__(self, index, val):
      if not (index % 2): 
        self.first = val
      else:
        self.second = val
    def __repr__(self):
      return str((self.first, self.second))

    def __del__(self, destroy=_Py_Scream_EE.delete_pairds):
        try:
            if self.thisown: destroy(self)
        except: pass


class pairdsPtr(pairds):
    def __init__(self, this):
        _swig_setattr(self, pairds, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, pairds, 'thisown', 0)
        _swig_setattr(self, pairds,self.__class__,pairds)
_Py_Scream_EE.pairds_swigregister(pairdsPtr)

class MutInfoListPy(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MutInfoListPy, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MutInfoListPy, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ std::vector<MutInfo > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def empty(*args): return _Py_Scream_EE.MutInfoListPy_empty(*args)
    def size(*args): return _Py_Scream_EE.MutInfoListPy_size(*args)
    def clear(*args): return _Py_Scream_EE.MutInfoListPy_clear(*args)
    def swap(*args): return _Py_Scream_EE.MutInfoListPy_swap(*args)
    def get_allocator(*args): return _Py_Scream_EE.MutInfoListPy_get_allocator(*args)
    def pop_back(*args): return _Py_Scream_EE.MutInfoListPy_pop_back(*args)
    def __init__(self, *args):
        _swig_setattr(self, MutInfoListPy, 'this', _Py_Scream_EE.new_MutInfoListPy(*args))
        _swig_setattr(self, MutInfoListPy, 'thisown', 1)
    def push_back(*args): return _Py_Scream_EE.MutInfoListPy_push_back(*args)
    def front(*args): return _Py_Scream_EE.MutInfoListPy_front(*args)
    def back(*args): return _Py_Scream_EE.MutInfoListPy_back(*args)
    def assign(*args): return _Py_Scream_EE.MutInfoListPy_assign(*args)
    def resize(*args): return _Py_Scream_EE.MutInfoListPy_resize(*args)
    def reserve(*args): return _Py_Scream_EE.MutInfoListPy_reserve(*args)
    def capacity(*args): return _Py_Scream_EE.MutInfoListPy_capacity(*args)
    def __nonzero__(*args): return _Py_Scream_EE.MutInfoListPy___nonzero__(*args)
    def __len__(*args): return _Py_Scream_EE.MutInfoListPy___len__(*args)
    def pop(*args): return _Py_Scream_EE.MutInfoListPy_pop(*args)
    def __getslice__(*args): return _Py_Scream_EE.MutInfoListPy___getslice__(*args)
    def __setslice__(*args): return _Py_Scream_EE.MutInfoListPy___setslice__(*args)
    def __delslice__(*args): return _Py_Scream_EE.MutInfoListPy___delslice__(*args)
    def __delitem__(*args): return _Py_Scream_EE.MutInfoListPy___delitem__(*args)
    def __getitem__(*args): return _Py_Scream_EE.MutInfoListPy___getitem__(*args)
    def __setitem__(*args): return _Py_Scream_EE.MutInfoListPy___setitem__(*args)
    def append(*args): return _Py_Scream_EE.MutInfoListPy_append(*args)
    def __del__(self, destroy=_Py_Scream_EE.delete_MutInfoListPy):
        try:
            if self.thisown: destroy(self)
        except: pass


class MutInfoListPyPtr(MutInfoListPy):
    def __init__(self, this):
        _swig_setattr(self, MutInfoListPy, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, MutInfoListPy, 'thisown', 0)
        _swig_setattr(self, MutInfoListPy,self.__class__,MutInfoListPy)
_Py_Scream_EE.MutInfoListPy_swigregister(MutInfoListPyPtr)

class MutInfoPairListPy(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MutInfoPairListPy, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MutInfoPairListPy, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ std::vector<MutInfoPair > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def empty(*args): return _Py_Scream_EE.MutInfoPairListPy_empty(*args)
    def size(*args): return _Py_Scream_EE.MutInfoPairListPy_size(*args)
    def clear(*args): return _Py_Scream_EE.MutInfoPairListPy_clear(*args)
    def swap(*args): return _Py_Scream_EE.MutInfoPairListPy_swap(*args)
    def get_allocator(*args): return _Py_Scream_EE.MutInfoPairListPy_get_allocator(*args)
    def pop_back(*args): return _Py_Scream_EE.MutInfoPairListPy_pop_back(*args)
    def __init__(self, *args):
        _swig_setattr(self, MutInfoPairListPy, 'this', _Py_Scream_EE.new_MutInfoPairListPy(*args))
        _swig_setattr(self, MutInfoPairListPy, 'thisown', 1)
    def push_back(*args): return _Py_Scream_EE.MutInfoPairListPy_push_back(*args)
    def front(*args): return _Py_Scream_EE.MutInfoPairListPy_front(*args)
    def back(*args): return _Py_Scream_EE.MutInfoPairListPy_back(*args)
    def assign(*args): return _Py_Scream_EE.MutInfoPairListPy_assign(*args)
    def resize(*args): return _Py_Scream_EE.MutInfoPairListPy_resize(*args)
    def reserve(*args): return _Py_Scream_EE.MutInfoPairListPy_reserve(*args)
    def capacity(*args): return _Py_Scream_EE.MutInfoPairListPy_capacity(*args)
    def __nonzero__(*args): return _Py_Scream_EE.MutInfoPairListPy___nonzero__(*args)
    def __len__(*args): return _Py_Scream_EE.MutInfoPairListPy___len__(*args)
    def pop(*args): return _Py_Scream_EE.MutInfoPairListPy_pop(*args)
    def __getslice__(*args): return _Py_Scream_EE.MutInfoPairListPy___getslice__(*args)
    def __setslice__(*args): return _Py_Scream_EE.MutInfoPairListPy___setslice__(*args)
    def __delslice__(*args): return _Py_Scream_EE.MutInfoPairListPy___delslice__(*args)
    def __delitem__(*args): return _Py_Scream_EE.MutInfoPairListPy___delitem__(*args)
    def __getitem__(*args): return _Py_Scream_EE.MutInfoPairListPy___getitem__(*args)
    def __setitem__(*args): return _Py_Scream_EE.MutInfoPairListPy___setitem__(*args)
    def append(*args): return _Py_Scream_EE.MutInfoPairListPy_append(*args)
    def __del__(self, destroy=_Py_Scream_EE.delete_MutInfoPairListPy):
        try:
            if self.thisown: destroy(self)
        except: pass


class MutInfoPairListPyPtr(MutInfoPairListPy):
    def __init__(self, this):
        _swig_setattr(self, MutInfoPairListPy, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, MutInfoPairListPy, 'thisown', 0)
        _swig_setattr(self, MutInfoPairListPy,self.__class__,MutInfoPairListPy)
_Py_Scream_EE.MutInfoPairListPy_swigregister(MutInfoPairListPyPtr)


derefString = _Py_Scream_EE.derefString

derefRotamer = _Py_Scream_EE.derefRotamer

derefAARotamer = _Py_Scream_EE.derefAARotamer

castRotamerToAARotamer = _Py_Scream_EE.castRotamerToAARotamer

