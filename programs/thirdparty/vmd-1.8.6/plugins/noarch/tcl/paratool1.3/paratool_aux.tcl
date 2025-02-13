#
# Misc helper routines
#
# $Id: paratool_aux.tcl,v 1.33 2006/10/18 10:16:29 saam Exp $
#

proc ::Paratool::deg2rad { deg } {
   return [expr {$deg*0.0174532925}]
}

proc ::Paratool::rad2deg { rad } {
   return [expr {$rad*57.2957795786}]
}

# Extracts the arguments of an option from a list and returns them.
# If the option $tag was not found the default value $deflt is returned
proc ::Paratool::getargs {arglist tag deflt {n 1}} {
   set pos [lsearch $arglist $tag]
   if {!$n} { return [expr {$pos<0 ? 0 : 1}] }
   if {$pos<0}  { return $deflt }
   return [join [lrange $arglist [expr {$pos+1}] [expr {$pos+$n}]]]
}

# Checks if a certain switch $tag occurs in $taglist
proc ::Paratool::getswitch {arglist tag} {
   return [expr {[lsearch $arglist $tag]<0 ? 0 : 1}]
}

proc ::Paratool::max {a b} { return [expr {$a>$b ? $a : $b}] }
proc ::Paratool::min {a b} { return [expr {$a<$b ? $a : $b}] }

proc ::Paratool::format_float { format float {empty "{}"} } {
   if {![llength $float] || $float=="{}"} { 
      set len [string length [format "$format" 0.0]]
      return [format "%${len}s" $empty]
   } else {
      return [format "$format" $float]
   }
}

proc ::Paratool::vecangle2 { v1 v2 } {
   set cross [veccross $v1 $v2]
   set absv1 [veclength $v1]
   set absv2 [veclength $v2]
   return   [expr {asin([veclength $cross]/($absv1*$absv2))*57.2957795786}]
}

# Computes the angle between the specified coordinates
proc ::Paratool::angle_from_coords { p0 p1 p2 } {
   set x [vecnorm [vecsub $p0 $p1]]
   set y [vecnorm [vecsub $p2 $p1]]
   return [expr {57.2957795786*acos([vecdot $x $y])}]
}


# Computes the angle between two vectors x and y  #
proc ::Paratool::vecangle {x y} {
   if {[llength $x] != [llength $y]} {
      error "vecangle needs arrays of the same size: $x : $y"
   }
   if {[llength $x]==0 || [llength $y]==0} {
      error "vecangle: zero length vector: [llength $x] : [llength $y]"
   }
   # Compute scalar-produt
   set dot [vecdot $x $y]
   return [expr {57.2957795786*(acos($dot/([veclength $x] * [veclength $y])))}]
}


# Computes the angle between the specified coordinates
proc ::Paratool::dihed_from_coords { coord1 coord2 coord3 coord4 } {
  set v1 [vecsub $coord1 $coord2]
  set v2 [vecsub $coord3 $coord2]
  set v3 [vecsub $coord4 $coord3]
  set cross1 [vecnorm [veccross $v2 $v1]]
  set cross2 [vecnorm [veccross $v2 $v3]]
  return [expr {57.2957795131 * acos([vecdot $cross1 $cross2])}]
}

###################################################
# Returns the difference of lists a and b,        #
# i.e all elements that occur in a, but not in b. #
###################################################

proc ::Paratool::ldiff { a b } {
   set r {}
   foreach j $a {
      if { [lsearch $b $j]==-1 } {
         lappend r $j
      }
   }
   return $r
}


###########################################################
# Returns the opposite of the intersection of two lists,  #
# i.e. all elements that occur only in one of both lists. #
###########################################################

proc ::Paratool::lnand { a b } {
   set r {}
   foreach j $a {
      if { [lsearch $b $j]==-1 } {
         lappend r $j
      }
   }
   foreach j $b {
      if { [lsearch $a $j]==-1 } {
         lappend r $j
      }
   }
   return $r
}


#############################################################
# Returns the intersection of two lists, i.e. all elements  #
# that occur at least once in both lists.                   #
#############################################################

proc ::Paratool::lintersect { a b } {
   set r {}
   foreach j $a {
      if { [lsearch $b $j]>=0 } {
         lappend r $j
      }
   }
   foreach j $b {
      if { [lsearch $a $j]>=0 } {
         lappend r $j
      }
   }
   if { [llength $r]>0 } { return [lsort -unique $r] }
}


##########################################################
# Returns the coordinate filename of a given molecule.   #
##########################################################

