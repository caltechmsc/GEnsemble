#!/usr/bin/perl
my $pl_version = 1.1;

my $print_copyright1 = 0;
my $print_copyright2 = 0;
my $copyright = "
#####################################################################
#                                                                   #
# OptHelix.pl / OptHelix.pm                                         #
#                                                                   #
# Copyright (c) 2008                                                #
# Adam R. Griffith, Ravinder Abrol, and William A. Goddard III      #
# Materials and Process Simulation Center                           #
# California Institute of Technology                                #
# Pasadena, CA, USA                                                 #
# All Rights Reserved.                                              #
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

use Modules::OptHelix ();

################################################################################
##### Make Sure that we have Some Input                                    #####
################################################################################
my $numargv = @ARGV;
if ($numargv == 0) {
    Modules::OptHelix::help();
    exit;
}

################################################################################
##### Get Default Values                                                   #####
################################################################################
my ($printstring, $dot_version, $dot_location, $pm_version, $user_home);

my ($mfta, $name, $prefix, $tms_to_run, $help, $quiet, $showdefaults, $user_temp, $dynsteps, $dyntimestep, $dynsnapint, $dyntemp, $dynresidues, $ff, $alaninecap, $caplength, $staticcaps, $backboneminrms, $backboneminsteps, $warmup, $warmupstart, $warmupinterval, $warmupsteps, $warmuptimestep, $ignorepct, $finalminimize, $finalminsteps, $finalminrms, $runlocal, $runparallel, $qsub, $queuetype, $polyalanines_dir, $scream_dir, $mpsim_data, $mpsim_executable, $host, $onqueue, $python_executable, $raw, $cap);

my ($user_dynsteps, $user_dyntimestep, $user_dynsnapint, $user_dyntemp, $user_dynresidues, $user_ff, $user_alaninecap, $user_caplength, $user_staticcaps, $user_backboneminrms, $user_backboneminsteps, $user_warmup, $user_warmupstart, $user_warmupinterval, $user_warmupsteps, $user_warmuptimestep, $user_ignorepct, $user_finalminimize, $user_finalminsteps, $user_finalminrms, $user_runlocal, $user_runparallel, $user_qsub, $user_queuetype, $consensustms, $user_raw, $user_cap);

$pm_version = Modules::OptHelix::checkVersion();

$user_home = "";
if (-e "${Bin}/.gensemble/.opthelix") {
    open DEF, "${Bin}/.gensemble/.opthelix";
    while (<DEF>) {
	if (/user_home\s+(\S+)/) {
	    $user_home = $1;
	}
    }
    close DEF;
} else {
    die "OptHelix :: Unable to find ${Bin}/.gensemble/.opthelix for default values.\n\n";
}
if ($user_home eq "") { $user_home = "/dev/null/"; }

    $printstring .=
	"\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\n".
	"\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@ Loading OptHelix Defaults \@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\n".
	"\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\n\n";

