#!/usr/bin/perl
my $pl_version = 1.25;

my $print_copyright1 = 0;
my $print_copyright2 = 0;
my $copyright = "
#####################################################################
#                                                                   #
# PredicTM.pl/PredicTM.pm/BLAST.pl/BLAST.pm/Clustal.pm/Mafft.pm     #
#                                                                   #
# Copyright (c) 2008                                                #
# Adam R. Griffith, Ravinder Abrol, and William A. Goddard III      #
# Materials and Process Simulation Center                           #
# California Institute of Technology                                #
# Pasadena, CA, USA                                                 #
# All Rights Reserved.                                              #
#                                                                   #
# Uses BLAST:                                                       #
# Altschul S.F., Madden T.L., Schaffer A.A., Zhang J., Zhang Z.,    #
# Miller W., Lipman D.J.  Gapped BLAST and PSI-BLAST: a new         #
# generation of protein database search programs. (1997)            #
# _Nucleic Acids Res_ 25:3389-3402.                                 #
#                                                                   #
# BLAST is performed at the SIB using the BLAST network service.    #
# The SIB BLAST network service uses a server developed at SIB and  #
# the NCBI BLAST 2 software.                                        #
#                                                                   #
# This version:                                                     #
# Uses the Uniprot keyword KW-0297 (G-protein coupled receptor) to  #
# identfy GPCR sequences when flagging/cutting potential non-GPCRs  #
# http://www.uniprot.org/uniprot/?query=keyword\%3aKW-0297\         #
#      \&format=list                                                #
#                                                                   #
# Old version:                                                      #
# Uses the GPCRDB when flagging of cutting potential non-GPCR       #
# sequences: http://www.gpcr.org/7tm/htmls/entries.html             #
#                                                                   #
# Uses libwww-perl-5.808 from the Comprehensive Perl Archive        #
# Network (CPAN).                                                   #
# libwww-perl (c) 1995-2005 Gisle Aas. All rights reserved.         #
# libwww-perl (c) 1995 Martijn Koster. All rights reserved.         #
#                                                                   #
# Uses ClustalW 1.83:                                               #
# Chenna, et al. \"Multiple sequence alignment with the Clustal      #
# series of programs.\" (2003)                                       #
# _Nucleic Acids Res_ 31 (13):3497-500 PubMedID: 12824352           #
#                                                                   #
# Uses MAFFT 6.240:                                                 #
# MAFFT v6.240 (2007/04/04)  Copyright (c) 2006 Kazutaka Katoh      #
# http://align.bmr.kyushu-u.ac.jp/mafft/software/                   #
# NAR 30:3059-3066, NAR 33:511-518                                  #
#                                                                   #
#####################################################################

";

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
}

use strict;
use warnings;

use Cwd;
use File::Copy;
use File::Path;
use Getopt::Long;
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

use Modules::Blast ();

################################################################################
##### Make Sure that we have Some Input                                    #####
################################################################################
my $numargv = @ARGV;
if ($numargv == 0) {
    Modules::Blast::help();
    exit;
}

################################################################################
##### Get Default Values                                                   #####
################################################################################
my ($printstring, $dot_version, $dot_location, $pm_version, $user_home, $protdb, $ethreshold, $sequences, $compiter, $maxseqs, $complete, $flagnongpcr, $cutnongpcr, $filter, $trembl, $clustal_executable, $mafft_executable, $mafft_binaries, $libwww_dir);

my ($user_protdb, $user_ethreshold, $user_sequences, $user_compiter, $user_maxseqs, $user_complete, $user_flagnongpcr, $user_cutnongpcr, $user_filter, $user_trembl);

my ($accession, $fasta, $raw, $name, $prefix, $help, $quiet, $showdefaults);

$pm_version = Modules::Blast::checkVersion();

$user_home = "";
if (-e "${Bin}/.gensemble/.blast") {
    open DEF, "${Bin}/.gensemble/.blast";
    while (<DEF>) {
	if (/user_home\s+(\S+)/) {
	    $user_home = $1;
	}
    }
    close DEF;
} else {
    die "Blast :: Unable to find ${Bin}/.gensemble/.blast for default values.\n\n";
}
if ($user_home eq "") { $user_home = "/dev/null/"; }

