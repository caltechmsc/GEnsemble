############################################################
#
#   This file contains procedures to join compounds of atoms that are
# wrapped around unit cell boundaries.
#
# $Id: pbcjoin.tcl,v 1.3 2007/02/27 17:09:55 johns Exp $
#

package provide pbcjoin 2.0

namespace eval ::PBCTools:: {
    namespace export pbc*
    ############################################################
    #
    # pbcjoin [OPTIONS...]
    #
    #   Joins compounds (residues, chains, segments) of atoms, so that
    # they are not split anymore. 
    # 
    # OPTIONS:
    #   -molid $molid|top   the molecule to use (default: top)
    #   -first $first|first|now 
    #                       the first frame to use (default: now)
    #   -last $last|last|now
    #                       the last frame to use (default: now)
    #   -all|allframes      equivalent to "-first first -last last"
    #   -now                equivalent to "-first now -last now"
    #   -sel $sel           the selection of atoms to be joined
    #                       (default: all)
    #   -compound res[idue]|seg[ment]|chain|none
    #                       the type of compound that should be joined. If
    #                       the distance of any atom of a compound is
    #                       larger than half the box length, it will not
    #                       be joined correctly.
    #                       (default: residue)
    #
}
