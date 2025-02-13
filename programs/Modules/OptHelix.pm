package Modules::OptHelix;

my $copyright = "
#####################################################################
#                                                                   #
# OptHelix.pl/OptHelix.pm                                           #
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
    push @INC, "$Bin/thirdparty/libwww/";
}

use strict;
use warnings;
use base 'Exporter';

use Cwd;
use File::Copy;
use File::Path;
use File::Spec;
use LWP::Simple;
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

our $VERSION = 1.1;
our @EXPORT  = qw(opthelix
		  checkVersion
		  help);

# Global Input Variables
our ($mfta, $name, $prefix, $tms_to_run, $help, $quiet, $showdefaults, $user_temp, $dynsteps, $dyntimestep, $dynsnapint, $dyntemp, $dynresidues, $ff, $alaninecap, $caplength, $staticcaps, $backboneminrms, $backboneminsteps, $warmup, $warmupstart, $warmupinterval, $warmupsteps, $warmuptimestep, $ignorepct, $finalminimize, $finalminsteps, $finalminrms, $runlocal, $runparallel, $qsub, $queuetype, $print_copyright1, $print_copyright2, $polyalanines_dir, $scream_dir, $mpsim_data, $mpsim_executable, $host, $onqueue, $python_executable, $raw, $cap);

# Global Internal Variables
our (@tmlist, %tms, $target_header, $target_fasta, $target_seq, %skiptm, $numsnaps, $numsnapstokeep, $numsnapstoskip, $firstsnap, $firstsnaptokeep, $firstsnapnumtokeep, %dynamics, $maxtmnum, $fnpfx, $pfx);

################################################################################
##### Version Check                                                        #####
################################################################################
sub checkVersion { return $VERSION; }

################################################################################
##### Main Routine                                                         #####
################################################################################
sub opthelix {
    # Load Input
    (my $printstring,
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
     $print_copyright2) = @_;

    # Calculate some Snap Information
    $maxtmnum           = 0;
    $numsnaps           = ($dynsteps / $dynsnapint);
    $numsnapstokeep     = $numsnaps - (floor($numsnaps * $ignorepct / 100));
    $numsnapstoskip     = floor($numsnaps * $ignorepct / 100);
    $firstsnap          = $dynsnapint - 1;
    $firstsnapnumtokeep = $numsnapstoskip + 1;
    $firstsnaptokeep    = ($firstsnapnumtokeep * $dynsnapint) - 1;
    if (int($numsnaps) != $numsnaps) {
	die "OptHelix :: Number of dynamics steps ($dynsteps) and snap interval ($dynsnapint)\n".
	    "         :: do not give an integer number of snapshots.\n\n";
    }

    # Check Help Conditions
    if ($help) { help(); }

    # Check Input
#    checkInput();

    # Resubmit to Queue
    if (($qsub || $runparallel) && (!$onqueue)) {
	qsub();
    }

    # Open Output File
    ($fnpfx = $mfta) =~ s/.mfta//;
    if ($prefix) {
	$fnpfx = "$prefix";
    }
    if ($prefix) {
	$pfx = $prefix . ".";
    } else {
	$pfx = "";
    }
    open LOG, ">${fnpfx}.log";
    if ($print_copyright1) { printDuo($copyright,0); }
    printDuo($printstring, $quiet);

    # Print Program Parameters
    $printstring =
	"\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\n".
	"\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@ Running OptHelix v$VERSION \@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\n".
	"\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\n\n";
    printDuo($printstring, 0);

    # Load Helices from MFTA
    loadMFTA();
    loadScreamMPSim();
    printSetupInfo();

    # For Each TM
    for (my $i = 0; $i < @tmlist; $i++) {
	$printstring = "Working on TM :: $tmlist[$i]\n";
	printDuo($printstring,0);

        # Set Up and Change Directory
	mkdir "${pfx}helix$tmlist[$i]";
	chdir "${pfx}helix$tmlist[$i]";

        # SCREAM Pro & Gly
	screamProAndGly($tmlist[$i]);
	if ($skiptm{$tmlist[$i]}) { next; } # Skip the rest of this TM if Scream failed

        # Minimize Backbone
	minimizeBackbone($tmlist[$i]);

        # SCREAM Dynamics Residues
	screamDynamicsResidues($tmlist[$i]);
	if ($skiptm{$tmlist[$i]}) { next; } # Skip the rest of this TM if Scream failed

        # Set Up Warmup & Dynamics
	runDynamics($tmlist[$i]);

	printDuo("\n",$quiet);
	chdir "..";
    }

    # Monitor Jobs
    my $wait = 1;
    while ($wait) {
	$wait = 0;
	for (my $i = 0; $i < @tmlist; $i++) {
	    if ($skiptm{$tmlist[$i]}) { next; } # Skip this TM if Scream failed
	    if (! -e "${pfx}helix$tmlist[$i]/4_Dynamics/_dyn_finished_") { $wait = 1; }
	}
	sleep 5;
    }

    # For Each TM
    for (my $i = 0; $i < @tmlist; $i++) {
	if ($skiptm{$tmlist[$i]}) { next; } # Skip the rest of this TM if Scream failed
	chdir "${pfx}helix$tmlist[$i]";
	$printstring = "Finishing TM :: $tmlist[$i]\n";
	printDuo($printstring, 0);

        # Find Lowest Energy & Average RMSD structures
	findBestStructures($tmlist[$i]);

        # SCREAM Remaining Sidechains
	screamRemaining($tmlist[$i]);
	if ($skiptm{$tmlist[$i]}) { next; } # Skip the rest of this TM if Scream failed

        # Final Minimization
	if ($finalminimize) {
	    finalMinimization($tmlist[$i]);
	}

	# Remove Caps & Renumber TMs
	chdir "..";
	finalizeTMs($tmlist[$i]);

	printDuo("\n",$quiet);
    }

#    # Fix Hydrogens
#    `${Bin}/utilities/f-t-h-all.pl *.bgf`;

    # Print VMD Files
    vmd();

    # Print Copyright
    if ($print_copyright2) { printDuo($copyright, 0); }

    close LOG;
    return "$fnpfx";
}

################################################################################
##### Check Input                                                          #####
################################################################################
sub checkInput {
}

################################################################################
##### QSub                                                                 #####
################################################################################
sub qsub {
    my $cwd = cwd;
    my $queuestring =
	"cd ${cwd}\n".
	"${Bin}/OptHelix.pl -f $mfta";
    
    $queuestring .=
	" --raw $raw".
	" --cap $cap".
	" --dynsteps $dynsteps".
	" --dyntimestep $dyntimestep".
	" --dynsnapint $dynsnapint".
	" --dyntemp $dyntemp".
	" --dynresidues $dynresidues".
	" --ff $ff".
	" --caplength $caplength".
	" --backboneminrms $backboneminrms".
	" --backboneminsteps $backboneminsteps".
	" --warmupstart $warmupstart".
	" --warmupinterval $warmupinterval".
	" --warmupsteps $warmupsteps".
	" --warmuptimestep $warmuptimestep".
	" --ignorepct $ignorepct".
	" --finalminrms $finalminrms".
	" --finalminsteps $finalminsteps".
	" --queuetype $queuetype";

    if ($name) {
	$queuestring .= " --name $name";
    } elsif ($prefix) {
	$queuestring .= " --prefix $prefix";
    }

    if ($tms_to_run) {
	$queuestring .= " --tms $tms_to_run";
    }

    if ($host) {
	$queuestring .= " --host $host";
    } else {
	$host = `hostname`; chomp $host;
	$queuestring .= " --host $host";
    }

    if ($alaninecap) {
	$queuestring .= " --alaninecap $alaninecap";
    } else {
	$queuestring .= " --noalaninecap";
    }

    if ($staticcaps) {
	$queuestring .= " --staticcaps $staticcaps";
    } else {
	$queuestring .= " --nostaticcaps";
    }

    if ($warmup) {
	$queuestring .= " --warmup $warmup";
    } else {
	$queuestring .= " --nowarmup";
    }

    if ($finalminimize) {
	$queuestring .= " --finalminimize $finalminimize";
    } else {
	$queuestring .= " --nofinalminimize";
    }

    if ($runlocal) {
	$queuestring .= " --runlocal $runlocal";
    } else {
	$queuestring .= " --norunlocal";
    }

    if ($runparallel) {
	$queuestring .= " --runparallel $runparallel";
    } else {
	$queuestring .= " --norunparallel";
    }

    if ($quiet) {
	$queuestring .= " --quiet";
    }

    $queuestring .= " --onqueue";

    print "OptHelix is re-submitting itself to the queue on $host.\n\n";

    if ($queuetype eq "sge") {
	my $sge = "\#!/bin/csh\n".
	    "#\$ -N OptHelix\n".
	    "#\$ -j y\n".
	    "$queuestring\n";
	open SGE, ">opthelix.sge";
	print SGE "$sge";
	close SGE;
	system("ssh $host 'cd $cwd ; qsub -cwd opthelix.sge'");

    } elsif ($queuetype eq "pbs") {
	my $pbs = "#PBS -l nodes=1,walltime=48:00:00\n".
	    "#PBS -q workq\n".
	    "#PBS -j oe\n".
	    "#PBS -N OptHelix\n".
	    "#PBS -m e\n".
	    "#!/bin/csh\n".
	    "$queuestring\n";
	open PBS, ">opthelix.pbs";
	print PBS "$pbs";
	close PBS;
	system("ssh $host 'cd $cwd ; qsub opthelix.pbs'");
    }

    exit;
}

