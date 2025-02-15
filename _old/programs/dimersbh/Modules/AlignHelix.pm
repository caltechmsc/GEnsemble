package Modules::AlignHelix;

use strict;
use warnings;
use Math::Complex;
use Math::Trig;
use POSIX qw(ceil floor);
use myMath::VectorReal qw(:all);
use myMath::MatrixReal qw(:all);

use Modules::readbgf_coord;
use Modules::writebgf_coord;
use myMath::MomOfInertiaAxes;
use Modules::Align2z;
 
our $VERSION = '1.10';

use base 'Exporter';

our @EXPORT = qw(AlignHelix);

# define the function

sub AlignHelix {

my ($helixid,$inputbgf,$helixhpc,$thelx,$thely,$theltheta,$thelphi,$theleta,$etaresid,$nter,$zout) = @_;

my $halfpi = pi/2;
my $twopi = 2*pi;
my $outputbgf = "aligned_helix".$helixid.".bgf";

my ($i,$j,$k);

my ($num_allatoms,$allatom_x_ref,$allatom_y_ref,$allatom_z_ref,$num_bbatoms,$bbatom_mass_ref,$bbatom_x_ref,$bbatom_y_ref,$bbatom_z_ref,$bbatom_resid_ref,$bbatom_name_ref,$hpcanchor1,$hpcanchor2) = readbgf_coord($inputbgf,$helixhpc);

my @allatom_x=@$allatom_x_ref;
my @allatom_y=@$allatom_y_ref;
my @allatom_z=@$allatom_z_ref;

my @bbatom_mass=@$bbatom_mass_ref;
my @bbatom_x=@$bbatom_x_ref;
my @bbatom_y=@$bbatom_y_ref;
my @bbatom_z=@$bbatom_z_ref;
my @bbatom_resid=@$bbatom_resid_ref;
my @bbatom_name=@$bbatom_name_ref;

my $helxlen = $bbatom_x[$num_bbatoms-1] - $bbatom_x[0];
my $helylen = $bbatom_y[$num_bbatoms-1] - $bbatom_y[0];
my $helzlen = $bbatom_z[$num_bbatoms-1] - $bbatom_z[0];
my $helrlen = sqrt($helxlen*$helxlen + $helylen*$helylen + $helzlen*$helzlen);

# Move COM of HELIX to origin
my $totm = 0.0;
my $totmx = 0.0;
my $totmy = 0.0;
my $totmz = 0.0;
for ($k = 0; $k < $num_bbatoms; $k++) {
    $totm   = $totm   + $bbatom_mass[$k];
    $totmx  = $totmx  + $bbatom_mass[$k]*$bbatom_x[$k];
    $totmy  = $totmy  + $bbatom_mass[$k]*$bbatom_y[$k];
    $totmz  = $totmz  + $bbatom_mass[$k]*$bbatom_z[$k];
}
my $xcom = $totmx/$totm;
my $ycom = $totmy/$totm;
my $zcom = $totmz/$totm;
for ($i=0;$i<$num_allatoms;$i++) {
    $allatom_x[$i] = $allatom_x[$i] - $xcom;
    $allatom_y[$i] = $allatom_y[$i] - $ycom;
    $allatom_z[$i] = $allatom_z[$i] - $zcom;
}
for ($i=0;$i<$num_bbatoms;$i++) {
    $bbatom_x[$i] = $bbatom_x[$i] - $xcom;
    $bbatom_y[$i] = $bbatom_y[$i] - $ycom;
    $bbatom_z[$i] = $bbatom_z[$i] - $zcom;
}

my ($eigx,$eigy,$eigz);
# Get the helix axis as the lowest moment of inertia vector
($xcom,$ycom,$zcom,$eigx,$eigy,$eigz) = MomOfInertiaAxes($num_bbatoms,\@bbatom_mass,\@bbatom_x,\@bbatom_y,\@bbatom_z);

# Flip the moment of inertia axis vector to make sure that it is pointing to
#  +z for odd helices and -z for even helices if nter is out and zout is plus
#  -z for odd helices and +z for even helices if nter is in and zout in plus
#  ...
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

## align the helix vector along the z-axis
## +z for odd helices and -z for even helices

($allatom_x_ref,$allatom_y_ref,$allatom_z_ref,$bbatom_x_ref,$bbatom_y_ref,$bbatom_z_ref) = Align2z($num_allatoms,\@allatom_x,\@allatom_y,\@allatom_z,$num_bbatoms,\@bbatom_x,\@bbatom_y,\@bbatom_z,$helixid,$nter,$zout,$eigx,$eigy,$eigz,0.0,0.0);

@allatom_x=@{$allatom_x_ref};
@allatom_y=@{$allatom_y_ref};
@allatom_z=@{$allatom_z_ref};

@bbatom_x=@{$bbatom_x_ref};
@bbatom_y=@{$bbatom_y_ref};
@bbatom_z=@{$bbatom_z_ref};

# Flip the helix to make sure that it has correct orientation relative to bundle
my $flip = 1;
if (($nter eq 'out' and $zout eq 'plus') or ($nter eq 'in' and $zout eq 'minus')) {
  if ($helixid % 2) {
    if ($bbatom_z[0] < 0.0) { $flip = -1; }
  } else {
    if ($bbatom_z[0] > 0.0) { $flip = -1; }
  }
} elsif (($nter eq 'out' and $zout eq 'minus') or ($nter eq 'in' and $zout eq 'plus')) {
  if ($helixid % 2) {
    if ($bbatom_z[0] > 0.0) { $flip = -1; }
  } else {
    if ($bbatom_z[0] < 0.0) { $flip = -1; }
  }
}
#print "$flip\n";
for ($i=0;$i<$num_allatoms;$i++) {
#   $allatom_x[$i] = $allatom_x[$i];
    $allatom_y[$i] = $flip*$allatom_y[$i];
    $allatom_z[$i] = $flip*$allatom_z[$i];
}
for ($i=0;$i<$num_bbatoms;$i++) {
#   $bbatom_x[$i] = $bbatom_x[$i];
    $bbatom_y[$i] = $flip*$bbatom_y[$i];
    $bbatom_z[$i] = $flip*$bbatom_z[$i];
}

#Find the offset for matching the hydrophobic center to z=0 plane
#
my $iz1=$bbatom_z[$hpcanchor1];
my $iz2=$bbatom_z[$hpcanchor2];
my $ifracz = $helixhpc - floor($helixhpc);
my $idelz = $iz1 + ($iz2 - $iz1)*$ifracz;

# translate the input helix to align the hydrophobic center with z=0 plane
for ($i=0;$i<$num_allatoms;$i++) {
    $allatom_z[$i] = $allatom_z[$i] - $idelz;
}
for ($i=0;$i<$num_bbatoms;$i++) {
    $bbatom_z[$i] = $bbatom_z[$i] - $idelz;
}

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
# check for correctness of HPC
#my ($hpcz1,$hpcz2);
#for ($j=0;$j<$num_caatoms;$j++) {
#    my $zsign = $caatom_z[$j]*$caatom_z[$j+1];
#    if ($zsign < 0.0) {
#        $hpcanchor1 = $caatom_resid[$j];
#        $hpcz1 = $caatom_z[$j];
#        $hpcanchor2 = $caatom_resid[$j+1];
#        $hpcz2 = $caatom_z[$j+1];
#        last;
#    }
#}
# hydrophobic center
#my $helhpc = $hpcanchor1 + ((-$hpcz1)/($hpcz2-$hpcz1));
#print "hpc: $hpcanchor1,$hpcz1,$hpcanchor2,$hpcz2,$helhpc\n";

# rotate by eta angle
my $etaresvecx = $etares_x;
my $etaresvecy = $etares_y;
my $heletar = atan2($etaresvecy,$etaresvecx);
if ($heletar < 0.0) { $heletar = 2*pi + $heletar; }
my $heletad = rad2deg($heletar);
#print "eta: $etaresvecx,$etaresvecy,$heletad,$theleta\n";

my $cosrefang=1.0;
my $sinrefang=0.0;
    my $refangr = $heletar - deg2rad($theleta);
    if ($refangr < 0.0) { $refangr = 2*pi+$refangr; }
    my $refangd=rad2deg($refangr);
#    print "$refangd\n";
    $cosrefang=cos($refangr);
    $sinrefang=sin($refangr);

my $rmvecx = vector($cosrefang,-$sinrefang,0.0);
my $rmvecy = vector($sinrefang,$cosrefang,0.0);
my $rmvecz = vector(0.0,0.0,1.0);

# rotation matrix.
# Each of the three arguments to vector_matrix should be row vectors.
my $rmat = vector_matrix( $rmvecx, $rmvecy, $rmvecz );

for ($j=0;$j<$num_bbatoms;$j++) {
    my $scoord = vector($bbatom_x[$j],$bbatom_y[$j],$bbatom_z[$j]);
    my $rcoord = $scoord * $rmat;
    $bbatom_x[$j] = $rcoord . X;
    $bbatom_y[$j] = $rcoord . Y;
    $bbatom_z[$j] = $rcoord . Z;
}
for ($j=0;$j<$num_allatoms;$j++) {
    my $scoord = vector($allatom_x[$j],$allatom_y[$j],$allatom_z[$j]);
    my $rcoord = $scoord * $rmat;
    $allatom_x[$j] = $rcoord . X;
    $allatom_y[$j] = $rcoord . Y;
    $allatom_z[$j] = $rcoord . Z;
}
#writebgf_coord($inputbgf,$outputbgf,\@allatom_x,\@allatom_y,\@allatom_z);

# Get the helix axis as the lowest moment of inertia vector
($xcom,$ycom,$zcom,$eigx,$eigy,$eigz) = MomOfInertiaAxes($num_bbatoms,\@bbatom_mass,\@bbatom_x,\@bbatom_y,\@bbatom_z);

# Flip the moment of inertia axis vector to make sure that it is pointing to
#  +z for odd helices and -z for even helices if nter is out and zout is plus
#  -z for odd helices and +z for even helices if nter is in and zout in plus
#  ...
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

## align the helix vector which is currently along the z-axis
## along the template helix vector

# unit vector of the input helix axis at origin currently along z-axis
#print "$helixid $eigx $eigy $eigz\n";
my $ihelvec = vector($eigx,$eigy,$eigz);
my $normihel = sqrt($eigx**2 + $eigy**2 + $eigz**2);

if (($nter eq 'out' and $zout eq 'plus') or ($nter eq 'in' and $zout eq 'minus')) {
    if ( $helixid % 2 ) {
        $theltheta = 180.0 - $theltheta;
    }
} elsif (($nter eq 'out' and $zout eq 'minus') or ($nter eq 'in' and $zout eq 'plus')) {
    if ( ($helixid+1)%2 ) {                                                               $theltheta = 180.0 - $theltheta;                                            }
}


# unit vector of the template helix axis at origin
my $thelvecx = sin($theltheta*pi/180.0)*cos($thelphi*pi/180.0);
my $thelvecy = sin($theltheta*pi/180.0)*sin($thelphi*pi/180.0);
my $thelvecz = cos($theltheta*pi/180.0);
my $thelvec = vector($thelvecx,$thelvecy,$thelvecz);
my $normthel = sqrt($thelvecx**2 + $thelvecy**2 + $thelvecz**2);

# unit vector perpendicular to the input and template helix axis vectors
my $normvec = vector(0.0,0.0,0.0);
$normvec = $thelvec x $ihelvec;
my $normvecx = $normvec . X;
my $normvecy = $normvec . Y;
my $normvecz = $normvec . Z;
my $normnorm = sqrt($normvecx**2 + $normvecy**2 + $normvecz**2);
$normvecx = $normvecx/$normnorm;
$normvecy = $normvecy/$normnorm;
$normvecz = $normvecz/$normnorm;

# angle between the input and template helix axis vectors
my $anghelsr = acos($thelvec . $ihelvec);
my $anghelsd = rad2deg($anghelsr);

# rotation matrix construction that will rotate the input helix axis vector
# to align with the template helix axis vector
my $rmc = $thelvec . $ihelvec;
my $rms = sin($anghelsr);
my $rmC = 1.0-$rmc;
my $rmx = $normvecx;
my $rmy = $normvecy;
my $rmz = $normvecz;

my $rm11=$rmx*$rmx*$rmC + $rmc;
my $rm21=$rmx*$rmy*$rmC + $rmz*$rms;
my $rm31=$rmz*$rmx*$rmC - $rmy*$rms;

my $rm12=$rmx*$rmy*$rmC - $rmz*$rms;
my $rm22=$rmy*$rmy*$rmC + $rmc;
my $rm32=$rmy*$rmz*$rmC + $rmx*$rms;

my $rm13=$rmz*$rmx*$rmC + $rmy*$rms;
my $rm23=$rmy*$rmz*$rmC - $rmx*$rms;
my $rm33=$rmz*$rmz*$rmC + $rmc;

$rmvecx = vector($rm11,$rm12,$rm13);
$rmvecy = vector($rm21,$rm22,$rm23);
$rmvecz = vector($rm31,$rm32,$rm33);

# rotation matrix.
# Each of the three arguments to vector_matrix should be row vectors.
$rmat = vector_matrix( $rmvecx, $rmvecy, $rmvecz );

# transform the helix coordinates to align with the template helix
for ($i=0;$i<$num_allatoms;$i++) {
    my $scoord = vector($allatom_x[$i],$allatom_y[$i],$allatom_z[$i]);
    my $rcoord = $scoord * $rmat;
    $allatom_x[$i] = $rcoord . X;
    $allatom_y[$i] = $rcoord . Y;
    $allatom_z[$i] = $rcoord . Z;
}
for ($i=0;$i<$num_bbatoms;$i++) {
    my $scoord = vector($bbatom_x[$i],$bbatom_y[$i],$bbatom_z[$i]);
    my $rcoord = $scoord * $rmat;
    $bbatom_x[$i] = $rcoord . X;
    $bbatom_y[$i] = $rcoord . Y;
    $bbatom_z[$i] = $rcoord . Z;
}

# tranalate the aligned helix to the template's x,y,z 
for ($i=0;$i<$num_allatoms;$i++) {
    $allatom_y[$i] = $allatom_y[$i] + $thely;
    $allatom_x[$i] = $allatom_x[$i] + $thelx;
}
for ($i=0;$i<$num_bbatoms;$i++) {
    $bbatom_y[$i] = $bbatom_y[$i] + $thely;
    $bbatom_x[$i] = $bbatom_x[$i] + $thelx;
}

#for ($i = 0; $i < $num_bbatoms; $i++) {
#   print "$i $bbatom_mass[$i] $bbatom_x[$i] $bbatom_y[$i] $bbatom_z[$i]\n";
#}

writebgf_coord($inputbgf,$outputbgf,\@allatom_x,\@allatom_y,\@allatom_z);

undef @bbatom_x;
undef @bbatom_y;
undef @bbatom_z;
undef @allatom_x;
undef @allatom_y;
undef @allatom_z;

reset;

}

1;
