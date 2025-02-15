
# Makefile for vmd
# VMD for LINUXAMD64, version 1.8.6 (February 24, 2008)

.SILENT:

CD          = cd
COPY        = cp
COPYDIR     = cp -r
MAKEDIR     = mkdir -p
MOVE        = mv -f
DELETE      = rm -f
DELETEDIR   = rm -rf
ECHO        = echo
TAR         = tar
COMPRESS    = compress
GNUCOMPRESS = /usr/local/bin/gzip
LATEX       = latex

# makefile configuration
VPATH                   = .:../LINUXAMD64
SHELL                   = /bin/sh
.SUFFIXES: .C .c .cu ..c .i .o


# C++ source files
VMD_CCPP    =	OpenGLDisplayDevice.C \
		OpenGLExtensions.C \
		OpenGLRenderer.C \
		OpenGLShader.C \
		OpenGLCache.C \
		Hershey.C \
		IMDMgr.C \
		IMDSim.C \
		IMDSimThread.C \
		CmdIMD.C \
		imd.C \
		Spaceball.C \
		SpaceballTracker.C \
		LibTachyonDisplayDevice.C \
		P_VRPNTracker.C \
		P_VRPNButtons.C \
		P_VRPNFeedback.C \
		P_RotateTool.C \
		PythonTextInterp.C \
		VMDTkinterMenu.C \
		py_animate.C \
		py_atomsel.C \
		py_atomselection.C \
		py_axes.C \
		py_color.C \
		py_commands.C \
		py_display.C \
		py_graphics.C \
		py_imd.C \
		py_label.C \
		py_material.C \
		py_menu.C \
		py_molecule.C \
		py_molrep.C \
		py_mouse.C \
		py_render.C \
		py_trans.C \
		py_numeric.C \
		Animation.C \
		ArtDisplayDevice.C \
		AtomColor.C \
		AtomParser.C \
		AtomLexer.C \
		AtomRep.C \
		AtomSel.C \
		Axes.C \
		BaseMolecule.C \
		BondSearch.C \
		CmdAnimate.C \
		CmdColor.C \
		CmdDisplay.C \
		CmdLabel.C \
		CmdMaterial.C \
		CmdMenu.C \
		CmdMol.C \
		CmdRender.C \
		CmdTrans.C \
		CommandQueue.C \
		CoorPluginData.C \
		CUDAAccel.C \
		DisplayDevice.C \
		Displayable.C \
		DisplayRocker.C \
		DispCmds.C \
		DrawMolecule.C \
		DrawMolItem.C \
		DrawMolItem2.C \
		DrawMolItemRibbons.C \
		DrawMolItemMSMS.C \
		DrawMolItemRings.C \
		DrawMolItemSurface.C \
		DrawMolItemVolume.C \
		DrawForce.C \
		DrawRingsUtils.C \
		FileRenderList.C \
		FileRenderer.C \
		FPS.C \
		GelatoDisplayDevice.C \
		GeometryAngle.C \
		GeometryAtom.C \
		GeometryBond.C \
		GeometryDihedral.C \
		GeometryList.C \
		GeometryMol.C \
		GeometrySpring.C \
		Inform.C \
		ImageIO.C \
		Isosurface.C \
		JRegex.C \
		JString.C \
		macosxvmdstart.C \
		MaterialList.C \
		Matrix4.C \
		Measure.C \
		Molecule.C \
		MoleculeList.C \
		MoleculeGraphics.C \
		MolFilePlugin.C \
		Mouse.C \
		MSMSInterface.C \
		PeriodicTable.C \
		P_JoystickTool.C \
		P_TugTool.C \
		P_GrabTool.C \
		P_PrintTool.C \
		P_PinchTool.C \
		P_UIVR.C \
		P_Buttons.C \
		P_Tracker.C \
		P_Tool.C \
		P_CmdTool.C \
		P_SensorConfig.C \
		ParseTree.C \
		PickList.C \
		PickModeAddBond.C \
		PickModeCenter.C \
		PickModeForce.C \
		PickModeList.C \
		PickModeMolLabel.C \
		PickModeMove.C \
		PickModeUser.C \
		PlainTextInterp.C \
		PluginMgr.C \
		POV3DisplayDevice.C \
		PSDisplayDevice.C \
		VMDQuat.C \
		RadianceDisplayDevice.C \
		RayShadeDisplayDevice.C \
		R3dDisplayDevice.C \
		RenderManDisplayDevice.C \
		Scene.C \
		SnapshotDisplayDevice.C \
		SpringTool.C \
		Stage.C \
		STLDisplayDevice.C \
		Stride.C \
		Surf.C \
		SymbolTable.C \
		TachyonDisplayDevice.C \
		Timestep.C \
		UIObject.C \
		UIText.C \
		VMDApp.C \
		VMDCollab.C \
		VMDDir.C \
		VMDDisplayList.C \
		VMDMenu.C \
		VMDTitle.C \
		VMDThreads.C \
		VolCPotential.C \
		VolMap.C \
		VolMapCreate.C \
		VolumetricData.C \
		VolumeTexture.C \
		VrmlDisplayDevice.C \
		Vrml2DisplayDevice.C \
		WavefrontDisplayDevice.C \
		utilities.C \
		vmd.C \
		vmdmain.C \
		ColorInfo.C \
		TclCommands.C \
		TclMeasure.C \
		TclMolInfo.C \
		TclTextInterp.C \
		TclVec.C \
		TclGraphics.C \
		TclVolMap.C \
		cmd_animate.C \
		cmd_collab.C \
		cmd_color.C \
		cmd_display.C \
		cmd_imd.C \
		cmd_label.C \
		cmd_material.C \
		cmd_menu.C \
		cmd_mol.C \
		cmd_mouse.C \
		cmd_plugin.C \
		cmd_render.C \
		cmd_tool.C \
		cmd_trans.C \
		cmd_user.C \
		cmd_util.C \
		tcl_commands.C \
		VMDTkMenu.C \
		ColorFltkMenu.C \
		DisplayFltkMenu.C \
		FileChooserFltkMenu.C \
		GraphicsFltkMenu.C \
		SelectionBuilder.C \
		GeometryFltkMenu.C \
		MaterialFltkMenu.C \
		MolBrowser.C \
		RenderFltkMenu.C \
		SaveTrajectoryFltkMenu.C \
		VMDFltkMenu.C \
		MainFltkMenu.C \
		ToolFltkMenu.C \
		frame_selector.C