$printstring .=
    "\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\n".
    "\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@ Loading Blast Defaults \@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\n".
    "\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\n\n";

if (($user_home ne "/dev/null") && ($user_home ne "~")) {
    if ($user_home !~ /\/$/) { $user_home .= "/"; }
    my $username = `whoami`;
    chomp $username;
    $user_home .= $username;
}
if (-e "${user_home}/.gensemble/.blast") {
    $dot_location = "${user_home}/.gensemble/.blast";
    open DEF, "${user_home}/.gensemble/.blast";
    while (<DEF>) {
	if    (/^protdb\s+(\S+)/)             { $protdb             = $1; }
	elsif (/^ethreshold\s+(\S+)/)         { $ethreshold         = $1; }
	elsif (/^sequences\s+(\S+)/)          { $sequences          = $1; }
	elsif (/^compiter\s+(\S+)/)           { $compiter           = $1; }
	elsif (/^maxseqs\s+(\S+)/)            { $maxseqs            = $1; }
	elsif (/^complete\s+(\S+)/)           { $complete           = $1; }
	elsif (/^flagnongpcr\s+(\S+)/)        { $flagnongpcr        = $1; }
	elsif (/^cutnongpcr\s+(\S+)/)         { $cutnongpcr         = $1; }
	elsif (/^filter\s+(\S+)/)             { $filter             = $1; }
	elsif (/^trembl\s+(\S+)/)             { $trembl             = $1; }
	elsif (/^clustal_executable\s+(\S+)/) { $clustal_executable = $1; }
	elsif (/^mafft_executable\s+(\S+)/)   { $mafft_executable   = $1; }
	elsif (/^mafft_binaries\s+(\S+)/)     { $mafft_binaries     = $1; }
	elsif (/^libwww_dir\s+(\S+)/)         { $libwww_dir         = $1; }
	elsif (/^version\s+(\S+)/)            { $dot_version        = $1; }
    }
    close DEF;

    $printstring .= "Default Values Loaded From :: ${user_home}/.gensemble/.blast\n";

} elsif (-e "${Bin}/.gensemble/.blast") {
    $dot_location = "${Bin}/.gensemble/.blast";
    open DEF, "${Bin}/.gensemble/.blast";
    while (<DEF>) {
	if    (/^protdb\s+(\S+)/)             { $protdb             = $1; }
	elsif (/^ethreshold\s+(\S+)/)         { $ethreshold         = $1; }
	elsif (/^sequences\s+(\S+)/)          { $sequences          = $1; }
	elsif (/^compiter\s+(\S+)/)           { $compiter           = $1; }
	elsif (/^maxseqs\s+(\S+)/)            { $maxseqs            = $1; }
	elsif (/^complete\s+(\S+)/)           { $complete           = $1; }
	elsif (/^flagnongpcr\s+(\S+)/)        { $flagnongpcr        = $1; }
	elsif (/^cutnongpcr\s+(\S+)/)         { $cutnongpcr         = $1; }
	elsif (/^filter\s+(\S+)/)             { $filter             = $1; }
	elsif (/^trembl\s+(\S+)/)             { $trembl             = $1; }
	elsif (/^clustal_executable\s+(\S+)/) { $clustal_executable = $1; }
	elsif (/^mafft_executable\s+(\S+)/)   { $mafft_executable   = $1; }
	elsif (/^mafft_binaries\s+(\S+)/)     { $mafft_binaries     = $1; }
	elsif (/^libwww_dir\s+(\S+)/)         { $libwww_dir         = $1; }
	elsif (/^version\s+(\S+)/)            { $dot_version        = $1; }
    }
    close DEF;

    $printstring .= "Default Values Loaded From :: ${Bin}/.gensemble/.blast\n";

} else {
    die "Blast :: Unable to find ${Bin}/.gensemble/.blast for default values.\n\n";
}

