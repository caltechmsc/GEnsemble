############################################################################
#cr
#cr            (C) Copyright 1995-2004 The Board of Trustees of the
#cr                        University of Illinois
#cr                         All Rights Reserved
#cr
############################################################################

package provide phylotree 1.0

# Declare global variables for this package.
namespace eval ::PhyloTree::Data {
    
    # A list of the current trees.
    set treeIDs {}
    
    # The map storing the tree data.
    variable treeData
    array set treeData {}
    
    # Resets the sequence data store.
    proc reset {} {
    
        # Import global variables.
        variable treeIDs
        variable treeData
        
        # Reset the data structures.
        set treeIDs {}
        unset treeData
        array set treeData {}
    }
    
    # Gets the next available tree id.
    # return:   The next available tree id.
    proc getNextTreeID {} {
    
        # Import global variables.
        variable treeIDs
        
        # Loop through the currently used sequence ids and find the maximum value.
        set nextID 0
        foreach treeID $treeIDs {
            if {$treeID >= $nextID} {
                set nextID [expr $treeID+1]
            }
        }
        
        # Return the next id.
        return $nextID
    }

    proc createTree {name} {
    
        # Import global variables.
        variable treeIDs
        variable treeData
        
        # Get the next tree id and add it to the list of used ids.
        set treeID [getNextTreeID]
        lappend treeIDs $treeID
        
        # Set the sequence data.
        set treeData($treeID,name) $name
        set treeData($treeID,maxDistance) 0.0
        set treeData($treeID,nextNode) 1
        set treeData($treeID,attributeKeys) {}
        set treeData($treeID,distanceMatrix) {}
        set rootNode 0
        set treeData($treeID,root) $rootNode
        set treeData($treeID,$rootNode,parent) -1
        set treeData($treeID,$rootNode,children) {}
        set treeData($treeID,$rootNode,distanceToParent) 0.0
        set treeData($treeID,$rootNode,distanceToRoot) 0.0
        set treeData($treeID,$rootNode,name) ""
        set treeData($treeID,$rootNode,label) ""
        
        # Return the tree id.
        return $treeID
    }
    
