############################################################################
#cr                                                                       
#cr            (C) Copyright 1995-2007 The Board of Trustees of the            
#cr                        University of Illinois                         
#cr                         All Rights Reserved                           
#cr                                                                       
############################################################################

############################################################################
# RCS INFORMATION:
#
# 	$RCSfile: vmdinit.tcl,v $
# 	$Author: johns $	$Locker:  $		$State: Exp $
#	$Revision: 1.145 $	$Date: 2007/01/12 20:11:32 $
#
############################################################################
# DESCRIPTION:
#   install the "core" vmd/tcl procedures and variables
#
############################################################################

# This is part of the VMD installation.
# For more information about VMD, see http://www.ks.uiuc.edu/Research/vmd

#######################################
# TclX commands we still use in VMD
proc lassign { listvar args } {
  set i 0
  foreach var $args {
    upvar $var x
    set x [lindex $listvar $i] 
    incr i
  }
  return [lrange $listvar $i end]
}

proc lvarpush { listvar var } {
  upvar $listvar x
  set x [list $var $x]
}

proc lvarpop { var } {
  upvar $var x
  set retval [lindex $x 0]
  set x [lrange $x 1 end]
  return $retval
}


#######################################
# This proc exists for backwards compatibility
proc vmd_calculate_structure { molid } {
  mol ssrecalc $molid
}


#######################################
# rename the Tcl commands that VMD overrides
# VMD 1.1 and Tk have some conflicts in their names.  The VMD
# commands with this problem are: label, menu and scale
# Luckily, the 1st word in all these for Tk require a .path.name,
# and VMD does not, so we can write a wrapper to distinguish them.
if {[info commands label] == "label"} {
    rename label vmd_tk_label
}
proc label {args} {
    lassign $args arg1
    if {[string first . $arg1] >= 0} {
	return [eval "vmd_tk_label $args"]
    } else {
	return [eval "vmd_label $args"]
    }
}
if {[info commands menu] == "menu"} {
    rename menu vmd_tk_menu
}
proc menu {args} {
    lassign $args arg1
    if {[string first . $arg1] >= 0} {
	return [eval "vmd_tk_menu $args"]
    } else {
	return [eval "vmd_menu $args"]
    }
}
if {[info commands scale] == "scale"} {
    rename scale vmd_tk_scale
}
proc scale {args} {
    lassign $args arg1
    if {[string first . $arg1] >= 0} {
	return [eval "vmd_tk_scale $args"]
    } else {
	return [eval "vmd_scale $args"]
    }
}
proc help {args} {
    return [eval "vmd_help $args"]
}


#######################################
# default directory locations
if {![info exists env(VMDDIR)]} {
  set env(VMDDIR) /usr/local/lib/vmd
}
if {![info exists env(TMPDIR)]} {
  switch [vmdinfo arch] {
    WIN64 -
    WIN32 {
      set env(TMPDIR) "c:"
    }
    MACOSXX86 -
    MACOSX {
      set env(TMPDIR) /tmp
    }
    default {
      set env(TMPDIR) /usr/tmp
    }
  }
}


#######################################
# Define the default HTML viewer, if it hasn't been defined already; 
# this is used by openURL.tcl
if { ![info exists env(VMDHTMLVIEWER)] } {
  switch [vmdinfo arch] {
    WIN64 -
    WIN32 {
      set env(VMDHTMLVIEWER) "c:/WINDOWS/explorer.exe %s &"  
    }
    MACOSXX86 -
    MACOSX {
      set env(VMDHTMLVIEWER) "/usr/bin/open %s"
    }
    default {
      # If you wish, uncomment one of the other mozilla options
      # for different window behavior.
      # Open in the current window (default)
      #set env(VMDHTMLVIEWER) "mozilla -remote openURL(%s)" 
      # Open in a new window
      set env(VMDHTMLVIEWER) "firefox -remote openURL(%s,new-window)"
      # Open a new instance of mozilla
      # set env(VMDHTMLVIEWER) "mozilla %s &" 
    }
  }
}


#######################################
# set the autoloading functions
lappend auto_path $env(VMDDIR)/scripts/vmd


#######################################
# initialize the vmd_mouse_mode and vmd_mouse_submode variables
set vmd_mouse_mode rotate
set vmd_mouse_submode -1