proc ::Paratool::get_coorfilename { molid } {
   # Get the pdb filename
   foreach i [join [molinfo $molid get filetype]] j [join [molinfo $molid get filename]] {
      if {$i!="psf"} { return $j }
   }
}


##########################################################
# Returns the coordinate filename of a given molecule.   #
##########################################################

proc ::Paratool::get_psffilename { molid } {
   # Get the pdb filename
   foreach i [join [molinfo $molid get filetype]] j [join [molinfo $molid get filename]] {
      if {$i=="psf"} { return $j }
   }
}


##################################################################
# If variable $extrabonds contains bond definitions then add     #
# these bonds to VMD's bond list.                                #
# This proc is used after startup when a list of extrabonds was  #
# provided by autopsf (which read it from the CONECT records).   #
##################################################################

proc ::Paratool::set_extrabonds {} {
   variable molidparent
   variable extrabonds
   variable complexbondlist {}

   foreach bond $extrabonds {
      foreach {segid0 resid0 name0} [lindex $bond 0] {}
      foreach {segid1 resid1 name1} [lindex $bond 1] {}
      set sel0 [atomselect $molidparent "segid $segid0 and resid $resid0 and name $name0"]
      set sel1 [atomselect $molidparent "segid $segid1 and resid $resid1 and name $name1"]
      if {[$sel0 num] && [$sel1 num]} {
	 puts "Setting extra bond from PDB CONECT: [$sel0 get {segid resid name}] -- [$sel1 get {segid resid name}]"
	 vmd_addbond [join [$sel0 list]] [join [$sel1 list]] $molidparent
	 if {[$sel0 list]<[$sel1 list]} {
	    lappend complexbondlist [list [list [list $segid0 $resid0 $name0] [list $segid1 $resid1 $name1]] 1.0]
	 } else {
	    lappend complexbondlist [list [list [list $segid1 $resid1 $name1] [list $segid0 $resid0 $name0]] 1.0]
	 }
      }
   }
}


#######################################################################
# Atom names should be consisting of the element symbol and a number. #
#######################################################################

proc ::Paratool::alias_qmtool_atomnames {} {
   ::QMtool::alias_atomnames
}


##########################################################
# Find a unique names for all atoms.                     #
##########################################################

proc ::Paratool::assign_unique_atomnames {} {
   variable molidbase
   set all [atomselect $molidbase all]
   foreach atom [$all get {name resid resname segid atomicnumber index}] {
      foreach {name resid resname segid atomnum index} $atom {}
      if {![llength $segid]} { set segid FRAG }
      set sel [atomselect $molidbase "name '[string map {' \\'} $name]' and resid $resid and segid $segid"]
      if {[$sel num]>1} {
	 set elem [::QMtool::atomnum2element $atomnum]
	 set newname [find_new_atomname $resid $segid $elem]
	 set_atomprop Name $index $newname
	 puts "Assigned unique name ([$sel num] equal atoms): $name -> $newname"
      }
      $sel delete
   }
   $all delete
}


##########################################################
# Find a unique name for the given atom                  #
##########################################################

proc ::Paratool::find_new_atomname { resid segid elem } {
   variable molidbase
   set ressel [atomselect $molidbase "resid $resid and segid $segid"]
   set newname {}
   set maxnum 99
   if {[string length $elem]==1} { set maxnum 999 }

   for {set i 1} {$i<$maxnum} {incr i} {
      set newname "$elem$i"
      if {[lsearch [$ressel get name] $newname]<0} { $ressel delete; return $newname }
   }
   for {set i 1} {$i<$maxxnum/10} {incr i} {
      foreach letter {A B C D E F G H I J K L M N P Q R S T U V W X Y Z} {
	 set newname "$elem$i$letter"
	 if {[lsearch [$ressel get name] $newname]<0} { $ressel delete; return $newname }
      }
   }
}


##########################################################
# Find type names for all atoms with no defined type.    #
# Equivalent atoms will get the same type name.          #
##########################################################

proc ::Paratool::assign_unique_atomtypes {} {
   variable molidbase
   variable topologylist
   set masslist {}
   foreach topo $topologylist {
      lappend masslist [::Toporead::topology_get types $topo]
   }
   set masslist [join $masslist]

   set alltypelist {}
   foreach massentry $masslist {
      lappend alltypelist [lindex $massentry 0]
   }

   set all [atomselect $molidbase all]
   set processedatoms {}
   foreach atom [$all get {type resid segid atomicnumber index}] {
      foreach {type resid segid atomnum index} $atom {}
      if {![llength $type] && [lsearch [join $processedatoms] $index]<0} {
	 set elem [string toupper [::QMtool::atomnum2element $atomnum]]
	 set newtype [find_new_typename $resid $segid $elem $alltypelist]
	 foreach equiv [find_all_equivalent_types $molidbase $index 3] {
	    set_atomprop Type $equiv $newtype
	    lappend processedatoms $equiv
	    puts "Assigned unique type: $type -> $newtype"
	 }
      }
   }
   $all delete
   atomedit_update_list
}

