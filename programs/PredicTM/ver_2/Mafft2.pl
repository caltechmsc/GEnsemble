#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
#    push @INC, '/ul/griffith/perl5/lib/perl5/';
#    push @INC, '/ul/griffith/perl5/lib/perl5/x86_64-linux-thread-multi/';
}

use strict;
use warnings;
use Cwd;
#use Data::Dumper;
#use Data::Table;
use File::Basename;
use File::Copy;
use File::Path;
use File::Spec;
use Getopt::Long qw(:config no_ignore_case);
use List::Util qw(min max sum);
#use List::MoreUtils qw(:all);
#use List::Compare;
use LWP::Simple;
use POSIX qw(ceil clock cuserid difftime floor getcwd getenv getlogin);
#use Storable;
use Sys::Hostname;
#use Text::CSV;
use Time::Local;
#use XML::Hash;

use SequenceTools::SequenceTools;

###
### Arguments & Variables
###

our $machine = "ion";

if (@ARGV == 0) { help(); }

my ($help, $ftafile, $fast, $memory, $local, $debug);
my $nproc = 1;

#ABCDEFGHIJKLMNOPQRSTUVWXYZ
# b    g ijklm o qrs uvwxyz
GetOptions ('h|help'          => \$help,
	    'f|fasta=s'       => \$ftafile,
	    'fast'            => \$fast,
	    'm|machine=s'     => \$machine,
	    'mem=i'           => \$memory,
	    'p|nproc=i'       => \$nproc,
	    'local'           => \$local,
	    'debug'           => \$debug);

if ($help) { help(); }

if (!$ftafile) {
    die "Mafft2 :: Must provide fasta file\n";
} elsif (! -e $ftafile) {
    die "Mafft2 :: Cannot find fasta file: $ftafile\n";
}

############################################################
### Main Routine                                         ###
############################################################

###
### Input
###

# Load File
open FTA, "$ftafile";
my $fta = join("", <FTA>);
close FTA;

# File prefix
$ftafile =~ /(\S+)\.(seq|fta|fasta)$/;
my $pfx = $1;

# Number of Sequences
my $nseq = fasta_nseq($fta);

# Memory Usage
if (! defined $memory) {
    # <= 2000 sequences = 4GB
    if ($nseq <= 2000) { $memory = 4; }

    # > 2000 sequences = 8GB
    else { $memory = 8; }
}

# Hostname
my $host = hostname;

# Cannot run local on frontends
if (($local) && ($host =~ /(borg|matrix|hive|ion|atom|wolf1|wolf2|wolf3)/)) {
    die "Mafft2 :: Cannot run locally on cluster frontends!\n";
}

# Cannot submit to borg/matrix/hive
if ($machine =~ /(borg|matrix|hive|wolf3)/) {
    die "Mafft2 :: Please do not run Maff2 on $machine\n".
	"       :: It is recommended that you run on atom or ion\n";
}

###
### QSub & Exit
###
if (! $local) {
    # PBS setup
    my $cwd = cwd();
    my $faststr = "";
    if ($fast) { $faststr = " --fast"; }
    my $pbs =
	"#PBS -l nodes=1:ppn=${nproc},pvmem=${memory}GB,walltime=96:00:00\n".
	"#PBS -q workq\n".
	"#PBS -j oe\n".
	"#PBS -N mafft.${pfx}\n".
	"#PBS -m e\n".
	"#!/bin/csh\n".
	"\n".
	"cd \$PBS_O_WORKDIR\n".
	"${Bin}/Mafft2.pl -f $ftafile $faststr -p $nproc --local\n";

    # Print PBS file
    open PBS, ">mafft.${pfx}.pbs";
    print PBS $pbs;
    close PBS;

    # Submit job
    my $jobinfo = `ssh $machine 'cd $cwd ; qsub mafft.${pfx}.pbs'`;

    # Print Info
    print
	"Mafft2 :: " . localtime() . "\n".
	" :: Input File :: $ftafile\n".
	" :: Num. Seqs. :: $nseq\n\n".
	"Resubmitting Job ::\n".
	" :: Machine    :: $machine\n".
	" :: Job Info   :: $jobinfo".
	" :: Processors :: $nproc\n".
	" :: Memory     :: $memory / processor\n\n";

    # Qsubbed - Exit
    exit;
}

###
### Run
###
my $logfile;
open $logfile, ">${pfx}.mafft.log";

# Print
log $logfile,
    "Mafft2 :: " . localtime() . "\n".
    " :: Input File :: $ftafile\n".
    " :: Num. Seqs. :: $nseq\n".
    " :: Hostname   :: $host\n\n";

# Output
my ($pir,$aln);
my $tic = time();

# Accurate
if (! $fast) {
    log $logfile,
        "Running MAFFT :: Accurate Mode ::\n".
	" :: MAFFT Setting :: --genafpair\n";
    ($pir,$aln) = mafft($ftafile,$pfx,$fast,$nproc);
}

# Fast
else {
    log $logfile,
	"Running MAFFT :: Fast Mode ::\n".
	" :: MAFFT Setting :: --retree 2 --maxiterate 0\n";
    ($pir,$aln) = mafft($ftafile,$pfx,$fast,$nproc);
}

# Print
my $toc = tocf(toc($tic));
log($logfile,
    "\nOutput ::\n".
    " :: Timing   :: $toc\n".
    " :: PIR File :: $pir\n".
    " :: ALN File :: $aln\n".
    " :: Log File :: ${pfx}.mafft.log\n\n");
close $logfile;

# Done
exit;

############################################################
### Help                                                 ###
############################################################

sub help {

    my $help = "
Program:
 :: Mafft2.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: Mafft2.pl -f {fasta file} [options]

Input:
 :: -f | --fasta       :: FASTA File
 :: FASTA-formatted file to run MAFFT on.

Options:
 :: --fast             :: No Input
 :: This flag causes MAFFT to run using a fast and dirty
 :: method and should be USED WITH CAUTION.

 :: -m | --machine     :: Cluster Name
 :: Cluster to submit jobs to: ion/atom/wolf1/wolf2

 :: --mem              :: Integer > 0
 :: Amount of memory to allocate.
 :: Default: 4GB for < 2000 sequences
 ::          8GB for > 2000 sequences

 :: --local            :: No Input
 :: Run on the current machine.  Please note that you
 :: CANNOT run on one of the cluster frontends, but you
 :: CAN run on one of the desktop workstations using this
 :: flag.

 :: -p | --nproc       :: Integer
 :: Number of processors to use.  Default = 1
 :: Multiple processors are not useful unless you have 500+
 :: sequences.  Recommendations:
 :: <  500 sequences: 1 processor
 :: < 1000 sequences: 2 processors
 :: > 2000 sequences: 4+ processors

 :: -h | --help        :: No Input
 :: Displays this help message.

Description:
 :: Runs MAFFT on the provided FASTA file.  Produces both
 :: PIR and ALN alignments.  There are two ways in which
 :: MAFFT can be run:
 ::
 :: Default MAFFT Method:
 :: The default settings are ideal for aligning sequences
 :: like GPCRs, which have multiple segments that align (TMs)
 :: separated by non-aligning segments (loops).  The downside
 :: is that it can be slow and memory-intensive.
 :: Settings: --genafpair
 ::
 :: Fast MAFFT Method:
 :: The fast settings are intended to give a rough idea of
 :: the proper alignment and should be used with caution.
 :: Settings: --retree 2 --maxiterate 0

Usage:
 :: Mafft2.pl -f {fasta file} [options]

";

    die "$help";
}
