#!/usr/bin/perl -w

$version = '060414';
# caglar tanrikulu # runMPSim.pl # Apr 28 2003 # ver: 060414
#   Writes out an MPSim control file based on the command 
#   line input and runs MPSim.
#
# options:
#   -f <.par-file> 
#      : set forcefield parameter file
#   -l <level>
#      : set CMM level
#   -s <number-of-steps>
#      : set number of minimization steps (or dynamics steps
#      : if dynamics is specified)
#   -t <desired-RMS-threshold>
#      : set RMS threshold at which minimization will stop
#   -T <temperature-in-K>
#      : set dynamics temperature
#   -v <interval>
#      : save structures during dynamics every <interval> 
#      : number of steps  [default: none]
#   -e : use FINAL_ENER flag in ctl file
#   -H : run calculation on H-atoms only (non-H fixed)
#   -P : print control file only (does not run MPSim)
#   -S : silent mode / output on a single line
#
# job-types:  #this list may not be complete#
#   minsgb  : minimize under SGB solvation [default]
#   minfsm  : minimize under FSM solvation
#   minvac  : minimize in vacuum (no solvation)
#   oneEsgb : run one-energy calculation with SGB solvation
#   oneEavgb: run one-energy calculation with AVGB solvation
#   oneEfsm : run one-energy calculation with FSM solvation
#   oneEvac : run one-energy calculation with in vacuum (no solvation)
#   anneal  : run a single annealing cycle with SGB solvation
#   Hanneal : run annealing on H-atoms with short cycles and SGB
#   tvnsgb  : run TVN dynamics with SGB solvation
#
# usage: 
#   runMPSim.pl [-efHlPsStv] <bgf-file> (job-type) (project-name) 
#
# versions:
#   030428 # initial version
#   030517 # add option '-t' for the minimization threshold
#            program echoes ctl-file and final energy
#   030724 # add option '-H' for running MPSim on H-atoms only
#            add job-types 'anneal' and 'Hanneal'
#            fix bug in setting RMSF thereshold with '-t'
#   031019 # add job-type 'oneEavgb' 
#            for each such job, the BGF version of input bgf file 
#            is checked and if this is not '400' the file is 
#            converted to version 400 by bgf2fsm by J.Wendel 
#   031021 # package the bgf2fsm conversion code into a subroutine
#   031023 # realized that bgf2fsm resets all movable recs in a 
#            bgf file.  fixed this by saving all the movable atoms into
#            a .lst file and set them movable using toggleMovableRecs
#            in the v400 file
#   031104 # add job-types:  minfsm, minvac, oneEvac, oneEfsm
#   031105 # fixed a bug in &convert_BGF_to_v400 that only shows up when
#              the initial BGF file does not have ordered atom numbers.
#            updated this script with the one from runMPScream.pl and 
#              added a scratch file to better understand what's going
#              on when stuff starts crashing... 
#   040325 # added the job-type:  tvnsgb
#            added option '-T' to set dynamics temperature, and option
#              '-v' to set the snap intervals in dynamics
#   050810 # added the job-type:  anlfsm  (for annealing in fsm)
#            added the job-type:  anlsgb  (same as 'anneal')
#   050812 # checks for core dumps and deletes dumped 
#            help information shown only with option '-h' and is now 
#              piped to 'less' in &printHelp()
#   060414 # checks for default files first in the users own directory
#              and then in my defaults directory, and can execute them 
#              both
#            default method defined by the 'default_job' file
#
#
#$debug = 1;
$startTime = time;
#
use Env;
$|=1;
#

# where am i
use FindBin ();
use lib "$FindBin::Bin";
$sbin = $FindBin::Bin;

# Set Defaults:
# ... executables:
$s2t      = "$sbin/secs2time.pl";
$pwb      = "$sbin/playWithBGF/playWithBGF";
$toggleMR = "$sbin/toggleMovableRecs";
$bgf2fsm  = "$sbin/bgf2fsm"; # by John Wendel
$mpsim    = "$sbin/../mpsim/mpsim";        # by MSC
#
# ... default parameters:
&getSysInfo();
$userInputDir = "$homedir/.caglar.defaults/runMPSim/";
$defaultInputDir = "$sbin/runMPSim.defaults/";

