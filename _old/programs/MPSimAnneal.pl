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
use List::Util qw(min max);
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

%tic      = ();
$ff       = "/project/Biogroup/FF/dreiding-0.3.par";
$cycles   =   5; # Number of annealing cycles
$steps    = 100; # Number of steps (1 fs) at each temperature
$tmp_low  =  50; # Low temperature
$tmp_high = 600; # High temperature
$tmp_step =  50; # Temperature Interval
$machine  = "atom";

if (@ARGV == 0) { help(); }

#abcdefghijklmnopqrstuvwxyz
#a  defg ijk  n p r   vwxyz
GetOptions ('h|help'          => \$help,
	    'b|bgf=s'         => \$bgf,
	    'o|out=s'         => \$out,
	    'f|ff=s'          => \$ff,
	    'c|cycles=i'      => \$cycles,   #   5
	    's|steps=i'       => \$steps,    # 100
	    'l|temp_low=i'    => \$tmp_low,  #  50
	    'u|temp_upper=i'  => \$tmp_high, # 600
	    't|temp_step=i'   => \$tmp_step, #  50
	    'q|qsub'          => \$qsub,
	    'm|machine=s'     => \$machine,
	    'nopremin'        => \$nopremin,
	    'onqueue'         => \$onqueue,
	    'debug'           => \$debug);

if ($help) { help(); }

# FF: Absolute path
$ff = File::Spec->rel2abs($ff);

############################################################
### Main Routine                                         ###
############################################################
if (!$bgf) {
    die "MPSimAnneal :: Must provide BGF file!\n";
} elsif (! -e $bgf) {
    die "MPSimAnneal :: Could not find BGF file: $bgf\n";
}
($pfx = $bgf) =~ s/.bgf//;
if (!$out) {
    ($out = $bgf) =~ s/.bgf/.annealed.bgf/;
}

if ($tmp_low <= 0) {
    die "MPSimAnneal :: Invalid low temperature: $tmp_low\n".
	"            :: Must be > 0\n";
}
if ($tmp_step <= 0) {
    die "MPSimAnneal :: Invalid temperature interval size: $tmp_step\n".
	"            :: Must be > 0\n";
}
if ($tmp_low >= $tmp_high) {
    die "MPSimAnneal :: Invalid lower/upper temperatures:\n".
	"            :: Low temp $tmp_low >= High temp $tmp_high\n";
}
if ($cycles <= 0) {
    die "MPSimAnneal :: Number of cycles ($cycles) must be greater than 0.\n";
}
if ($steps <= 0) {
    die "MPSimAnneal :: Number of steps at each temperature ($steps) must\n".
	"            :: be greater than zero.\n";
}

if ($machine !~ /(borg|matrix|hive|wolf1|wolf2|atom|ion|giant8)/) {
    die "MPSimAnneal :: Machine must be: borg|matrix|hive|wolf1|wolf2|atom|ion|giant8\n";
}

# If not running on the queue, submit it
if (!$onqueue) {
    print 
	"MPSimAnneal :: " . localtime() . "\n".
	" :: BGF File :: $bgf\n\n".
	"Settings ::\n".
	" :: Forcefield    :: $ff\n".
	" :: Cycles        :: $cycles\n".
	" :: Steps / Temp  :: $steps\n".
	" :: Low Temp      :: $tmp_low\n".
	" :: High Temp     :: $tmp_high\n".
	" :: Temp Interavl :: $tmp_step\n".
	" :: Pre-Minimize  :: ";
    if ($nopremin) {
	print "No\n\n";
    } else {
	print "Yes\n".
	    " :: Threshold     :: 0.5\n".
	    " :: Max Steps     :: 1000\n\n";
    }

    $pbs =
	"#PBS -l nodes=1,walltime=400:00:00\n".
	"#PBS -q workq\n".
	"#PBS -j oe\n".
	"#PBS -N MPSimAnneal\n".
	"#PBS -m e\n".
	"#!/bin/csh\n".
	"\n".
	"cd \$PBS_O_WORKDIR\n".
	"\n".
	"hostname > node\n".
	"\n".
	"${Bin}/MPSimAnneal.pl".
	" -b $bgf".
	" -o $out".
	" -f $ff".
	" -c $cycles".
	" -s $steps".
	" -l $tmp_low".
	" -u $tmp_high".
	" -t $tmp_step".
	" -m $machine".
	" --onqueue";
    if ($debug) {
	$pbs .= " --debug";
    }
    if ($nopremin) {
	$pbs .= " --nopremin\n";
    } else {
	$pbs .= "\n";
    }
    open PBS, ">${pfx}.pbs";
    print PBS "$pbs";
    close PBS;
    $cwd = cwd();

    if ($qsub) {
	print "Submitting to $machine\n\n";
	`ssh $machine 'cd $cwd ; qsub ${pfx}.pbs'`;
    } else {
	print "PBS Script :: ${pfx}.pbs\n\n";
    }
    exit;
}

