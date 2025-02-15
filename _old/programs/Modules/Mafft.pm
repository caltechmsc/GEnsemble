package Modules::Mafft;

use FindBin qw($Bin);
use lib $FindBin::Bin;

use strict;
use warnings;
use base 'Exporter';
use File::Copy;
use Time::Local;

our $VERSION = '1.00'; 
our @EXPORT = qw(mafft);

#####################################################################
#                                                                   #
# PREDICTM                                                          #
#                                                                   #
# Copyright (c) 2007                                                #
# Adam R. Griffith, Ravinder Abrol, and William A. Goddard III      #
# Materials and Process Simulation Center                           #
# California Institute of Technology                                #
# Pasadena, CA, USA                                                 #
# All Rights Reserved.                                              #
#                                                                   #
# Uses ClustalW 1.83:                                               #
# Chenna, et al. "Multiple sequence alignment with the Clustal      #
# series of programs." (2003)                                       #
# _Nucleic Acids Res_ 31 (13):3497-500 PubMedID: 12824352           #
#                                                                   #
# Uses MAFFT 6.240:                                                 #
# MAFFT v6.240 (2007/04/04)  Copyright (c) 2006 Kazutaka Katoh      #
# http://align.bmr.kyushu-u.ac.jp/mafft/software/                   #
# NAR 30:3059-3066, NAR 33:511-518                                  #
#                                                                   #
#####################################################################

################################################################################
### Public subroutines                                                       ###
################################################################################
sub mafft {
    my $sequences          = shift;
    my $mafft_executable   = shift;
    my $mafft_binaries     = shift;
    my $clustal_executable = shift;
    my $prefix;
    if ($sequences =~ /\.txt$/) {
	($prefix = $sequences) =~ s/\.txt//;
    } else {
	($prefix = $sequences) =~ s/\.fta//;
    }

    if (! -e "$sequences") {
	die "Mafft :: Sequences file not found!\n";
    } elsif (($sequences !~ /.txt/) && ($sequences !~ /.fta/)) {
	die "Mafft :: Sequences file not correct: $sequences\n";
    }

    $ENV{MAFFT_BINARIES} = "${Bin}/$mafft_binaries";
    `(${Bin}/$mafft_executable --op 10.0 --ep 0.2 --genafpair $sequences > tmp.pir) >& $prefix.mafft.out`;

    # Note that the MAFFT PIR format does not conform to the Clustal PIR format used in
    # the PredicTM Package.  The following section fixes this.

    open PIR, "tmp.pir";
    my $firstline = 1;
    my $pirtext = "";
    while (<PIR>) {
	if (/^>/) {
	    if ($firstline) {
		$_ =~ s/>/>P1;/;
		$pirtext .= "$_" . "\n";
		undef $firstline;
	    } else {
		$_ =~ s/>/>P1;/;
		$pirtext .= "\*" . "\n" . "$_" . "\n";
	    }
	} else {
	    $pirtext = $pirtext .= "$_";
	}
    }
    $pirtext = $pirtext . "\*" . "\n";
    close PIR;

    my $outpirfile = $prefix . ".pir";
    open PIR, ">$outpirfile";
    print PIR "$pirtext";
    close PIR;
    unlink "tmp.pir";

    # Convert PIR file to ALN file
    my $outalnfile = $prefix . ".aln";
    `${Bin}/$clustal_executable -infile=${prefix}.pir -convert -outfile=${prefix}.aln`;

    return 1;
}

# v-- This line must be included --v 
1;