##########################################################
# Find a unique type name for the given atom             #
##########################################################

proc ::Paratool::find_new_typename { resid segid stem {existingtypes {}} } {
   variable molidbase
   set ressel [atomselect $molidbase "resid $resid and segid $segid"]
   set newtype {}
   set maxnum 9
   if {[string length $stem]==2} { 
      set maxnum 99
   } elseif {[string length $stem]==1} { 
      set maxnum 999
   }

   for {set i 1} {$i<$maxnum} {incr i} {
      set newtype "$stem$i"
      if {[lsearch [$ressel get type] $newtype]<0 && [lsearch $existingtypes $newtype]<0} {
	 $ressel delete;
	 return $newtype
      }
   }
   for {set i 1} {$i<$maxxnum/10} {incr i} {
      foreach letter {A B C D E F G H I J K L M N P Q R S T U V W X Y Z} {
	 set newtype "$stem$i$letter"
	 if {[lsearch [$ressel get type] $newtype]<0 && [lsearch $existingtypes $newtype]<0} {
	    $ressel delete;
	    return $newtype
	 }
      }
   }
}


##############################################################
# Returns the periodic table of elements in form of a list.  #
##############################################################

proc ::Paratool::get_periodic_system {} {
   return {
      H  {  1.00800 Hydrogen}
      He {  4.00260 Helium}
      Li {  6.94100 Lithium}
      Be {  9.01218 Beryllium}
      B  { 10.81100 Boron}
      C  { 12.01100 Carbon}
      N  { 14.00700 Nitrogen}
      O  { 15.99900 Oxygen}
      F  { 18.99840 Fluorine}
      Ne { 20.17970 Neon}
      Na { 22.98977 Sodium}
      Mg { 24.30500 Magnesium}
      Al { 26.98154 Aluminum}
      Si { 28.08550 Silicon}
      P  { 30.97400 Phosphorus}
      S  { 32.06000 Sulfur}
      Cl { 35.45000 Chlorine}
      K  { 39.10200 Potassium}
      Ar { 39.94800 Argon}
      Ca { 40.07800 Calcium}
      Sc { 44.95591 Scandium}
      Ti { 47.88000 Titanium}
      V  { 50.94150 Vanadium}
      Cr { 51.99610 Chromium}
      Mn { 54.93805 Manganese}
      Fe { 55.84700 Iron}
      Ni { 58.69340 Nickel}
      Co { 58.93320 Cobalt}
      Cu { 63.54600 Copper}
      Zn { 65.37000 Zinc}
      Ga { 69.72300 Gallium}
      Ge { 72.61000 Germanium}
      As { 74.92159 Arsenic}
      Se { 78.96000 Selenium}
      Br { 79.90400 Bromine}
      Kr { 83.80000 Krypton}
      Rb { 85.46780 Rubidium}
      Sr { 87.62000 Strontium}
      Y  { 88.90585 Yttrium}
      Zr { 91.22400 Zirconium}
      Nb { 92.90638 Niobium}
      Mo { 95.94000 Molybdenum}
      Tc { 98       Technetium}
      Ru {101.07    Ruthenium}
      Rh {102.9055  Rhodium}
      Pd {106.42    Palladium}
      Ag {107.8682  Silver}
      Cd {112.411   Cadmium}
      In {114.82    Indium}
      Sn {118.71    Tin}
      Sb {121.757   Antimony}
      I  {126.9045  Iodine}
      Te {127.6	    Tellurium}
      Xe {131.29    Xenon}
      Cs {132.90000 Cesium}
      Ba {137.327   Barium}
      La {138.9055  Lanthanum}
      Ce {140.115   Cerium}
      Pr {140.9077  Praseodymium}
      Nd {144.24    Neodymium}
      Pm {145	    Promethium}
      Sm {150.36    Samarium}
      Eu {151.965   Europium}
      Gd {157.25    Gadolinium}
      Tb {158.9253  Terbium}
      Dy {162.5	    Dysprosium}
      Ho {164.9303  Holmium}
      Er {167.26    Erbium}
      Tm {168.9342  Thulium}
      Yb {173.04    Ytterbium}
      Lu {174.967   Lutetium}
      Hf {178.49    Hafnium}
      Ta {180.9479  Tantalum}
      W  {183.85    Tungsten}
      Re {186.207   Rhenium}
      Os {190.2	    Osmium}
      Ir {192.22    Iridium}
      Pt {195.08    Platinum}
      Au {196.9665  Gold}
      Hg {200.59    Mercury}
      Tl {204.3833  Thallium}
      Pb {207.2	    Lead}
      Bi {208.9804  Bismuth}
      Po {209	    Polonium}
      At {210	    Astatine}
      Pa {213.0359  Protactinium}
      Rn {222	    Radon}
      Fr {223	    Francium}
      Ra {226.0254  Radium}
      Ac {227	    Actinium}
      Th {232.0381  Thorium}
      Np {237.0482  Neptunium}
      U  {238.0289  Uranium}
   }
}


