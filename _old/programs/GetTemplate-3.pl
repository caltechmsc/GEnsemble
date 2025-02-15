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
use Math::Trig;
use myMath::VectorReal qw(:all);
use myMath::MatrixReal qw(:all);
use utils::Template;
use inout::readpdb_bbcoord;

############################################################
### Input                                                ###
############################################################

if (@ARGV == 0) { help(); }

my $nter       = 'out';
my $zout       = 'plus';
my $tmatorigin = 3;
my $tmalongx   = 2;
my $pair       = 1;

#abcdefghijklmnopqrstuvwxyz
#abcdefg ijklmnopqrstuvwxyz
GetOptions ('h|help'   => \$help,
	    'm|mfta=s' => \$mfta,
	    'b|bgf=s'  => \$bgf,
	    'p|pair=i' => \$pair
	    );

if ($help)       { help(); }
if (! $bgf) {
    die "GetTemplate-3 :: Must provide BGF file to align.\n";
} elsif (! -e $bgf) {
    die "GetTemplate-3 :: Provided BGF could not be found :: $bgf\n";
}

if (! $mfta) {
    die "GetTemplate-3 :: Must provide MFTA file corresponding to BGF.\n";
} elsif (! -e $mfta) {
    die "GetTemplate-3 :: Provided MFTA could not be found :: $mfta\n";
}

if (!(1 <= $pair) && !($pair <= 4)) {
	die "GetTemplate-3 :: TM pair must be number 1-4\n";
}

############################################################
### Main Routine                                         ###
############################################################

# Load MFTA
open MFTA, $mfta;
my @tmid;
my @begintm;
my @endtm;
my @etares;
my @etaresid;
while (<MFTA>) {
    # Get Eta Residue Number
    if (/\*\s+(\d+)tm\s+
	(\S+)\s+(\S+)\s+
	(\S+)\s+(\S+)\s+
	(\S+)\s+(\S+)\s+
	(\S+)\s+(\S+)\s+
	(\S+)\s+(\d+)/x) {
		if ($pair == 1) {
			$begintm[$1]  = $2;
			$endtm[$1]    = $3;
		} elsif ($pair == 2) {
			$begintm[$1]  = $4;
			$endtm[$1]    = $5;
		} elsif ($pair == 3) {
			$begintm[$1]  = $6;
			$endtm[$1]    = $7;
		} elsif ($pair == 4) {
			$begintm[$1]  = $8;
			$endtm[$1]    = $9;
		}
		$etares[$1]   = $10;
		$etaresid[$1] = $11;
    }
}
close MFTA;

# BGF to PDB
$pdb = bgf2pdb($bgf);

# MAIN LOOP
my @tmhpc=();
my @tmx=();
my @tmy=();
my @tmtheta=();
my @tmphi=();
my @tmeta=();
my $natoms;
my @num_bbatoms=();
my @bbatom_mass=();
my @bbatom_x=();
my @bbatom_y=();
my @bbatom_z=();
my @bbatom_resid=();
my @bbatom_name=();
my @bundle_bbatom_mass=();
my @bundle_bbatom_x=();
my @bundle_bbatom_y=();
my @bundle_bbatom_z=();
my @bundle_bbatom_resid=();
my @bundle_bbatom_name=();
my $bundlex = 0;
my $bundley = 0;
my ($i,$j,$k,$dum1,$dum2,$dum3,$dum4,$dum5,$dum6,$dum7,$dum8,$dumx,$dumy,$dumz);
for ($i = 1; $i <= 7; $i++) {
    # Read Backbone PDB Coordinate for TM $i
    ($natoms,$bbatom_mass_ref,
     $bbatom_x_ref,$bbatom_y_ref,$bbatom_z_ref,
     $bbatom_resid_ref,$bbatom_name_ref)
	= readpdb_bbcoord($pdb,$begintm[$i],$endtm[$i],$nter,$zout);
    $num_bbatoms[$i]=$natoms;
    my @bbatom_mass=@{$bbatom_mass_ref};
    my @bbatom_x=@{$bbatom_x_ref};
    my @bbatom_y=@{$bbatom_y_ref};
    my @bbatom_z=@{$bbatom_z_ref};
    my @bbatom_resid=@{$bbatom_resid_ref};
    my @bbatom_name=@{$bbatom_name_ref};
    push(@bundle_bbatom_mass,\@bbatom_mass);
    push(@bundle_bbatom_x,\@bbatom_x);
    push(@bundle_bbatom_y,\@bbatom_y);
    push(@bundle_bbatom_z,\@bbatom_z);
    push(@bundle_bbatom_resid,\@bbatom_resid);
    push(@bundle_bbatom_name,\@bbatom_name);

    # Calculate Positions and Tilts for that TM
    ($tmx[$i],$tmy[$i],$tmhpc[$i],$tmtheta[$i],$tmphi[$i],$tmeta[$i])
	= Template($num_bbatoms[$i],\@bbatom_mass,
		   \@bbatom_x,\@bbatom_y,\@bbatom_z,
		   \@bbatom_resid,\@bbatom_name,
		   $i,$etaresid[$i],$nter,$zout);
    $bundlex += $tmx[$i];
    $bundley += $tmy[$i];


}
# END of MAIN LOOP
@bbatom_x=();
@bbatom_y=();
@bbatom_z=();
@bbatom_mass=();
@bbatom_resid=();
@bbatom_name=();
$numtms = 7;
$bundlex = $bundlex/$numtms;
$bundley = $bundley/$numtms;