# C source files
VMD_CC      = 	hash.c \
		inthash.c \
		intstack.c \
		vmdsock.c \
		vmddlopen.c \
		pcre.c \
		fitrms.c

# CUDA source files
VMD_CU      = 	

# Header files
VMD_H       = 	OpenGLDisplayDevice.h \
		OpenGLExtensions.h \
		OpenGLRenderer.h \
		OpenGLShader.h \
		OpenGLCache.h \
		Hershey.h \
		imd.h \
		IMDMgr.h \
		IMDSim.h \
		IMDSimThread.h \
		CmdIMD.h \
		Spaceball.h \
		SpaceballTracker.h \
		LibTachyonDisplayDevice.h \
		P_VRPNTracker.h \
		P_VRPNButtons.h \
		P_VRPNFeedback.h \
		P_RotateTool.h \
		PythonTextInterp.h \
		VMDTkinterMenu.h \
		py_commands.h \
		py_molecule.h \
		 \
		Animation.h \
		ArtDisplayDevice.h \
		Atom.h \
		AtomColor.h \
		AtomParser.h \
		AtomRep.h \
		AtomSel.h \
		Axes.h \
		BaseMolecule.h \
		BondSearch.h \
		CmdAnimate.h \
		CmdColor.h \
		CmdDisplay.h \
		CmdLabel.h \
		CmdMaterial.h \
		CmdMenu.h \
		CmdMol.h \
		CmdRender.h \
		CmdTrans.h \
		Command.h \
		CommandQueue.h \
		CoorData.h \
		CUDAAccel.h \
		CoorPluginData.h \
		DepthSortObj.h \
		DispCmds.h \
		DisplayDevice.h \
		Displayable.h \
		DisplayRocker.h \
		DrawMolecule.h \
		DrawMolItem.h \
		DrawMolItemSolventPoints.data \
		DrawForce.h \
		GelatoDisplayDevice.h \
		FPS.h \
		FileRenderList.h \
		FileRenderer.h \
		Fragment.h \
		GeometryAngle.h \
		GeometryAtom.h \
		GeometryBond.h \
		GeometryDihedral.h \
		GeometryList.h \
		GeometryMol.h \
		GeometrySpring.h \
		Inform.h \
		ImageIO.h \
		Isosurface.h \
		JRegex.h \
		JString.h \
		macosxvmdstart.h \
		MaterialList.h \
		Matrix4.h \
		Measure.h \
		Molecule.h \
		MoleculeGraphics.h \
		MoleculeList.h \
		MolFilePlugin.h \
		Mouse.h \
		MSMSInterface.h \
		NameList.h \
		PeriodicTable.h \
		P_JoystickTool.h \
		P_TugTool.h \
		P_PinchToo.h \
		P_GrabTool.h \
		P_PrintTool.h \
		P_Feedback.h \
		P_UIVR.h \
		P_Buttons.h \
		P_Tracker.h \
		P_CmdTool.h \
		P_SensorConfig.h \
		P_Tool.h \
		ParseTree.h \
		PickList.h \
		PickMode.h \
		PickModeAddBond.h \
		PickModeCenter.h \
		PickModeForce.h \
		PickModeList.h \
		PickModeMolLabel.h \
		PickModeMove.h \
		Pickable.h \
		PlainTextInterp.h \
		PluginMgr.h \
		PointerTool.h \
		POV3DisplayDevice.h \
		PSDisplayDevice.h \
		VMDQuat.h \
		RadianceDisplayDevice.h \
		RayShadeDisplayDevice.h \
		R3dDisplayDevice.h \
		ResizeArray.h \
		RenderManDisplayDevice.h \
		Residue.h \
		Scene.h \
		SnapshotDisplayDevice.h \
		SortableArray.h \
		SpringTool.h \
		Stack.h \
		Stage.h \
		STLDisplayDevice.h \
		Stride.h \
		Surf.h \
		SymbolTable.h \
		TachyonDisplayDevice.h \
		TextEvent.h \
		TextInterp.h \
		Timestep.h \
		UIObject.h \
		UIText.h \
		VMDApp.h \
		VMDDir.h \
		VMDDisplayList.h \
		VMDMenu.h \
		VMDTitle.h \
		VMDThreads.h \
		VolCPotential.h \
		VolMap.h \
		VolMapCreate.h \
		VolumetricData.h \
		VolumeTexture.h \
		VrmlDisplayDevice.h \
		Vrml2DisplayDevice.h \
		WavefrontDisplayDevice.h \
		utilities.h \
		pcre.h \
		pcreinternal.h \
		pcretables.h \
		vmdsock.h \
		fitrms.h \
		TclCommands.h \
		TclTextInterp.h \
		tcl_commands.h \
		VMDTkMenu.h \
		plugin.h \
		molfile_plugin.h \
		libmolfile_plugin.h \
		ColorFltkMenu.h \
		DisplayFltkMenu.h \
		FileChooserFltkMenu.h \
		GeometryFltkMenu.h \
		GraphicsFltkMenu.h \
		GraphicsFltkReps.h \
		SelectionBuilder.h \
		MaterialFltkMenu.h \
		MolBrowser.h \
		RenderFltkMenu.h \
		SaveTrajectoryFltkMenu.h \
		VMDFltkMenu.h \
		MainFltkMenu.h \
		ToolFltkMenu.h \
		frame_selector.h