    proc getTreeName {treeID} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)]} {
            return -code error "The specified tree ($treeID) does not exist."
        }
        
        return $treeData($treeID,name)
    }
    
    proc getTreeRootNode {treeID} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)]} {
            return -code error "The specified tree ($treeID) does not exist."
        }
        
        return $treeData($treeID,root)
    }
    
    proc getTreeDistance {treeID} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)]} {
            return -code error "The specified tree ($treeID) does not exist."
        }
        
        return $treeData($treeID,maxDistance)
    }
    
    proc getTreeUnits {treeID} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)]} {
            return -code error "The specified tree ($treeID) does not exist."
        }
        
        if {[info exists treeData($treeID,units)]} {
            return $treeData($treeID,units)
        }
        return ""
    }
    
    proc setTreeUnits {treeID units} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)]} {
            return -code error "The specified tree ($treeID) does not exist."
        }
        
        set treeData($treeID,units) $units
    }
    
    proc getDistanceMatrix {treeID} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)]} {
            return -code error "The specified tree ($treeID) does not exist."
        }
        
        return $treeData($treeID,distanceMatrix)
    }
    
    proc setDistanceMatrix {treeID distanceMatrix} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)]} {
            return -code error "The specified tree ($treeID) does not exist."
        }
        
        set treeData($treeID,distanceMatrix) $distanceMatrix
    }
    
    proc getNodeAttributeKeys {treeID} {
        
        # Import global variables.
        variable treeData

        return $treeData($treeID,attributeKeys)
    }
    
    proc getNodeAttributeValues {treeID attribute} {
        
        # Import global variables.
        variable treeData

        return $treeData($treeID,$attribute,attributeValues)
    }
    
    proc getNodeName {treeID node} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node,name)]} {
            return -code error "The specified tree ($treeID) or node ($node) does not exist."
        }
        
        return $treeData($treeID,$node,name)
    }
    
    proc setNodeName {treeID node name} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node,name)]} {
            return -code error "The specified tree ($treeID) or node ($node) does not exist."
        }
        
        set treeData($treeID,$node,name) $name
    }
    
    proc getNodeLabel {treeID node} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node,name)]} {
            return -code error "The specified tree ($treeID) or node ($node) does not exist."
        }
        
        return $treeData($treeID,$node,label)
    }
    
    proc setNodeLabel {treeID node label} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node,name)]} {
            return -code error "The specified tree ($treeID) or node ($node) does not exist."
        }
        
        set treeData($treeID,$node,label) $label
    }
    
    proc getNodeAttribute {treeID node attribute} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node,name)]} {
            return -code error "The specified tree ($treeID) or node ($node) does not exist."
        }
        
        if {[info exists treeData($treeID,$node,attribute,$attribute)]} {
            return $treeData($treeID,$node,attribute,$attribute)
        }
        return ""
    }
    
    proc setNodeAttribute {treeID node attribute value {valueList {}} {hidden 0}} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node,name)]} {
            return -code error "The specified tree ($treeID) or node ($node) does not exist."
        }
        
        # Set the attribute.
        set treeData($treeID,$node,attribute,$attribute) $value
        
        # Add this to the list of available attributes.
        if {!$hidden} {
            if {[lsearch $treeData($treeID,attributeKeys) $attribute] == -1} {
                lappend treeData($treeID,attributeKeys) $attribute
                set treeData($treeID,attributeKeys) [lsort $treeData($treeID,attributeKeys)]
            }
            if {![info exists treeData($treeID,$attribute,attributeValues)]} {
                set treeData($treeID,$attribute,attributeValues) $valueList
            }
            if {$value != "" && [lsearch $treeData($treeID,$attribute,attributeValues) $value] == -1} {
                lappend treeData($treeID,$attribute,attributeValues) $value
                set treeData($treeID,$attribute,attributeValues) [lsort $treeData($treeID,$attribute,attributeValues)]
            }
        }
    }
    
    proc getParentNode {treeID node} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node,name)]} {
            return -code error "The specified tree ($treeID) or node ($node) does not exist."
        }
        
        return $treeData($treeID,$node,parent)
    }
    
    proc addChildNode {treeID parentNode {distanceToParent 1.0}} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$parentNode,name)]} {
            return -code error "The specified tree ($treeID) or node ($parentNode) does not exist."
        }
        
        # Get the node index.
        set node $treeData($treeID,nextNode)
        incr treeData($treeID,nextNode)

        # Create the node.
        lappend treeData($treeID,$parentNode,children) $node
        set treeData($treeID,$node,parent) $parentNode
        set treeData($treeID,$node,children) {}
        set treeData($treeID,$node,distanceToParent) [expr double($distanceToParent)]
        set treeData($treeID,$node,distanceToRoot) [expr $treeData($treeID,$parentNode,distanceToRoot)+$distanceToParent]
        if {$treeData($treeID,$node,distanceToRoot) > $treeData($treeID,maxDistance)} {
            set treeData($treeID,maxDistance) $treeData($treeID,$node,distanceToRoot)
        }
        set treeData($treeID,$node,name) ""
        set treeData($treeID,$node,label) ""
        
        return $node
    }
    
    proc getChildNodes {treeID parentNode} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$parentNode,name)]} {
            return -code error "The specified tree ($treeID) or node ($parentNode) does not exist."
        }
        
        return $treeData($treeID,$parentNode,children)
    }

    
    proc rotateChildNodes {treeID parentNode {direction left}} {
        
        # Import global variables.
        variable treeData
        
        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$parentNode,name)]} {
            return -code error "The specified tree ($treeID) or node ($parentNode) does not exist."
        }
                
        if {$direction == "left"} {
            set children $treeData($treeID,$parentNode,children)
            set numChildren [llength $children]
            set newChildren [lrange $children 1 [expr $numChildren-1]]
            lappend newChildren [lindex $children 0]
            set treeData($treeID,$parentNode,children) $newChildren
        } elseif {$direction == "right"} {
            set children $treeData($treeID,$parentNode,children)
            set numChildren [llength $children]
            set newChildren [list [lindex $children [expr $numChildren-1]]]
            set newChildren [concat $newChildren [lrange $children 0 [expr $numChildren-2]]]
            set treeData($treeID,$parentNode,children) $newChildren
        }
    }
    
    proc getLeafNodes {treeID parentNode} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$parentNode,name)]} {
            return -code error "The specified tree ($treeID) or node ($parentNode) does not exist."
        }
                
        if {$treeData($treeID,$parentNode,children) == {}} {
            return $parentNode
        } else {
            set leafNodes {}
            foreach childNode $treeData($treeID,$parentNode,children) {
                set leafNodes [concat $leafNodes [getLeafNodes $treeID $childNode]]
            }
            return $leafNodes            
        }
    }
    
    proc getDistanceToParentNode {treeID node} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node,name)]} {
            return -code error "The specified tree ($treeID) or node ($node) does not exist."
        }
        
        return $treeData($treeID,$node,distanceToParent)
    }
    
    proc getDistanceToRootNode {treeID node} {

        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node,name)]} {
            return -code error "The specified tree ($treeID) or node ($node) does not exist."
        }
        
        return $treeData($treeID,$node,distanceToRoot)
    }
    
    proc isAncestorNode {treeID node ancestor} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node,name)] || ![info exists treeData($treeID,$ancestor,name)]} {
            return -code error "The specified tree ($treeID) or node ($node,$ancestor) does not exist."
        }
                
        # If this node is the root node, return 0.
        if {$treeData($treeID,$node,parent) == -1} {
            return 0
        
        # If the two node are parent child, return 1.
        } elseif {$treeData($treeID,$node,parent) == $ancestor} {
            return 1
            
        # Otherwise, move up the tree.
        } else {
            return [isAncestorNode $treeID $treeData($treeID,$node,parent) $ancestor]
        }
    }
    
    proc isDescendantNode {treeID node descendant} {
        
        return [isAncestorNode $treeID $descendant $node]
    }
    
    proc getPathToAncestorNode {treeID node ancestor} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node,name)] || ![info exists treeData($treeID,$ancestor,name)]} {
            return -code error "The specified tree ($treeID) or node ($node,$ancestor) does not exist."
        }
        
        # If this node is the root node, return an error.
        if {$treeData($treeID,$node,parent) == -1} {
            return -code error "In the specified tree ($treeID) the nodes ($node,$ancestor) are not in the same lineage."
        
        # If the two node are parent child, just return the two.
        } elseif {$treeData($treeID,$node,parent) == $ancestor} {
            return [list $node $ancestor]
            
        # Otherwise, move down the tree.
        } else {
            
            # Get our parent's path.
            set parentPath [getPathToAncestorNode $treeID $treeData($treeID,$node,parent) $ancestor]
            
            # If our parent had a path, use it, otherwise we have no path.
            if {$parentPath != {}} {
                return [linsert $parentPath 0 $node]
            } else {
                return {}
            }
        }
    }
    
        
    proc getDistanceToAncestorNode {treeID node ancestor} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node,name)] || ![info exists treeData($treeID,$ancestor,name)]} {
            return -code error "The specified tree ($treeID) or node ($node,$ancestor) does not exist."
        }

        # Get the path from the node to the descendant.
        set path [getPathToAncestorNode $treeID $node $ancestor]
        
        # Add up the distances in the path.
        set distance 0.0
        for {set i 0} {$i < [expr [llength $path]-1]} {incr i} {
            set node [lindex $path $i]
            set distance [expr $distance+$treeData($treeID,$node,distanceToParent)]
        }
        
        return $distance
    }
    
    proc getPathToDescendantNode {treeID node descendant} {
        
        # Get the reverse path and then reverse it.
        set path [getPathToAncestorNode $treeID $descendant $node]
        set reversePath {}
        for {set i [expr [llength $path]-1]} {$i >= 0} {incr i -1} {
            lappend reversePath [lindex $path $i]
        }
        return $reversePath
    }
        
    proc getDistanceToDescendantNode {treeID node descendant} {
        
        return [getDistanceToAncestorNode $treeID $descendant $node]
    }
        
    proc getPathBetweenNodes {treeID node1 node2} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$node1,name)] || ![info exists treeData($treeID,$node2,name)]} {
            return -code error "The specified tree ($treeID) or node ($node1,$node2) does not exist."
        }

        # See if one of the nodes is a descendant of the other.
        if {[isAncestorNode $treeID $node1 $node2]} {
            return [list [getPathToAncestorNode $treeID $node1 $node2] [list $node2]]
        } elseif {[isDescendantNode $treeID $node1 $node2]} {
            return [list [list $node1] [getPathToDescendantNode $treeID $node1 $node2]]
            
        # Find the path using a common ancestor.
        } else {
            
            # Move up the tree until we find a common ancestor.
            set commonAncestor {}
            set ancestor1 $treeData($treeID,$node1,parent)
            set ancestor2 $treeData($treeID,$node2,parent)
            while {$ancestor1 != -1 && $ancestor2 != -1} {
                if {[isAncestorNode $treeID $node1 $ancestor2]} {
                    set commonAncestor $ancestor2
                    break
                } elseif {[isAncestorNode $treeID $node2 $ancestor1]} {
                    set commonAncestor $ancestor1
                    break
                }
                set ancestor1 $treeData($treeID,$ancestor1,parent)
                set ancestor2 $treeData($treeID,$ancestor2,parent)
            }
            
            # If we found a common ancestor, find the path for it to both nodes.
            if {$commonAncestor != {}} {
                return [list [getPathToAncestorNode $treeID $node1 $commonAncestor] [getPathToDescendantNode $treeID $commonAncestor $node2]]
            } else {
                return -code error "In the specified tree ($treeID) the nodes ($node1,$node2) do not share a common ancestor."
            }
        }
    }
    
    proc getDistanceBetweenNodes {treeID node1 node2} {

        set paths [getPathBetweenNodes $treeID $node1 $node2]
        set distance 0.0
        if {[llength [lindex $paths 0]] >= 2} {
            set distance [expr $distance+[getDistanceToAncestorNode $treeID [lindex [lindex $paths 0] 0] [lindex [lindex $paths 0] end]]]
        }
        if {[llength [lindex $paths 1]] >= 2} {
            set distance [expr $distance+[getDistanceToDescendantNode $treeID [lindex [lindex $paths 1] 0] [lindex [lindex $paths 1] end]]]
        }
        
        return $distance
    }
    
    proc getAllDescendantNodes {treeID parentNode} {
        
        # Import global variables.
        variable treeData

        # Make sure this is a real tree.
        if {![info exists treeData($treeID,root)] || ![info exists treeData($treeID,$parentNode,name)]} {
            return -code error "The specified tree ($treeID) or node ($parentNode) does not exist."
        }
                
        set descendantNodes [list $parentNode]
        foreach childNode $treeData($treeID,$parentNode,children) {
            set descendantNodes [concat $descendantNodes [getAllDescendantNodes $treeID $childNode]]
        }
        return $descendantNodes            
    }
}
