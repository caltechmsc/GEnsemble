#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
}

use Cwd;
use File::Basename;
use File::Copy;
use File::Path;
use File::Spec;
use Getopt::Long;
use LWP::Simple;
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

if (@ARGV == 0) { help(); }
$out = "default.out";
GetOptions ('h|help'        => \$help,
            'scream=s'      => \$screamfile,
	    'onee=s'        => \$oneefile,
	    'min=s'         => \$minfile,
	    'o|output=s'    => \$output);

if ($help) { help(); }
if (! -e $screamfile)              { die "Could not find SCREAM energies\n"; }
if (! -e $oneefile)                { die "Could not find MPSim oneE energies\n"; }
if (($minfile) && (! -e $minfile)) { die "Could not find MPSim minimized energies\n"; }
if (! $output)                     { die "No output file given\n"; }

# List of energy sets
if ($minfile) {
    @list = ("$minfile", "$oneefile", "$screamfile");
} else {
    @list = ("$oneefile", "$screamfile");
}


%energy;
%structures;

# Read energies
foreach $item (@list) {

    open ENG, "$item";
    @LINES = <ENG>; shift @LINES; shift @LINES;
    close ENG;

    foreach $line (@LINES) {
	$line =~ /(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)/;

	$structure = $1;
	$total     = $2;
	$nihvdw    = $3;
	$navdw     = $4;
	$ihb       = $5;

	$energy{$structure}{$item}{total}  = $total;
	$energy{$structure}{$item}{nihvdw} = $nihvdw;
	$energy{$structure}{$item}{navdw}  = $navdw;
	$energy{$structure}{$item}{ihb}    = $ihb;

	$structures{$structure} = 1;
    }
}

# Print out everything
open OUT, ">$output";

$ctr = 0;
print OUT ",,,,,,,,";
if ($minfile) {
    print OUT "MPSim Min,MPSim Min,MPSim Min,MPSim Min,";
}
print OUT "MPSim OneE,MPSim OneE,MPSim OneE,MPSim OneE,SCREAM,SCREAM,SCREAM,SCREAM";
print OUT "\n";
print OUT "Structure,H1,H2,H3,H4,H5,H6,H7";
foreach $item (@list) {
    print OUT ",Total,No IH VDW, No VDW, IHHB";
}
print OUT "\n";

foreach $structure (keys %structures) {
    $ctr++;
    print OUT "$structure";

    @helices = split(/\_/,$structure);
    foreach (@helices) { print OUT ",$_"; }

    foreach $item (@list) {
	if (exists $energy{$structure}{$item}{total}) {
	    printf OUT ",%.2f,%.2f,%.2f,%.2f",
	    $energy{$structure}{$item}{total},
	    $energy{$structure}{$item}{nihvdw},
	    $energy{$structure}{$item}{navdw},
	    $energy{$structure}{$item}{ihb};
	} else {
	    print OUT ",,,,";
	}
    }
    print OUT "\n";
}
close OUT;

print "Structures :: $ctr\n";

sub help {

    my $help = "
Program:
 :: BiHelix_Merge_Energies.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: BiHelix_Merge_Energies.pl --scream {scream energy file}
 ::                           --onee {mpsim energy onee file}
 ::                           --min {mpsim min energy file}
 ::                           -o {output file}

Input:
 :: --scream :: Filename
 :: SCREAM BiHelix energy file

 :: --onee   :: Positive Integer
 :: MPSim Single-Point BiHelix energy file

 :: --min    :: Filename
 :: MPSim Minimized BiHelix energy file (optional)

 :: -o       :: Filename
 :: Output file

 :: -h | --help      :: No Input
 :: Display this help information

Description:
 :: This program takes the two (or three) energy files
 :: from BiHelix and puts them together into one,
 :: comma-separated output file.
 ::
 :: It also prints to the screen the number of unique
 :: structures found in the output files.

";

    die "$help";

}