if (($user_home ne "/dev/null") && ($user_home ne "~")) {
    if ($user_home !~ /\/$/) { $user_home .= "/"; }
    my $username = `whoami`;
    chomp $username;
    $user_home .= $username;
}
if (-e "${user_home}/.gensemble/.opthelix") {
    $dot_location = "${user_home}/.gensemble/.opthelix";
    open DEF, "${user_home}/.gensemble/.opthelix";
    while (<DEF>) {
	if    (/^version\s+(\S+)/)            { $dot_version       = $1; }
	elsif (/^user_temp\s+(\S+)/)          { $user_temp         = $1; }
	elsif (/^dynsteps\s+(\S+)/)           { $dynsteps          = $1; }
	elsif (/^dyntimestep\s+(\S+)/)        { $dyntimestep       = $1; }
	elsif (/^dynsnapint\s+(\S+)/)         { $dynsnapint        = $1; }
	elsif (/^dyntemp\s+(\S+)/)            { $dyntemp           = $1; }
	elsif (/^dynresidues\s+(\S+)/)        { $dynresidues       = $1; }
	elsif (/^ff\s+(\S+)/)                 { $ff                = $1; }
	elsif (/^alaninecap\s+(\S+)/)         { $alaninecap        = $1; }
	elsif (/^caplength\s+(\S+)/)          { $caplength         = $1; }
	elsif (/^staticcaps\s+(\S+)/)         { $staticcaps        = $1; }
	elsif (/^backboneminrms\s+(\S+)/)     { $backboneminrms    = $1; }
	elsif (/^backboneminsteps\s+(\S+)/)   { $backboneminsteps  = $1; }
	elsif (/^warmup\s+(\S+)/)             { $warmup            = $1; }
	elsif (/^warmupstart\s+(\S+)/)        { $warmupstart       = $1; }
	elsif (/^warmupinterval\s+(\S+)/)     { $warmupinterval    = $1; }
	elsif (/^warmupsteps\s+(\S+)/)        { $warmupsteps       = $1; }
	elsif (/^warmuptimestep\s+(\S+)/)     { $warmuptimestep    = $1; }
	elsif (/^ignorepct\s+(\S+)/)          { $ignorepct         = $1; }
	elsif (/^finalminimize\s+(\S+)/)      { $finalminimize     = $1; }
	elsif (/^finalminrms\s+(\S+)/)        { $finalminrms       = $1; }
	elsif (/^finalminsteps\s+(\S+)/)      { $finalminsteps     = $1; }
	elsif (/^runlocal\s+(\S+)/)           { $runlocal          = $1; }
	elsif (/^runparallel\s+(\S+)/)        { $runparallel       = $1; }
	elsif (/^qsub\s+(\S+)/)               { $qsub              = $1; }
	elsif (/^queuetype\s+(\S+)/)          { $queuetype         = $1; }
	elsif (/^scream_dir\s+(\S+)/)         { $scream_dir        = $1; }
	elsif (/^polyalanines_dir\s+(\S+)/)   { $polyalanines_dir  = $1; }
	elsif (/^mpsim_data\s+(\S+)/)         { $mpsim_data        = $1; }
	elsif (/^mpsim_executable\s+(\S+)/)   { $mpsim_executable  = $1; }
	elsif (/^python_executable\s+(\S+)/)  { $python_executable = $1; }
	elsif (/^raw\s+(\S+)/)                { $raw               = $1; }
	elsif (/^cap\s+(\S+)/)                { $cap               = $1; }
    }
    close DEF;

    $printstring .= "Default Values Loaded From :: ${user_home}/.gensemble/.opthelix\n";

} elsif (-e "${Bin}/.gensemble/.opthelix") {
    $dot_location = "${Bin}/.gensemble/.opthelix";
    open DEF, "${Bin}/.gensemble/.opthelix";
    while (<DEF>) {
	if    (/^version\s+(\S+)/)            { $dot_version       = $1; }
	elsif (/^user_temp\s+(\S+)/)          { $user_temp         = $1; }
	elsif (/^dynsteps\s+(\S+)/)           { $dynsteps          = $1; }
	elsif (/^dyntimestep\s+(\S+)/)        { $dyntimestep       = $1; }
	elsif (/^dynsnapint\s+(\S+)/)         { $dynsnapint        = $1; }
	elsif (/^dyntemp\s+(\S+)/)            { $dyntemp           = $1; }
	elsif (/^dynresidues\s+(\S+)/)        { $dynresidues       = $1; }
	elsif (/^ff\s+(\S+)/)                 { $ff                = $1; }
	elsif (/^alaninecap\s+(\S+)/)         { $alaninecap        = $1; }
	elsif (/^caplength\s+(\S+)/)          { $caplength         = $1; }
	elsif (/^staticcaps\s+(\S+)/)         { $staticcaps        = $1; }
	elsif (/^backboneminrms\s+(\S+)/)     { $backboneminrms    = $1; }
	elsif (/^backboneminsteps\s+(\S+)/)   { $backboneminsteps  = $1; }
	elsif (/^warmup\s+(\S+)/)             { $warmup            = $1; }
	elsif (/^warmupstart\s+(\S+)/)        { $warmupstart       = $1; }
	elsif (/^warmupinterval\s+(\S+)/)     { $warmupinterval    = $1; }
	elsif (/^warmupsteps\s+(\S+)/)        { $warmupsteps       = $1; }
	elsif (/^warmuptimestep\s+(\S+)/)     { $warmuptimestep    = $1; }
	elsif (/^ignorepct\s+(\S+)/)          { $ignorepct         = $1; }
	elsif (/^finalminimize\s+(\S+)/)      { $finalminimize     = $1; }
	elsif (/^finalminrms\s+(\S+)/)        { $finalminrms       = $1; }
	elsif (/^finalminsteps\s+(\S+)/)      { $finalminsteps     = $1; }
	elsif (/^runlocal\s+(\S+)/)           { $runlocal          = $1; }
	elsif (/^runparallel\s+(\S+)/)        { $runparallel       = $1; }
	elsif (/^qsub\s+(\S+)/)               { $qsub              = $1; }
	elsif (/^queuetype\s+(\S+)/)          { $queuetype         = $1; }
	elsif (/^scream_dir\s+(\S+)/)         { $scream_dir        = $1; }
	elsif (/^polyalanines_dir\s+(\S+)/)   { $polyalanines_dir  = $1; }
	elsif (/^mpsim_data\s+(\S+)/)         { $mpsim_data        = $1; }
	elsif (/^mpsim_executable\s+(\S+)/)   { $mpsim_executable  = $1; }
	elsif (/^python_executable\s+(\S+)/)  { $python_executable = $1; }
	elsif (/^raw\s+(\S+)/)                { $raw               = $1; }
	elsif (/^cap\s+(\S+)/)                { $cap               = $1; }
    }
    close DEF;

    $printstring .= "Default Values Loaded From :: ${Bin}/.gensemble/.opthelix\n";

} else {
    die "OptHelix :: Unable to find ${Bin}/.gensemble/.opthelix for default values.\n\n";
}