#
# ... read default .ctl files from the defaultInputDir:
@defInputDirList = `ls $defaultInputDir`;
chomp(@defInputDirList);
for $ctlfile (@defInputDirList) {
    if ($ctlfile eq 'default_job') {
	$defaultJob = `cat ${defaultInputDir}default_job`;
	$defaultJob =~ s/\s+//g;
	$defJobSelector = $defaultInputDir.$ctlfile;
    } elsif ($ctlfile =~ /^(.+)\.ctl$/) {
	$jobType = $1;
	$defInput{$jobType} = $defaultInputDir.$ctlfile;
    }
}
# ... read default .ctl files from the userInputDir:
if (-d $userInputDir) {
    @userInputDirList = `ls $userInputDir`;
    chomp(@userInputDirList);
    for $ctlfile (@userInputDirList) {
	if ($ctlfile eq 'default_job') {
	    $defaultJob = `cat ${userInputDir}default_job`;
	    $defaultJob =~ s/\s+//g;
	    $defJobSelector = $userInputDir.$ctlfile;
	} elsif ($ctlfile =~ /^(.+)\.ctl$/) {
	    $jobType = $1;
	    $defInput{$jobType} = $userInputDir.$ctlfile;
	}
    }
}

@jobTypes = sort { $a cmp $b } keys %defInput;
$defaultJob = 'minsgb' unless ($defaultJob);  # obsolete

# ... read jobType descriptions
for $jobType (@jobTypes) {
    $info = ` head -1 $defInput{$jobType} `;
    if ($info =~ /^\# (.*)\s+$/) { 
	$defInputInfo{$jobType} = $1;
    } else {
	$defInputInfo{$jobType} = $defInput{$jobType};
    }
}


#&cdj();  #TEST#

# get command line arguments:
if (! @ARGV) {
    die "
 caglar tanrikulu # runMPSim.pl # Apr 28 2003 # ver: $version
   Writes out an MPSim control file based on the command 
     line input and runs MPSim.

 usage: 
   $0 
     [-efHlPsStTv|-h for help] <bgf-file> (job-type) (project-name) 

";

} else {
    ($bgfFile, $job, $project) = &setOptions(@ARGV);
}

print "\n" unless ($silent);
print " caglar tanrikulu # runMPSim.pl # Apr 28 2003 # ver: $version";
print "\n" unless ($silent);

# check for bgf file
die "$0: ERROR: BGF file $bgfFile not found!\n" unless ( -e $bgfFile );

# if job not set, set to the default job
if (defined $job) {
    die "$0: ERROR: Job-type '$job' not found or not implemented.\nImplemented job types are:  (use -h for more info)\n@jobTypes\n" unless (grep {/\b$job\b/} @jobTypes);
} else {
    if (grep {/\b$defaultJob\b/} @jobTypes) {
	$job = $defaultJob;
    } else {
	die "$0: ERROR: The default job-type selected, '$defaultJob', cannot be found.  Check $defJobSelector and make sure a .ctl file for this job type is available.\n";
    }
}

#&cdj();  #TEST#

# set scratch file:
$scratchFile = 'runMPSim.scratch.'.time;

# read default input file from defaults-directory
print " ... reading default parameters from: $defInput{$job} ...\n" unless ($silent);
@inFile = &readInFile($defInput{$job});


# set project name if not specified:
unless (defined $project) {
    $prefix = $bgfFile;
    $prefix =~ s/\.bgf//g;
    $project = $prefix."_".$job;
}


# set H-movable for H-annealing / minimizations
if ($H_only) {

    warn "$0: WARNING: You are running annealing on H-atoms only.  You may want to use job-type \"Hanneal\" instead of \"anneal\"\n" if ($job eq 'anneal');

    print " ... setting H-atoms movable:\n" unless ($silent);

    # set new BGF-file name:
    $wBgfFile = $bgfFile . '.Hmov';
    @wBgfFile = split /\//, $wBgfFile;
    $wBgfFile = $wBgfFile[-1];

    # set H_ atoms movable 
    print "     writing new BGF file:  $wBgfFile ..." unless ($silent);
    system "$pwb $bgfFile -F H_ -V on -Lo $wBgfFile >> $scratchFile";   
    print " done\n" unless ($silent);
    $bgfFile = $wBgfFile;
}


