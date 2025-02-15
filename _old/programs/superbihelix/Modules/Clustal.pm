package Modules::Clustal;

use FindBin qw($Bin);
use lib $FindBin::Bin;

use strict;
use warnings;
use base 'Exporter';
use File::Copy;
use Time::Local;

our $VERSION = '1.00'; 
our @EXPORT = qw(clustal
		 clustalpairwise);

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
sub clustal {
    my $sequences          = shift;
    my $clustal_executable = shift;
    my $prefix;
    if ($sequences =~ /\.txt$/) {
	($prefix = $sequences) =~ s/\.txt//;
    } else {
	($prefix = $sequences) =~ s/\.fta//;
    }

    if (! -e "$sequences") {
	die "Clustal :: Sequences file not found!\n";
    } elsif (($sequences !~ /.txt/) && ($sequences !~ /.fta/)) {
	die "Clustal :: Sequences file not correct: $sequences\n";
    }

    my $clustalinput;
    $clustalinput = 
	"1\n".
	"$sequences\n".
	"2\n".
	"9\n".
	"2\n".
	"9\n".
	"\n".
	"1\n".
	"\n".
	"\n".
	"y\n".
	"x\n".
	"\n".
	"x\n";

    open IN, ">clustal_input";
    print IN "$clustalinput";
    close IN;

    my $output = "$prefix" . "clustal.out";

    `${Bin}/$clustal_executable < clustal_input > $output`;

    unlink "clustal_input";
    unlink "y";

    return 1;
}

sub clustalpairwise {
    my $seq1               = shift;
    my $seq2               = shift;
    my $clustal_executable = shift;

    if (!$seq1 || !$seq2) {
	die "Clustal :: One or both sequence inputs are incorrect.\n";
    }

    open  SEQ1, ">seq1.fta";
    print SEQ1 "$seq1";
    close SEQ1;

    open  SEQ2, ">seq2.fta";
    print SEQ2 "$seq2";
    close SEQ2;

    my $clustalin = "-profile1=seq1.fta -profile2=seq2.fta -sequences";

    my $clustalout = 
	`${Bin}/$clustal_executable $clustalin`;

    $clustalout =~ /Sequences\s+\(\d+\:\d+\)\s+Aligned\.\s+Score\:\s+(\d+)/;
    my $seqid = $1;

    unlink "seq1.fta";
    unlink "seq2.fta";
    unlink "seq2.aln";
    unlink "seq2.dnd";

    return $seqid;
}

# v-- This line must be included --v 
1;