if (($dot_version != $pm_version) ||
    ($dot_version != $pl_version) ||
    ($pm_version  != $pl_version)) {

    my ($l1, $l2, $l3, $s1, $s2, $s3, $max);
    $l1 = length("$dot_location");
    $l2 = length("${Bin}/OptHelix.pl");
    $l3 = length("${Bin}/Modules/OptHelix.pm");
    $max = 0;
    if ($l1 > $max) { $max = $l1; }
    if ($l2 > $max) { $max = $l2; }
    if ($l3 > $max) { $max = $l3; }
    $s1 = " " x ($max - $l1);
    $s2 = " " x ($max - $l2);
    $s3 = " " x ($max - $l3);

    die
	"OptHelix :: Version information does not match ::\n".
	"         :: $dot_location Version ${s1}:: $dot_version\n".
	"         :: ${Bin}/OptHelix.pl Version ${s2}:: $pl_version\n".
	"         :: ${Bin}/Modules/OptHelix.pm Version ${s3}:: $pm_version\n\n";
}

################################################################################
##### Print Default Values                                                 #####
################################################################################
$printstring .=
    " :: dynsteps         :: $dynsteps\n".
    " :: dyntimestep      :: $dyntimestep\n".
    " :: dynsnapint       :: $dynsnapint\n".
    " :: dyntemp          :: $dyntemp\n".
    " :: dynresidues      :: $dynresidues\n".
    " :: ff               :: $ff\n".
    " :: alaninecap       :: $alaninecap\n".
    " :: caplength        :: $caplength\n".
    " :: staticcaps       :: $staticcaps\n".
    " :: backboneminrms   :: $backboneminrms\n".
    " :: backboneminsteps :: $backboneminsteps\n".
    " :: warmup           :: $warmup\n".
    " :: warmupstart      :: $warmupstart\n".
    " :: warmupinterval   :: $warmupinterval\n".
    " :: warmupsteps      :: $warmupsteps\n".
    " :: warmuptimestep   :: $warmuptimestep\n".
    " :: ignorepct        :: $ignorepct\n".
    " :: finalminimize    :: $finalminimize\n".
    " :: finalminrms      :: $finalminrms\n".
    " :: finalminsteps    :: $finalminsteps\n".
    " :: runlocal         :: $runlocal\n".
    " :: runparallel      :: $runparallel\n".
    " :: qsub             :: $qsub\n".
    " :: queuetype        :: $queuetype\n".
    " :: raw              :: $raw\n".
    " :: cap              :: $cap\n";

