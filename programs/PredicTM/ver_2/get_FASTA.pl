#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
    push @INC, "/ul/griffith/libwww/";
}

use strict;
use warnings;
use Cwd;
use File::Basename;
use File::Copy;
use File::Path;
use File::Spec;
use Getopt::Long qw(:config no_ignore_case);
use List::Util qw(min max);
use LWP::Simple;
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

my ($help, $file, $debug);
my @accs;

if (@ARGV == 0) { help(); }

#ABCDEFGHIJKLMNOPQRSTUVWXYZ
#abcdefghijklmnopqrstuvwxyz

#ABCDEFGHIJKLMNOPQRSTUVWXYZ
#abcdefg ijklmnopqrstuvwxyz
GetOptions ('h|help'          => \$help,
	    'a|accessions=s'  => \@accs,
	    'f|file=s'        => \$file,
	    'debug'           => \$debug);

if ($help) { help(); }
if ((@accs == 0) && (!$file)) {
    die "get_FASTA :: Must provide UniProt accession codes!\n";
}

############################################################
### Main Routine                                         ###
############################################################

# Print
print "get_FASTA :: Get FASTA files from UniProt\n";

# Parse input file
if ($file) {
    if (-e $file) {
	open FILE, "$file";
	while (<FILE>) {
	    my $line = $_;
	    chomp $line;
	    if ($line =~ /^[\w\.\s\[\]]+$/) {
		push @accs, $line;
	    } else {
		print "  incorrect formatting: $line\n";
	    }
	}
    }
}

# Parse input file
my @newaccs = ();
foreach my $acc (@accs) {
    if ($acc =~ /^[\w\.\s\[\]]+$/) {
	my @split = split(/\s+/, $acc);
	push @newaccs, @split;
    } else {
	print "  incorrect formatting: $acc\n";
    }
}
my %acchash = ();
foreach (@newaccs) { $acchash{$_} = 1; }
@accs = sort {$a cmp $b} keys %acchash;

# No good codes
if (@accs == 0) {
    die "No accession codes found in input.\n";
}

# Find fastas
print "Getting FASTAs:\n";
foreach my $acc (@accs) {
    print "  ${acc}... ";

    # Parse input for alternative name
    my $name = "";
    if ($acc =~ /\[(\S+)\]/) {
	$name = $1;
	$acc =~ s/\[\S+\]//;
    } else {
	$name = $acc;
    }
    my $code = $acc;

    # Get File
    my $file = "${name}.fta";
    my $url  = "http://www.uniprot.org/uniprot/${code}.fasta";
    my $txt  = get $url;

    # Failed
    if (! defined $txt) {
	print "failed\n";
    }

    # Worked
    else {
	print "success";
	if (-e "${name}.fta") {
	    my $bak = "${name}.fta.bak";
	    move("${name}.fta", $bak);
	    print "... moved old file ${name}.fta to ${name}.fta.bak to prevent overwrite\n";
	} else {
	    print "\n";
	}
	open ACC, ">$file";
	print ACC $txt;
	close ACC;
    }
}

print "\nDone\n";

exit;

############################################################
### Help                                                 ###
############################################################

sub help {

    my $help = "
Program:
 :: get_FASTA.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: get_FASTA.pl -a {UniProt accession codes}

Input:
 :: -a | --accessions  :: UniProt ID codes
 :: Codes for UniProt entries.
 :: Examples:
 ::   -a P07550 -a P07700 -a P29274
 ::   -a 'P07550 P07700 P29274'
 ::   -a 'P07550 P07700' -a P29274
 :: NOTE: Multiple codes must be separated by spaces,
 ::       but NO COMMAS!
 :: NOTE: NO EXTRA CHARACTERS! Allowed: [A-Z,0-9]

 :: -f | --file        :: Filename
 :: File containing UniProt entries.  Multiple entries
 :: can be on the same line if separated by spaces.
 :: NOTE: NO EXTRA CHARACTERS! Allowed: [A-Z,0-9]

 :: -h | --help        :: No Input
 :: Displays this help message.

Description:
 :: Downloads the specified UniProt FASTA entries.
 ::
 :: Note: By default the accession code will be the
 :: output filename.  An alternative filename can be
 :: used by providing a different prefix in this manner:
 :: 'P07550[adrb2_human]'
 ::
 :: Note that there is no space between the accession
 :: code and the alternative name in brackets.  Also
 :: note that the '_' character is allowed. NO OTHER
 :: UNUSUAL CHARACTERS ARE ALLOWED.
 :: Allowed: [A-Z,0-9,_]
 ::
 :: Also note, when on the command line, input with '['
 :: and ']' must be put in quotes, like this:
 :: 'P07550[adrb2_human]'

";

    die "$help";
}