# yacc and lex files
VMD_YACC    = 	AtomParser.y

VMD_LEX     = 	AtomLexer.l

# Misc. data file
VMD_DATA    = 	.vmdsensors .vmdrc

VMD_EXTRA          = 	

VMD_OTHER_EXE      = 	../lib/stride/stride_LINUXAMD64 ../lib/surf/surf_LINUXAMD64 ../lib/tachyon/tachyon_LINUXAMD64

VMD_OTHER_NAMES    = 	stride_LINUXAMD64

VMD_MAIN_DIR_FILES = 	Announcement FEEDBACK LICENSE README configure

# Turn things into objects
VMD_OBJS    =   $(VMD_CCPP:.C=.o) $(VMD_CC:.c=.o) $(VMD_CU:.cu=.o)

INCDIRS     =  -I../lib/actc/include  -I../lib/libsball/include -I../lib/tachyon/include -I../lib/vrpn/vrpn -I../lib/vrpn/quat -I../lib/python/lib_LINUXAMD64/include/python2.2   -I../lib/tcl/include -I../lib/tk/include -I../plugins/include -I../plugins/LINUXAMD64/molfile -I../lib/netcdf/include -I../lib/fltk/include -I.

LIBS        = -L/usr/X11R6/lib64 -lGL -lGLU -lX11 -lactc  -lsball -ltachyon -lvrpn -lquat -lpython2.2 -lpthread -lpthread  -ltk8.4 -lX11 -ltcl8.4 -lmolfile_plugin -lnetcdf -lfltk -lX11 -lm -ldl -lutil $(VMDEXTRALIBS)

