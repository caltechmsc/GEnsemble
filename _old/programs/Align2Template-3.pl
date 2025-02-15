#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
}

use warnings;
use Cwd;
use File::Copy;
use File::Basename;
use File::Path;
use File::Spec;
use Getopt::Long;
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;
use Modules::AlignHelix;

############################################################
### Input                                                ###
############################################################

if (@ARGV == 0) { help(); }

my $nter       = 'out';
my $zout       = 'plus';
my $tmatorigin = 3;
my $tmalongx   = 2;
my $hpcinmfta  = 0;
my $pair       = 1;

#abcdefghijklmnopqrstuvwxyz
#abcdefg ijklmnopqrstuvwxyz
GetOptions ('h|help'         => \$help,
	    'b|bgf=s'        => \$bgf,
	    'i|inp=s'        => \$inp,
	    'm|mfta=s'       => \$mfta,
	    'x|hpcinmfta'    => \$hpcinmfta,
	    'e|eta=s'        => \$changeeta,
	    't|theta=s'      => \$changetheta,
	    'p|phi=s'        => \$changephi,
	    'y|modhpc_rel=s' => \$changehpc_rel,
	    'z|modhpc_abs=s' => \$changehpc_abs,
	    'pair=i'         => \$pair
	    );

if ($help) { help(); }
if (! $bgf) {
    die "Align2Template-3 :: Must provide BGF file to align.\n";
} elsif (! -e $bgf) {
    die "Align2Template-3 :: Provided BGF file could not be found :: $bgf\n";
}

if (! $mfta) {
    die "Align2Template-3 :: Must provide MFTA file corresponding to BGF.\n";
} elsif (! -e $mfta) {
    die "Align2Template-3 :: Provided MFTA file could not be found :: $mfta\n";
}

############################################################
### Main Routine                                         ###
############################################################

# Parse Changes
my @eta_changes = (0,0,0,0,0,0,0);
if ($changeeta) {
    undef @eta_changes;
    @eta_changes = split(/\s+/,$changeeta);
}
if (@eta_changes != 7) {
    die "Align2Template-3 :: Must specify 7 values for change in Eta.\n".
	"                 :: You provided :: $changeeta\n";
}

my @theta_changes = (0,0,0,0,0,0,0);
if ($changetheta) {
    undef @theta_changes;
    @theta_changes = split(/\s+/,$changetheta);
}
if (@theta_changes != 7) {
    die "Align2Template-3 :: Must specify 7 values for change in Theta.\n".
	"                 :: You provided :: $changetheta\n";
}

my @phi_changes = (0,0,0,0,0,0,0);
if ($changephi) {
    undef @phi_changes;
    @phi_changes = split(/\s+/,$changephi);
}
if (@phi_changes != 7) {
    die "Align2Template-3 :: Must specify 7 values for change in Phi.\n".
	"                 :: You provided :: $changephi\n";
}

my @hpcrel_changes = (0,0,0,0,0,0,0);
my @hpcabs_changes = (0,0,0,0,0,0,0);
if ($changehpc_rel && $changehpc_abs) {
    die "Align2Template-3 :: Cannot specify both relative and absolute changes to HPC!\n";
} elsif ($changehpc_rel) {
    undef @hpcrel_changes;
    @hpcrel_changes = split(/\s+/,$changehpc_rel);
} elsif ($changehpc_abs) {
    undef @hpcabs_changes;
    @hpcabs_changes = split(/\s+/,$changehpc_abs);
}
if (@hpcrel_changes != 7) {
    die "Align2Template-3 :: Must specify 7 values for change in HPC.\n".
	"                 :: You provided :: $changehpc_rel\n";
}
if (@hpcabs_changes != 7) {
    die "Align2Template-3 :: Must specify 7 values for change in HPC.\n".
	"                 :: You provided :: $changehpc_abs\n";
}

# Load MFTA
open MFTA, $mfta;
my %dat;
while (<MFTA>) {
    # Get Eta Residue Number
    if (/\*\s+(\d+)tm\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(\S+)\s+(\d+)/) {
	$dat{$1}{mftaetaresid}  = $2;
	$dat{$1}{mftaetaresnum} = $3;
    }
    # Get HPC from MFTA
    if (/\*\s+(\d+)hpc\s+(\S+)/) {
	$dat{$1}{mftahpc} = $2;
    }
}
close MFTA;

# Get INP Structure File
if (!$inp) {
    `${Bin}/GetTemplate-3.pl -b $bgf -m $mfta -p $pair`;
    ($inp = $bgf) =~ s/.bgf/.inp/;
} elsif (! -e $inp) {
    die "Align2Template-3 :: Provided INP file could not be found :: $inp\n";
}