# Does Something
$dumx = $tmx[$tmatorigin];
$dumy = $tmy[$tmatorigin];
for ($i=1;$i<=$numtms;$i++) {
    $tmx[$i] -= $dumx;
    $tmy[$i] -= $dumy;
    for ($j=0;$j<$num_bbatoms[$i];$j++) {
        $bundle_bbatom_x[$i-1][$j]=$bundle_bbatom_x[$i-1][$j]-$dumx;
        $bundle_bbatom_y[$i-1][$j]=$bundle_bbatom_y[$i-1][$j]-$dumy;
    }
    $helixid=$i;
}

# Rotate and align
my $cosrefang=1.0;
my $sinrefang=0.0;
if ($tmalongx > 0) {
    my $refangr = atan2($tmy[$tmalongx],$tmx[$tmalongx]);
    if ($refangr < 0.0) { $refangr = 2*pi+$refangr; }
    my $refangd=rad2deg($refangr);
    $cosrefang=cos($refangr);
    $sinrefang=sin($refangr);
}
my $rmvecx = vector($cosrefang,-$sinrefang,0.0);
my $rmvecy = vector($sinrefang,$cosrefang,0.0);
my $rmvecz = vector(0.0,0.0,1.0);

# Rotation matrix.
# Each of the three arguments to vector_matrix should be row vectors.
my $rmat = vector_matrix( $rmvecx, $rmvecy, $rmvecz );
for ($i=1;$i<=$numtms;$i++) {
    my $scoord = vector($tmx[$i],$tmy[$i],0.0);
    my $rcoord = $scoord * $rmat;
    $tmx[$i]=$rcoord . X;
    $tmy[$i]=$rcoord . Y;
    for ($j=0;$j<$num_bbatoms[$i];$j++) {
        my $scoord = vector($bundle_bbatom_x[$i-1][$j],
			    $bundle_bbatom_y[$i-1][$j],
			    $bundle_bbatom_z[$i-1][$j]);
        my $rcoord = $scoord * $rmat;
        $bundle_bbatom_x[$i-1][$j] = $rcoord . X;
        $bundle_bbatom_y[$i-1][$j] = $rcoord . Y;
        $bundle_bbatom_z[$i-1][$j] = $rcoord . Z;
    }
    $helixid=$i;
}

# Recalculate the tilts and centers
my $txt = "";
for ($i=1;$i<=$numtms;$i++) {
    $helixid=$i;
    for ($j=0;$j<$num_bbatoms[$i];$j++) {
        $bbatom_x[$j]=$bundle_bbatom_x[$i-1][$j];
        $bbatom_y[$j]=$bundle_bbatom_y[$i-1][$j];
        $bbatom_z[$j]=$bundle_bbatom_z[$i-1][$j];
        $bbatom_resid[$j]=$bundle_bbatom_resid[$i-1][$j];
        $bbatom_name[$j]=$bundle_bbatom_name[$i-1][$j];
        $bbatom_mass[$j]=$bundle_bbatom_mass[$i-1][$j];
    }
    # calculate positions and tilts for that TM
    ($tmx[$i],$tmy[$i],$tmhpc[$i],$tmtheta[$i],$tmphi[$i],$tmeta[$i])
	= Template($num_bbatoms[$i],\@bbatom_mass,
		   \@bbatom_x,\@bbatom_y,\@bbatom_z,
		   \@bbatom_resid,\@bbatom_name,
		   $i,$etaresid[$i],$nter,$zout);
    $txt .= sprintf
	"*%3dtmpl %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f %4s%5d\n",
	$helixid,$tmx[$helixid],$tmy[$helixid],$tmhpc[$helixid],
	$tmtheta[$helixid],$tmphi[$helixid],$tmeta[$helixid],
	$etares[$i],$etaresid[$i];
}
$txt .= "* TM          X        Y       HPC     Theta      Phi      Eta    EtaRes\n";
$txt =~ s/\-0\.00/ 0\.00/g;
($outfile = $bgf) =~ s/.bgf/.inp/;
open OUT, ">$outfile";
print OUT $txt;
close OUT;

unlink "$pdb";

exit;

############################################################
### BGF2PDB                                              ###
############################################################