LIBDIRS     =  -L../lib/actc/lib_LINUXAMD64  -L../lib/libsball/lib_LINUXAMD64 -L../lib/tachyon/lib_LINUXAMD64 -L../lib/vrpn/lib_LINUXAMD64 -L../lib/python/lib_LINUXAMD64/lib/python2.2/config   -L../lib/tcl/lib_LINUXAMD64 -L../lib/tk/lib_LINUXAMD64 -L../plugins/LINUXAMD64/molfile -L../lib/netcdf/lib_LINUXAMD64 -L../lib/fltk/LINUXAMD64 

DEFINES     = -DVMDOPENGL -DVMDGRAPHICS -DVMDACTC -DVMDIMD -DVMDSPACEBALL -DVMDLIBTACHYON -DVMDVRPN -DVMDPYTHON -DVMDTHREADS -DUSEPOSIXTHREADS -D_REENTRANT -DVMDNUMPY -DVMDSURF -DVMDMSMS -DVMDFIELDLINES -DVMDVOLUMETEXTURE -DVMDTCL -DVMDTK -DVMDSTATICPLUGINS  -DVMDGUI -DVMDFLTK 

# compiler and compiler directives 
CC          = gcc
CFLAGS      = -m64 -Wall -O6 -ffast-math -DARCH_LINUXAMD64 $(DEFINES) $(INCDIRS) 

CCPP	    = g++
CPPFLAGS    = -m64 -fno-for-scope -Wno-deprecated -Wall -O6 -ffast-math  -DARCH_LINUXAMD64 $(DEFINES) $(INCDIRS) 

NVCC        = nvcc
NVCCFLAGS   =  -DARCH_LINUXAMD64 $(DEFINES) $(INCDIRS)

COMPILERC   = echo
RCFLAGS     = No resource compiler required on this platform.

DEPEND      = -MM
DEPENDFILE  = Makedata.depend

LOADLIBES   = $(LIBDIRS) $(LIBS) -rdynamic

LEX 	    = flex
YACC	    = yacc
YFLAGS      = -d

############################### 
# default rules 
###############################

.C.o: 
	$(ECHO) "Compiling " $< " --> " $*.o " ..."; \
	$(CCPP) $(CPPFLAGS) -c $< -o ../LINUXAMD64/$@

.c.o:
	$(ECHO) "Compiling " $< " --> " $*.o " ..."; \
	$(CC) $(CFLAGS) -c $< -o ../LINUXAMD64/$@

.cu.o:
	$(ECHO) "Compiling " $< " --> " $*.o " ..."; \
	$(NVCC) $(NVCCFLAGS) -c $< -o ../LINUXAMD64/$@

.y.o:

.l.o:

########## Targets

### Source targets
all default:   vmd_LINUXAMD64

vmd_LINUXAMD64: y.tab.h $(VMD_OBJS)
	$(ECHO) "Linking " $@ "..."; \
	$(CD) ../LINUXAMD64 ; \
	if [ ! -r ./foobar ]; then \
	  ln -s ../src/foobar ./foobar ; \
	fi; \
	$(CCPP) $(CPPFLAGS) -I../src -o $@ $(VMD_OBJS) $(LOADLIBES) ; 
	$(COMPILERC) $(RCFLAGS)

