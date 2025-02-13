#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
}

use strict;
use warnings;
use Cwd;
use File::Basename;
use File::Copy;
use File::Path;
use File::Spec;
use Getopt::Long qw(:config no_ignore_case);
use List::Util qw(min max sum);
use LWP::Simple;
use POSIX qw(ceil clock cuserid difftime floor getcwd getenv getlogin);
use Sys::Hostname;
use Time::Local;

###
### Template List
###
my @tmplist = glob "/ul/griffith/dev/Homologize/skkim_templates/*.mfta";
our %tmps = ();
foreach my $t (@tmplist) {
    # MFTA
    open MFTA, $t;
    my @lines = <MFTA>;
    close MFTA;

    # Header
    my $hdr = shift @lines;
    chomp $hdr;
    if ($hdr !~ /^\>(\S+)\|(\S+)\|(\S+)/) {
	die "AddTemplateSequences :: Could not parse header for $t\n";
    }
    $hdr =~ /^\>(\S+)\|(\S+)\|(\S+)/;
    my $db  = $1;
    my $acc = $2;
    my $id  = $3;

    # Sequence
    my $seq = "";
    while ($lines[0] =~ /^[ABCDEFGHIJKLMNOPQRSTUVWXYZ]/) {
	$lines[0] =~ s/\r//g;
	$lines[0] =~ s/\n//g;
	$seq .= shift @lines;
    }

    # Add to list
    $tmps{$acc}{db}    = $db;
    $tmps{$acc}{hdr}   = $hdr;
    $tmps{$acc}{id}    = $id;
    $tmps{$acc}{seq}   = $seq;
    $tmps{$acc}{found} = 0;
}

our $list = "";
foreach my $acc (sort {$tmps{$a}{id} cmp $tmps{$b}{id}} keys %tmps) {
    $list .=
	sprintf " :: %2s - %-8s - %-11s - %s\n",
	$tmps{$acc}{db}, $acc, $tmps{$acc}{id}, $tmps{$acc}{hdr};
}

###
### Arguments & Variables
###

if (@ARGV == 0) { help(); }

my ($help, $ftafile, $debug);

#ABCDEFGHIJKLMNOPQRSTUVWXYZ
# b    g ijklm o qrs uvwxyz
GetOptions ('h|help'          => \$help,
	    'f|fasta=s'       => \$ftafile,
	    'debug'           => \$debug);

if ($help) { help(); }

if (!$ftafile) {
    die "AddTemplateSequences :: Must provide fasta file\n";
} elsif (! -e $ftafile) {
    die "AddTemplateSequences :: Cannot find fasta file: $ftafile\n";
}

############################################################
### Main Routine                                         ###
############################################################

# File prefix
$ftafile =~ /(\S+)\.(seq|fta|fasta)$/;
my $pfx = $1;

# Load file
open FTA, "$ftafile";
my $fta = join("", <FTA>);
$fta =~ s/\r\n/\n/g;
$fta =~ s/\r/\n/g;
close FTA;
my @seqlist = split(/\n\>/, $fta);
my %seqs    = ();
for (my $i = 0; $i < @seqlist; $i++) {
    $seqlist[$i] =~ s/^\>P1;/\>/;
    my @lines = split(/\n/, $seqlist[$i]);

    # Header
    my $hdr = shift @lines;
    chomp $hdr;
    if ($hdr !~ /^\>/) { $hdr = ">" . $hdr; }
    if ($hdr !~ /^\>(\S+)\|(\S+)\|(\S+)/) {
	die "AddTemplateSequences :: Could not parse input sequence: $hdr\n";
    }
    $hdr =~ /^\>(\S+)\|(\S+)\|(\S+)/;
    my $db  = $1;
    my $acc = $2;
    my $id  = $3;
    my $seq = join("",@lines);
    $seq =~ s/\n//g;
    $seqs{$acc}{db}    = $db;
    $seqs{$acc}{hdr}   = $hdr;
    $seqs{$acc}{id}    = $id;
    $seqs{$acc}{seq}   = $seq;
    $seqs{$acc}{order} = $i;
    
    # Template
    if (defined $tmps{$acc}) {
	$tmps{$acc}{found} = 1;
    }
}
my $nseq = scalar @seqlist;

# Print Stuff
my $logfile;
open $logfile, ">${pfx}.add_tmps.log";