################################################################################
##### loadScream                                                           #####
################################################################################
sub loadScreamMPSim {
    $ENV{INSTALL_PATH}               = "${Bin}/$scream_dir";
    $ENV{SCREAM_MAIN_SCRIPT_PATH}    = "$ENV{INSTALL_PATH}/scripts/";
    $ENV{SCREAM_LIB_PATH}            = "$ENV{INSTALL_PATH}/lib/v3.0/Clustered/lib/";
    $ENV{SCWRL_LIB_PATH}             = "$ENV{INSTALL_PATH}/lib/v3.0/SCWRL/lib/";
    $ENV{SCREAM_CNN_PATH}            = "$ENV{INSTALL_PATH}/lib/v3.0/NtrlAARotConn/";
    $ENV{SCREAM_DELTA_PAR_FILE_PATH} = "$ENV{INSTALL_PATH}/lib/SCREAM_delta_par_files/";
    $ENV{FORCE_FIELD_FILE}           = "${Bin}/$ff";
    $ENV{PYTHON_EXE}                 = "${Bin}/$python_executable";

    $ENV{PYTHONPATH} =
	      "${Bin}/$scream_dir/SCREAM/swig/python/build/lib.linux-i686-2.3/".
	":" . "${Bin}/$scream_dir/SCREAM/python/app/".
	":" . "${Bin}/$scream_dir/PythonDeps/";

    $ENV{MPSIM_DATA} = "${Bin}/$mpsim_data";
}