install:
	if [ ! -d "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib" ]; then \
		$(MAKEDIR) "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib" ; \
	fi ; \
	if [ ! -d "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/bin" ]; then \
		$(MAKEDIR) "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/bin" ; \
	fi ; \
	if [ ! -d "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib"/doc ]; then \
		$(MAKEDIR) "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib"/doc; \
	fi
	-$(COPY) ../Announcement  "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib"
	-$(COPY) ../README        "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib"
	-$(COPY) ../LICENSE       "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib"
	-$(COPY) ../doc/ug.pdf        "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib"/doc
	if [ -f /home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib/vmd_LINUXAMD64 ]; then \
           $(MOVE) "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib/vmd_LINUXAMD64" "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib/OLD_vmd_LINUXAMD64" ; $(DELETE) "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib/OLD_vmd_LINUXAMD64" ; fi
	-$(COPY) ../LINUXAMD64/vmd_LINUXAMD64 "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib"
	-$(COPY) ../lib/stride/stride_LINUXAMD64 ../lib/surf/surf_LINUXAMD64 ../lib/tachyon/tachyon_LINUXAMD64 "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib"
	-$(CD) ..; $(TAR) -cf - scripts | \
	(cd "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib" ; $(TAR) -xf -)
	-$(CD) ../lib; $(TAR) -cf - scripts | \
	(cd "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib" ; $(TAR) -xf -)
	-$(CD) ..; $(TAR) -cf - python | \
	(cd "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib"/scripts ; $(TAR) -xf -)
	-$(CD) ..; $(TAR) -cf - plugins | \
	(cd "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib" ; $(TAR) -xf -)
	-$(CD) ..; $(TAR) -cf - shaders | \
	(cd "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib" ; $(TAR) -xf -)
	-$(COPY) ../data/.vmdrc ../data/.vmdsensors "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib"
	$(CD) ../bin ; \
	if [ -f run_vmd_tmp ]; then $(DELETE) run_vmd_tmp; fi ; \
	$(ECHO) '#!/bin/csh' >> run_vmd_tmp ; \
	$(ECHO) 'set defaultvmddir="/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/lib"' >> run_vmd_tmp ; \
	$(ECHO) 'set vmdbasename=vmd' >> run_vmd_tmp ; \
	cat vmd >> run_vmd_tmp ; \
	chmod +x run_vmd_tmp ; \
	$(COPY) run_vmd_tmp "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/bin"/vmd ; \
	$(DELETE) run_vmd_tmp
	$(ECHO) Make sure "/home/adam/GEnsemble/programs/thirdparty/vmd-1.8.6/bin"/vmd is in your path.
	$(ECHO) "VMD installation complete.  Enjoy!"

##### remove most of the cruft
clean:
	$(CD) ../LINUXAMD64 ; \
		$(DELETE) *.o *.warnings *.depend.old core

veryclean: clean swigclean
	$(CD) ../LINUXAMD64 ; \
	  $(DELETEDIR) foobar; \
	  $(DELETE) vmd_LINUXAMD64
	$(CD) ../src ; \
	  $(DELETE) *.o *.a *~ core; \
	  $(DELETEDIR) foobar; \
	  $(DELETE) vmd_LINUXAMD64
	$(CD) ../doc ; \
	  $(DELETE) *~ core

# The '/usr/include' stuff is to reduce checking /usr/include dates
depend: y.tab.h
	if [ "$(DEPEND)" != "" ]; then \
	echo "Building Makefile dependencies"; \
	  $(ECHO) "Creating " $(DEPENDFILE) " ..."; \
	  if [ -f $(DEPENDFILE) ]; then \
	    $(MOVE) -f $(DEPENDFILE) $(DEPENDFILE).old; \
	fi; \
	  touch $(DEPENDFILE); \
	for i in ZZZ $(VMD_CCPP) ; do \
	  if [ "$$i" != "ZZZ" ]; then \
	        $(ECHO) checking dependencies for $$i ...; \
	        $(CCPP) $(DEPEND) $(CPPFLAGS) $$i |  \
			sed -e 's/\/usr\/include\/[^ ]*\..//g' \
			    -e 's/\.\.\/lib\/.*\/[^ ]*\..//g' | \
			grep -v '^ *\\$$' >> $(DEPENDFILE) ; \
	  fi; \
	done; \
	for i in ZZZ $(VMD_CC) ; do \
	  if [ "$$i" != "ZZZ" ]; then \
	        $(ECHO) checking dependencies for $$i ...; \
	        $(CC) $(DEPEND) $(CFLAGS) $$i |  \
			sed -e 's/\/usr\/include\/[^ ]*\..//g' \
			    -e 's/\.\.\/lib\/.*\/[^ ]*\..//g' | \
			grep -v '^ *\\$$' >> $(DEPENDFILE) ; \
	  fi; \
	done; \
	$(ECHO) ParseTree.o AtomLexer.o AtomParser.o: y.tab.h \
                >> $(DEPENDFILE); \
	$(COPY) $(DEPENDFILE) $(DEPENDFILE).LINUXAMD64 ; \
	else \
	  $(ECHO) "Cannot find dependencies; your compiler does not support dependency checking."; \
        fi



# to bootstrap without a Makedata.depend file, either
#   touch Makedata.depend
# or change the following line to 'sinclude'
include Makedata.depend

# Rules for SWIG-generated interface.  Ignored unless SWIG option is present
include Makefile.swig

vmd_python.o: vmd_python.C
	$(ECHO) "Compiling " $< " --> " $*.o " ..."; \
	$(CCPP) $(CPPFLAGS)  -c $< -o ../LINUXAMD64/$@