if (($dot_version != $pm_version) ||
    ($dot_version != $pl_version) ||
    ($pm_version  != $pl_version)) {

    my ($l1, $l2, $l3, $s1, $s2, $s3, $max);
    $l1 = length("$dot_location");
    $l2 = length("${Bin}/Blast.pl");
    $l3 = length("${Bin}/Modules/Blast.pm");
    $max = 0;
    if ($l1 > $max) { $max = $l1; }
    if ($l2 > $max) { $max = $l2; }
    if ($l3 > $max) { $max = $l3; }
    $s1 = " " x ($max - $l1);
    $s2 = " " x ($max - $l2);
    $s3 = " " x ($max - $l3);

    die
	"Blast :: Version information does not match ::\n".
	"      :: $dot_location Version ${s1}:: $dot_version\n".
	"      :: ${Bin}/Blast.pl Version ${s2}:: $pl_version\n".
	"      :: ${Bin}/Modules/Blast.pm Version ${s3}:: $pm_version\n\n";
}

################################################################################
##### Print Default Values                                                 #####
################################################################################
$printstring .=
    " :: protdb      :: $protdb\n".
    " :: ethreshold  :: $ethreshold\n".
    " :: sequences   :: $sequences\n".
    " :: compiter    :: $compiter\n".
    " :: maxseqs     :: $maxseqs\n".
    " :: complete    :: $complete\n".
    " :: flagnongpcr :: $flagnongpcr\n".
    " :: cutnongpcr  :: $cutnongpcr\n".
    " :: filter      :: $filter\n".
    " :: trembl      :: $trembl\n";

################################################################################
##### Read User Input                                                      #####
################################################################################
#abcdefghijklmnopqrstuvwxyz
# b   f   jk   op    uvw yz
GetOptions (
	    # Required User Input
	    'a|accession=s'  => \$accession,
	    'fasta=s'        => \$fasta,
	    'r|raw=s'        => \$raw,

	    # Optional User Input With Default Values
	    'd|protdb=s'     => \$user_protdb,
	    'e|ethreshold=f' => \$user_ethreshold,
	    's|sequences=i'  => \$user_sequences,
	    'i|compiter=i'   => \$user_compiter,
	    'm|maxseqs=i'    => \$user_maxseqs,

	    # Optional User Input Without Default Values
	    'n|name=s'         => \$name,
	    'prefix=s'       => \$prefix,

	    # On/Off Flags With Default Values
	    'c|complete!'    => \$user_complete,
	    'g|flagnongpcr!' => \$user_flagnongpcr,
	    'l|filter!'      => \$user_filter,
	    't|trembl!'      => \$user_trembl,
	    'x|cutnongpcr!'  => \$user_cutnongpcr,

	    # On/Off Flags Without Default Values
	    'h|help'         => \$help,
	    'q|quiet'        => \$quiet,
	    'showdefaults'   => \$showdefaults
	    );

if ($showdefaults) {
    if ($print_copyright1) {
	die "$copyright"."$printstring\n";
    } else {
	die "$printstring\n";
    }
}

################################################################################
##### Handle User Input                                                    #####
################################################################################
my $user_changed = 0;
$printstring .= "Defaults Changed By User\n";

