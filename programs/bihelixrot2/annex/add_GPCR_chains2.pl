#!/usr/bin/perl -w

use strict;

($#ARGV >=0 ) or die "Must specify input bgf file! \nUsage: $0 input_bgf_file\nFunction: This script specifically adds chain names to a rotmin GPCR file without chain names.\nOutput: in buffer.\n";

my $infile = $ARGV[0];

open INFILE, $infile or die "Can't open $infile!!! $!\n";

my @ABCDEFG = qw/A B C D E F G/;
my $chain_c = -1;
my $crnt_chain_designator = $ABCDEFG[$chain_c];

my $last_res_pstn = -1;
my $crnt_res_pstn = -1;

while (<INFILE>) {
    
    if (/^ATOM/ || /^HETATM/) {
	my $cur_line = $_;

	$last_res_pstn = $crnt_res_pstn;
	$crnt_res_pstn = &res_pstn($cur_line);

	if ($crnt_res_pstn-$last_res_pstn > 1) {
	    $chain_c++;
	    $crnt_chain_designator = $ABCDEFG[$chain_c];
	}
	
	substr($cur_line, 23, 1) = $crnt_chain_designator;
	print $cur_line;
    } else {
	print;
    }
}



sub res_pstn {
    substr($_[0], 25, 5);
}