sub bgf2pdb {
    (my $infile) = @_;
    (my $outfile = $infile) =~ s/.bgf/.temp.pdb/;

    open(INBGF, $infile);
    open(OUTPDB, ">$outfile");

    my $atom = 1;
    my @TRANSLATIONS = ();

    while (my $line = <INBGF>) {
	my @LINE = split(' ', $line);
    
	if ($LINE[0] eq 'DESCRP') {
	    $newline = 'HEADER ' . substr($line, 7, 43);
	    chomp($newline);
	    $newline .= "\n";
	    print OUTPDB $newline;
	}

	if ($LINE[0] eq 'REMARK') {
	    print OUTPDB $line;
	}

	if ($LINE[0] eq 'ATOM') {
	    $newline = "                                                       \n";
	    substr($newline, 0, 4) = 'ATOM';
	    substr($newline, (11 - length($atom)), length($atom)) = $atom;
	    substr($newline, 13, length($LINE[2])) = $LINE[2];
	    substr($newline, 17, 3) = $LINE[3];
	    substr($newline, 21, 1) = $LINE[4];
	    substr($newline, (26 - length($LINE[5])), length($LINE[5])) = $LINE[5];
	    if (length($LINE[6]) > 7) {
		$LINE[6] = substr($LINE[6], 0, 7);
	    }
	    substr($newline, (38 - length($LINE[6])), length($LINE[6])) = $LINE[6];
	    if (length($LINE[7]) > 7) {
		$LINE[7] = substr($LINE[7], 0, 7);
	    }
	    substr($newline, (46 - length($LINE[7])), length($LINE[7])) = $LINE[7];
	    if (length($LINE[8]) > 7) {
		$LINE[8] = substr($LINE[8], 0, 7);
	    }
	    substr($newline, (54 - length($LINE[8])), length($LINE[8])) = $LINE[8];
	    print OUTPDB $newline;
	    $TRANSLATIONS[$LINE[1]] = $atom;
	    $atom++;
	}

	if ($LINE[0] eq 'HETATM') {
	    $newline = "                                                       \n";
	    substr($newline, 0, 4) = 'HETATM';
	    substr($newline, (11 - length($atom)), length($atom)) = $atom;
	    substr($newline, 13, length($LINE[2])) = $LINE[2];
	    substr($newline, 17, 3) = $LINE[3];
	    substr($newline, 21, 1) = $LINE[4];
	    substr($newline, (26 - length($LINE[5])), length($LINE[5])) = $LINE[5];
	    if (length($LINE[6]) > 7) {
		$LINE[6] = substr($LINE[6], 0, 7);
	    }
	    substr($newline, (38 - length($LINE[6])), length($LINE[6])) = $LINE[6];
	    if (length($LINE[7]) > 7) {
		$LINE[7] = substr($LINE[7], 0, 7);
	    }
	    substr($newline, (46 - length($LINE[7])), length($LINE[7])) = $LINE[7];
	    if (length($LINE[8]) > 7) {
		$LINE[8] = substr($LINE[8], 0, 7);
	    }
	    substr($newline, (54 - length($LINE[8])), length($LINE[8])) = $LINE[8];
	    print OUTPDB $newline;
	    $TRANSLATIONS[$LINE[1]] = $atom;
	    $atom++;
	}

    
	if ($LINE[0] eq 'CONECT' && (defined $TRANSLATIONS[$LINE[1]])) {
	    $newline = 'CONECT';
	    $count = 1;
	  LOOP:	while ($currnum = $LINE[$count]) {
	      if (!(defined $TRANSLATIONS[$LINE[$count]])) {
		  splice(@LINE, $count, 1);
		  goto LOOP;
	      }
	      $newline .= "     ";
	      $newnum = $TRANSLATIONS[$currnum];
	      substr($newline, (6 + (5 * $count) - length($newnum)), length($newnum)) = $newnum;
	      $count++;
	  }
	    $newline .= "\n";
	    print OUTPDB $newline;
	}
	
	if ($LINE[0] eq 'END') {
	    print OUTPDB $line;
	}
    }

    return $outfile;
}

############################################################
### Help                                                 ###
############################################################

sub help {
    $help_message = "
Program:
 :: GetTemplate-3.pl

Authors:
 :: Adam Griffith (griffith\@wag.caltech.edu
 :: Ravi Abrol (abrol\@wag.caltech.edu)

Usage:
 :: GetTemplate-3.pl -b {bgf} -m {mfta}

Input:
 :: -b | --bgf              :: Filename
 :: BGF file to get structure information for.

 :: -m | --mfta             :: Filename
 :: MFTA file corresponding to BGF.  Expects that the
 :: TM start/stop values are in the first pair of TM
 :: values in the MFTA file.  Also reads the Eta Residue
 :: information from the MFTA file.
 
 :: -p | --pair             :: Integer 1-4
 :: Pair of TM start/stop values to use

 :: -h | --help             :: No Input
 :: Prints this help message.

";
    die $help_message;
}
