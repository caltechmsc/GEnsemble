#!/usr/local/bin/perl -w

# This little perl script takes in a bgf file and converts it into a pdb file.  The results are printed in the buffer.


# conectivity format:
# 

use strict;

($#ARGV < 1) or die "No bgf file provided!  This file takes in a bgf file and prints in the buffer the the same structure in pdb format.  \n\nUsage: $0 bgf_file\nOutput: in buffer.\n";

# Variables 

my $bgf_file = $ARGV[0];
my $current_line;
my @current_fields;
my $chain_designation_flag = 1;      # some bgf files don't have a chain designator.


# Prints header info on pdb file.


print "HEADER $bgf_file converted to pdb format using bgf2pdb.pl\n";


# Main Body


open BGF_FILE, $bgf_file or die "Can't open $bgf_file! Make sure you have the right file. #!\n";


while (<BGF_FILE>) {
    if (/^REMARK/) { print; }
    if ((/^ATOM/) || (/^HETATM/)) {
	$current_line = $_;
	@current_fields = split;
	my $check_alphabet = substr $current_line, 23, 1;
	if (!($check_alphabet =~ /\w/)) {  $chain_designation_flag = 0; }
	if ($chain_designation_flag == 1) {
  # quirks in pdb formats.  H's have a different format from the other common atoms.  Hence the if-else control structure below.  

	    if (substr($current_line, 13, 1) eq " ") {

		printf "%-6s%5g  %-3s %3s %1s%4g    %8.3f%8.3f%8.3f\n", $current_fields[0], $current_fields[1], $current_fields[2], $current_fields[3], $current_fields[4], $current_fields[5], $current_fields[6], $current_fields[7], $current_fields[8], $current_fields[9];

	    } else {
#elsif (substr($current_line, 13, 1) eq "H") 
	     printf "%-6s%5g %-4s %3s %1s%4g    %8.3f%8.3f%8.3f\n", $current_fields[0], $current_fields[1], $current_fields[2], $current_fields[3], $current_fields[4], $current_fields[5], $current_fields[6], $current_fields[7], $current_fields[8], $current_fields[9];
	   } 

	} else {

	    if (substr($current_line, 13, 1) eq " ") {

		printf "%-6s%5g  %-3s %3s %5g    %8.3f%8.3f%8.3f\n", $current_fields[0], $current_fields[1], $current_fields[2], $current_fields[3], $current_fields[4], $current_fields[5], $current_fields[6], $current_fields[7], $current_fields[8];

	    } else {
#elsif (substr($current_line, 13, 1) eq "H")
	     printf "%-6s%5g %-4s %3s %5g    %8.3f%8.3f%8.3f\n", $current_fields[0], $current_fields[1], $current_fields[2], $current_fields[3], $current_fields[4], $current_fields[5], $current_fields[6], $current_fields[7], $current_fields[8];
	 } 


	}


    }

    
#    if ((/^FORMAT CONECT/) || (/^FORMAT ORDED/)) {};

  # while pdb file do not require conect info for ATOM entries (HETATM entries are required), this scripts writes them out anyway. 

#    if (/^CONECT/) {
#	print "CONECT";
#	$current_line = $_;
#	@current_fields = split;
#	if ($#current_fields >= 6 ) {     # hopefully no atom has >= 8 bonds.  
#	    shift @current_fields;
#	    my $conect_atom = shift @current_fields;
#	    printf "%5g%5g%5g%5g%5g\n", $conect_atom, shift @current_fields, shift @current_fields, shift @current_fields, shift @current_fields;
## $current_fields[1], $current_fields[2], $current_fields[3], $current_fields[4], $current_fields[5];
#	    printf "CONECT%5g", $conect_atom;
#	    
#	    
#	    for (@current_fields) {
#		printf "%5g", $_;
#	    } 
#	    print "\n";
#	}  
#  # pdb file conect info only allow 4 bonds to an atom in one line.  if an atom makes more than 4 bonds, 
#  # that info continues on the next line.
#
#
#	  else {
#	    shift @current_fields;
#	    for (@current_fields) {
#		printf "%5g", $_;
#	    }
#	    printf "\n";
#	}
#    }

    if (/^END/) { print "END\n"; last}



}