#############################################################
# Returns mass, name, or ordinal number for a given element #
# symbol.                                                   #
#############################################################

proc ::Paratool::get_periodic_element { type elem } {
   array set periodic [get_periodic_system]
   set element    "[string toupper [string index $elem 0]]"
   append element "[string tolower [string index $elem 1]]"
   set elementinfo [lindex [array get periodic $element] 1]
   switch [string tolower $type] {
      mass   { return [lindex $elementinfo 0] }
      name   { return [lindex $elementinfo 1] }
      ordnum { return [expr {[lsearch [array names periodic] $elem]+1}] }
   }
}


#############################################################
# Tries to guess the chemical element from the given mass.  #
# Only works correctly for lower ordinal numbers!           #
#############################################################

proc ::Paratool::mass2element { mass } {
   set periodic [get_periodic_system]
   foreach {elem data} $periodic {
      if {round($mass*10)==round([lindex $data 0])*10} {
	 return $elem
      }
   }
   return {}
}


#############################################################
# Returns a list of atoms describing the tree of bonded     #
# atoms starting with a root of $visited--$atom1.           #
# (Recursive proc; This is why I call the root $visited,    #
# these are the atoms that were visited already and atom0   #
# is the first visited atom.)                               #
#############################################################

proc ::Paratool::bondedsel { molid atom1 {visited {}} {maxdepth 20} {depth 0} } {
   set sel1 [atomselect $molid "index $atom1"]
   set bonds [join [$sel1 getbonds]]
   if {![llength $bonds]} { return }
   if {[llength $visited]} {
      set nbsel [atomselect $molid "index [join [$sel1 getbonds]] and not index [join $visited]"]
   } else {
      set nbsel [atomselect $molid "index [join [$sel1 getbonds]]"]
   }
   #puts "atom1=$atom1; [$nbsel list]; $depth"

   incr depth
   if {$depth>$maxdepth} { return }

   lappend visited $atom1
   if {![$nbsel num]} { return $atom1 }

   foreach nb [$nbsel list] {
      lappend visited [bondedsel $molid $nb $visited $maxdepth $depth]
   }

   return [lsort -unique -integer [join $visited]]
}


#############################################################
# Returns a list of atoms that are 1-n bonded with respect  #
# to atom $visited.                                         #
# (Recursive proc; This is why I call the root $visited,    #
# these are the atoms that were visited already and atom0   #
# is the first visited atom.)                               #
#############################################################

proc ::Paratool::n-bondedsel { molid atom1 {visited {}} {maxdepth 20} {depth 0} {found {}} } {

   set sel1 [atomselect $molid "index $atom1"]
   set nbsel {}
   if {[llength $visited]} {
      set nbsel [atomselect $molid "index [join [$sel1 getbonds]] and not index [join $visited]"]
   } else {
      set nbsel [atomselect $molid "index [join [$sel1 getbonds]]"]
   }
   #puts "atom1=$atom1; nbsel=[$nbsel list]; depth=$depth; found=$found"

   incr depth
   if {$depth>$maxdepth} { return }

   lappend visited $atom1
   if {$depth==$maxdepth} { return [list $atom1 $atom1]}
   if {![$nbsel num]} { return [list $atom1 {}]}

   foreach nb [$nbsel list] {
      set ret [n-bondedsel $molid $nb $visited $maxdepth $depth $found]
      lappend visited [lindex $ret 0]
      lappend found   [lindex $ret 1]
   }

   return [list [lsort -unique -integer [join $visited]] [lsort -unique -integer [join $found]]]
}


#############################################################
# Return a list of atoms of the same chemical element,      #
# bonded to the same mother atom and having the same        #
# ligands as atom $index.                                   #
#############################################################

