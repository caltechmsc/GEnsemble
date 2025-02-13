############################################################################
#cr
#cr            (C) Copyright 1995-2004 The Board of Trustees of the
#cr                        University of Illinois
#cr                         All Rights Reserved
#cr
############################################################################

############################################################################
# RCS INFORMATION:
#
#       $RCSfile: seqdata_phy.tcl,v $
#       $Author: johns $        $Locker:  $             $State: Exp $
#       $Revision: 1.1 $       $Date: 2006/08/09 17:11:16 $
#
############################################################################

# This file provides functions for reading and writing sequence data from 
# NEXUS format files

package provide seqdata 1.0

# Sample file format:
#    88    697
#MmazeAla   ---------- ---------- N-ISEM--RE YYLSFFEA-- --RG--HTRI 
#PaeroAla   ---------- ---------- DSLTEL--RE RFLRFFER-- --RG--HARI 
#
#           NRYP-VVARW ---------- ---------- ---------- ---------- 
#           KRYP-VVARW ---------- ---------- ---------- ---------- 
#
#           TIYDALF--- ---------- ---------- ---------- -------
#           TIYDAVF--- ---------- ---------- ---------- -------
namespace eval ::SeqData::Phy {

    # Export the package namespace.
    namespace export saveSequences
    
    # The width of the name column.
    variable nameWidth 10
    
    # The width of the data columns.
    variable columnWidth 10
    
    # The number of data columns per line.
    variable columnsPerLine 5

    
    # Save a series of sequences into a PHY file from the sequence store.
    # arg:  sequences - The list of sequences ids that should be saved to the 
    #                       file. These ids should have come from the seqdata 
    #                       package.
    #       filename - The name of the file to load.
    #       names - An optional list of strings to use to override the sequence names.
    proc saveSequences {sequenceIDs filename {names {}}} {
        
        # Import global variables.
        variable nameWidth
        variable columnWidth
        variable columnsPerLine
    
        # Figure out the maximum sequence length.
        set maxLength 0
        foreach sequenceID $sequenceIDs {
            if {[SeqData::getSeqLength $sequenceID] > $maxLength} {
                set maxLength [SeqData::getSeqLength $sequenceID]
            }
        }
                    
        # Open the file.
        set fp [open $filename w]

        # Write out the header
        puts $fp "[getFixedLengthString [llength $sequenceIDs] 6 left] [getFixedLengthString $maxLength 6 left]"
        
        # Go through all of the sequence data one block at a time.
        for {set i 0} {$i < $maxLength} {incr i [expr $columnWidth*$columnsPerLine]} {
            
            # Write a blank line between sections.
            if {$i != 0} {
            	puts $fp ""
            }
            
            # Go through each sequence.
            for {set j 0} {$j < [llength $sequenceIDs]} {incr j} {
                
                # Get the sequence.
                set sequenceID [lindex $sequenceIDs $j]
                
                # If this is the first block, write out the name.
                if {$i == 0} {
                    
                    # Figure out the name to use.
                    set name [SeqData::getName $sequenceID]
                    if {$j < [llength $names]} {
                        set name [lindex $names $j]
                    }
                    
                    # Replace any invalid characters in the name.
                    regsub {\-} $name "_" name
                    regsub {\_+$} $name "" name
                    
                    # Write the name.
                    puts -nonewline $fp [getFixedLengthString $name $nameWidth]
                
                # Otherwise write an empty block.
                } else {
                    puts -nonewline $fp [getFixedLengthString "" $nameWidth]
                }
                
                # Get the sequence data.
                set sequenceData [SeqData::getSeq $sequenceID]
                    
                # Write out each column, one at a time.
                for {set k 0} {$k < $columnsPerLine} {incr k} {
                    
                    # Write out the sequence data.
                    set startPos [expr $i+($k*$columnWidth)]
                    set endPos [expr $startPos+$columnWidth-1]
                    if {$endPos >= $maxLength} {
                        set endPos [expr $maxLength-1]   
                    }
                    if {$k > 0} {
                        puts -nonewline $fp " "
                    }
                    puts -nonewline $fp [join [lrange $sequenceData $startPos $endPos] ""]                    
                }
                # Write out the newline.
                puts $fp ""
            }
        }

        # Close the file.
        close $fp
    }
    
    proc getFixedLengthString {str count {paddingSide right}} {
        
        if {$paddingSide == "right"} {
            while {[string length $str] < $count} {
                append str " "
            }
            if {[string length $str] > $count} {
                return [string range $str 0 [expr $count-1]]
            } else {
                return $str
            }
        } elseif {$paddingSide == "left"} {
            while {[string length $str] < $count} {
                set str " $str"
            }
            if {[string length $str] > $count} {
                return [string range $str [expr [string length $str]-$count] [expr [string length $str]-1]]
            } else {
                return $str
            }
        }
    }    
}
