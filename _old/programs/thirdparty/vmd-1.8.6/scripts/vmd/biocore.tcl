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
#       $RCSfile: biocore.tcl,v $
#       $Author: johns $        $Locker:  $             $State: Exp $
#       $Revision: 1.7 $        $Date: 2007/01/12 20:11:31 $
#
############################################################################
#
# BioCoRE web-based script bootstrap code 
#
# $Id: biocore.tcl,v 1.7 2007/01/12 20:11:31 johns Exp $
#

# http 2.4 provides a -binary option to geturl which is need for downloading
# binary trajectory files.
package require http 2.4

#
# Check for BioCoRE special startup, downloading and executing a 
# bootstrap script from a URL passed in through a BIOCORE_URL 
# environment variable.
#
proc check_biocore {} {
  global env
  global tcl_platform

  if { [catch {set url $env(BIOCORE_URL)} foo] } {
#    puts "Failed to detect BioCoRE URL."
#    puts "Reason: $foo"
    set url ""
  } else {
    set url $env(BIOCORE_URL)
  }

  switch $tcl_platform(platform) {
    windows {
      set tmpfile [file join / vmd[pid]biocore.tcl]
    }
    default {
      set tmpfile [file join $env(TMPDIR) vmd[pid]biocore.tcl]
    }
  }     

  if {[string length $url] > 0} {
    puts "Initiating automatic download of BioCoRE scripts..."
    puts "BioCoRE URL: $url"
    vmdhttpcopy $url $tmpfile
    if {[file exists $tmpfile] > 0} {
      source $tmpfile
      file delete -force $tmpfile
    } else {
      puts "Failed to create temporary BioCoRE script file."
    }
  }
}


# Copy a URL to a file and print meta-data
proc vmdhttpcopy { url file {chunk 4096} } {
  set out [open $file w]
  set token [::http::geturl $url -channel $out -progress vmdhttpProgress \
	-blocksize $chunk -binary 1]
  close $out
  # This ends the line started by http::Progress
  puts stderr ""
  upvar #0 $token state
  set max 0
  foreach {name value} $state(meta) {
    if {[string length $name] > $max} {
      set max [string length $name]
    }
    if {[regexp -nocase ^location$ $name]} {
      # Handle URL redirects
      puts stderr "Location:$value"
      return [copy [string trim $value] $file $chunk]
    }
  }
  incr max

#  foreach {name value} $state(meta) {
#    puts [format "%-*s %s" $max $name: $value]
#  }

  return $token
}

proc vmdhttpProgress {args} {
  puts -nonewline stderr . ; flush stderr
}