proc ::Paratool::find_equivalent_types { molid index dist } {
   set sel [atomselect $molid "index $index"]
   set bonds [join [$sel getbonds]]
   set atomnum [$sel get atomicnumber]
   $sel delete

   if {$atomnum<1} { return }
   
   # Check all neighbors for motherhood
   set indexlist {}
   foreach neighbor $bonds {
      set mothersel [atomselect $molid "index $neighbor"]
      set children [join [$mothersel getbonds]]
      $mothersel delete
      if {[llength $children]<=1} { continue }
      #puts "nb=$neighbor"
      # Get list of other children of the same mother, not including self
      set otherchildren [lsearch -not -all -inline $children $index]
      set othersel [atomselect $molid "index $otherchildren"]
      #puts "oc=$otherchildren"

      # Loop over the brothers
      foreach otherindex [$othersel get index] otheratomnum [$othersel get atomicnumber] otherbonds [$othersel getbonds] {
	 if {$atomnum==$otheratomnum} {
	    set selfsmile  [get_smiles $molid $neighbor $index $dist]
	    set othersmile [get_smiles $molid $neighbor $otherindex $dist]
	    #puts "ssm=$selfsmile"
	    #puts "osm=$othersmile"
	    if {$othersmile==$selfsmile} {
	       lappend indexlist $otherindex
	    }
	 }
      }
      $othersel delete
   }
   return $indexlist
}

#############################################################
# Return a list of atoms of the same chemical element,      #
# having the same chemical environment up to $dist bonds    #
# away from atom $index.                                    #
#############################################################

proc ::Paratool::find_all_equivalent_types { molid index dist } {
   set sel [atomselect $molid "index $index"]
   set atomnum [$sel get atomicnumber]
   $sel delete

   if {$atomnum<1} { puts noelem; return }

   set selfsmile [get_all_smiles $molid $index $dist]

   # Check all atoms of the same element for motherhood
   set indexlist {}
   set all [atomselect $molid "atomicnumber $atomnum"]
   foreach other [$all list] {
      #puts "other=$other"

      set othersmile [get_all_smiles $molid $other $dist]
      #puts "ssm=$selfsmile"
      #puts "osm=$othersmile"
      if {$othersmile==$selfsmile} {
	 lappend indexlist $other
      }
   }
   return $indexlist
}

proc ::Paratool::compute_dipolemoment {sel {center {0 0 0}}} {
   if {[string tolower $center]=="com"} { set center [measure center $sel] }
   set dipole {0 0 0}
   foreach i [$sel get index] r [$sel get {x y z}] q [$sel get charge] {
      set dipole [vecadd $dipole [vecscale $q [vecsub $r $center]]]
   }
   set debye 4.77350732929
   return [vecscale $dipole $debye]
}

proc ::Paratool::compute_dipolemoment_esp {sel {center {0 0 0}}} {
   if {[string tolower $center]=="com"} { set center [measure center $sel] }
   set dipole {0 0 0}
   foreach i [$sel get index] r [$sel get {x y z}] {
      set q [get_atomprop ESP $i]
      set dipole [vecadd $dipole [vecscale $q [vecsub $r $center]]]
   }
   set debye 4.77350732929
   return [vecscale $dipole $debye]
}


################################################################
# Returns a SMILES string for a molecular subtree, i.e. all    #
# atoms connected to a mother atom through it's child $child.  #
# The SMILES is unique for each topology and can be used to    #
# compare topologies of molecular components.                  #
################################################################

proc ::Paratool::get_SMILES { molid mother child } {
   set csel [atomselect $molid "index $child"]
   set bonds [join [$csel getbonds]]
   set bondorders [join [$csel getbondorders]]
   set elem [::QMtool::atomnum2element [$csel get atomicnumber]]
   set smiles $elem
   if {[llength $bonds]==0} { return }
   if {[llength $bonds]==1} { 
      return $smiles
   }

   # Get list of all children of child
   #set grandchildren [lsearch -inline -not -all $bonds $mother]
   set grandchildren $bonds

   set max [llength $grandchildren]
   set i 1
   set childsmilelist {}
   foreach grandchild $grandchildren bondo $bondorders {
      if {$grandchild==$mother} { incr i; continue }

      set childsmile {}
      if {$bondo==2} { 
	 set childsmile "="
       } elseif {$bondo==3} { 
 	 set childsmile "\#"
       }

      append childsmile [get_SMILES $molid $child $grandchild]
      lappend childsmilelist $childsmile
   }
   # Sorting the branches makes the SMILES unique
   set newchildsmilelist [lsort $childsmilelist]

   foreach childsmile $newchildsmilelist {
      if {$i==$max} {
	 append smiles $childsmile
      } else {
	 append smiles ($childsmile)
      }
      incr i
   }

   return $smiles
}