# Load INP Structure File
open TMPL, "$inp";
while (<TMPL>) {
    if (/\*\s+(\d+)tmpl\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)/) {
	$dat{$1}{x}            = $2;
	$dat{$1}{y}            = $3;
	$dat{$1}{inphpc}       = $4;
	$dat{$1}{t}            = $5;
	$dat{$1}{p}            = $6;
	$dat{$1}{e}            = $7 * -1;
	$dat{$1}{inpetaresid}  = $8;
	$dat{$1}{inpetaresnum} = $9;
    }
}
close TMPL;

# Do some checking
for (my $i = 1; $i <= 7; $i++) {
    if ($dat{$i}{mftaetaresid} ne $dat{$i}{inpetaresid}) {
	die "Align2Template-3 :: Mismatch in TM$i between MFTA and INP Eta Residue ID ::\n".
	    " :: MFTA $dat{$i}{mftaetaresid} vs INP $dat{$i}{inpetaresid}\n";
    } else {
	$dat{$i}{etaresid} = $dat{$i}{mftaetaresid};
    }
    
    if ($dat{$i}{mftaetaresnum} != $dat{$i}{inpetaresnum}) {
	die "Align2Template-3 :: Mismatch in TM$i between MFTA and INP Eta Residue Num ::\n".
	    " :: MFTA $dat{$i}{mftaetaresnum} vs INP $dat{$i}{inpetaresnum}\n";
    } else {
	$dat{$i}{etaresnum} = $dat{$i}{mftaetaresnum};
    }

    if ($hpcinmfta) {
	$dat{$i}{hpc} = $dat{$i}{mftahpc};
    } else {
	$dat{$i}{hpc} = $dat{$i}{inphpc};
    }
}

# MAIN LOOP TO ALIGN EACH HELIX
my $geutils = "/project/Biogroup/Software/GEnsemble/programs/utilities";
my $pwb = "${geutils}/playWithBGF/playWithBGF";
for (my $i = 1; $i <= 7; $i++) {
    # Chop off helix
    `$pwb $bgf -c $i -o temp${i}.bgf`;

    # Apply changes to HPC, Theta, Phi, Eta
    if ($changeeta) {
	$dat{$i}{e}   -= $eta_changes[$i-1]; # Note: Eta runs backward to everything else
    }
    if ($changetheta) {
	$dat{$i}{t}   += $theta_changes[$i-1];
    }
    if ($changephi) {
	$dat{$i}{p}   += $phi_changes[$i-1];
    }
    if ($changehpc_rel) {
	$dat{$i}{hpc} += $hpcrel_changes[$i-1];
    }
    if ($changehpc_abs) {
	$dat{$i}{hpc}  = $hpcabs_changes[$i-1];
    }

    # Align Helix
    AlignHelix($i,"temp${i}.bgf",
	       $dat{$i}{hpc},
	       $dat{$i}{x},
	       $dat{$i}{y},
	       $dat{$i}{t},
	       $dat{$i}{p},
	       $dat{$i}{e},
	       $dat{$i}{etaresnum},
	       $nter,
	       $zout);
}

# Merge
(my $output = $bgf) =~ s/.bgf/.aligned.bgf/;
my $command =
    "/project/Biogroup/scripts/BGFtools/mergeBGFs.py".
    " aligned_helix1.bgf".
    " aligned_helix2.bgf".
    " aligned_helix3.bgf".
    " aligned_helix4.bgf".
    " aligned_helix5.bgf".
    " aligned_helix6.bgf".
    " aligned_helix7.bgf".
    " -s -o $output";
`$command`;

for (my $i = 1; $i <= 7; $i++) {
    unlink "temp${i}.bgf";
    unlink "aligned_helix${i}.bgf";
}
exit;