# generate a v400 bgf input file if needed for oneEavgb/oneEfsm/minfsm
if ($job =~ /avgb/ || $job =~ /fsm/) {
    $bgfVersion = `grep 'BIOGRF ' $bgfFile`;
    $bgfVersion =~ s/^BIOGRF\s+//;

    if ($bgfVersion !~ /^400/) {
	print " ... BGF file is not in v400 format ... converting file:\n" unless ($silent);
	$bgfFile = &convert_BGF_to_v400($bgfFile,$silent,1,$scratchFile);
    }
}


# set dynamics parameters for tvnsgb, etc...
if ($job =~ /tvn/) {
    if (defined $minSteps) {
	$dynSteps = $minSteps;
	undef $minSteps;
    }
}


# modify and print the MPSim input (i.e. ctl) file:
$controlFile = "$project.ctl";
print " ... writing MPSim control file: $controlFile:\n\n" unless ($silent);
&printCtlFile($controlFile);


# run MPSim
unless ($printOnly) {
    # set MPSim command line options:
    $mpsimOptions = '';
    $mpsimOptions .= "-s $snapInterval " if (defined $snapInterval);

    # run MPSim:
    print " ... running MPSim" unless ($silent);
    $outputFile = "$project.out";
    system "$mpsim $mpsimOptions $controlFile >& $outputFile";

    # get energy from output:
    $finEnergy = &getEnergyFromOutput($outputFile);
    if ($finEnergy eq 'ERROR') {
	warn "$0: WARNING: Cannot get energy from output. MPSim run failed...\n";
	print " !!! ERROR in MPSim: Check MPSim output:  $outputFile\n" unless ($silent);
    } else {
	print " ... final energy: ",$finEnergy," kcal/mol\n" unless ($silent);
    }
}


# check for dumped core files and delete them
@coredumps = glob("core*");
if (@coredumps) {
    warn "$0: WARNING: Encountered a core dump!  Deleted core files...\n";
    system "ls -l core* > deleted.core";
    system "rm -f core* ";
}


# remove scratch file if everything went well...
system "rm -f $scratchFile" if (defined $finEnergy && $finEnergy ne 'ERROR');

# done!
$eTimeInSecs = time - $startTime;
$eTime   = `perl $s2t $eTimeInSecs`;
chomp($eTime);
print " ... done in $eTime.\n";
print "\n" unless ($silent);
exit;



###################
### SUBROUTINES ###
###################

sub setOptions {
    my @args = @_;
    my ($opts, $entry, @wArgs);
    my $i = 0;

    while (defined $args[$i]) {

	if ($args[$i] =~ /^-/) {
	    @opts = split("",$args[$i]);
            shift(@opts); 
	    
	    foreach $entry (@opts) { 

		if ($entry eq 'h') {              # -h
		    $i++;
		    &printHelp();

		} elsif ($entry eq 'f') {         # -f
		    $forcefield = $args[$i+1];
		    $i++;

		} elsif ($entry eq 'l') {         # -l
		    $level = $args[$i+1];
		    $i++;

		} elsif ($entry eq 's') {         # -s
		    $minSteps = $args[$i+1];
		    $i++;

		} elsif ($entry eq 't') {         # -t
		    $minThreshold = $args[$i+1];
		    $i++;
		    
		} elsif ($entry eq 'T') {         # -T
		    $dynTemp = $args[$i+1];
		    $i++;

		} elsif ($entry eq 'v') {         # -v
		    $snapInterval = $args[$i+1];
		    $i++;

		} elsif ($entry eq 'e') {         # -e
		    $finEner = 1;
		    
		} elsif ($entry eq 'H') {         # -H
		    $H_only = 1;
		    
		} elsif ($entry eq 'P') {         # -P
		    $printOnly = 1;
		    
		} elsif ($entry eq 'S') {         # -S
		    $silent = 1;
		    
		} else {
		    die "$0: ERROR: Unsupported option: '-$entry'\n";
		}
	    }

	} else {
	    push(@wArgs, $args[$i]);
	}
	$i++;
    }

    # return
    return @wArgs;
}


