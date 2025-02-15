package utils::Template;

use strict;
use warnings;
use Math::Complex;
use Math::Trig;
use POSIX qw(ceil floor);
use myMath::VectorReal qw(:all);
use myMath::MatrixReal qw(:all);

use utils::MomOfInertiaAxes;
use utils::Align2z;
 
our $VERSION = '1.00';

use base 'Exporter';

our @EXPORT = qw(Template);

# define the function

sub Template {

my ($num_bbatoms,$bbatom_mass_ref,$bbatom_x_ref,$bbatom_y_ref,$bbatom_z_ref,$bbatom_resid_ref,$bbatom_name_ref,$helixid,$etaresid,$nter,$zout) = @_;

my $halfpi = pi/2;
my $twopi = 2*pi;

my $i = 0;
my $j = 0;

my @bbatom_mass=();
my @bbatom_x=();
my @bbatom_y=();
my @bbatom_z=();
my @bbatom_resid=();
my @bbatom_name=();

@bbatom_mass=@{$bbatom_mass_ref};
@bbatom_x=@{$bbatom_x_ref};
@bbatom_y=@{$bbatom_y_ref};
@bbatom_z=@{$bbatom_z_ref};
@bbatom_resid=@{$bbatom_resid_ref};
#        for ($j=0;$j<$num_bbatoms;$j++) {
#            print "$bbatom_resid[$j]\n";
#        }
@bbatom_name=@{$bbatom_name_ref};

my $helxlen = $bbatom_x[$num_bbatoms-1] - $bbatom_x[0];
my $helylen = $bbatom_y[$num_bbatoms-1] - $bbatom_y[0];
my $helzlen = $bbatom_z[$num_bbatoms-1] - $bbatom_z[0];
my $helrlen = sqrt($helxlen*$helxlen + $helylen*$helylen + $helzlen*$helzlen);


# Get the helix axis as the lowest moment of inertia vector
my ($xcom,$ycom,$zcom,$eigx,$eigy,$eigz) = MomOfInertiaAxes($num_bbatoms,\@bbatom_mass,\@bbatom_x,\@bbatom_y,\@bbatom_z);
#if ($helixid == 3) {
#printf '%3d %8.2f %8.2f %8.2f %8.4f %8.4f %8.4f', $helixid,$xcom,$ycom,$zcom,$eigx,$eigy,$eigz;
#print "\n";
#}

if (($nter eq 'out' and $zout eq 'plus') or ($nter eq 'in' and $zout eq 'minus')) {
  if ($helixid % 2) {
    if ($eigz > 0.0) { $eigz = -$eigz; $eigy = -$eigy; $eigx = -$eigx;}
  } else {
    if ($eigz < 0.0) { $eigz = -$eigz; $eigy = -$eigy; $eigx = -$eigx; }
  }
} elsif (($nter eq 'out' and $zout eq 'minus') or ($nter eq 'in' and $zout eq 'plus')) {
  if ($helixid % 2) {
    if ($eigz < 0.0) { $eigz = -$eigz; $eigy = -$eigy; $eigx = -$eigx; }
  } else {
    if ($eigz > 0.0) { $eigz = -$eigz; $eigy = -$eigy; $eigx = -$eigx; }
  }
}

my $helvecx1 = $xcom;
my $helvecy1 = $ycom;
my $helvecz1 = $zcom;

my $helvecx2 = $xcom+$eigx;
my $helvecy2 = $ycom+$eigy;
my $helvecz2 = $zcom+$eigz;

# intersection with z=0 plane
my $helz0x = $helvecx1+($helvecz1/($helvecz1-$helvecz2))*($helvecx2-$helvecx1);
my $helz0y = $helvecy1+($helvecz1/($helvecz1-$helvecz2))*($helvecy2-$helvecy1);

my $heltheta = acos($eigz);
my $helphi = atan2($eigy,$eigx);

if ($heltheta > $halfpi) { $heltheta = pi-$heltheta; }
if ($helphi < 0) { $helphi = $twopi+$helphi; }


### now for the Hydrophobic center

#  First align the helix vector along the z-axis
($bbatom_x_ref,$bbatom_y_ref,$bbatom_z_ref) = Align2z($num_bbatoms,\@bbatom_x,\@bbatom_y,\@bbatom_z,$helixid,$nter,$zout,$eigx,$eigy,$eigz,$helz0x,$helz0y);

@bbatom_x=@{$bbatom_x_ref};
@bbatom_y=@{$bbatom_y_ref};
@bbatom_z=@{$bbatom_z_ref};

# now recalculate the Moment of Inertia axes to confirm that axis is aligned
# with z-axis
($xcom,$ycom,$zcom,$eigx,$eigy,$eigz) = MomOfInertiaAxes($num_bbatoms,\@bbatom_mass,\@bbatom_x,\@bbatom_y,\@bbatom_z);

if (($nter eq 'out' and $zout eq 'plus') or ($nter eq 'in' and $zout eq 'minus')) {
  if ($helixid % 2) {
    if ($eigz > 0.0) { $eigz = -$eigz; $eigy = -$eigy; $eigx = -$eigx;}
  } else {
    if ($eigz < 0.0) { $eigz = -$eigz; $eigy = -$eigy; $eigx = -$eigx; }
  }
} elsif (($nter eq 'out' and $zout eq 'minus') or ($nter eq 'in' and $zout eq 'plus')) {
  if ($helixid % 2) {
    if ($eigz < 0.0) { $eigz = -$eigz; $eigy = -$eigy; $eigx = -$eigx; }
  } else {
    if ($eigz > 0.0) { $eigz = -$eigz; $eigy = -$eigy; $eigx = -$eigx; }
  }
}

$helvecx1 = $xcom;
$helvecy1 = $ycom;
$helvecz1 = $zcom;

$helvecx2 = $xcom+$eigx;
$helvecy2 = $ycom+$eigy;
$helvecz2 = $zcom+$eigz;

# intersection with z=0 plane
my $helz0x2 = $helvecx1+($helvecz1/($helvecz1-$helvecz2))*($helvecx2-$helvecx1);
my $helz0y2 = $helvecy1+($helvecz1/($helvecz1-$helvecz2))*($helvecy2-$helvecy1);

#printf '%3d %8.2f %8.2f %8.2f %8.4f %8.4f %8.4f', $helixid,$xcom,$ycom,$zcom,$eigx,$eigy,$eigz;
#print "\n";


my $num_caatoms=0;
my @caatom_z = ();
my @caatom_resid = ();
my ($etares_x,$etares_y,$etares_z);
for ($j=0;$j<$num_bbatoms;$j++) {
    if ($bbatom_name[$j] eq 'CA') {
        $num_caatoms++;
        $caatom_z[$num_caatoms-1] = $bbatom_z[$j];
        $caatom_resid[$num_caatoms-1] = $bbatom_resid[$j];
        if ($bbatom_resid[$j] == $etaresid) {
            $etares_x = $bbatom_x[$j];
            $etares_y = $bbatom_y[$j];
            $etares_z = $bbatom_z[$j];
        }
    }
}
my ($hpcanchor1,$hpcz1,$hpcanchor2,$hpcz2);
for ($j=0;$j<$num_caatoms;$j++) {
    my $zsign = $caatom_z[$j]*$caatom_z[$j+1];
    if ($zsign < 0.0) {
        $hpcanchor1 = $caatom_resid[$j];
        $hpcz1 = $caatom_z[$j];
        $hpcanchor2 = $caatom_resid[$j+1];
        $hpcz2 = $caatom_z[$j+1];
        last;
    }
}
# hydrophobic center 
my $helhpc = $hpcanchor1 + ((-$hpcz1)/($hpcz2-$hpcz1));
#print "hpc: $hpcanchor1,$hpcz1,$hpcanchor2,$hpcz2,$helhpc\n";

# eta angle
my $etaresvecx = $etares_x-$helz0x;
my $etaresvecy = $etares_y-$helz0y;
# eta clockwise is positive looking at the TM bundle from EC side
my $heleta = -atan2($etaresvecy,$etaresvecx);
if ($heleta < 0.0) { $heleta = 2*pi + $heleta; }
my $heletad = rad2deg($heleta);
#print "eta: $etaresvecx,$etaresvecy,$heletad\n";

my $helthetad = rad2deg($heltheta);
my $helphid = rad2deg($helphi);
return ($helz0x,$helz0y,$helhpc,$helthetad,$helphid,$heletad);

@bbatom_x=();
@bbatom_y=();
@bbatom_z=();
@bbatom_mass=();
@bbatom_resid=();
@bbatom_name=();

reset;

}

1;
