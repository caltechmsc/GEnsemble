#!/usr/bin/perl -w

#####################################################################
#                                                                   #
# BiHelix (GEnsemble)                                               #
# all_bihelix_pairs.pl                                              #
# bihelixrot_scream2.pl                                             #
# combi_frombihelixsum.pl                                           #
# combihelixrot_membscream.pl                                       #
#                                                                   #
# Copyright (c) 2008                                                #
# Ravinder Abrol and William A. Goddard III                         #
# Materials and Process Simulation Center                           #
# California Institute of Technology                                #
# Pasadena, CA, USA                                                 #
# All Rights Reserved.                                              #
#####################################################################

BEGIN {
    # add these modules to @INC
    use FindBin ();
    use lib "$FindBin::Bin";
}

use Cwd;
use File::Copy;
use File::Basename;
use Getopt::Long;
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

$sbin = $FindBin::Bin;
$curdir = cwd();
#$localmach = hostname;

GetOptions ('h|help'                 => \$help,
        'p|protfile=s'               => \$protfile,
        'pairs|helixpairfile=s'      => \$helixpairfile,
        'a|anglefile=s'              => \$anglefile,
        'r|rotate'                   => \$rotate,
        's|scream'                   => \$scream,
        'mp|mpsim:i'                 => \$mpsim,
        'rlib|rotalib=f'             => \$rotalib,
        'an|analyze=i'               => \$analyze,
        'd|debug'                    => \$debug,
        'mach|machine=s'             => \$machine);

if ($help)       { &help; }
if (not defined $protfile)  { &help; }

#Set Default for BiHelix Mean Field Analysis
if (not defined $analyze) { $analyze = 1000; }

if (defined $machine) { $jobmode = 'parallel'; }
if (not defined $machine) { die "Specify machine to run jobs with -mach option.\n"; }
#($machine) = $localmach =~ /([^.]*)/;
#$jobmode = 'serial';

print "jobmode $jobmode\n";

# Set default rotamer library to be 1.0 A
if (not defined $rotalib) { $rotalib = 1.0; }

if ($rotalib < 0.1 || $rotalib > 5.0) { die "specify a value from 0.1 to 5.0\n";}

$rdiv = floor(10*$rotalib+0.5);
if ($rdiv < 10) { $rdiv = "0"."$rdiv"; }

if (defined $debug) {
    $keep = 1;
} else {
    $keep = 0;
}

$action = "no";
if ($rotate || $scream) { $action = "yes";}

if ($action eq "no") { die "specify action to rotate or scream\n"; }

( $protprefix, $path, $suffix ) = fileparse( $protfile, qr/\.[^.]*/ );
 if ($path || $suffix) {}; # Avoid warning

if (not defined $helixpairfile) {
    system("cp $sbin/annex/default_helixpairs.dat myhelixpairs.dat");
    $helixpairfile = "myhelixpairs.dat";
}
    open (PAIRS,"< $helixpairfile");
    $paircount++ while (<PAIRS>);
    close (PAIRS);

if ($paircount == 12) {
$analyze_command = "${sbin}/bihelix_anal.pl $protprefix $analyze 0_0_0_0_0_0_0";
}

$defaultsfile = "${sbin}/../.gensemble/.bihelix";
open DEF, "$defaultsfile";
while (<DEF>) {
    if (/^queuetype\s+(\S+)/)          { $queuetype         = $1; }
}
close DEF;
print "queuetype $queuetype\n";

if ($scream) {
    if ($anglefile) {
        $subcommand = "${sbin}/bihelixrot_scream2.pl -rdiv $rdiv -p $protfile -a $anglefile -r -s -k $keep";
    } else {
        $subcommand = "${sbin}/bihelixrot_scream2.pl -rdiv $rdiv -p $protfile -r -s -k $keep";
    }
} else {
    if ($anglefile) {
        $subcommand = "${sbin}/bihelixrot_scream2.pl -rdiv $rdiv -p $protfile -a $anglefile -r";
    } else {
        $subcommand = "${sbin}/bihelixrot_scream2.pl -rdiv $rdiv -p $protfile -r";
    }
}


if (defined $mpsim) {
    $subcommand = "$subcommand"."  -mp";
    if ($mpsim > 0) {
        $subcommand = "$subcommand"." $mpsim";
    }
}

$paircount = 0;