################################################################
# Returns a SMILES string for a molecular subtree, i.e. all    #
# atoms connected to a mother atom through it's child $child.  #
# The SMILES is unique for each topology and can be used to    #
# compare topologies of molecular components.                  #
################################################################

proc ::Paratool::get_smiles { molid mother child maxdepth } {
   return [get_smiles_from_tree [get_molecular_tree $molid $mother $child $maxdepth]]
}

proc ::Paratool::get_all_smiles { molid mother maxdepth } {
   set sel [atomselect $molid "index $mother"]
   set allsmiles {}
   foreach child [join [$sel getbonds]] {
      lappend allsmiles [get_smiles_from_tree [get_molecular_tree $molid $mother $child $maxdepth]]
   }
   return [lsort $allsmiles]
}

proc ::Paratool::get_smiles_from_tree { tree } {
   set smiles {}
   set bo [lindex $tree 2]

   if {$bo==2} {
      append smiles "=[lindex $tree 1]"
   } elseif {$bo==3} {
      append smiles "\#[lindex $tree 1]"
   } else {
      append smiles [lindex $tree 1]
   }

   # Search the children
   if {[llength $tree]==4} { 
      set i 1
      set childsmilelist {}
      set childtree [lindex $tree 3]
      set num [llength $childtree]
      foreach entry $childtree {
	 # Recursion
	 lappend childsmilelist [get_smiles_from_tree $entry]
      }
#puts $childsmilelist
      # Sorting the branches makes the SMILES unique
      set newchildsmilelist [lsort $childsmilelist]
      #set newchildsmilelist [lsort -command compare_string_length $childsmilelist]

      foreach childsmile $newchildsmilelist {
	 if {$i<$num} { 
	    append smiles "($childsmile)"
	 } else {
	    append smiles $childsmile
	 }
	 incr i 
      } 
   }
   return $smiles
}

#26 O 1.0 {27 P 1.0 {29 O 1.0 {50 H 1.0}} {30 O 1.0 {51 H 1.0}} {28 O 2.0}}
proc ::Paratool::get_molecular_tree { molid mother child maxdepth } {
   global molecular_tree_counter
   if {[info exists molecular_tree_counter]} {
      incr molecular_tree_counter
   } else { set molecular_tree_counter 0 }

   global molecular_tree_knownatoms_${molecular_tree_counter}
   set molecular_tree_knownatoms_${molecular_tree_counter} {}

   set tree [get_molecular_subtree $molid $mother $child 0 $maxdepth molecular_tree_knownatoms_${molecular_tree_counter}]

   unset molecular_tree_knownatoms_${molecular_tree_counter}

   return $tree
}

proc ::Paratool::get_molecular_subtree { molid mother child depth maxdepth knownatoms } {
   global $knownatoms
   lappend $knownatoms $mother

   set csel [atomselect $molid "index $child"]
   set grandchildren [join [$csel getbonds]]
   set bondorders    [join [$csel getbondorders]]
   set elem [::QMtool::atomnum2element [$csel get atomicnumber]]
#   set ring {}
   if {[llength $grandchildren]==0} { return }
   if {[llength $grandchildren]==1} { 
      return [list $child $elem $bondorders {}]
   }

   # Get bondorder for bond to mother:
   set bom [lindex $bondorders [lsearch $grandchildren $mother]]

   incr depth
   if {$depth>=$maxdepth} { return [list $child $elem $bom {}] }

   set grandchilddef {}
   foreach grandchild $grandchildren bondo $bondorders {
      if {$grandchild==$mother} { continue }
      if {[lsearch [subst $[subst $knownatoms]] $grandchild]<0} { 
#	 lappend $knownatoms $grandchild
#	 puts $grandchild
      } else { 
	 puts "ring=$grandchild"; 
	 continue
      }
      lappend grandchilddef [get_molecular_subtree $molid $child $grandchild $depth $maxdepth $knownatoms]
   }
   set childdef [list $child $elem $bom]
   # sort after bondorders
# FIXME somehow the smiles don't get sorted the way I want...
   set tmpchilddef [lsort -real -index 2 $grandchilddef]
   set tmpchilddef2 [lsort -index 1 $tmpchilddef]
   set childdefsortbysize [lsort -index 3 -command compare_llength $tmpchilddef2]
   lappend childdef $childdefsortbysize

   return $childdef
}
#38 C 1.0 {{39 C 2.0 {{40 H 1.0} {41 C 1.0 {{42 H 1.0} {43 C 2.0 {{44 H 1.0} {47 C 1.0 {{45 C 2.0 {{46 H 1.0}}} {48 H 1.0}}}}}}}}}}