################################################################################
##### Load MFTA                                                            #####
################################################################################
sub loadMFTA {
    my $printstring = "Loading MFTA File :: $mfta\n";

    # Load info from the MFTA file.
    open MFTA, "$mfta";
    $target_seq = "";
    while (<MFTA>) {
	my $line = $_;
	chomp $line;
	if ($line =~ /^\>/) {
	    $target_header .= $line;
	    $target_fasta  .= $line . "\n";
	} elsif ($line !~ /^[\>,\*,\#]/) {
	    $target_seq    = "$target_seq" . "$line";
	    $target_fasta  = "$target_fasta" . "$line" . "\n";
	}

	#          TM        RawB    RawE    CapB    CapE    ManRB   ManRE   ManCB   ManCE
	elsif ($line =~ /^\*\s+(\S+)tm\s+(\S+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)/) {
	    my $currtm = $1;
	    $tms{$currtm}{predrawstart} = $2;
	    $tms{$currtm}{predrawstop}  = $3;
	    $tms{$currtm}{predcapstart} = $4;
	    $tms{$currtm}{predcapstop}  = $5;
	    $tms{$currtm}{manrawstart}  = $6;
	    $tms{$currtm}{manrawstop}   = $7;
	    $tms{$currtm}{mancapstart}  = $8;
	    $tms{$currtm}{mancapstop}   = $9;

	    if ($raw =~ /pred/) {
		$tms{$currtm}{rawstart} = $tms{$currtm}{predrawstart};
		$tms{$currtm}{rawstop}  = $tms{$currtm}{predrawstop};
	    } elsif ($raw =~ /man/) {
		$tms{$currtm}{rawstart} = $tms{$currtm}{manrawstart};
		$tms{$currtm}{rawstop}  = $tms{$currtm}{manrawstop};		
	    }

	    if ($cap =~ /pred/) {
		$tms{$currtm}{start} = $tms{$currtm}{predcapstart};
		$tms{$currtm}{stop}  = $tms{$currtm}{predcapstop};
	    } elsif ($cap =~ /man/) {
		$tms{$currtm}{start} = $tms{$currtm}{mancapstart};
		$tms{$currtm}{stop}  = $tms{$currtm}{mancapstop};
	    }

	    if ($tms{$currtm}{start} !~ /^\d+$/) {
		die "OptHelix :: Capped TM Start Invalid :: $tms{$currtm}{start}\n";
	    }
	    if ($tms{$currtm}{stop} !~ /^\d+$/) {
		die "OptHelix :: Capped TM Stop Invalid :: $tms{$currtm}{stop}\n";
	    }
	    if ($tms{$currtm}{start} >= $tms{$currtm}{stop}) {
		die "OptHelix :: Capped TM Start/Stop Invalid\n".
		    "         :: $tms{$currtm}{start} >= $tms{$currtm}{stop}\n";
	    }
	    if ($raw !~ /none/) {
		if ($tms{$currtm}{rawstart} !~ /^\d+$/) {
		    die "OptHelix :: Raw TM Start Invalid :: $tms{$currtm}{rawstart}\n";
		}
		if ($tms{$currtm}{rawstop} !~ /^\d+$/) {
		    die "OptHelix :: Raw TM Stop Invalid :: $tms{$currtm}{rawstop}\n";
		}
		if ($tms{$currtm}{rawstart} < $tms{$currtm}{start}) {
		    die "OptHelix :: TM Start Invalid :: Raw starts before Cap\n".
			"         :: $tms{$currtm}{rawstart} < $tms{$currtm}{start}\n";
		}
		if ($tms{$currtm}{rawstop}  > $tms{$currtm}{stop}) {
		    die "OptHelix :: TM Stop Invalid :: Raw stops after Cap\n".
			"         :: $tms{$currtm}{rawstop} > $tms{$currtm}{stop}\n";
		}
		if ($tms{$currtm}{rawstart} >= $tms{$currtm}{rawstop}) {
		    die "OptHelix :: Raw TM Start/Stop Invalid\n".
			"         :: $tms{$currtm}{rawstart} >= $tms{$currtm}{rawstop}\n";
		}
	    }

	    push @tmlist, $currtm;
	    if ($currtm > $maxtmnum) { $maxtmnum = $currtm; }
	}
    }
    close MFTA;

    if (@tmlist < 1) {
	die "OptHelix :: No TMs Found.  Check the Modified FASTA File.\n\n";
    }

    foreach my $currtm (@tmlist) {
	if ($raw !~ /none/) {
	    $tms{$currtm}{rawsequence} = substr($target_seq, $tms{$currtm}{rawstart}-1, $tms{$currtm}{rawstop}-$tms{$currtm}{rawstart}+1);
	    $tms{$currtm}{rawlength}   = $tms{$currtm}{rawstop}-$tms{$currtm}{rawstart}+1;
	}

	$tms{$currtm}{sequence} = substr($target_seq, $tms{$currtm}{start}-1, $tms{$currtm}{stop}-$tms{$currtm}{start}+1);
	$tms{$currtm}{length}   = $tms{$currtm}{stop}-$tms{$currtm}{start}+1;
    }

    # Apply Capping
    my $max_tm_length = -1;
    for (my $i = 0; $i < @tmlist; $i++) {
	# If we want to cap
	if ($alaninecap) {
	    # If we want static caps
	    if ($staticcaps) {
		$tms{$tmlist[$i]}{ncap}        = "A" x $caplength;
		$tms{$tmlist[$i]}{ncap_length} = $caplength;
		$tms{$tmlist[$i]}{ccap}        = "A" x $caplength;
		$tms{$tmlist[$i]}{ccap_length} = $caplength;
		$tms{$tmlist[$i]}{capseq}      = $tms{$tmlist[$i]}{ncap} . $tms{$tmlist[$i]}{sequence} . $tms{$tmlist[$i]}{ccap};
		$tms{$tmlist[$i]}{caplength}   = length($tms{$tmlist[$i]}{ncap}) + $tms{$tmlist[$i]}{length} + length($tms{$tmlist[$i]}{ccap});

	    # If we want dynamic caps
	    } else {
		my $n_p =  index($tms{$tmlist[$i]}{sequence}, "P");
		my $c_p = rindex($tms{$tmlist[$i]}{sequence}, "P");

		# N-term Cap
		if (($n_p != -1) && ($n_p < $caplength)) {
		    $tms{$tmlist[$i]}{ncap}        = "A" x ($caplength - $n_p);
		    $tms{$tmlist[$i]}{ncap_length} = $caplength - $n_p;
		} else {
		    $tms{$tmlist[$i]}{ncap}        = "";
		    $tms{$tmlist[$i]}{ncap_length} = 0;
		}

		# C-term Cap
		if (($c_p != -1) && ($tms{$tmlist[$i]}{length} - $c_p < ($caplength + 1))) {
		    $tms{$tmlist[$i]}{ccap}        = "A" x ($caplength - ($tms{$tmlist[$i]}{length} - $c_p) + 1);
		    $tms{$tmlist[$i]}{ccap_length} = $caplength - ($tms{$tmlist[$i]}{length} - $c_p) + 1;
		} else {
		    $tms{$tmlist[$i]}{ccap}        = "";
		    $tms{$tmlist[$i]}{ccap_length} = 0;
		}

		$tms{$tmlist[$i]}{capseq}    = $tms{$tmlist[$i]}{ncap} . $tms{$tmlist[$i]}{sequence} . $tms{$tmlist[$i]}{ccap};
		$tms{$tmlist[$i]}{caplength} = length($tms{$tmlist[$i]}{ncap}) + $tms{$tmlist[$i]}{length} + length($tms{$tmlist[$i]}{ccap});
	    }

	# If we don't want to cap
	} else {
	    $tms{$tmlist[$i]}{ncap}        = "";
	    $tms{$tmlist[$i]}{ncap_length} = 0;
	    $tms{$tmlist[$i]}{ccap}        = "";
	    $tms{$tmlist[$i]}{ccap_length} = 0;
	    $tms{$tmlist[$i]}{capseq}      = $tms{$tmlist[$i]}{sequence};
	    $tms{$tmlist[$i]}{caplength}   = $tms{$tmlist[$i]}{length};
	}

	if (length($tms{$tmlist[$i]}{capseq}) > $max_tm_length) { $max_tm_length = length($tms{$tmlist[$i]}{capseq}); }
    }

    for (my $i = 0; $i < @tmlist; $i++) {
	if ($raw !~ /none/) {
	    $printstring .= sprintf
		" :: TM %2d RAW :: %3d :: %s%s%s%s%s%s :: %3d :: Length %2d\n",
		$tmlist[$i],
		$tms{$tmlist[$i]}{rawstart},
		" " x ($tms{$tmlist[$i]}{ncap_length}),
		" " x ($tms{$tmlist[$i]}{rawstart} - $tms{$tmlist[$i]}{start}),
		$tms{$tmlist[$i]}{rawsequence},
		" " x ($tms{$tmlist[$i]}{stop} - $tms{$tmlist[$i]}{rawstop}),
		" " x ($tms{$tmlist[$i]}{ccap_length}),
		" " x ($max_tm_length - ($tms{$tmlist[$i]}{ncap_length} + $tms{$tmlist[$i]}{length} + $tms{$tmlist[$i]}{ccap_length})),
		$tms{$tmlist[$i]}{rawstop},
		$tms{$tmlist[$i]}{rawlength};
	}

	$printstring .= sprintf
	    " :: TM %2d CAP :: %3d :: %s%s%s%s :: %3d :: Length %2d\n",
	    $tmlist[$i],
	    $tms{$tmlist[$i]}{start},
	    " " x ($tms{$tmlist[$i]}{ncap_length}),
	    $tms{$tmlist[$i]}{sequence},
	    " " x ($tms{$tmlist[$i]}{ccap_length}),
	    " " x ($max_tm_length - ($tms{$tmlist[$i]}{ncap_length} + $tms{$tmlist[$i]}{length} + $tms{$tmlist[$i]}{ccap_length})),
	    $tms{$tmlist[$i]}{stop},
	    $tms{$tmlist[$i]}{length};

	if ($alaninecap) {
	    $printstring .= sprintf
		" :: TM %2d ALA :: +%2d :: %s%s :: +%2d :: Length %2d\n",
		$tmlist[$i],
		$tms{$tmlist[$i]}{ncap_length},
		$tms{$tmlist[$i]}{capseq},
		" " x ($max_tm_length - $tms{$tmlist[$i]}{caplength}),
		$tms{$tmlist[$i]}{ccap_length},
		$tms{$tmlist[$i]}{caplength};
	}

	if (($raw !~ /none/) || ($alaninecap)) {
	    $printstring .= "\n";
	}

    }
    if (!$alaninecap) { $printstring .= "\n"; }
    printDuo($printstring,0);
}

################################################################################
##### Print Setup Information                                              #####
################################################################################
sub printSetupInfo {
    my $printstring .=
	"OptHelix Setup ::\n".
	" :: Place Proline & Glycine\n".
	"    :: Scream Library             :: 1.0 A\n".
	" :: Minimizing Backbone\n".
	"    :: RMS Force Threshold        :: $backboneminrms\n".
	"    :: Maximum Steps              :: $backboneminsteps\n".
	" :: Residues for Dynamics\n".
	"    :: Scream Library             :: 1.0 A\n";

    if ($warmup) {
	$printstring .= sprintf
	    " :: Warmup Information\n".
	    "    :: Start Temperature          :: $warmupstart K\n".
	    "    :: Temperature Increment      :: $warmupinterval K\n".
	    "    :: Warmup Timestep            :: $warmuptimestep fs\n".
	    "    :: Warmup Steps               :: $warmupsteps\n".
	    "    :: Warmup Length (per temp)   :: %g ps (per temp. increment)\n",
	    ($warmuptimestep * $warmupsteps) / 1000;
    }

    $printstring .= sprintf
	" :: Dynamics Information\n".
	"    :: Dynamics Temperature       :: $dyntemp K\n".
	"    :: Dynamics Timestep          :: $dyntimestep fs\n".
	"    :: Dynamics Steps             :: $dynsteps\n".
	"    :: Dynamics Length            :: %g ns (%g ps)\n".
	"    :: Dynamics Snaps Interval    :: $dynsnapint (%g ps)\n".
	"    :: Total Number of Snapshots  :: $numsnaps\n".
	"    :: %% of Snaps Ignored         :: $ignorepct %%\n".
	"    :: Snapshots Used in Analysis :: $numsnapstokeep\n".
	"    :: First Snapshot in Analysis :: snap$firstsnaptokeep\n",
	($dyntimestep * $dynsteps / 1000000), ($dyntimestep * $dynsteps / 1000),
	($dynsnapint * $dyntimestep / 1000);

    if ($finalminimize) {
	$printstring .=
	" :: Final Minimization\n".
	"    :: RMS Force Threshold        :: $finalminrms\n".
	"    :: Maximum Steps              :: $finalminsteps\n";
    }

    # Figure out if we need to run a particular set of TMs
    if ($tms_to_run) {
	if ($tms_to_run =~ /^(\d+)-(\d+)$/) {
	    my $tmstart = $1;
	    my $tmstop  = $2;
	    my $start_in_list = 0;
	    my $stop_in_list  = 0;
	    for (my $i = 0; $i < @tmlist; $i++) {
		if ($tmlist[$i] == $tmstart) { $start_in_list = 1; }
		if ($tmlist[$i] == $tmstop)  { $stop_in_list  = 1; }
	    }

	    if ($tmstart > $tmstop) {
		die "OptHelix :: Requested TM Range ($tms_to_run) not valid.\n\n";
	    }

	    if (!$start_in_list || !$stop_in_list) {
		die "OptHelix :: Requested TM Range ($tms_to_run) not valid.\n\n";
	    }

	    undef @tmlist;
	    $printstring .= " :: TMs to Use ::";
	    for (my $i = $tmstart; $i <= $tmstop - 1; $i++) {
		push @tmlist, $i;
		$printstring .= " $i,";
	    }
	    push @tmlist, $tmstop;
	    $printstring .= " $tmstop\n";

	} elsif (($tms_to_run =~ /\,/) && (!$tms_to_run =~ /-/)) {
	    $tms_to_run =~ s/\s//g;
	    my @newtms = split(/\,/,$tms_to_run);
	    for (my $i = 0; $i < @newtms; $i++) {
		my $tm_in_list = 0;
		for (my $j = 0; $j < @tmlist; $j++) {
		    if ($tmlist[$j] == $newtms[$i]) { $tm_in_list = 1; }
		}
		if (!$tm_in_list) {
		    die "OptHelix :: Requested TM Set ($tms_to_run) not valid.\n\n";
		}
	    }
	    undef @tmlist;
	    @tmlist = sort {$a <=> $b} @newtms;
	    $printstring .= " :: TMs to Use ::";
	    for (my $i = 0; $i < @tmlist - 1; $i++) {
		$printstring .= " $tmlist[$i],";
	    } $printstring .= " $tmlist[$#tmlist]\n";

	} elsif ($tms_to_run =~ /^(\d+)$/) {
	    my $new_tm = $1;
	    my $tm_in_list = 0;
	    for (my $i = 0; $i < @tmlist; $i++) {
		if ($tmlist[$i] == $new_tm) { $tm_in_list = 1; }
	    }
	    if (!$tm_in_list) {
		die "OptHelix :: Requested TM ($tms_to_run) not valid.\n\n";
	    }
	    $printstring .= " :: TM to Use :: $new_tm\n";
	    undef @tmlist;
	    push @tmlist, $new_tm;

	} else {
	    die "OptHelix :: Requested TMs ($tms_to_run) not valid.\n\n";
	}
    }

    printDuo($printstring."\n",0);
}

################################################################################
##### SCREAM Proline and Glycine                                           #####
################################################################################
sub screamProAndGly {
    (my $tmnum)  = @_;
    my $tm       = $tms{$tmnum}{capseq};
    my $tmlength = $tms{$tmnum}{caplength};
    my $infile   = "${pfx}helix${tmnum}.0.polyalanine.bgf";
    my $outfile  = "${pfx}helix${tmnum}.1.pre_backbone_min.bgf";

    my $printstring =
	" :: Placing Proline and Glycine ::\n".
	"    ::";

    # Make Directory to Scream In
    mkdir "1_ScreamProAndGly";
    chdir "1_ScreamProAndGly";
    copy("${Bin}/$polyalanines_dir/ala${tmlength}.bgf", "$infile");

    # Find Residues to Scream
    my $mutatelist = "";
    for (my $i = 0; $i < $tmlength; $i++) {
	if (substr($tm, $i, 1) =~ /[GP]/) {
	    $mutatelist .= " " . substr($tm, $i, 1) . ($i+1) . "_A";
	    $printstring .= " " . substr($tm, $i, 1) . ($i + $tms{$tmnum}{start});
	}
    }
    printDuo($printstring,$quiet); $printstring = "";
    if ($mutatelist eq "") {
	$printstring .=
	    " No Prolines or Glycines found in this TM";
	copy("$infile","$outfile");
	
    } else {
	my $screamctr = 0;
	while (($screamctr < 3) && (! -e "best_1.bgf")) {
	    # Run Scream
	    `${Bin}/$python_executable ${Bin}/$scream_dir/scripts/SCREAM_wrap.py $infile 10 FULL 0.0 $mutatelist >& /dev/null`;
	    copy("best_1.bgf", "$outfile");
	}

	# Make Sure that Scream Finished
	if (! -e "best_1.bgf") {
	    $printstring .=
		"    :: ERROR :: SCREAM Failed for TM $tmnum!  Cannot proceed with this TM.\n";
	    $skiptm{$tmnum} = 1;
	}
    }

    chdir "..";
    printDuo($printstring."\n", $quiet);
}

################################################################################
##### Minimize Backbone                                                    #####
################################################################################
sub minimizeBackbone {
    (my $tmnum) = @_;
    my $infile  = "${pfx}helix${tmnum}.1.pre_backbone_min.bgf";
    my $outfile = "${pfx}helix${tmnum}.2.post_backbone_min.bgf";
    (my $inprefix  = $infile)  =~ s/.bgf//;
    (my $outprefix = $outfile) =~ s/.bgf//;

    my $printstring =
	" :: Minimizing Backbone\n";
    printDuo($printstring,$quiet); $printstring = "";

    # Make Directory to Minimize In
    mkdir "2_MinimizeBackbone";
    chdir "2_MinimizeBackbone";
    copy("../1_ScreamProAndGly/$infile", "$infile");

    # Run Minimization
    my $ctl = 
	"PROJECT            $outprefix\n".
	"FF                 ${Bin}/$ff\n".
	"BBOX               -180 180        -180 180        -180 180\n".
	"STRUCTURE          $infile\n".
	"NB_METHOD          CMM\n".
	"CMM_EXPANSION      CENTROID\n".
	"LEVEL              0\n".
	"NB_UPDATE_FREQ     5\n".
	"CELL_REALLOC_FREQ  5\n".
	"LOAD_BAL_FREQ      10\n".
	"MIN_RMS_DESIRED    $backboneminrms\n".
	"MIN_MAX_STEPS      $backboneminsteps\n".
	"MIN_METHOD         CONJUGATE_WAG\n".
	"ACTION             MINIMIZE\n".
	"FINAL_BGF\n".
	"SETUP_EEX\n".
	"DO\n".
	"INFO\n".
	"EXIT\n";

    open CTL, ">${outprefix}.ctl";
    print CTL "$ctl";
    close CTL;

    `${Bin}/${mpsim_executable} ${outprefix}.ctl >& ${outprefix}.out`;

    if (-e "${outprefix}.fin.bgf") {
	move("${outprefix}.fin.bgf", "$outfile");
    } else {
	die "\nERROR !! MPSim Failed for Backbone Minimiziation of TM $tmnum\n\n";
    }

    chdir "..";
    printDuo($printstring, $quiet);
}

################################################################################
##### Scream Dynamics Residues                                             #####
################################################################################
sub screamDynamicsResidues {
    (my $tmnum)  = @_;
    my $tm       = $tms{$tmnum}{capseq};
    my $tmlength = $tms{$tmnum}{caplength};
    my $infile   = "${pfx}helix${tmnum}.2.post_backbone_min.bgf";
    my $outfile;
    if ($warmup) {
	$outfile = "${pfx}helix${tmnum}.3.pre_warmup.bgf";
    } else {
	$outfile = "${pfx}helix${tmnum}.4.pre_dynamics.bgf";
    }

    my $printstring =
	" :: Placing Dynamics Residues ::\n".
	"    ::";

    # Make Directory to Scream In
    mkdir "3_ScreamDynamicsResidues";
    chdir "3_ScreamDynamicsResidues";
    copy("../2_MinimizeBackbone/$infile", "$infile");

    # Find Residues to Scream
    my $mutatelist = "";
    for (my $i = 0; $i < $tmlength; $i++) {
	if (substr($tm, $i, 1) =~ /[$dynresidues]/) {
	    $mutatelist .= " " . substr($tm, $i, 1) . ($i+1) . "_A";
	    $printstring .= " " . substr($tm, $i, 1) . ($i + $tms{$tmnum}{start});
	}
    }
    printDuo($printstring,$quiet); $printstring = "";
    if ($mutatelist eq "") {
	$printstring .=
	    " No Residues Found in this TM to Scream\n";
	copy("$infile","$outfile");
	
    } else {
	my $screamctr = 0;
	while (($screamctr < 3) && (! -e "best_1.bgf")) {
	    # Run Scream
	    `${Bin}/$python_executable ${Bin}/$scream_dir/scripts/SCREAM_wrap.py $infile 10 FULL 0.0 $mutatelist >& /dev/null`;
	    copy("best_1.bgf","$outfile");
	}

	# Make Sure that Scream Finished
	if (! -e "best_1.bgf") {
	    $printstring .=
		"    :: ERROR :: SCREAM Failed for TM $tmnum!  Cannot proceed with this TM.\n";
	    $skiptm{$tmnum} = 1;
	}
    }

    chdir "..";
    printDuo($printstring."\n",$quiet);
}

################################################################################
##### Set Up & Run Dynamics                                                #####
################################################################################
sub runDynamics {
    (my $tmnum) = @_;
    my ($infile, $inprefix, $outfile, $outprefix);
    if ($warmup) {
	$infile = "${pfx}helix${tmnum}.3.pre_warmup.bgf";
    } else {
	$infile = "${pfx}helix${tmnum}.4.pre_dynamics.bgf";
    }

    my $printstring;

    # Make Directory to Scream In
    mkdir "4_Dynamics";
    chdir "4_Dynamics";
    copy("../3_ScreamDynamicsResidues/$infile", "$infile");

    my $shell;
    if ($warmup) {
	$printstring .= " :: Setting Up Warmup\n";
	for (my $temp = $warmupstart; $temp < $dyntemp; $temp += $warmupinterval) {
	    if ($temp != $warmupstart) {
		$infile   = "${pfx}helix${tmnum}.3." . ($temp - $warmupinterval) . "_K.fin.bgf";
		$inprefix = "${pfx}helix${tmnum}.3." . ($temp - $warmupinterval) . "_K";
	    } else {
		$infile = "${pfx}helix${tmnum}.3.pre_warmup.bgf";
		($inprefix  = $infile) =~ s/.fin.bgf//;
	    }
	    $outprefix = "${pfx}helix${tmnum}.3.${temp}_K";
	    my $ctl =
		"PROJECT            $outprefix\n".
		"FF                 ${Bin}/$ff\n".
		"BBOX               -900 900 -900 900 -900 900\n".
		"STRUCTURE          $infile\n".
		"NB_METHOD          CMM\n".
		"CMM_EXPANSION      CENTROID\n".
		"LEVEL              0\n".
		"NB_UPDATE_FREQ     5\n".
		"CELL_REALLOC_FREQ  5\n".
		"VEL_RESCALE_FREQ   0\n".
		"LOAD_BAL_FREQ      10\n".
		"RESET_GLOBAL_F     T\n".
		"VEL_START          NONMIN\n".
		"DYN_TEMP           $temp\n".
		"DYN_TIME_STEP      $warmuptimestep\n".
		"DYN_STEPS          $warmupsteps\n".
		"NOSE               tau 0.05\n".
		"FINAL_BGF\n".
		"ACTION             TVN\n".
		"SETUP_EEX\n".
		"DO\n".
		"INFO\n".
		"EXIT\n";

	    open CTL, ">${outprefix}.ctl";
	    print CTL "$ctl";
	    close CTL;

	    $shell .= 
		"${Bin}/${mpsim_executable} ${outprefix}.ctl > ${outprefix}.out\n";
	}
	$shell .=
	    "\ncp ${outprefix}.fin.bgf ${pfx}helix${tmnum}.4.pre_dynamics.bgf\n\n";
    }

    $printstring .= " :: Setting up Dynamics\n";
    my $ctl =
	"PROJECT            ${pfx}helix${tmnum}.5.dynamics\n".
	"FF                 ${Bin}/$ff\n".
	"BBOX               -900 900 -900 900 -900 900\n".
	"STRUCTURE          ${pfx}helix${tmnum}.4.pre_dynamics.bgf\n".
	"NB_METHOD          CMM\n".
	"CMM_EXPANSION      CENTROID\n".
	"LEVEL              0\n".
	"NB_UPDATE_FREQ     5\n".
	"CELL_REALLOC_FREQ  5\n".
	"VEL_RESCALE_FREQ   0\n".
	"LOAD_BAL_FREQ      10\n".
	"RESET_GLOBAL_F     T\n".
	"VEL_START          NONMIN\n".
	"DYN_TEMP           $dyntemp\n".
	"DYN_TIME_STEP      $dyntimestep\n".
	"DYN_STEPS          $dynsteps\n".
	"NOSE               tau 0.05\n".
	"FINAL_BGF\n".
	"ACTION             TVN\n".
	"SETUP_EEX\n".
	"DO\n".
	"INFO\n".
	"EXIT\n";
    
    open CTL, ">${pfx}helix${tmnum}.5.dynamics.ctl";
    print CTL "$ctl";
    close CTL;
    
    $shell .=
	"${Bin}/${mpsim_executable} -s$dynsnapint ${pfx}helix${tmnum}.5.dynamics.ctl  > ${pfx}helix${tmnum}.5.dynamics.out\n".
	"${Bin}/utilities/snapgz2bgf.pl -s '${pfx}helix${tmnum}.5.dynamics.snap*' -t ${pfx}helix${tmnum}.4.pre_dynamics.bgf --skip $firstsnaptokeep >& ${pfx}helix${tmnum}.5.dynamics.eng\n".
	"${Bin}/utilities/bgf_snap_rmsd -m -v -t ${pfx}helix${tmnum}.4.pre_dynamics.bgf ${pfx}helix${tmnum}.5.dynamics.snap${firstsnaptokeep} $dynsnapint $numsnapstokeep > ${pfx}helix${tmnum}.5.dynamics.rmsd\n".
	"${Bin}/utilities/bgf_match.pl -p ${pfx}helix${tmnum}.5.dynamics.snap -f $firstsnaptokeep -i $dynsnapint -n $numsnapstokeep\n".
	"\n".
	"mkdir ${pfx}helix${tmnum}.3.warmup\n".
	"mv ${pfx}helix${tmnum}.3.*.* ${pfx}helix${tmnum}.3.warmup\n".
	"gzip -r ${pfx}helix${tmnum}.3.warmup\n".
	"\n".
	"mkdir ${pfx}helix${tmnum}.5.dynamics.bgfs\n".
	"${Bin}/utilities/multi_bgf2pdb.pl ${pfx}helix${tmnum}.5.dynamics.snap*.bgf\n".
	"mv *.bgf ${pfx}helix${tmnum}.5.dynamics.bgfs\n".
	"\n".
	"mkdir ${pfx}helix${tmnum}.5.dynamics.pdbs\n".
	"mv *.pdb ${pfx}helix${tmnum}.5.dynamics.pdbs\n".
	"gzip -r ${pfx}helix${tmnum}.5.dynamics.pdbs\n".
	"\n".
	"mkdir ${pfx}helix${tmnum}.5.dynamics.snaps\n".
	"mv *.snap* ${pfx}helix${tmnum}.5.dynamics.snaps\n".
	"gzip -r ${pfx}helix${tmnum}.5.dynamics.snaps\n".
	"\n".
	"gzip ${pfx}helix${tmnum}.5.dynamics.ctl\n".
	"gzip ${pfx}helix${tmnum}.5.dynamics.traj1\n".
	"gzip ${pfx}helix${tmnum}.5.dynamics.rst\n".
	"gzip ${pfx}helix${tmnum}.5.dynamics.out\n".
	"touch _dyn_finished_\n";

    # Control Options
    # 1 - parallel
    #     if this is the case, then we need to qsub the shell script except for the
    #     last TM.
    if ($runparallel && ($tmnum != $tmlist[$#tmlist])) {
	if ($queuetype eq "sge") {
	    $printstring .= "    :: Submitting Dynamics Job to SGE Queue\n";
	    printDuo($printstring,$quiet);
	    open SGE, ">${pfx}helix${tmnum}.sge";
	    print SGE
		"#!/bin/csh\n".
		"#\$ -N ${pfx}helix${tmnum}\n".
		"#\$ -j y\n".
		"\n".
		"setenv MPSIM_DATA ${Bin}/${mpsim_data}\n".
		"$shell\n";
	    close SGE;
	    
	    my $cwd = cwd;
	    `ssh $host 'cd $cwd ; qsub -cwd ${pfx}helix${tmnum}.sge >& /dev/null'`;

	} else {
	    $printstring .= "    :: Submitting Dynamics Job to PBS Queue\n";
	    printDuo($printstring,$quiet);
	    open PBS, ">${pfx}helix${tmnum}.pbs";
	    print PBS
		"#PBS -l nodes=1,walltime=48:00:00\n".
		"#PBS -q workq\n".
		"#PBS -j oe\n".
		"#PBS -N ${pfx}helix${tmnum}\n".
		"#PBS -m e\n".
		"#!/bin/csh\n".
		"\n".
		"setenv MPSIM_DATA ${Bin}/${mpsim_data}\n".
		"cd \$PBS_O_WORKDIR\n".
		"\n".
		"$shell\n";
	    close PBS;

	    my $cwd = cwd;
	    `ssh $host 'cd $cwd ; qsub ${pfx}helix${tmnum}.pbs >& /dev/null'`;

	}

    # 2 - linear, qsub
    #     if this is the case, then the main job is already running on the queue
    #     and we can run the shell script directly
    # 3 - linear, nonqsub
    #     if this is the case, then the main job is already running on the frontend
    #     and we can run the shell script directly
    } else {
	$printstring .= "    :: Running Dynamics Job on Current Machine\n";
	printDuo($printstring,$quiet);
	open SHELL, ">${pfx}helix${tmnum}.sh";
	print SHELL
	    "\#!/bin/csh\n".
	    "setenv MPSIM_DATA ${Bin}/${mpsim_data}\n".
	    "$shell\n";
	close SHELL;
	chmod 0755, "${pfx}helix${tmnum}.sh";

	`${pfx}helix${tmnum}.sh >& /dev/null`;
    }

    chdir "..";
}

################################################################################
##### Find Lowest Energy and Closest RMSD Structures from Dynamics         #####
################################################################################
sub findBestStructures {
    (my $tmnum) = @_;
    my $printstring = " :: Analyzing Dynamics\n";
    printDuo($printstring,$quiet); $printstring = "";
    my $line;

    # Find the snapshot with the lowest energy
    chdir "4_Dynamics";
    open ENG, "${pfx}helix${tmnum}.5.dynamics.eng";
    my @ENGLINES = <ENG>;
    close ENG;  unlink "${pfx}helix${tmnum}.5.dynamics.eng";
    my $snap                      = $firstsnaptokeep;
    my $snapctr_eng               = 0;
    $dynamics{$tmnum}{minenergy}  = 999999999.999999999;
    $dynamics{$tmnum}{minengsnap} = 0;
    foreach $line (@ENGLINES) {
	$line =~ /potential energy\s+(\S+)\,/;
	$dynamics{$tmnum}{$snap}{energy} = $1;

	if ($dynamics{$tmnum}{$snap}{energy} < $dynamics{$tmnum}{minenergy}) {
	    $dynamics{$tmnum}{minenergy}  = $dynamics{$tmnum}{$snap}{energy};
	    $dynamics{$tmnum}{minengsnap} = $snap;
	}

	$snap        += $dynsnapint;
	$snapctr_eng += 1;
    }

    # Find the snapshot with RMSD closest to the average trajectory structure
    open RMSD, "${pfx}helix${tmnum}.5.dynamics.rmsd";
    my @RMSDLINES = <RMSD>; shift @RMSDLINES;
    close RMSD;  unlink "${pfx}helix${tmnum}.5.dynamics.rmsd";
    $snap                          = $firstsnaptokeep;
    my $snapctr_rmsd               = 0;
    $dynamics{$tmnum}{minrmsd}     = 999999999.999999999;
    $dynamics{$tmnum}{minrmsdsnap} = 0;
    foreach $line (@RMSDLINES) {
	$line =~ /\S+\s+(\S+)/;
	$dynamics{$tmnum}{$snap}{rmsd} = $1;

	if ($dynamics{$tmnum}{$snap}{rmsd} < $dynamics{$tmnum}{minrmsd}) {
	    $dynamics{$tmnum}{minrmsd}     = $dynamics{$tmnum}{$snap}{rmsd};
	    $dynamics{$tmnum}{minrmsdsnap} = $snap;
	}

	$snap         += $dynsnapint;
	$snapctr_rmsd += 1;
    }

    if (($snapctr_eng != $numsnapstokeep) || ($snapctr_rmsd != $numsnapstokeep)) {
	$printstring .=
	    " :: WARNING :: It seems that an error has ocurred.  The number\n".
	    "            :: of energy values ($snapctr_eng) and/or the number of rmsd\n".
	    "            :: values ($snapctr_rmsd) does not match the expected number of\n".
	    "            :: snapshots ($numsnapstokeep).\n";
    }

    $printstring .=
	" :: RMSD Closest to Average\n".
	"    :: RMSD to Average :: $dynamics{$tmnum}{minrmsd}\n".
	"    :: Energy          :: $dynamics{$tmnum}{$dynamics{$tmnum}{minrmsdsnap}}{energy}\n".
	"    :: Snapshot        :: ${pfx}helix${tmnum}.5.dynamics.snap$dynamics{$tmnum}{minrmsdsnap}\n".
	" :: Minimum Energy\n".
	"    :: RMSD to Average :: $dynamics{$tmnum}{$dynamics{$tmnum}{minengsnap}}{rmsd}\n".
	"    :: Energy          :: $dynamics{$tmnum}{minenergy}\n".
	"    :: Snapshot        :: ${pfx}helix${tmnum}.5.dynamics.snap$dynamics{$tmnum}{minengsnap}\n";

    copy("${pfx}helix${tmnum}.5.dynamics.bgfs/".
	 "${pfx}helix${tmnum}.5.dynamics.snap$dynamics{$tmnum}{minrmsdsnap}.bgf",
	 "${pfx}helix${tmnum}.6.minrmsd.bgf");
    copy("${pfx}helix${tmnum}.5.dynamics.bgfs/".
	 "${pfx}helix${tmnum}.5.dynamics.snap$dynamics{$tmnum}{minengsnap}.bgf",
	 "${pfx}helix${tmnum}.6.mineng.bgf");

    chdir "..";
    printDuo($printstring, $quiet);
}

################################################################################
##### Scream in the reamining sidechains                                   #####
################################################################################
sub screamRemaining {
    (my $tmnum) = @_;
    my $tm           = $tms{$tmnum}{capseq};
    my $tmlength     = $tms{$tmnum}{caplength};
    my $infile_rmsd  = "${pfx}helix${tmnum}.6.minrmsd.bgf";
    my $infile_eng   = "${pfx}helix${tmnum}.6.mineng.bgf";
    my $outfile_rmsd = "${pfx}helix${tmnum}.7.minrmsd.scream.bgf";
    my $outfile_eng  = "${pfx}helix${tmnum}.7.mineng.scream.bgf";

    my $printstring =
	" :: Placing Remaining Residues ::\n".
	"    ::";

    # Make Directory to Scream In
    mkdir "5_ScreamFinal";
    chdir "5_ScreamFinal";
    copy("../4_Dynamics/$infile_rmsd", "$infile_rmsd");
    copy("../4_Dynamics/$infile_eng", "$infile_eng");

    # Find Residues to Scream
    my $mutatelist = "";
    my $resctr = -1;
    for (my $i = 0; $i < $tmlength; $i++) {
	if (substr($tm, $i, 1) =~ /[CDEFHIKLMNPQRSTVWY]/) {
	    $resctr++;
	    if ($resctr == 10) {
		$printstring .= "\n    ::";
		$resctr = 0;
	    }
	    $mutatelist .= " " . substr($tm, $i, 1) . ($i+1) . "_A";
	    $printstring .= " " . substr($tm, $i, 1) . ($i + $tms{$tmnum}{start});
	}
    }
    printDuo($printstring,$quiet); $printstring = "";
    if ($mutatelist eq "") {
	$printstring .=
	    " No Residues Found in this TM to Scream\n";
	copy("$infile_rmsd","$outfile_rmsd");
	copy("$infile_eng","$outfile_eng");
	
    } else {
	# Run Scream for RMSD
	my $screamctr = 0;
	while (($screamctr < 3) && (! -e "best_1.bgf")) {
	    `${Bin}/$python_executable ${Bin}/$scream_dir/scripts/SCREAM_wrap.py $infile_rmsd 10 FULL 0.0 $mutatelist >& /dev/null`;
	    copy("best_1.bgf", "$outfile_rmsd");
	}

	# Make Sure that Scream Finished
	if (! -e "best_1.bgf") {
	    $printstring .=
		"    :: ERROR :: SCREAM Failed for TM $tmnum (RMSD)!  Cannot proceed with this TM.\n";
	    $skiptm{$tmnum} = 1;
	} unlink "best_1.bgf";

	# Run Scream for Energy
	$screamctr = 0;
	while (($screamctr < 3) && (! -e "best_1.bgf")) {
	    `${Bin}/$python_executable ${Bin}/$scream_dir/scripts/SCREAM_wrap.py $infile_eng 10 FULL 0.0 $mutatelist >& /dev/null`;
	    copy("best_1.bgf", "$outfile_eng");
	}

	# Make Sure that Scream Finished
	if (! -e "best_1.bgf") {
	    $printstring .=
		"    :: ERROR :: SCREAM Failed for TM $tmnum (Energy)!  Cannot proceed with this TM.\n";
	    $skiptm{$tmnum} = 1;
	} unlink "best_1.bgf";
    }

    chdir "..";
    printDuo($printstring."\n", $quiet);
}

################################################################################
##### (Optional) Final Minimization                                        #####
################################################################################
sub finalMinimization {
    (my $tmnum) = @_;
    my $infile_rmsd  = "${pfx}helix${tmnum}.7.minrmsd.scream.bgf";
    my $infile_eng   = "${pfx}helix${tmnum}.7.mineng.scream.bgf";
    my $outfile_rmsd = "${pfx}helix${tmnum}.8.minrmsd.scream.min.bgf";
    my $outfile_eng  = "${pfx}helix${tmnum}.8.mineng.scream.min.bgf";
    (my $inprefix_rmsd  = $infile_rmsd)  =~ s/.bgf//;
    (my $inprefix_eng   = $infile_eng)   =~ s/.bgf//;
    (my $outprefix_rmsd = $outfile_rmsd) =~ s/.bgf//;
    (my $outprefix_eng  = $outfile_eng)  =~ s/.bgf//;

    my $printstring = " :: Final Minimization\n";
    printDuo($printstring,$quiet); $printstring = "";
    # Make Directory to Minimize In
    mkdir "6_FinalMinimize";
    chdir "6_FinalMinimize";
    copy("../5_ScreamFinal/$infile_rmsd", "$infile_rmsd");
    copy("../5_ScreamFinal/$infile_eng",  "$infile_eng");

    # Run Minimization for RMSD
    my $ctl = 
	"PROJECT            $outprefix_rmsd\n".
	"FF                 ${Bin}/$ff\n".
	"BBOX               -180 180        -180 180        -180 180\n".
	"STRUCTURE          $infile_rmsd\n".
	"NB_METHOD          CMM\n".
	"CMM_EXPANSION      CENTROID\n".
	"LEVEL              0\n".
	"NB_UPDATE_FREQ     5\n".
	"CELL_REALLOC_FREQ  5\n".
	"LOAD_BAL_FREQ      10\n".
	"MIN_RMS_DESIRED    $finalminrms\n".
	"MIN_MAX_STEPS      $finalminsteps\n".
	"MIN_METHOD         CONJUGATE_WAG\n".
	"ACTION             MINIMIZE\n".
	"FINAL_BGF\n".
	"SETUP_EEX\n".
	"DO\n".
	"INFO\n".
	"EXIT\n";

    open CTL, ">${outprefix_rmsd}.ctl";
    print CTL "$ctl";
    close CTL;

    `${Bin}/${mpsim_executable} ${outprefix_rmsd}.ctl >& ${outprefix_rmsd}.out`;

    if (-e "${outprefix_rmsd}.fin.bgf") {
	move("${outprefix_rmsd}.fin.bgf", "$outfile_rmsd");
    } else {
	die "\nERROR !! MPSim Failed for Final Minimiziation of TM $tmnum\n\n";
    }

    # Run Minimization for Energy
    $ctl = 
	"PROJECT            $outprefix_eng\n".
	"FF                 ${Bin}/$ff\n".
	"BBOX               -180 180        -180 180        -180 180\n".
	"STRUCTURE          $infile_eng\n".
	"NB_METHOD          CMM\n".
	"CMM_EXPANSION      CENTROID\n".
	"LEVEL              0\n".
	"NB_UPDATE_FREQ     5\n".
	"CELL_REALLOC_FREQ  5\n".
	"LOAD_BAL_FREQ      10\n".
	"MIN_RMS_DESIRED    $finalminrms\n".
	"MIN_MAX_STEPS      $finalminsteps\n".
	"MIN_METHOD         CONJUGATE_WAG\n".
	"ACTION             MINIMIZE\n".
	"FINAL_BGF\n".
	"SETUP_EEX\n".
	"DO\n".
	"INFO\n".
	"EXIT\n";

    open CTL, ">${outprefix_eng}.ctl";
    print CTL "$ctl";
    close CTL;

    `${Bin}/${mpsim_executable} ${outprefix_eng}.ctl >& ${outprefix_eng}.out`;

    if (-e "${outprefix_eng}.fin.bgf") {
	move("${outprefix_eng}.fin.bgf", "$outfile_eng");
    } else {
	die "\nERROR !! MPSim Failed for Final Minimiziation of TM $tmnum\n\n";
    }

    chdir "..";

    printDuo($printstring, $quiet);
}

################################################################################
##### Finalize TMs                                                         #####
################################################################################
sub finalizeTMs {
    (my $tmnum) = @_;
    my $infile_rmsd      = "${pfx}helix${tmnum}/5_ScreamFinal/${pfx}helix${tmnum}.7.minrmsd.scream.bgf";
    my $infile_eng       = "${pfx}helix${tmnum}/5_ScreamFinal/${pfx}helix${tmnum}.7.mineng.scream.bgf";
    my $outfile_rmsd     = "${pfx}helix${tmnum}.fin.minrmsd.cap.bgf";
    my $outfile_eng      = "${pfx}helix${tmnum}.fin.mineng.cap.bgf";
    my $outfile_rmsd_raw = "${pfx}helix${tmnum}.fin.minrmsd.raw.bgf";
    my $outfile_eng_raw  = "${pfx}helix${tmnum}.fin.mineng.raw.bgf";

    my $infile_rmsd_min      = "${pfx}helix${tmnum}/6_FinalMinimize/${pfx}helix${tmnum}.8.minrmsd.scream.min.bgf";
    my $infile_eng_min       = "${pfx}helix${tmnum}/6_FinalMinimize/${pfx}helix${tmnum}.8.mineng.scream.min.bgf";
    my $outfile_rmsd_min     = "${pfx}helix${tmnum}.fin.minrmsd.cap.min.bgf";
    my $outfile_eng_min      = "${pfx}helix${tmnum}.fin.mineng.cap.min.bgf";
    my $outfile_rmsd_min_raw = "${pfx}helix${tmnum}.fin.minrmsd.raw.min.bgf";
    my $outfile_eng_min_raw  = "${pfx}helix${tmnum}.fin.mineng.raw.min.bgf";

    my $printstring = " :: Removing Caps and Renumbering\n";
    my $aa_start = $tms{$tmnum}{ncap_length} + 1;
    my $aa_stop  = $tms{$tmnum}{ncap_length} + $tms{$tmnum}{length};
    my $aastring = "-r ${aa_start}...${aa_stop}A";

    `${Bin}/utilities/playWithBGF/playWithBGF $infile_rmsd $aastring +H -o $outfile_rmsd`;
    `${Bin}/utilities/playWithBGF/playWithBGF $outfile_rmsd -n -N -o $outfile_rmsd`;
    reNumReChain($tmnum, "$outfile_rmsd", "cap");
    `${Bin}/${scream_dir}/scripts/fix_atom_ordering $outfile_rmsd $outfile_rmsd`;

    `${Bin}/utilities/playWithBGF/playWithBGF $infile_eng $aastring +H -o $outfile_eng`;
    `${Bin}/utilities/playWithBGF/playWithBGF $outfile_eng -n -N -o $outfile_eng`;
    reNumReChain($tmnum, "$outfile_eng", "cap");
    `${Bin}/${scream_dir}/scripts/fix_atom_ordering $outfile_eng $outfile_eng`;

    if ($raw !~ /none/) {
	`${Bin}/utilities/playWithBGF/playWithBGF $outfile_rmsd -r $tms{$tmnum}{rawstart}...$tms{$tmnum}{rawstop}_${tmnum} +H -o $outfile_rmsd_raw`;
	`${Bin}/utilities/playWithBGF/playWithBGF $outfile_rmsd_raw -n -N -o $outfile_rmsd_raw`;
	reNumReChain($tmnum, "$outfile_rmsd_raw", "raw");
	`${Bin}/${scream_dir}/scripts/fix_atom_ordering $outfile_rmsd_raw $outfile_rmsd_raw`;

	`${Bin}/utilities/playWithBGF/playWithBGF $outfile_eng -r $tms{$tmnum}{rawstart}...$tms{$tmnum}{rawstop}_${tmnum} +H -o $outfile_eng_raw`;
	`${Bin}/utilities/playWithBGF/playWithBGF $outfile_eng_raw -n -N -o $outfile_eng_raw`;
	reNumReChain($tmnum, "$outfile_eng_raw", "raw");
	`${Bin}/${scream_dir}/scripts/fix_atom_ordering $outfile_eng_raw $outfile_eng_raw`;
    }

    if ($finalminimize) {
	`${Bin}/utilities/playWithBGF/playWithBGF $infile_rmsd_min $aastring +H -o $outfile_rmsd_min`;
	`${Bin}/utilities/playWithBGF/playWithBGF $outfile_rmsd_min -n -N -o $outfile_rmsd_min`;
	reNumReChain($tmnum, "$outfile_rmsd_min", "cap");
	`${Bin}/${scream_dir}/scripts/fix_atom_ordering $outfile_rmsd_min $outfile_rmsd_min`;

	`${Bin}/utilities/playWithBGF/playWithBGF $infile_eng_min  $aastring +H -o $outfile_eng_min`;
	`${Bin}/utilities/playWithBGF/playWithBGF $outfile_eng_min -n -N -o $outfile_eng_min`;
	reNumReChain($tmnum, "$outfile_eng_min", "cap");
	`${Bin}/${scream_dir}/scripts/fix_atom_ordering $outfile_eng_min $outfile_eng_min`;

	if ($raw !~ /none/) {
	    `${Bin}/utilities/playWithBGF/playWithBGF $outfile_rmsd_min -r $tms{$tmnum}{rawstart}...$tms{$tmnum}{rawstop}_${tmnum} +H -o $outfile_rmsd_min_raw`;
	    `${Bin}/utilities/playWithBGF/playWithBGF $outfile_rmsd_min_raw -n -N -o $outfile_rmsd_min_raw`;
	    reNumReChain($tmnum, "$outfile_rmsd_min_raw", "raw");
	    `${Bin}/${scream_dir}/scripts/fix_atom_ordering $outfile_rmsd_min_raw $outfile_rmsd_min_raw`;

	    `${Bin}/utilities/playWithBGF/playWithBGF $outfile_eng_min -r $tms{$tmnum}{rawstart}...$tms{$tmnum}{rawstop}_${tmnum} +H -o $outfile_eng_min_raw`;
	    `${Bin}/utilities/playWithBGF/playWithBGF $outfile_eng_min_raw -n -N -o $outfile_eng_min_raw`;
	    reNumReChain($tmnum, "$outfile_eng_min_raw", "raw");
	    `${Bin}/${scream_dir}/scripts/fix_atom_ordering $outfile_eng_min_raw $outfile_eng_min_raw`;
	}
    }

    printDuo($printstring, $quiet);
}

################################################################################
##### Renumber and Rechain TMs                                             #####
################################################################################
sub reNumReChain {
    (my $tmnum, my $file, my $style) = @_;
    my $mftatmp = $mfta;
    
    my $header =
	"BIOGRF  332\n".
	"DESCRP $file\n".
	"REMARK MFTA ".File::Spec->rel2abs("mfta")."\n".
	"REMARK TM$tmnum $tms{$tmnum}{start} $tms{$tmnum}{stop}\n".
	"FORCEFIELD DREIDING\n".
	"FORMAT ATOM   (a6,1x,i5,1x,a5,1x,a3,1x,a1,1x,a5,3f10.5,1x,a5,i3,i2,1x,f8.5,i2,i4,f10.5)\n";

    open IN, "$file";
    my @LINES = <IN>;
    close IN;

    open OUT, ">$file";
    my $write = 0;
    my $bgf_curr_res = 1;
    my $curr_res;
    my $abs_curr_res;
    if ($style eq "cap") {
	$abs_curr_res = $tms{$tmnum}{start};
    } elsif ($style eq "raw") {
	$abs_curr_res = $tms{$tmnum}{rawstart};
    }
    print OUT "$header";
    my $line;
    foreach $line (@LINES) {
	if ($line =~ /^ATOM/) {
	    $write = 0;

	    # Fix Residue Number & Chain
	    $line =~ /^ATOM\s+\S+\s+\S+\s+\S+\s+\S+\s+(\S+)/;
	    $curr_res = $1;
	    if ($curr_res != $bgf_curr_res) {
		$bgf_curr_res = $curr_res;
		$abs_curr_res++;
	    }
	    my $string = "$abs_curr_res";
	    while (length($string) < 5) { $string = " " . "$string"; }
	    if ($maxtmnum < 10) {
		$string = "$tmnum" . "$string";
	    } else {
		$string = "A" . "$string";
	    }
	    substr($line,23,6) = $string;

	    # Fix HN Charges
	    if      ((substr($line, 13, 2) eq "HN")  &&
		     (substr($line, 19, 3) ne "PRO") &&
		     ((substr($line, 10, 2) eq " 1") ||
		      (substr($line, 10, 2) eq " 2") ||
		      (substr($line, 10, 2) eq " 3"))) {
		substr($line,71,9) = "  0.15500";
	    } elsif ((substr($line, 13, 2) eq "HN")  &&
		     (substr($line, 19, 3) eq "PRO") &&
		     ((substr($line, 10, 2) eq " 1") ||
		      (substr($line, 10, 2) eq " 2"))) {
		substr($line,71,9) = "  0.00000";
	    }

	    # Print Fixed Line
	    print OUT "$line";
	    $write = 1;
	} elsif ($write) {
	    print OUT "$line";
	}
    }
    close OUT;
}

################################################################################
##### Make some VMD script files                                           #####
################################################################################
sub vmd {
    mkdir "vmd";
    chdir "vmd";

    for (my $i = 0; $i < @tmlist; $i++) {
 	open VMD, ">${pfx}helix$tmlist[$i].dynamics.vmd";
 	print VMD
	    "cd ../${pfx}helix$tmlist[$i]/4_Dynamics\n".
	    "cd ${pfx}helix$tmlist[$i].5.dynamics.bgfs\n".
	    "mol new ${pfx}helix$tmlist[$i].4.pre_dynamics.bgf\n".
	    "for { set i $firstsnaptokeep } { \$i < $dynsteps } {incr i $dynsnapint } {\n".
	    "mol addfile ${pfx}helix$tmlist[$i].5.dynamics.snap\${i}.bgf\n".
	    "}\n".
	    "cd ../../../vmd\n";
	close VMD;

 	open VMD, ">${pfx}helix$tmlist[$i].final.vmd";
	print VMD
	    "cd ..\n".
	    "mol new ${pfx}helix$tmlist[$i].fin.minrmsd.cap.bgf\n";
	if ($finalminimize) {
	    print VMD
		"mol new ${pfx}helix$tmlist[$i].fin.minrmsd.cap.min.bgf\n";
	}
	print VMD
	    "mol new ${pfx}helix$tmlist[$i].fin.mineng.cap.bgf\n";
	if ($finalminimize) {
	    print VMD
		"mol new ${pfx}helix$tmlist[$i].fin.mineng.cap.min.bgf\n";
	}
	print VMD "cd vmd\n";
 	close VMD;

	open VMD, ">>${pfx}all.dynamics.vmd";
	print VMD
	    "source ${pfx}helix$tmlist[$i].dynamics.vmd\n";
	close VMD;

	open VMD, ">>${pfx}all.final.vmd";
	print VMD
	    "source ${pfx}helix$tmlist[$i].final.vmd\n";
	close VMD;
    }

}

################################################################################
##### Print to screen and log file                                         #####
################################################################################
sub printDuo {
    (my $message, my $quiet) = @_;
    if (!$quiet) {
	print LOG "$message";
	print     "$message";
    }
}

################################################################################
##### Help Info                                                            #####
################################################################################
sub help {
    my $help = "
Program:
 :: OptHelix.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: OptHelix.pl -f {modified FASTA file}

Required Input:
 :: -f | --mfta        :: Filename
 :: This should be a modified FASTA file containing
 :: information about the TMs, particularly the start and
 :: stop residue numbers.  The modified FASTA file format
 :: will be discussed below.

Optional:
 :: --tms                                    :: String
 :: This option allows a specific set of the TMs to be used
 :: rather than all of the TMs specified in the MFTA file.
 :: The TMs can either be specified in a range:
 ::    Ex: --tms '3-5'
 :: Or in a list:
 ::    Ex: --tms '3,4,5'
 :: Or individually:
 ::    Ex: --tms 3

 :: --raw                                    :: Keyword
 :: This value specifies which set of raw/uncapped
 :: start/stop values from the MFTA file to use.  There
 :: are three accepted keywords:
 :: * pred, for predicted (these are the values from
 ::   PredicTM)
 :: * man, for manual (these are values that are manually
 ::   entered)
 :: * none, to not produce output based on the raw
 ::   TM start/stop values
 :: The raw output BGFs are simply the capped results
 :: with the appropriate residues removed.

 :: --cap                                    :: Keyword
 :: This value specifies which set of capped start/stop
 :: values from the MFTA file to use.  There are two
 :: accepted keywords:
 :: * pred, for predicted (these are the values from
 ::   PredicTM)
 :: * man, for manual (these are values that are manually
 ::   entered)

 :: -s | --dynsteps                          :: Integer
 :: This is the number of steps performed during the
 :: equilibration dynamics.

 :: -t | --dyntimestep                       :: Integer
 :: This is the timestep (in fs) for the equilibration.

 :: -i | --dynsnapint                        :: Integer
 :: This is the number of steps to be taken between
 :: snapshots during the equilibration.  Please note that
 :: the snapshot interval should divide into the number
 :: of steps (\"-s\") evenly.

 :: -d | --dyntemp                           :: Float
 :: This is the temperature (in K) for the equilibration.

 :: -r | --dynresidues                       :: String
 :: These are the sidechains that should be present during
 :: the equilibration dynamics.  Proline, glycine, and
 :: alanine will always be present, but if proline is
 :: included in this list, it will be re-SCREAMed before
 :: the dynamics.  By default, proline, serine, and
 :: glycine are present during the dynamics.  Use of this
 :: flag will completely override those defaults.  
 :: Ex: -r PST (This would provide the same as the defaults)
 :: Ex: -r P   (Only proline will be present)

 :: --ff                                     :: Filename
 :: This is the forcefield file to be used for all dynamics
 :: and minimizations.

 :: -a | --alaninecap | --noalaninecap       :: No Input
 :: This flag causes the TMs to be capped or padded with
 :: extra alanines.  The \"--noalaninecap\" option turns
 :: off the alanine capping.

 :: --staticcaps | --nostaticcaps            :: No Input
 :: The \"--staticcaps\" option causes all TMs to be capped
 :: at the same length, regardless of the position of
 :: prolines.  The \"--nostaticcaps\" option causes the
 :: TMs to be capped depending on the position of prolines.

 :: -c | --caplength                         :: Integer
 :: With the \"--staticcaps\" option, this number of alanines
 :: will be added to the TMs.  With the \"--nostaticcaps\"
 :: option, alanines will be added until all prolines are
 :: this distance from the end of the TMs.

 :: --backboneminrms                         :: Float
 :: This is the RMS force threshold for the backbone
 :: minimization.

 :: --backboneminsteps                       :: Integer
 :: This is the maximum number of steps for the backbone
 :: minimization.

 :: -w | --warmup | --nowarmup               :: No Input
 :: Use of this flag will cause a set of warmup dynamics
 :: to be performed before the equilibration dynamics.
 :: The \"--nowarmup\" option turns off the warmup.

 :: --warmupstart                            :: Float
 :: This is the temperature (in K) at which the warmup
 :: dynamics starts.

 :: --warmupinterval                         :: Float
 :: This is the temperature step size (in K) for the
 :: warmup dynamics.

 :: --warmupsteps                            :: Integer
 :: This is the number of steps at each temperature for the
 :: warmup dynamics.

 :: --warmuptimestep                         :: Integer
 :: This is the step size (in fs) for the warmup dynamics.

 :: --ignorepct                              :: Integer
 :: This percentage of the equilibration dynamics will be
 :: ignored when analyzing the results.

 :: -m | --finalminimize | --nofinalminimize :: No Input
 :: This flag turns on a final minimization of the results
 :: of the equilibration dynamics.  The \"--nofinalminimize\"
 :: option turns off the final minimization.

 :: --finalminrms                            :: Float
 :: This is the RMS force threshold for the final
 :: minimization.

 :: --finalminsteps                          :: Integer
 :: This is the maximum number of steps for the final
 :: minimization.

 :: -p | --runparallel | --norunparallel     :: No Input
 :: With the \"--runparallel\" option turned on, the
 :: warmup and equilibration for each TM will be performed
 :: in it's own individual queue job.  The \"--norunparallel\"
 :: option causes the jobs to be run in sequence.  Note that
 :: when the jobs are run in parallel, the *must* run on a
 :: queuing system.

 :: --qsub | --noqsub                        :: No Input
 :: This flag tells the program to run using a queue,
 :: meaning that it will not run in the foreground.
 :: The \"--noqsub\" flag turns off this option
 :: if it is turned on by default.  Please note that if
 :: the \"-p\" option is used (either manually or by
 :: default), then the job *must* be submitted to a queue.

 :: --queuetype                              :: sge or pbs
 :: This tells the program what type of queuing system
 :: to use when submitting the program to the queue
 :: (if indicated with the \"--qsub\" flag).  Two options
 :: are allowed: sge (for Sun Grid Engine) and pbs (for
 :: the Portable Batch System).

 :: --prefix                                 :: String
 :: The value given here will be added to the beginning of
 :: all output files.

 :: -q | --quiet                             :: No Input
 :: This flag will turn off some of the output to the screen.

 :: -h | --help                              :: No Input
 :: Prints this help message.

 :: --showdefaults                           :: No Input
 :: Prints out the current defaults based on the .opthelix
 :: file being used.

Description:
 :: This program optimizes the kinks of individual helices.
 ::
 :: The procedure is as follows:
 :: 1) Start with canonical polyalanine helices (optionally
 ::    padded with alanines).
 :: 2) Mutate appropriate residues to Pro and Gly with
 ::    SCREAM
 :: 3) Minimize each helix separately
 :: 4) Mutate appropriate residues to Ser and Thr with
 ::    SCREAM
 :: 5) Perform a warmup sequence and equilibration dynamics
 ::    for each helix separately
 :: 6) Find the snapshots that are closest in RMSD to the
 ::    average structure during dynamics and the snapshots
 ::    that are lowest in energy during dynamics, ignoring
 ::    the first 25% of the dynamics.
 :: 7) Mutate all remaining residues.
 :: 8) Optionally minimize the final structures.
 :: 9) Remove the optional alanine padding.
 :: 10) Provide VMD source files for easy viewing of the
 ::     equilibration dynamics or final structures.
 ::     They can be viewed using \"vmd -e {source file}\",
 ::     assuming that VMD is installed.