sub getSysInfo {
    #$execCom = "$0 @ARGV";
    #$curdir  = $ENV{PWD};
    #$curuser = $ENV{USER};
    $homedir = $ENV{HOME};
    
    $curhost = $ENV{HOST};
    $curhost =~ s/\.wag\.caltech\.edu//;
       
    $curdate = `date`;
    chomp($curdate);
}


sub readInFile {
    my ($inFile) = @_;
    my ($line, @line);

    open(FILE,"$inFile") || die "$0: ERROR: Can't open $inFile: $!\n";
    my @inFile = <FILE>;
    close(FILE);    

    # read default values:
    foreach $line (@inFile) {
	if ($line =~ /^LEVEL / && !defined $level) {
	    @line = split (/\s+/, $line);
	    $level = $line[1];
	} elsif ($line =~ /^FF / && !defined $forcefield) {
	    @line = split (/\s+/, $line);
	    $forcefield = $line[1];
	}
    }

    # return
    return @inFile;
}


sub convert_BGF_to_v400 {
    # subroutine to convert BGF file to v400 using John Wendel's bgf2fsm
    my ($bgfFile,$silent, $workUp, $scratch) = @_;
    my ($tempfile, $lstfile, $wBgfFile);
    my $starttime = time;

    # set defaults:                        
    $workUp = 1 unless (defined $workUp);  # if $workUp is ommitted, transfer movable records
    $scratch = '/dev/null' unless (defined $scratch);  # discard output if no scratch file

    # renumber atoms in the input bgf 
    print "     renumbering atoms in $bgfFile ...\n" unless ($silent);
    $tempfile = time.'temp.bgf';
    system "$pwb $bgfFile -no $tempfile >> $scratch";
    
    # save movable atoms in a .lst file
    if ($workUp) {
	print "     saving movable atoms ...\n" unless ($silent);
	$lstfile = time.'temp.lst';
	system "$pwb $tempfile -ml $lstfile >> $scratch";
    }

    # set new BGF-file name:
    $wBgfFile = $bgfFile . '.v400';
    @wBgfFile = split /\//, $wBgfFile;
    $wBgfFile = $wBgfFile[-1];

    # get FSM typing using bgf2fsm (by John Wendel)
    print "     entering the FSM types for each atom in new file: $wBgfFile ..." unless ($silent);
    system "$bgf2fsm $tempfile $forcefield $wBgfFile >> $scratch";
    
    die "$0: ERROR: $wBgfFile not written!\n" unless (-e $wBgfFile);

    if ($workUp) {
	# reset atoms movable/fixed using the .lst file 
	print "\n     resetting atoms movable/fixed in $wBgfFile ..." unless ($silent);
	system "$toggleMR $lstfile $wBgfFile $wBgfFile >> $scratch";
#	system "$pwb $wBgfFile -A $lstfile -V on -Lo $wBgfFile >> $scratch";  # toggleMR is dumber but faster...

	# remove temporary .lst file:
	system "rm -f $lstfile";
    }

    # finish!
    my $etimeinsecs = time - $starttime;
    my $etime = `perl $s2t $etimeinsecs`;
    print " done in $etime\n" unless ($silent);

    # remove temporary file:
    system "rm -f $tempfile";

    # return new BGF file name:
    return $wBgfFile;    
}