############################################################
### Setup Temp Dir                                       ###
############################################################
tic("X");
$username = `whoami`;   chomp $username;
$node     = `hostname`; chomp $node;
$cwd      = cwd();
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime(time());
$mon  += 1;
$year += 1900;
$timestamp = "${year}_${mon}_${mday}.${hour}_${min}_${sec}";
$tmpdir = "/temp1/${username}/${pfx}.MPSimAnneal.${timestamp}";
if (-e $tmpdir) {
    die "MPSimAnneal :: Temp directory already exists:\n".
	" :: Cluster  :: $machine\n".
	" :: Node     :: $node\n".
	" :: Temp Dir :: $tmpdir\n";
}
mkdir "$tmpdir";
copy($bgf,"${tmpdir}/system.bgf");
chdir "$tmpdir";

open LOG, ">${cwd}/${pfx}.MPSimAnneal.out";
print LOG
    "MPSimAnneal :: " . localtime() . "\n".
    " :: Cluster  :: $machine\n".
    " :: Node     :: $node\n".
    " :: BGF File :: $bgf\n\n".
    "Settings ::\n".
    " :: Forcefield    :: $ff\n".
    " :: Cycles        :: $cycles\n".
    " :: Steps / Temp  :: $steps\n".
    " :: Low Temp      :: $tmp_low\n".
    " :: High Temp     :: $tmp_high\n".
    " :: Temp Interavl :: $tmp_step\n".
    " :: Pre-Minimize  :: ";
if ($nopremin) {
    print LOG "No\n\n";
} else {
    print LOG "Yes\n\n";
}

############################################################
### Minimize                                             ###
############################################################
$preanneal = "system.bgf";
$preannealdir = "";
if (!$nopremin) {
    tic(0);
    print LOG
	"Pre-Minimize :: " . localtime() . "\n".
	" :: Threshold :: 0.5\n".
	" :: Max Steps :: 1000\n".
	" :: Runtime   :: ";

    # Setup
    mkdir "0_minimize";
    copy("system.bgf","0_minimize/system.bgf");
    chdir "0_minimize";

    # Minimize
    $command =
	"/project/Biogroup/Software/GEnsemble/utilities/runMPSim.pl".
	" system.bgf -f $ff -l 0 -s 1000 -t 0.5 minvac";
    `$command`;
    $preanneal    = "system_minvac.fin.bgf";
    $preannealdir = "0_minimize/";
    chdir "..";

    print LOG toc(0) . "\n\n";
}

############################################################
### Anneal                                               ###
############################################################
for ($c = 1; $c <= $cycles; $c++) {
    tic($c);
    print LOG "Anneal :: Cycle ${c} :: " . localtime() . "\n".
	" :: Runtime :: ";

    # Setup
    mkdir "${c}_cycle";
    copy("${preannealdir}${preanneal}","${c}_cycle/system.pre_round_${c}.bgf");
    if ($preannealdir ne "") {
	`gzip -r $preannealdir`;
    }
    chdir "${c}_cycle";

    # Control File
    open CTL, ">system.round_${c}.ctl";
    $ctl =
	"PROJECT            system.round_${c}\n".
	"FF                 ${ff}\n".
	"BBOX               -180 180 -180 180 -180 180\n".
	"BBOX_REFLECT       NO\n".
	"STRUCTURE          system.pre_round_${c}.bgf\n".
	"NB_METHOD          CMM\n".
	"CMM_EXPANSION      CENTROID\n".
	"LEVEL              0\n".
	"NB_UPDATE_FREQ     10\n".
	"CELL_REALLOC_FREQ  10\n".
	"RESET_GLOBAL_V     T\n".
	"RESTART_FREQ       500\n".
	"VEL_START          NONMIN\n".
	"BGF_TRAJ           T\n".
	"BGF_TRAJ_FREQ      10\n".
	"DYN_TIME_STEP      1\n".
	"NOSE               tau 0.01\n".
	"ANNEALING_DYNAMICS T\n".
	"AD_NUM_CYCLES      1\n".
	"AD_MIN             ${tmp_low}\n".
	"AD_MAX             ${tmp_high}\n".
	"AD_RATE            ${tmp_step}\n".
	"AD_STEP_SIZE       ${steps}\n".
	"MIN_RMS_DESIRED    0.5\n".
	"MIN_MAX_STEPS      1000\n".
	"MIN_METHOD         CONJUGATE_WAG\n".
	"FINAL_BGF\n".
	"ACTION             TVN\n".
	"SETUP_EEX\n".
	"DO\n".
	"INFO\n".
	"EXIT\n";

    print CTL "$ctl";
    close CTL;

    # MPSim
    `/usr/local/bin/mpsim -s ${steps} system.round_${c}.ctl >& system.round_${c}.txt`;

    # Output
    $preannealdir = "${c}_cycle/";
    $preanneal    = "system.round_${c}.fin.bgf";
    chdir "..";
    print LOG toc($c) . "\n\n";
}

