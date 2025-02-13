############################################################
#
#    This file contains procedures to wrap atoms into the central
# image of a system with periodic boundary conditions. The procedures
# required the VMD unit cell properties to be set. Use the procedure
# pbcset on this behalf.
#
# $Id: pbcunwrap.tcl,v 1.4 2007/02/28 22:55:25 johns Exp $
#

package provide pbctools 2.0

namespace eval ::PBCTools:: {
    namespace export pbc*

    ############################################################
    #
    # pbcunwrap [OPTIONS...]
    #
    # OPTIONS:
    #   -molid $molid|top
    #   -first $first|first|now 
    #   -last $last|last|now
    #   -all|allframes
    #   -sel $sel
    #
    # AUTHORS: Olaf, Jerome, Cameron
    #
    proc pbcunwrap {args} {
	# Set the defaults
	set molid "top"
	set first "first"
	set last "last"
	set seltext "all"
	
	# Parse options
	for { set argnum 0 } { $argnum < [llength $args] } { incr argnum } {
	    set arg [ lindex $args $argnum ]
	    set val [ lindex $args [expr {$argnum + 1}]]
	    switch -- $arg {
		"-molid" { set molid $val; incr argnum; }
		"-first" { set first $val; incr argnum }
		"-last" { set last $val; incr argnum }
		"-allframes" -
		"-all" { set last "last"; set first "first" }
		"-now" { set last "now"; set first "now" }
		"-sel" { set seltext $val; incr argnum }
		default { error "pbcunwrap: unknown option: $arg" }
	    }
	}
	
	if { $molid=="top" } then { set molid [ molinfo top ] }

	# Save the current frame number
	set frame_before [ molinfo $molid get frame ]

	if { $first=="now" }   then { set first $frame_before }
	if { $first=="first" || $first=="start" || $first=="begin" } then { 
	    set first 0 
	}
	if { $last=="now" }    then { set last $frame_before }
	if { $last=="last" || $last=="end" } then {
	    set last [expr {[molinfo $molid get numframes]-1}]
	}

	display update off

	if { $first == 0 } then {
	    set frame $first
	} else {
	    set frame [expr $first - 1]
	}
	molinfo $molid set frame $frame

	# get coordinates of the first reference frame
	set sel [atomselect $molid $seltext]

	set oldxs [$sel get x]
	set oldys [$sel get y]
	set oldzs [$sel get z]

	# create lists of the right lengths
	set shiftAs $oldxs
	set shiftBs $oldxs
	set shiftCs $oldxs
	
	set deg2rad [expr 3.14159265/180.0]

	# loop over all frames
	# for efficiency reasons, most operations are carried out as
	# vector operations on all coordinates at once
	for {incr frame} { $frame <= $last } { incr frame } {
	    molinfo $molid set frame $frame
	    $sel frame $frame

	    # get the cell vectors
	    set cell [lindex [pbc get -molid $molid -namd] 0]
	    set Ax   [lindex $cell 0 0]
	    set Bx   [lindex $cell 1 0]
	    set By   [lindex $cell 1 1]
	    set Cx   [lindex $cell 2 0]
	    set Cy   [lindex $cell 2 1]
	    set Cz   [lindex $cell 2 2]
	    set Ax2 [expr 0.5*$Ax]
	    set By2 [expr 0.5*$By]
	    set Cz2 [expr 0.5*$Cz]
	    set iAx  [expr 1.0/$Ax]
	    set iBy  [expr 1.0/$By]
	    set iCz  [expr 1.0/$Cz]

	    # get the current z coordinates 
	    set zs [$sel get z]
	    # compute the differences in the z coordinate
	    set dzs [vecsub $zs $oldzs]
	    # compute the required shift
	    set i 0
	    foreach dz $dzs {
		set shift 0
		if { $dz > $Cz2 } then {
		    incr shift -1
		    while { $dz+$shift*$Cz > $Cz2 } { incr shift -1 }
		} elseif { $dz < -$Cz2 } then {
		    incr shift
		    while { $dz+$shift*$Cz < -$Cz2 } { incr shift }
		}
		lset shiftCs $i $shift
		incr i
	    }
	    # apply shiftC to zs
	    set zs [vecadd $zs [vecscale $Cz $shiftCs]]

	    # get the current y coordinates and apply shiftC
	    set ys [vecadd [$sel get y] [vecscale $Cy $shiftCs]]
	    # compute the differences in the y coordinate
	    set dys [vecsub $ys $oldys]
	    # compute the required shift
	    set i 0
	    foreach dy $dys {
		set shift 0
		if { $dy > $By2 } then {
		    incr shift -1
		    while { $dy+$shift*$By > $By2 } { incr shift -1 }
		} elseif { $dy < -$By2 } then {
		    incr shift
		    while { $dy+$shift*$By < -$By2 } { incr shift }
		}
		lset shiftBs $i $shift
		incr i
	    }
	    # apply shiftB to ys
	    set ys [vecadd $ys [vecscale $By $shiftBs]]

	    # get the current x coordinates and apply shiftC and shiftB
	    set xs [vecadd [$sel get x] [vecscale $Cx $shiftCs] [vecscale $Bx $shiftBs]]
	    # compute the differences in the x coordinate
	    set dxs [vecsub $xs $oldxs]
	    # compute the required shift
	    set i 0
	    foreach dx $dxs {
		set shift 0
		if { $dx > $Ax2 } then {
		    incr shift -1
		    while { $dx+$shift*$Ax > $Ax2 } { incr shift -1 }
		} elseif { $dx < -$Ax2 } then {
		    incr shift
		    while { $dx+$shift*$Ax < -$Ax2 } { incr shift }
		}
		lset shiftAs $i $shift
		incr i
	    }
	    # apply shiftA to xs
	    set xs [vecadd $xs [vecscale $Ax $shiftAs]]
	    
	    # set the new coordinates
	    $sel set x $xs
	    $sel set y $ys 
	    $sel set z $zs

	    # save the coordinates
	    set oldxs $xs
	    set oldys $ys
	    set oldzs $zs
	}

	# Rewind to original frame
	molinfo $molid set frame $frame_before
	display update on
    }

}