if (defined $user_protdb) {
    if ($user_protdb ne $protdb) {
	$printstring .= " :: protdb      :: $protdb ==> $user_protdb\n";
	$protdb = $user_protdb;
	$user_changed++;
    }
}
if (defined $user_ethreshold) {
    if ($user_ethreshold != $ethreshold) {
	$printstring .= " :: ethreshold  :: $ethreshold ==> $user_ethreshold\n";
	$ethreshold = $user_ethreshold;
	$user_changed++;
    }
}
if (defined $user_sequences) {
    if ($user_sequences != $sequences) {
	$printstring .= " :: sequences   :: $sequences ==> $user_sequences\n";
	$sequences = $user_sequences;
	$user_changed++;
    }
}
if (defined $user_compiter) {
    if ($user_compiter != $compiter) {
	$printstring .= " :: compiter    :: $compiter ==> $user_compiter\n";
	$compiter = $user_compiter;
	$user_changed++;
    }
}
if (defined $user_maxseqs) {
    if ($user_maxseqs != $maxseqs) {
	$printstring .= " :: maxseqs     :: $maxseqs ==> $user_maxseqs\n";
	$maxseqs = $user_maxseqs;
	$user_changed++;
    }
}
if (defined $user_complete) {
    if ($user_complete != $complete) {
	$printstring .= " :: complete    :: $complete ==> $user_complete\n";
	$complete = $user_complete;
	$user_changed++;
    }
}
if (defined $user_flagnongpcr) {
    if ($user_flagnongpcr != $flagnongpcr) {
	$printstring .= " :: flagnongpcr :: $flagnongpcr ==> $user_flagnongpcr\n";
	$flagnongpcr = $user_flagnongpcr;
	$user_changed++;
    }
}
if (defined $user_cutnongpcr) {
    if ($user_cutnongpcr != $cutnongpcr) {
	$printstring .= " :: cutnongpcr  :: $cutnongpcr ==> $user_cutnongpcr\n";
	$cutnongpcr = $user_cutnongpcr;
	$user_changed++;
    }
}
if (defined $user_filter) {
    if ($user_filter != $filter) {
	$printstring .= " :: filter      :: $filter ==> $user_filter\n";
	$filter = $user_filter;
	$user_changed++;
    }
}
if (defined $user_trembl) {
    if ($user_trembl != $trembl) {
	$printstring .= " :: trembl      :: $trembl ==> $user_trembl\n";
	$trembl = $user_trembl;
	$user_changed++;
    }
}

if (!$user_changed) { $printstring .= " :: No defaults changed\n"; }
$printstring .= "\n";

################################################################################
##### Run BLAST                                                            #####
################################################################################
my $fnpfx = Modules::Blast::blast($printstring,
				  $accession,
				  $fasta,
				  $raw,
				  $protdb,
				  $ethreshold,
				  $sequences,
				  $compiter,
				  $maxseqs,
				  $name,
				  $prefix,
				  $complete,
				  $flagnongpcr,
				  $cutnongpcr,
				  $filter,
				  $trembl,
				  $help,
				  $quiet,
				  $print_copyright1,
				  $print_copyright2,
				  $clustal_executable,
				  $mafft_executable,
				  $mafft_binaries);

exit;

################################################################################
##### Backup .blast File                                                   #####
################################################################################
# Below is a backup copy of the .blast file that contains the program defaults.
# Should the .blast file be accidentally deleted, simply copy the text below,
# remove the first "# " at the beginning of each line (but only one on each line),
# and save the text to a file called ".blast" in GEnsemble/programs/.gensemble

# # ---> Copy the lines below <--- #
# #######################
# # Version Information #
# #######################
# version 1.2
#
# #########################
# # Directory Information #
# #########################
# # General location of user directories
# user_home          ~
#
# # Clustal Executable
# clustal_executable thirdparty/clustal/clustalw
#
# # MAFFT Executable
# mafft_executable   thirdparty/mafft/mafft
#
# # MAFFT Binaries
# mafft_binaries     thirdparty/mafft/lib/mafft
#
# # libwww-perl-5.808 :: Note that libwww must be installed in the libwww subdirectory of
# # the main program directory.  This parameter should not be altered and is listed here
# # only for reference.
# libwww_dir         thirdparty/libwww/
#
# ####################
# # Default Settings #
# ####################
# protdb           Mammalia     # BLAST Protein Database
# ethreshold       0.1          # BLAST E-Value Threshold
# sequences        1000         # Default/Initial number of sequences
# compiter         1000         # Step size for completeness
# maxseqs          10000        # Maximum number of sequences for completeness
# complete         1            # BLAST Completeness Flag                 (1 = on, 0 = off)
# flagnongpcr      0            # BLAST Flag Non-GPCRs Flag               (1 = on, 0 = off)
# cutnongpcr       0            # BLAST Cut Non-GPCRs Flag                (1 = on, 0 = off)
# filter           0            # BLAST Low Region Complexity Filter Flag (1 = on, 0 = off)
# trembl           0            # BLAST Use TrEMBL Flag                   (1 = on, 0 = off)
# 
# # ---> Copy the lines above <--- #