# Sort Templates
my %found    = ();
my %add      = ();
my $nfound   = 0;
my $nadd     = 0;
foreach my $acc (sort keys %tmps) {
    # Found
    if ($tmps{$acc}{found}) {
	$found{$acc}{db}  = $tmps{$acc}{db};
	$found{$acc}{hdr} = $tmps{$acc}{hdr};
	$found{$acc}{id}  = $tmps{$acc}{id};
	$found{$acc}{seq} = $tmps{$acc}{seq};
	$nfound++;
    }

    # Not Found - Add
    else {
	$add{$acc}{db}  = $tmps{$acc}{db};
	$add{$acc}{hdr} = $tmps{$acc}{hdr};
	$add{$acc}{id}  = $tmps{$acc}{id};
	$add{$acc}{seq} = $tmps{$acc}{seq};

	$seqs{$acc}{db}  = $tmps{$acc}{db};
	$seqs{$acc}{hdr} = $tmps{$acc}{hdr};
	$seqs{$acc}{id}  = $tmps{$acc}{id};
	$seqs{$acc}{seq} = $tmps{$acc}{seq};
	$seqs{$acc}{order} = $nseq + $nadd;
	$nadd++;
    }
}

my $foundtxt = "";
foreach my $acc (sort { $found{$a}{id} cmp $found{$b}{id} } keys %found) {
    $foundtxt .=
	sprintf " :: %2s - %-8s - %-11s - %s\n",
	$found{$acc}{db}, $acc, $found{$acc}{id}, $found{$acc}{hdr};
}

my $addtxt   = "";
foreach my $acc (sort { $add{$a}{id} cmp $add{$b}{id} } keys %add) {
    $addtxt .=
	sprintf " :: %2s - %-8s - %-11s - %s\n",
	$add{$acc}{db}, $acc, $add{$acc}{id}, $add{$acc}{hdr};
}

printlog($logfile,
	 "AddTemplateSequences :: " . localtime() . "\n".
	 " :: Input File                :: $ftafile\n".
	 " :: \# Initial Sequences       :: $nseq\n".
	 " :: \# Templates Found Already :: $nfound\n".
	 " :: \# Templates Added         :: $nadd\n\n".
	 "Templates Already in Input ::\n".
	 "$foundtxt\n".
	 "Templates Added to Input ::\n".
	 "$addtxt\n");

open FTA, ">${pfx}.add_tmps.fta";
foreach my $acc (sort {$seqs{$a}{order} <=> $seqs{$b}{order}} keys %seqs) {
    print FTA $seqs{$acc}{hdr} . "\n" . $seqs{$acc}{seq} . "\n";
}
close FTA;

printlog($logfile,
	 "Output ::\n".
	 " :: FASTA :: ${pfx}.add_tmps.fta\n".
	 " :: Log   :: ${pfx}.add_tmps.log\n\n");
close $logfile;

# Done
exit;

############################################################
### Subs                                                 ###
############################################################

sub printlog {
    my $fh  = $_[0];
    my $str = $_[1];

    print $fh $str;
    print     $str;
}

############################################################
### Help                                                 ###
############################################################

sub help {

    my $help = "
Program:
 :: AddTemplateSequences.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: AddTemplateSequences.pl -f {fasta file}

Input:
 :: -f | --fasta       :: FASTA File
 :: FASTA-formatted file to add GPCR sequences to.

Description:
 :: Adds a set of GPCR sequences to a given FASTA file.
 :: New sequences will be added to the END of your FASTA file.
 ::
 :: NOTE: The program uses the HEADERS in the FASTA file in order
 :: to determine whether a given protein is already present in 
 :: your FASTA file.
 ::
 :: Each sequence in your FASTA file should have the following
 :: header format:
 ::   >{database}|{accessioncode}|{ID}
 ::   >{database}|{accessioncode}|{ID} {description}
 :: Example:
 ::   >sp|P02699|OPSD_BOVIN
 ::   >sp|P02699|OPSD_BOVIN Rhodopsin - Bos taurus (Bovine).
 ::
 :: In some cases the header may read:
 ::   >P1;{database}|{accessioncode}|{ID}
 :: This is allowed.  The 'P1;' will be removed.
 ::
 :: Note: All newlines are removed from the output sequences.
 ::
 :: The program currently looks for template MFTA files to add
 :: from this directory:
 ::   ~griffith/dev/Homologize/skkim_templates/*.mfta

Template Sequences:
$list
Usage:
 :: AddTemplateSequences.pl -f {fasta file}

";

    die "$help";
}