proc ::Paratool::compare_string_length {s1 s2} {
   if {[string length $s1]>[string length $s2]} {
      return 1
   } elseif {[string length $s1]==[string length $s2]} {
      return 0
   } else {
      return -1
   }
}
proc ::Paratool::compare_llength {s1 s2} {
   if {[string length $s1]>[llength $s2]} {
      return 1
   } elseif {[llength $s1]==[llength $s2]} {
      return 0
   } else {
      return -1
   }
}

proc ::Paratool::deepsearch_moltree { list index pattern {pos 0} } {
   if {[lindex $list $index]==$pattern} { return $pos }
   if {[llength $list]==4} { lappend pos -1; return $pos }

   # Search the children
   set i 0
   foreach entry [lindex $list 4] {
      # puts "pos=$pos"
      set newpos [deepsearch $entry $index $pattern [join [list $pos $i]]]
      # puts "newpos=$newpos"
      if {[lindex $newpos end]>-1} { return $newpos }
      incr i 
   } 

   lappend pos -1
   return $pos
}

proc ::Paratool::set_moltree_ringstart { tree index ring } {
   set treepos [deepsearch_moltree $tree 0 $index]
   set listpos [lrange [string map {" " " 3 "} $treepos] 1 end]
   lset tree [join [list $listpos 3]] $ring
}


##########################################################
# Finds rings in the molecule.                           #
# For each ring a list of atom indices describing the    #
# ring is returned.                                      #
##########################################################

proc ::Paratool::find_rings {molid} {
   set rings [_find_rings_recursive 0 $molid]
   if {![llength $rings]} {
      return {}
   }

   foreach ring $rings {
      lappend sorted [lsort -unique -integer $ring]
   }

   set allrings [lindex [sort_alike $rings $sorted -unique] 0]

   return [ring_unique $allrings]
}


##########################################################
# Recursive helper function for find_rings.              #
# Returns a non-unique list of rings which have to be    #
# sorted and cleaned by find_rings. I.e. rings appear    #
# multiple times in the list if they were entered from   #
# different points or traversed in different directions. #
##########################################################

proc ::Paratool::_find_rings_recursive {index molid {atrace {}}} {
   set pos [lsearch $atrace $index]
   if {$pos>=0} {
      # Ring found!
      set found [lrange $atrace $pos end]
      set smallest [lsearch $found [lindex [lsort -integer $found] 0]]
      return [concat [lrange $found $smallest end] [lrange $found 0 [expr {$smallest-1}]]]
   }
   set rings {}
   set sel [atomselect $molid "index $index"]

   foreach child [join [$sel getbonds]] {
      if {$child == [lindex $atrace end]} {
	 # Don't just go back to grandma (avoid two membered rings)
	 continue
      }
      
      set ret [_find_rings_recursive $child $molid [concat $atrace $index]]
      if {[llength $ret]} {
	 if {[llength $ret]>1 && [string is integer [lindex $ret 0]]} {
	    lappend rings $ret
	 } else {
	    set rings [concat $rings $ret]
	 }
      }
   }
   $sel delete
   
   if {[llength $rings]} {
      # Crawling up the recursive tree
      return [lsort -unique $rings]
   }

   # If we have no children other than our own grandma we found a tree end
   return {}
}

# Removes rings that enclose other rings from the ringlist
proc ::Paratool::ring_unique {ringlist} {
   set i 1
   set badrings {}
   # Compare all rings, if the overlap>2 then the smaller ring
   # is part of the larger one.
   foreach ring1 $ringlist {
      foreach ring2 [lrange $ringlist $i end] {
	 #puts "$ring1 -- $ring2"
	 set compare [ring_compare $ring1 $ring2]	 
	 if {[llength $compare]>2} {
	    if {[llength $ring1]>[llength $ring2]} {
	       lappend badrings $ring1
	    } else {
	       lappend badrings $ring2
	    }
	 }
      }
      incr i
   }

   # Exclude the enclosing rings from the ringlist
   set uniquerings {}
   foreach ring $ringlist {
      if {[lsearch $badrings $ring]<0} {
	 lappend uniquerings $ring
      }
   }
   return $uniquerings
}