#######################################
# some things are NOT autoloaded since that overrides the 
# definitions overridden (for performance reasons) in C++
source $env(VMDDIR)/scripts/vmd/vectors.tcl
source $env(VMDDIR)/scripts/vmd/atomselect.tcl
source $env(VMDDIR)/scripts/vmd/graphlabels.tcl
source $env(VMDDIR)/scripts/vmd/logfile.tcl
# whereas this is needed to set the hotkeys
source $env(VMDDIR)/scripts/vmd/hotkeys.tcl


#######################################
# everything else is safe to autoload
# the index is made with:
# auto_mkindex . \
#     {{draw,save_state,openURL,www}.tcl}
#
# The following should not be indexed:
#  {atomselect,hotkeys,vectors,vmdinit}.tcl
#


#######################################
# Load a file over http or ftp.  Used by "mol urlload"
proc vmd_mol_urlload {url filename} {
  if { [string equal [string range $url 0 6] http:// ] } {
     vmdhttpcopy $url $filename
  } elseif { [string equal [string range $url 0 5] ftp:// ] } {
     package require ftp
     set base [string range $url 0 5]
     set rest [string range $url 6 end]
     set parts [split $rest /]
     set nparts [llength $parts]
     set site [lindex $parts 0]
     set path [join [lrange $parts 1 [expr $nparts - 2]] /]
     set fname [lindex $parts end]

     set handle [ftp::Open $site ftp ftp]
     ftp::Type $handle binary
     ftp::Cd $handle $path
     ftp::Get $handle $fname $filename
     ftp::Close $handle
   }
   return $filename
}


#######################################
# Running Tk, hide the default Tk toplevel menu
if [info exists tk_version] {
    # don't use the toplevel menu
    wm withdraw .
    # but give it a name, just in case
    wm title . "VMD Tk window"
}


#######################################
# This proc allows Tk windows to integrate with the rest of VMD's GUI.
# See the VMDTkMenu class for details.  
proc vmd_tkmenu_cb { win op args } {
  switch $op {
    create {
        lassign $args name
        wm protocol $win WM_DELETE_WINDOW "menu $name off"
        # These are used to tell VMD about the status of extension menus,
        # so that "menu $name status" gets the correct answer, but it causes
        # bad things to happen on OS X due to spurious events being generated
        # by Tk.  We should be able to get rid of these bindings and make
        # "menu status" work by a different mechanism; for now it's not 
        # critical that "menu $name status" always give the right answer.
        #bind $win <Map> "+menu $name on"
        #bind $win <Unmap> "+menu $name off"

	# For some window managers (KDE's, anyway), the Tk menu doesn't 
	# remember its screen position when withdraw until after the first
	# call to wm geometry.  So, we do it here.
	# Don't do this on the Mac, though, or the menus will end
	# up under the apple menubar.
        switch [vmdinfo arch] {
          MACOSXX86 -
          MACOSX { }
          default {
            wm geometry $win +[winfo x $win]+[winfo y $win]
	  }
	}
      }
    on { wm deiconify $win }
    off { wm withdraw $win }
    loc { return [list [winfo x $win] [winfo y $win]] }
    move {
        lassign $args x y
        wm geometry $win +$x+$y
    }
    remove { wm protocol $win WM_DELETE_WINDOW "" }
  }
  return
}


#######################################
# add a pause command
proc pause {} { 
    gets stdin 
}


#######################################
# Make Fltk the default file chooser, except for Windows, where the Tk
# file chooser is more native-like.
if ![info exists env(VMDFILECHOOSER)] { 
  switch [vmdinfo arch] {
    MACOSX -
    MACOSXX86 -
    WIN64 - 
    WIN32 {
      set env(VMDFILECHOOSER) TK 
    }
    default {
      set env(VMDFILECHOOSER) FLTK 
    }
  }
}

#######################################
# Add the plugin directories to Tcl/Python paths,
# load all of the molfile plugins,
# define proc to register all of the graphical interface extensions
source $env(VMDDIR)/scripts/vmd/loadplugins.tcl

#######################################
# BioCoRE features
# Force load of BioCoRE startup code
source $env(VMDDIR)/scripts/vmd/biocore.tcl

# Check for BioCoRE startup
check_biocore