############################################################
### Finalize                                             ###
############################################################
copy("${preannealdir}${preanneal}","$out");
if ($preannealdir ne "") {
    `gzip -r $preannealdir`;
}
if (!$debug) {
    chdir "$cwd";
    `mv $tmpdir ${cwd}`;
} else {
    chdir "$cwd";
    `cp -a $tmpdir ${cwd}`;
}
print LOG
    "Finished!\n".
    " :: Total Runtime :: " . toc("X") . "\n\n";

exit;

################################################################################
### tic/toc --- Timing subroutines
################################################################################
sub tic {
    (my $counter) = @_;
    $tic{$counter} = time();               # Store the current time in %tic
}

sub toc {
    (my $counter) = @_;
    my $toc    = time();                      # Get the current time

    my $dt     = $toc - $tic{$counter};       # Find the time difference in seconds
    my $tot_dt = $dt;                         # Save this value

    my $days   = floor($dt / (24 * 60 * 60)); # Find the total number of days
    $dt       -= $days * 24 * 60 * 60;        # Remove (days) worth of seconds

    my $hours  = floor($dt / (60 * 60));      # Find the total number of hours remaining
    $dt       -= $hours * 60 * 60;            # Remove (hours) worth of seconds

    my $mins   = floor($dt / 60);             # Find the total number of minutes remaining
    $dt       -= $mins * 60;                  # Remove (minutes) worth of seconds

    my $secs   = $dt;                         # Sconds remining

    # Return time: time (formatted time)
    if ($days > 0) {
	return "${days} d, ${hours} h, ${mins} m, ${secs} s";
    } elsif ($hours > 0) {
	return "${hours} h, ${mins} m, ${secs} s";
    } elsif ($mins > 0) {
	return "${mins} m, ${secs} s";
    } else {
	return "$tot_dt s";
    }
}

############################################################
### Help                                                 ###
############################################################

sub help {

    my $help = "
Program:
 :: MPSimAnneal.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: MPSimAnneal.pl -b {bgf} -c {cycles}
 ::    -s {steps ea. temp} -l {low temp} -u {high temp}
 ::    -t {temp interval} -m {machine} -q

Input:
 :: -b | --bgf        :: Filename
 :: BGF file to anneal.  Make sure to set flexible or movable atoms
 :: before submitting.

 :: -o | --out        :: Filename
 :: Final output filename.

 :: -f | --ff         :: Forcefield filename
 :: Forcefield.  Defaults to dreiding-0.3.par

 :: -c | --cycles     :: Integer > 0
 :: Number of annealing cycles.  Default is 5.

 :: -s | --steps      :: Integer > 0
 :: Number of steps at each temperature. Each step is 1 fs.  Default
 :: is 100 steps, or 0.1 ps at each temperature.

 :: -l | --temp_low   :: Integer > 0
 :: Low temperature in the annealing cycle.  Default is 50 K.

 :: -u | --temp_upper :: Integer > Low temp
 :: High temperature in the annealing cycle.  Default is 600 K.

 :: -t | --temp_step  :: Integer > 0
 :: Temperature interval.  Default is 50 K.

 :: --nopremin        :: Integer > 0
 :: Do not minimize before annealing.  If not used, the flexible atoms
 :: will be minimized to 0.5 rms force or 1000 steps.

 :: -m | --machine    :: borg|matrix|hive|wolf1|wolf2|atom|ion|giant8
 :: Cluster to run annealing on.  Default: hive

 :: -q | --qsub       :: No Input
 :: Submit to queue

 :: -h | --help       :: No Input
 :: Displays this help message.

Description:
 :: This program is designed to run multiple cycles of MPSim
 :: annealing.
 ::
 :: Steps:
 :: 1) Minimize movable atoms to 0.5 rms force (1000 steps max)
 :: 2) Take minimized structure for first cycle of annealing
 :: 3) Minimize movable atoms in final structure from annealing to 0.5
 ::    rms force (1000 steps max)
 :: 4) Repeat steps 2 and 3 for additional cycles of annealing.

Usage:
 :: MPSimAnneal.pl -b {bgf} -c {cycles}
 ::    -s {steps ea. temp} -l {low temp} -u {high temp}
 ::    -t {temp interval} -m {machine} -q

";

    die "$help";
}