# Compare two rings, return the longest common chain
proc ::Paratool::ring_compare {ring1 ring2} {
   set d1 [concat $ring1 $ring1]
   set d2 [concat $ring2 $ring2]
   set sub [lcontains $d1 $d2 -all]
   set rsub [lcontains $d1 [lrevert $ring2] -all]

   set best {}
   set maxlen 0
   foreach frag [concat $sub $rsub] {
      if {[llength $frag]>$maxlen} {
	 set maxlen [llength $frag]
	 set best $frag
      }
   }

   #if {[llength $best]<1} { puts "SEPARATE" }
   #if {[llength $best]==1} { puts "TOUCH" }
   #if {[llength $best]==2} { puts "ADJACENT" }
   #if {[llength $best]>2} { puts "SUBRING" }
   return $best
}


# Returns the last index in which two lists are equal.
# Returns -1 if the lists differ from the beginning.
proc lcompare { a b } {
   set c -1
   foreach i $a j $b {
      if { $i!=$j } {
	 return $c
      }
      incr c
   }
   return $c
}


# Returns the first sublist of b that is contained in a  
proc ::Paratool::lcontains {a b args} {
   set all [getswitch $args "-all"]
   set listofsame {}
   set posb 0
   set last 0
   set first 0
   for {set posb 0} {$posb<[llength $b]} {incr posb} {
      set elem [lindex $b $posb]
      set posa [lsearch -start $first $a $elem]

      if {$posa>=$first && $first<[llength $a]} {
	 set last [lcompare [lrange $a $posa end] [lrange $b $posb end]]
	 lappend listofsame [lrange $b $posb [expr {$posb+$last}]]
	 #puts "last=$last first=$first posa=$posa posb=$posb"
	 set posb  [expr {$posb+$last}]
	 set first [expr {$posa+$last+1}]
	 if {!$all || $last<0} { return [join $listofsame] }
      } 
   }

   return $listofsame
}

proc ::Paratool::ring_order {ring ind1 {ind2 {}}} {
   set pos1 [lsearch $ring $ind1]
   if {$pos1<0} { return }
   set neworder [concat [lrange $ring $pos1 end] [lrange $ring 0 [expr {$pos1-1}]]]
   if {[llength $ind2]} {
      if {[lsearch $neworder $ind2]>[llength $ring]/2.0} {
	 set neworder [concat $ind1 [lrevert [lrange $neworder 1 end]]]
      }
   }
   return $neworder
}

proc ::Paratool::atom_in_ring {index} {
   variable ringlist
   set found {}
   set i 0
   foreach ring $ringlist {
      set pos [lsearch $ring $index]
      if {$pos>=0} {
	 lappend found $i
      }
      incr i
   }
   return $found
}

proc ::Paratool::bond_in_ring {ind1 ind2} {
   variable ringlist
   set found {}
   set i 0
   foreach ring $ringlist {
      set pos1 [lsearch $ring $ind1]
      if {$pos1>=0} {
	 set pos2 [lsearch $ring $ind2]
	 if {$pos2>=0 && (abs($pos2-$pos1)==1 || abs($pos2-$pos1)==[llength $ring]-1)} {
	    lappend found $i
	 }
      }
      incr i
   }
   return $found
}

proc ::Paratool::angle_in_ring {ind1 ind2 ind3} {
   variable ringlist
   set found {}
   set i 0
   foreach ring $ringlist {
      set pos2 [lsearch $ring $ind2]
      if {$pos2>=0} {
	 set pos1 [lsearch $ring $ind1]
	 if {$pos1>=0 && (abs($pos1-$pos2)==1 || abs($pos1-$pos2)==[llength $ring]-1)} {
	    set pos3 [lsearch $ring $ind3]
	    if {$pos3>=0 && (abs($pos3-$pos2)==1 || abs($pos3-$pos2)==[llength $ring]-1)} {
	       lappend found $i
	    }
	 }
      }
      incr i
   }
   return $found
}

##########################################################
# Sorts elements in list1 in the same way as list2 would #
# be sorted using the rules given in args.               #
# Example:                                               #
# sort_alike {a b c d} {3 2 4 1} -integer                #
# --> c b d a                                            #
##########################################################

proc ::Paratool::sort_alike { list1 list2 args } {
   set index {}
   if {[lsearch $args "-index"]>=0}  {
      set index [lindex $args [expr {1+[lsearch $args "-index"]}]]
   }

   foreach s $list1 t $list2 {
      if {[llength $index]} {
	 lappend combined [list $s [lindex $t $index]]
      } else {
	 lappend combined [list $s $t]
      }
   }

   foreach pair [eval lsort $args -index 1 [list $combined]] {
      lappend sorted1 [lindex $pair 0]
      lappend sorted2 [lindex $pair 1]
   }
   return [list $sorted1 $sorted2]
}