############################################################
### Help                                                 ###
############################################################
sub help {
    my $help = "
Program:
 :: .pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: Align2Template-3.pl -b {bgf} -m {mfta} -i {inp} -x
 ::   -e '{7 eta changes}' -t '{7 theta changes}'
 ::   -p '{7 phi changes}'
 ::   -y '{7 relative HPC changes}'
 ::   -z '{7 relative HPC changes}'

Input:
 :: -b | --bgf         :: Filename
 :: BGF file to modify.  Should consist of 7 TMs only,
 :: with absolute residue numbers and chains 1-7.

 :: -i | --inp         :: Filename
 :: INP structure file with X, Y, HPC, Theta, Phi, Eta, and
 :: EtaRes info.  Residue numbers should correspond to those
 :: in the BGF.  If no INP file is provided, then the one
 :: will be generated from the BGF using GetTemplate-3.

 :: -m | --mfta        :: Filename
 :: MFTA file with start/stop TM values in the first pair
 :: and HPC values in the first column.  Note: By default,
 :: the HPC values used in the alignment will come from the
 :: INP file (or the BGF itself, if no INP is provided).  In
 :: order to use the HPC values in the MFTA file you must
 :: use the '-x' option

 :: -x | --hpcinmfta   :: No Input
 :: Flag to use the HPC values from the MFTA file instead of
 :: the values in the BGF or INP files.

 :: -e | --eta         :: 7 Numbers
 :: Set of seven numbers corresponding to modifications to
 :: the seven Eta rotation values.  You MUST specify seven
 :: values, even if some of the values are 0 (i.e. no
 :: change in rotation).
 ::
 :: Ex: -e '15 -15 0 0 0 0 30'
 ::     This will rotate TM1 by 15 degrees, TM2 by -15, and
 ::     TM7 by 30.  These rotations are RELATIVE to the
 ::     values in the INP file (or BGF if no INP).

 :: -t | --theta       :: 7 Numbers
 :: Set of seven numbers corresponding to modifications to
 :: the seven Theta tilt values.  You MUST specify seven
 :: values, even if some of the values are 0 (i.e. no
 :: change in tilt).
 ::
 :: Ex: -t '10 -10 0 0 0 0 10'
 ::     This will tilt TM1 by 10 degrees, TM2 by -10, and
 ::     TM7 by 10.  These tilts are RELATIVE to the values
 ::     in the INP file (or BGF if no INP).

 :: -p | --phi         :: 7 Numbers
 :: Set of seven numbers corresponding to modifications to
 :: the seven Phi tilt values.  You MUST specify seven
 :: values, even if some of the values are 0 (i.e. no
 :: change in tilt).
 ::
 :: Ex: -p '15 -15 0 0 0 0 30'
 ::     This will tilt TM1 by 15 degrees, TM2 by -15, and
 ::     TM7 by 30.  These tilts are RELATIVE to the values
 ::     in the INP file (or BGF if no INP).

 :: -y | --modhpc_rel  :: 7 Numbers
 :: Set of seven numbers corresponding to modifications to
 :: the seven HPC values.  You MUST specify seven values,
 :: even if some of the values are 0 (i.e. no change in HPC).
 ::
 :: Ex: -y '0 0 1 0 0 0 0'
 ::     This will increase the HPC of TM3 by 1 residue.  This
 ::     is RELATIVE to the values in the INP file (or BGF
 ::     or MFTA as the case may be).

 :: -z | --modhpc_abs  :: 7 Numbers
 :: Set of seven numbers corresponding to modifications to
 :: the seven HPC values.  You MUST specify seven values.
 ::
 :: Ex: -z '40.92 76.94 114.61 159.52 198.15 341.63 374.30'
 ::     This will set the HPC values to exactly these values.
 ::     Note that unlike the '-y' option these are ABSOLUTE
 ::     values, not relative changes.

 :: --pair             :: Integer
 :: Pair of start/stop values in the MFTA file corresponding to
 :: the BGF.

 :: -h | --help        :: No Input
 :: Displays this help message.

Description:
 :: This program takes in a BGF, MFTA, and (optionally) an
 :: INP file and aligns the helices in the BGF according to
 :: the information in the INP or MFTA files, which can be
 :: further modified by the '-e', '-t', '-p', '-y', and '-z'
 :: options.
 ::
 :: If no INP file is provided, one will be created for the
 :: BGF file using GetTemplate-3.  The user-provided INP
 :: or auto-generated INP file will determine the initial
 :: tilts/rotations/positions of the helices.
 ::
 :: By default, the HPC values come from the INP (if it is
 :: provided) or from the BGF (if no INP).  The user can
 :: specify that the HPC values from the MFTA file be used
 :: in place of these values by using the '-x' option.
 ::
 :: The '-e', '-t', '-p', '-y', and '-z' options allow you
 :: to modify the Eta, Theta, Phi, and HPC values relative
 :: to the values in the INP/BGF/MFTA files.
 ::
 :: The helices are then aligned to these new values, and
 :: a new BGF file ({prefix}.aligned.bgf) will be created.

Usage:
 :: Align2Template-3.pl -b {bgf} -m {mfta} -i {inp} -x
 ::   -e '{7 eta changes}' -t '{7 theta changes}'
 ::   -p '{7 phi changes}'
 ::   -y '{7 relative HPC changes}'
 ::   -z '{7 relative HPC changes}'

";
    die $help;
}
