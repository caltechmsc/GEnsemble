############################################################################
#cr
#cr            (C) Copyright 1995-2004 The Board of Trustees of the
#cr                        University of Illinois
#cr                         All Rights Reserved
#cr
############################################################################

package provide seqedit 1.0
package require seqdata 1.0

# Declare global variables for this package.
namespace eval ::SeqEdit::Metric::Entropy {

    # Export the package namespace.
    namespace export calculate

    proc calculateStrict {sequenceIDs} {
        set mapping {A A C C D D E E F F G G H H I I K K L L M M N N P P Q Q R R S S T T V V W W X X Y Y}
        return [calculate $mapping $sequenceIDs]
    }
        
    proc calculateSimilar {sequenceIDs} {
        set mapping {A S C C D N E N F F G S H H I V K H L V M V N N P S Q N R H S S T S V V W F X X Y Y}
        return [calculate $mapping $sequenceIDs]
    }
    
    # Calculates a metric for a given set of sequences.
    # args:     sequenceIDs - The list of sequences for which the metric should be calculated.
    # return:   A list containing the TCL array of sequence elements to values. The valued should be between 0.0 and 1.0.
    proc calculate {mapping sequenceIDs} {
        
        # Initialize the color map.
        array set metricMap {}
        array set map $mapping
        
        # Go through each sequence and set the metric for every element.
        foreach sequenceID $sequenceIDs {
            
            set sequence [::SeqData::getSeq $sequenceID]
            set elementIndex 0
            foreach element $sequence {
                set metricMap($sequenceID,$elementIndex) 0.0
                incr elementIndex
            }
            
        }
        
        set aaSym {A C D E F G H I K L M N P Q R S T V W X Y}
        
        set alignment {}
        set Naln -1;
        foreach sequenceID $sequenceIDs {
            
            set sequence [::SeqData::getSeq $sequenceID]
            lappend alignment $sequence
            if {$Naln == -1 || [llength $sequence] < $Naln} {
                set Naln [llength $sequence]
            }
            
        }
        set Nseq [llength $alignment];
        
        for {set i 0} {$i < $Naln} {incr i} {
        
            for {set j 0} {$j < [llength $aaSym]} {incr j} {
            set count($map([lindex $aaSym $j])) 0;
            }
            set count(-) 0;
            
        
            for {set j 0} {$j < $Nseq} {incr j} {
                set element [lindex [lindex $alignment $j] $i]
                if {[lsearch -exact $aaSym $element] == -1 && $element != "-"} {
                    set element "X"
                }
                if {$element == "-"} {
                    incr count(-);
                } else {
                    incr count($map($element));
                }
            }
        
            set S($i) 0;
            if {$count(-) < floor($Nseq/2)} {
            for {set j 0} {$j < [llength $aaSym]} {incr j} {
                if {$count($map([lindex $aaSym $j])) != 0} {
                set pr($j) [expr double($count($map([lindex $aaSym $j])))/double($Nseq)];
                set S($i) [expr double($S($i)) - double($pr($j))*double(log($pr($j)))];
                }
            }
            } else {
            set S($i) -1;
            }
        }
        
        set max $S(0);
        for {set i 1} {$i < $Naln} {incr i} {
            if {$S($i) > $max} {
            set max $S($i);
            }
        }
        
        for {set i 0} {$i < $Naln} {incr i} {
            if {$S($i) == -1 || $max == 0} {
            set S($i) 1;
            } else {
            set S($i) [expr double($S($i)/$max)];
            }
        }
        
        foreach sequenceID $sequenceIDs {
            for {set i 0} {$i < $Naln} {incr i} {
                set metricMap($sequenceID,$i) [expr 1.0-$S($i)]
            }
        }        
        
        # Return the color map.
        return [array get metricMap]
    }
}