if ($jobmode eq 'serial') {
    open (PAIRS,$helixpairfile);
    while ($lines = <PAIRS>) {
        chomp $lines;
        @helixids = split(/\s+/, $lines);
        $helix_i = $helixids[0];
        $helix_j = $helixids[1];
        $run_command="echo $helix_i $helix_j bihelix running.; $subcommand -i $helix_i -j $helix_j > ${protprefix}_H${helix_i}-H${helix_j}_bihel.out; echo $helix_i $helix_j bihelix finished.";
    if ($keep == 0) {
     $run_command .= "\nrm -f ${protprefix}_H${helix_i}-H${helix_j}_bihel.out";
    }
        system("$run_command");
    }
    close PAIRS;
    if ($paircount == 12) {
    system("echo Starting BiHelix Mean Field Analysis.; $analyze_command scream; echo Finished BiHelix Mean Field Analysis.");
    if (defined $mpsim) {
        if ($mpsim > 0) {
    system("echo Starting BiHelix Mean Field Analysis.; $analyze_command mpsim-aftmin; echo Finished BiHelix Mean Field Analysis.");
        } else {
    system("echo Starting BiHelix Mean Field Analysis.; $analyze_command mpsim-befmin; echo Finished BiHelix Mean Field Analysis.");
        }
    }
    }
} else {
    $pcount=0;
    open (PAIRS,$helixpairfile);
    while ($lines = <PAIRS>) {
	$pcount++;
        chomp $lines;
        @helixids = split(/\s+/, $lines);
        $helix_i = $helixids[0];
        $helix_j = $helixids[1];
        $runfile = "run_bihel_H${helix_i}-H${helix_j}";
        $run_command = "$subcommand -i $helix_i -j $helix_j > ${protprefix}_H${helix_i}-H${helix_j}_bihel.out";
        if ($pcount == 10 and defined $mpsim) {
        if ($mpsim > 0) {
        $run_command .= "\n${sbin}/annex/check_bihelix_status.pl\n".
                        "$analyze_command mpsim-aftmin";
        }
        } elsif ($pcount == 11 and defined $mpsim) {
        $run_command .= "\n${sbin}/annex/check_bihelix_status.pl\n".
                        "$analyze_command mpsim-befmin";
        } elsif ($pcount == 12) {
        $run_command .= "\n${sbin}/annex/check_bihelix_status.pl\n".
                        "$analyze_command scream";
	    }
    if ($keep == 0) {
     $run_command .= "\nrm -f ${protprefix}_H${helix_i}-H${helix_j}_bihel.out";
    }
	if ($queuetype eq "sge") {
	   my $sge = "\#!/bin/csh\n".
            "#\$ -N BiHelix_${helix_i}-${helix_j}\n".
            "#\$ -j y\n".
            "$run_command\n";
            open SGE, ">$runfile.sge";
            print SGE "$sge";
            close SGE;
            system("ssh $machine 'cd $curdir; qsub -cwd $runfile.sge'");
        } elsif ($queuetype eq "pbs") {
            my $pbs = "#PBS -l nodes=1,walltime=24:00:00\n".
            "#PBS -q workq\n".
            "#PBS -j oe\n".
            "#PBS -N BiHelix_${helix_i}-${helix_j}\n".
            "#PBS -m e\n".
            "#!/bin/csh\n".
	    "cd \$PBS_O_WORKDIR\n".
            "$run_command\n";
            open PBS, ">$runfile.pbs";
            print PBS "$pbs";
            close PBS;
            system("ssh $machine 'cd $curdir; qsub $runfile.pbs'");
#	    sleep 5; # ADAM
        } elsif ($queuetype eq "sbatch") {
            my $sbatch = "#!/bin/bash\n".
            "#SBATCH --job-name=BiHelix_${helix_i}-${helix_j}\n".
            "#SBATCH --output=BiHelix_${helix_i}-${helix_j}.out\n".
            "#SBATCH --error=BiHelix_${helix_i}-${helix_j}.err\n".
            "#SBATCH --time=48:00:00\n".
            "$run_command\n";
            open SBATCH, ">$runfile.sbatch";
            print SBATCH "$sbatch";
            close SBATCH;
            system("ssh $machine 'cd $curdir; sbatch $runfile.sbatch'");
        }
        print "$helix_i $helix_j pair rotscream job submitted on $machine.\n";
    }
}