sub printCtlFile {
    my ($ctlFile) = @_;
    my ($line);

    open(CTL,">$ctlFile") || die "$0: ERROR: Can't open $ctlFile: $!\n";

    foreach $line (@inFile) {

	if      ($line =~ /^PROJECT /) {
	    $line = "PROJECT            $project\n";

	} elsif ($line =~ /^FF/ && defined $forcefield) {
	    $line = "FF                 $forcefield\n";

	} elsif ($line =~ /^STRUCTURE /) {
	    $line = "STRUCTURE          $bgfFile\n";

	} elsif ($line =~ /^LEVEL / && defined $level) {
	    $line = "LEVEL              $level\n";

	} elsif ($line =~ /^MIN_RMS_DESIRED / && defined $minThreshold) {
	    $line = "MIN_RMS_DESIRED    $minThreshold\n";

	} elsif ($line =~ /^MIN_MAX_STEPS / && defined $minSteps) {
	    $line = "MIN_MAX_STEPS      $minSteps\n";

	} elsif ($line =~ /^DYN_STEPS / && defined $dynSteps) {
	    $line = "DYN_STEPS          $dynSteps\n";

	} elsif ($line =~ /^DYN_TEMP / && defined $dynTemp) {
	    $line = "DYN_TEMP           $dynTemp\n";

	} elsif ($line =~ /^\#FINAL_ENER/ && $finEner) {
	    $line = "FINAL_ENER\n";	    
	    # issue warning if level is not zero:
	    warn "$0: WARNING: Running with FINAL_ENER even though nonbond energy calculation is not exact (level = $level).\n" unless ($level == 0);

	} elsif ($line =~ /^\#/ || $line =~ /^\*/ || $line =~ /^\s+/) {
	    next;
	}

        print CTL $line;
	print $line unless ($silent);
    }

    close(CTL);

    print "\n" unless ($silent);
    # return
}


sub getEnergyFromOutput {
    my ($file) = @_;
    my $energy = ` grep 'TOTAL ENERGY = ' $file `;

    if ($energy =~ /TOTAL ENERGY = (.+) kcal/) {
	$energy = $1;
	$energy =~ s/\s+//g;	
    }

    # return
    if ($energy) {
	return "$energy";
    } elsif ($energy && $energy == 0) {
	return "$energy";
    } else {
	return 'ERROR';
    }
}


sub printHelp {
    my $helpText = "
 caglar tanrikulu # runMPSim.pl # Apr 28 2003 # ver: $version
   Writes out an MPSim control file based on the command 
     line input and runs MPSim.
   The <bgf-file> is the only required argument.  The <job-type> 
     defaults to '$defaultJob', and a default <project name> is
     provided in the absence of a user specified one. 

 contact:  
   caglar\@its.caltech.edu

 usage: 
   $0 
     [options|-h for help] <bgf-file> (job-type) (project-name) 

 options:
   -f <.par-file> 
      : set forcefield parameter file
   -l <level>
      : set CMM level
   -s <number-of-steps>
      : set number of minimization steps (or dynamics steps
      : if dynamics is specified)
   -t <desired-RMS-threshold>
      : set RMS threshold at which minimization will stop 
   -T <temperature-in-K>
      : set dynamics temperature
   -v <interval>
      : save structures during dynamics every <interval> 
      : number of steps  [default: none]
   -e : use FINAL_ENER flag in ctl file
   -H : run calculation on H-atoms only (non-H fixed)
   -P : print control file only (does not run MPSim)
   -S : silent mode / output on a single line
   -h : print this usage information

 default parameters:
   For default parameters see the corresponding .ctl file in 
     '$defaultInputDir'.  Default values are
     stored in a .ctl named after the corresponding job-type.  
     (e.g. 'minsgb.ctl' for 'minsgb')
";
    $helpText .= "   Your user defaults directory is '$userInputDir'\n" if (-d $userInputDir);

    $helpText .= "
 job-types:  
   [default job-type set to '$defaultJob']
";
    $helpText .= sprintf "   %-8s : %s\n",$_,$defInputInfo{$_} for (@jobTypes);
    $helpText .= "\n";

    if ( open(LESS, "| less ") ) {
	#open(LESS, "| less ")  || die "$0: cannot fork: $!";
	print LESS $helpText;
	close(LESS) || die "$0: can't close less: $!";
	exit;
    } else {
	die $helpText;
    }
}



sub cdj {  #TEST#
    print "\ndef = $defaultJob\n";
    print "$_ : $defInputInfo{$_}\n" for (@jobTypes);
    print "\n";
}