Modified FASTA Format:
 :: The Modified FASTA Format is designed to contain both
 :: information about the protein sequence and the TMs,
 :: while the original FASTA format only contains sequence
 :: information.  Two lines are added at the end of the file
 :: for each TM.  The first line contains TM start/stop and
 :: eta residue information.  The second line contains
 :: hydrophobic center information.
 ::
 :: The first line:
 ::  1) TM number followed by \"tm\" (no space)
 ::  2) Raw TM start residue
 ::  3) Raw TM stop residue
 ::  4) Capped TM start residue
 ::  5) Capped TM stop residue
 ::  6) Holder for manual/consensus raw TM start residue
 ::  7) Holder for manual/consensus raw TM stop residue
 ::  8) Holder for manual/consensus capped TM start residue
 ::  9) Holder for manual/consensus capped TM stop residue
 :: 10) Residue (letter) for helix eta angle calculation
 :: 11) Residue (number) for helix eta angle calculation
 :: 12) Flag (A for automatic, M for manual) for helix eta
 ::     angle calculation
 ::
 :: The second line:
 :: 1) TM number followed by \"hpc\" (no space)
 :: 2) PredicTM raw geometric hydrophobic center 
 :: 3) PredicTM capped geometric hydrophobic center
 :: 4) PredicTM peak hydrophobic center
 :: 5) PredicTM area/centroid hydrophobic center
 :: 6) Placeholder for future hydrophobic center
 :: 7) Manually selected hydrophobic center
 ::
 :: Here is an example:
>P1;P14416|DRD2_HUMAN D(2) dopamine receptor - Homo sapiens
MDPLNLSWYDDDLERQNWSRPFNGSDGKADRPHYNYYATLLTLLIAVIVFGNVLVCMAVS
REKALQTTTNYLIVSLAVADLLVATLVMPWVVYLEVVGEWKFSRIHCDIFVTLDVMMCTA
SILNLCAISIDRYTAVAMPMLYNTRYSSKRRVTVMISIVWVLSFTISCPLLFGLNNADQN
ECIIANPAFVVYSSIVSFYVPFIVTLLVYIKIYIVLRRRRKRVNTKRSSRAFRAHLRAPL
KGNCTHPEDMKLCTVIMKSNGSFPVNRRRVEAARRAQELEMEMLSSTSPPERTRYSPIPP
SHHQLTLPDPSHHGLHSTPDSPAKPEKNGHAKDHPKIAKIFEIQTMPNGKTRTSLKTMSR
RKLSQQKEKKATQMLAIVLGVFIICWLPFFITHILNIHCDCNIPPVLYSAFTWLGYVNSA
VNPIIYTTFNIEFRKAFLKILHC
* 1tm   36   57   33   61    X    X    X    X    N   52   A
* 2tm   70   94   70   95    X    X    X    X    D   80   A
* 3tm  113  126  108  131    X    X    X    X    D  114   A
* 4tm  155  171  151  173    X    X    X    X    W  160   A
* 5tm  191  212  187  217    X    X    X    X    P  201   A
* 6tm  376  398  370  398    X    X    X    X    P  388   A
* 7tm  406  428  406  432    X    X    X    X    P  423   A
* 1hpc    46.50    47.00    44.00    45.49   X.00   X.00
* 2hpc    82.00    82.50    88.00    86.33   X.00   X.00
* 3hpc   119.50   119.50   120.00   121.03   X.00   X.00
* 4hpc   163.00   162.00   163.00   162.42   X.00   X.00
* 5hpc   201.50   202.00   203.00   202.19   X.00   X.00
* 6hpc   387.00   384.00   387.00   386.79   X.00   X.00
* 7hpc   417.00   419.00   411.00   414.73   X.00   X.00

";
    die $help;
}

# v-- This line must be included --v 
1;