sub help {
    my $copyright = "\x{a9}";
    $help_message = "

Program:
 :: all_bihelix_pairs.pl

Location:
 :: \$ge_path/programs/bihelixrot2/all_bihelix_pairs.pl

Release:
 :: Version 1.2 (25 April 2008)

Authors:
 :: Ravi Abrol (abrol\@wag.caltech.edu)

Usage:
 :: all_bihelix_pairs.pl -p {protein_bgf_file} -rlib {rotamer library} -pairs {helixpairfile} -a {combinatorial_rotation_angle_data_file} -an {number of output combinations} -r -s -mp {minimization steps} -d -mach {machine}

GetOptions ('h|help'                 => \$help,
        'p|protfile=s'               => \$protfile,
        'pairs|helixpairfile=s'      => \$helixpairfile,
        'a|anglefile=s'              => \$anglefile,
        'r|rotate'                   => \$rotate,
        's|scream'                   => \$scream,
        'mp|mpsim:i'                 => \$mpsim,
        'rlib|rotalib=f'             => \$rotalib,
        'an|analyze=i'               => \$analyze,
        'd|debug'                    => \$debug,
        'mach|machine=s'             => \$machine);

Options:
 :: -h | --help             :: Optional    :: No Input
 :: Prints this help message.

 :: -p | --protfile         :: Required    :: Filename
 :: This is the protein BGF file

 :: -rlib | --rotalib       :: Optional    :: Float
 :: Diversity of the rotamer library requested in Angstroms.
 :: Acceptable inputs 0.1 through 5.0
 :: Default is 1.0

 :: -pairs | --helixpairfile    :: Optional    :: Integer
 ::  File containing helix pairs for performing bihelix_rotscream.
 ::  If not specified, default set of 12 pairs of helices are used:
     1-2, 1-7, 2-3, 2-4, 2-7, 3-4, 3-5, 3-6, 3-7, 4-5, 5-6, 6-7.

 :: -a | --anglefile        :: Optional    :: Filename
 :: This is the file containing the angles for each of the two helices
 :: to generate the combinatorial set of structures.
 :: An example anglefile that will generate 36 combinations:
 :: (First line corresponds to helix_i choices, second line
 :: corresponds to helix_j choices and so on. Also we have
 :: retired negative angles as they cause confusion in
 :: file names)
    0 60 120 180 240 300
    0 60 120 180 240 300
 ::
 :: If this flag is not provided then the default action is to take
 :: 144 combinations for two helix rotations corresponding to an angle file:
    0 30 60 90 120 150 180 210 240 270 300 330
    0 30 60 90 120 150 180 210 240 270 300 330

 :: -r | --rotate           :: Conditional-Optional    :: No Input
 :: Specify this option, if you only want to generate
 :: structure files corresponding to angles specified
 :: in the file given as an input to the -a option above.

 :: -s | --scream           :: Conditional-Optional    :: No Input
 :: Using this option will enable the -r option and
 :: then perform SCREAM on each of the rotated structures.

 :: You need to specify at least one of the two options: -r or -s
 :: Specifying both (-r -s) is equivalent to -s.

 :: -mp | --mpsim            :: Optional-Integer    :: No Input
 :: Use this option to evaluate MPSim energies for SCREAMed structures.
 :: Provide an interger number as input to perform that many minimization
 :: steps using MPSim.

 :: -an | --analyze         :: Optional                :: Integer
 :: Number of rotational combinations from BiHelix Analysis to output.
 :: Default is 1000

 :: -d | --debug            :: Optional                :: No Input
 :: Specify this flag if you want to keep all structure files for debugging
 :: or other purposes. Default is to keep only a minimal set of files.

 :: -mach | --machine          :: Required
 :: The machine to run the bihelix_rotscream jobs.
 :: If the machine is specified, then jobs are submitted for
 :: each helix-pair in parallel.


Description:
 :: This wrapper script sets up the bihelical combinatorial rotational
 :: scan (other helices are not present at all), for all pairs of
 :: interacting helices. The default interacting pairs of helices are:
 :: 1-2, 1-7, 2-3, 2-4, 2-7, 3-4, 3-5, 3-6, 3-7, 4-5, 5-6, 6-7.
 :: After this the bihelix analysis is performed to output a target number
 :: of top few structures specified by -an flag.


Usage (repeated):
 :: all_bihelix_pairs.pl -p {protein_bgf_file} -rlib {rotamer library} -pairs {helixpairfile} -a {combinatorial_rotation_angle_data_file} -an {number of output combinations} -r -s -mp {minimization steps} -d -mach {machine}

";
    die $help_message;
}