################################################################################
##### Read User Input                                                      #####
################################################################################
#abcdefghijklmnopqrstuvwxyz
# b  e g  jk  no     uv xyz
GetOptions (
	    # Required User Input
	    'f|mfta=s'           => \$mfta,

	    # Optional User Input With Default Values
	    's|dynsteps=i'       => \$user_dynsteps,
	    't|dyntimestep=i'    => \$user_dyntimestep,
	    'i|dynsnapint=i'     => \$user_dynsnapint,
	    'd|dyntemp=f'        => \$user_dyntemp,
	    'r|dynresidues=s'    => \$user_dynresidues,
	    'ff=s'               => \$user_ff,
	    'c|caplength=i'      => \$user_caplength,
	    'backboneminrms=f'   => \$user_backboneminrms,
	    'backboneminsteps=i' => \$user_backboneminsteps,
	    'warmupstart=f'      => \$user_warmupstart,
	    'warmupinterval=f'   => \$user_warmupinterval,
	    'warmupsteps=i'      => \$user_warmupsteps,
	    'warmuptimestep=i'   => \$user_warmuptimestep,
	    'ignorepct=f'        => \$user_ignorepct,
	    'finalminrms=f'      => \$user_finalminrms,
	    'finalminsteps=i'    => \$user_finalminsteps,
	    'queuetype=s'        => \$user_queuetype,
	    'raw=s'              => \$user_raw,
	    'cap=s'              => \$user_cap,

	    # Optional User Input Without Default Values
	    'prefix=s'           => \$prefix,
	    'tms=s'              => \$tms_to_run,
	    'host=s'             => \$host,

	    # On/Off Flags With Default Values
	    'a|alaninecap!'      => \$user_alaninecap,
	    'staticcaps!'        => \$user_staticcaps,
	    'w|warmup!'          => \$user_warmup,
	    'm|finalminimize!'   => \$user_finalminimize,
	    'l|runlocal!'        => \$user_runlocal,
	    'p|runparallel!'     => \$user_runparallel,
	    'qsub!'              => \$user_qsub,

	    # On/Off Flags Without Default Values
	    'h|help'             => \$help,
	    'q|quiet'            => \$quiet,
	    'showdefaults'       => \$showdefaults,
	    'onqueue'            => \$onqueue
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

if (defined $user_dynsteps) {
    if ($user_dynsteps != $dynsteps) {
	$printstring .= " :: dynsteps         :: $dynsteps ==> $user_dynsteps\n";
	$dynsteps = $user_dynsteps;
	$user_changed++;
    }
}

if (defined $user_dyntimestep) {
    if ($user_dyntimestep != $dyntimestep) {
	$printstring .= " :: dyntimestep      :: $dyntimestep ==> $user_dyntimestep\n";
	$dyntimestep = $user_dyntimestep;
	$user_changed++;
    }
}

if (defined $user_dynsnapint) {
    if ($user_dynsnapint != $dynsnapint) {
	$printstring .= " :: dynsnapint       :: $dynsnapint ==> $user_dynsnapint\n";
	$dynsnapint = $user_dynsnapint;
	$user_changed++;
    }
}

if (defined $user_dyntemp) {
    if ($user_dyntemp != $dyntemp) {
	$printstring .= " :: dyntemp          :: $dyntemp ==> $user_dyntemp\n";
	$dyntemp = $user_dyntemp;
	$user_changed++;
    }
}

if (defined $user_dynresidues) {
    if ($user_dynresidues ne $dynresidues) {
	$printstring .= " :: dynresidues      :: $dynresidues ==> $user_dynresidues\n";
	$dynresidues = $user_dynresidues;
	$user_changed++;
    }
}

if (defined $user_ff) {
    if ($user_ff ne $ff) {
	$printstring .= " :: ff               :: $ff ==> $user_ff\n";
	$ff = $user_ff;
	$user_changed++;
    }
}

if (defined $user_alaninecap) {
    if ($user_alaninecap != $alaninecap) {
	$printstring .= " :: alaninecap       :: $alaninecap ==> $user_alaninecap\n";
	$alaninecap = $user_alaninecap;
	$user_changed++;
    }
}

if (defined $user_staticcaps) {
    if ($user_staticcaps != $staticcaps) {
	$printstring .= " :: staticcaps       :: $staticcaps ==> $user_staticcaps\n";
	$staticcaps = $user_staticcaps;
	$user_changed++;
    }
}

if (defined $user_caplength) {
    if ($user_caplength != $caplength) {
	$printstring .= " :: caplength        :: $caplength ==> $user_caplength\n";
	$caplength = $user_caplength;
	$user_changed++;
    }
}

if (defined $user_backboneminrms) {
    if ($user_backboneminrms != $backboneminrms) {
	$printstring .= " :: backboneminrms   :: $backboneminrms ==> $user_backboneminrms\n";
	$backboneminrms = $user_backboneminrms;
	$user_changed++;
    }
}

if (defined $user_backboneminsteps) {
    if ($user_backboneminsteps != $backboneminsteps) {
	$printstring .= " :: backboneminsteps :: $backboneminsteps ==> $user_backboneminsteps\n";
	$backboneminsteps = $user_backboneminsteps;
	$user_changed++;
    }
}

if (defined $user_warmup) {
    if ($user_warmup != $warmup) {
	$printstring .= " :: warmup           :: $warmup ==> $user_warmup\n";
	$warmup = $user_warmup;
	$user_changed++;
    }
}

if (defined $user_warmupstart) {
    if ($user_warmupstart != $warmupstart) {
	$printstring .= " :: warmupstart      :: $warmupstart ==> $user_warmupstart\n";
	$warmupstart = $user_warmupstart;
	$user_changed++;
    }
}

if (defined $user_warmupinterval) {
    if ($user_warmupinterval != $warmupinterval) {
	$printstring .= " :: warmupinterval   :: $warmupinterval ==> $user_warmupinterval\n";
	$warmupinterval = $user_warmupinterval;
	$user_changed++;
    }
}

if (defined $user_warmupsteps) {
    if ($user_warmupsteps != $warmupsteps) {
	$printstring .= " :: warmupsteps      :: $warmupsteps ==> $user_warmupsteps\n";
	$warmupsteps = $user_warmupsteps;
	$user_changed++;
    }
}

if (defined $user_warmuptimestep) {
    if ($user_warmuptimestep != $warmuptimestep) {
	$printstring .= " :: warmuptimestep   :: $warmuptimestep ==> $user_warmuptimestep\n";
	$warmuptimestep = $user_warmuptimestep;
	$user_changed++;
    }
}

if (defined $user_ignorepct) {
    if ($user_ignorepct != $ignorepct) {
	$printstring .= " :: ignorepct        :: $ignorepct ==> $user_ignorepct\n";
	$ignorepct = $user_ignorepct;
	$user_changed++;
    }
}

if (defined $user_finalminimize) {
    if ($user_finalminimize != $finalminimize) {
	$printstring .= " :: finalminimize    :: $finalminimize ==> $user_finalminimize\n";
	$finalminimize = $user_finalminimize;
	$user_changed++;
    }
}

if (defined $user_finalminrms) {
    if ($user_finalminrms != $finalminrms) {
	$printstring .= " :: finalminrms      :: $finalminrms ==> $user_finalminrms\n";
	$finalminrms = $user_finalminrms;
	$user_changed++;
    }
}

if (defined $user_finalminsteps) {
    if ($user_finalminsteps != $finalminsteps) {
	$printstring .= " :: finalminsteps    :: $finalminsteps ==> $user_finalminsteps\n";
	$finalminsteps = $user_finalminsteps;
	$user_changed++;
    }
}

if (defined $user_qsub) {
    if ($user_qsub != $qsub) {
	$printstring .= " :: qsub             :: $qsub ==> $user_qsub\n";
	$qsub = $user_qsub;
	$user_changed++;
    }
}

if (defined $user_queuetype) {
    if ($user_queuetype ne $queuetype) {
	$printstring .= " :: queuetype        :: $queuetype ==> $user_queuetype\n";
	$queuetype = $user_queuetype;
	$user_changed++;
    }
}

if (defined $user_runlocal) {
    if ($user_runlocal != $runlocal) {
	$printstring .= " :: runlocal         :: $runlocal ==> $user_runlocal\n";
	$runlocal = $user_runlocal;
	$user_changed++;
    }
}

if (defined $user_runparallel) {
    if ($user_runparallel != $runparallel) {
	$printstring .= " :: runparallel      :: $runparallel ==> $user_runparallel\n";
	$runparallel = $user_runparallel;
	$user_changed++;
    }
}

if (defined $user_raw) {
    if ($user_raw ne $raw) {
	$printstring .= " :: raw              :: $raw ==> $user_raw\n";
	$raw = $user_raw;
	$user_changed++;
    }
}

if (defined $user_cap) {
    if ($user_cap ne $cap) {
	$printstring .= " :: cap              :: $cap ==> $user_cap\n";
	$cap = $user_cap;
	$user_changed++;
    }
}

if (!$user_changed) { $printstring .= " :: No defaults changed\n"; }
$printstring .= "\n";

################################################################################
##### Run BLAST                                                            #####
################################################################################
my $fnpfx = Modules::OptHelix::opthelix($printstring,
					$mfta,
					$tms_to_run,
					$raw,
					$cap,
					$host,
					$dynsteps,
					$dyntimestep,
					$dynsnapint,
					$dyntemp,
					$dynresidues,
					$ff,
					$alaninecap,
					$staticcaps,
					$caplength,
					$backboneminrms,
					$backboneminsteps,
					$warmup,
					$warmupstart,
					$warmupinterval,
					$warmupsteps,
					$warmuptimestep,
					$ignorepct,
					$finalminimize,
					$finalminrms,
					$finalminsteps,
					$prefix,
					$runlocal,
					$runparallel,
					$help,
					$qsub,
					$queuetype,
					$onqueue,
					$quiet,
					$scream_dir,
					$python_executable,
					$polyalanines_dir,
					$mpsim_data,
					$mpsim_executable,
					$print_copyright1,
					$print_copyright2,
					);

exit;

################################################################################
##### Backup .opthelix File                                                #####
################################################################################
# Below is a backup copy of the .opthelix file that contains the program defaults.
# Should the .opthelix file be accidentally deleted, simply copy the text below,
# remove the first "# " at the beginning of each line (but only one on each line),
# and save the text to a file called ".opthelix" in the same directory as OptHelix.pl.

# # ---> Copy the lines below <--- #
# # ---> Copy the lines above <--- #
