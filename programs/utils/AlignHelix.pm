package utils::AlignHelix;

use strict;
use warnings;
use Math::Complex;
use Math::Trig;
use POSIX qw(ceil floor);
use myMath::VectorReal qw(:all);
use myMath::MatrixReal qw(:all);

use inout::readbgf_coord;
use inout::writebgf_coord;
use utils::MomOfInertiaAxes;
 
our $VERSION = '1.00';

use base 'Exporter';

our @EXPORT = qw(AlignHelix);

# define the function

sub AlignHelix {

my ($helixid,$inputbgf,$helixhpc,$thelx,$thely,$thelz,$theltheta,$thelphi,$theleta) = @_;

my $pi = 3.14159265359;
my $outputbgf = "aligned_helix".$helixid.".bgf";

my $i = 0;

my ($num_allatoms,$allatom_x_ref,$allatom_y_ref,$allatom_z_ref,$num_bbatoms,$bbatom_mass_ref,$bbatom_x_ref,$bbatom_y_ref,$bbatom_z_ref,$hpcanchor1,$hpcanchor2) = readbgf_coord($inputbgf,$helixhpc);

my @allatom_x=@$allatom_x_ref;
my @allatom_y=@$allatom_y_ref;
my @allatom_z=@$allatom_z_ref;

my @bbatom_mass=@$bbatom_mass_ref;
my @bbatom_x=@$bbatom_x_ref;
my @bbatom_y=@$bbatom_y_ref;
my @bbatom_z=@$bbatom_z_ref;

my $helxlen = $bbatom_x[$num_bbatoms-1] - $bbatom_x[0];
my $helylen = $bbatom_y[$num_bbatoms-1] - $bbatom_y[0];
my $helzlen = $bbatom_z[$num_bbatoms-1] - $bbatom_z[0];
my $helrlen = sqrt($helxlen*$helxlen + $helylen*$helylen + $helzlen*$helzlen);


# Get the helix axis as the lowest moment of inertia vector
my ($xcom,$ycom,$zcom,$eigx,$eigy,$eigz) = MomOfInertiaAxes($num_bbatoms,\@bbatom_mass,\@bbatom_x,\@bbatom_y,\@bbatom_z);

# Flip the helix axis vector and the helix itself to make sure
# that odd numbered helices have N-terminus in +z space
# and even numbered helices have N-terminus in -z space 
# Also translate the helix to have its center of mass coincide with origin.
if ($helixid % 2) {
    if ($eigz < 0.0) {
        $eigz = -$eigz;
        $eigy = -$eigy;
        $eigx = -$eigx;
    }
    if ($allatom_z[0] < 0.0) {
        for ($i=0;$i<$num_allatoms;$i++) {
            $allatom_z[$i] = -$allatom_z[$i] + $zcom;
            $allatom_y[$i] = -$allatom_y[$i] + $ycom;
            $allatom_x[$i] = -$allatom_x[$i] + $xcom;
        }
        for ($i=0;$i<$num_bbatoms;$i++) {
            $bbatom_z[$i] = -$bbatom_z[$i] + $zcom;
            $bbatom_y[$i] = -$bbatom_y[$i] + $ycom;
            $bbatom_x[$i] = -$bbatom_x[$i] + $xcom;
        }
    } else {
        for ($i=0;$i<$num_allatoms;$i++) {
            $allatom_z[$i] = $allatom_z[$i] - $zcom;
            $allatom_y[$i] = $allatom_y[$i] - $ycom;
            $allatom_x[$i] = $allatom_x[$i] - $xcom;
        }
        for ($i=0;$i<$num_bbatoms;$i++) {
            $bbatom_z[$i] = $bbatom_z[$i] - $zcom;
            $bbatom_y[$i] = $bbatom_y[$i] - $ycom;
            $bbatom_x[$i] = $bbatom_x[$i] - $xcom;
        }
    }
} else {
    if ($eigz > 0.0) {
        $eigz = -$eigz;
        $eigy = -$eigy;
        $eigx = -$eigx;
    }
    if ($allatom_z[0] > 0.0) {
        for ($i=0;$i<$num_allatoms;$i++) {
            $allatom_z[$i] = -$allatom_z[$i] + $zcom;
            $allatom_y[$i] = -$allatom_y[$i] + $ycom;
            $allatom_x[$i] = -$allatom_x[$i] + $xcom;
        }
        for ($i=0;$i<$num_bbatoms;$i++) {
            $bbatom_z[$i] = -$bbatom_z[$i] + $zcom;
            $bbatom_y[$i] = -$bbatom_y[$i] + $ycom;
            $bbatom_x[$i] = -$bbatom_x[$i] + $xcom;
        }
    } else {
        for ($i=0;$i<$num_allatoms;$i++) {
            $allatom_z[$i] = $allatom_z[$i] - $zcom;
            $allatom_y[$i] = $allatom_y[$i] - $ycom;
            $allatom_x[$i] = $allatom_x[$i] - $xcom;
        }
        for ($i=0;$i<$num_bbatoms;$i++) {
            $bbatom_z[$i] = $bbatom_z[$i] - $zcom;
            $bbatom_y[$i] = $bbatom_y[$i] - $ycom;
            $bbatom_x[$i] = $bbatom_x[$i] - $xcom;
        }
    }
}

## align the helix vector along the z-axis
## +z for odd helices and -z for even helices

my $thelvecx = 0.0;
my $thelvecy = 0.0;
my $thelvecz = 0.0;
if ($helixid % 2) {
# unit vector of the +z axis
    $thelvecz = 1.0;
} else {
# unit vector of the -z axis
    $thelvecz = -1.0;
}
my $thelvec = vector($thelvecx,$thelvecy,$thelvecz);

# unit vector of the input helix axis at origin
my $ihelvec = vector($eigx,$eigy,$eigz);

# unit vector perpendicular to the input and template helix axis vectors
my $normvec = vector(0.0,0.0,0.0);
$normvec = $thelvec x $ihelvec;

# angle between the input and +z axis is
my $anghels = acos($thelvec . $ihelvec)*180.0/$pi;

# rotation matrix construction that will rotate the input helix axis vector
# to align with the template helix axis vector
my $rmc = cos($anghels*$pi/180.0);
my $rms = sin($anghels*$pi/180.0);
my $rmC = 1.0-$rmc;
my $rmx = $normvec . X;
my $rmy = $normvec . Y;
my $rmz = $normvec . Z;

my $rm11=$rmx*$rmx*$rmC + $rmc;
my $rm21=$rmx*$rmy*$rmC + $rmz*$rms;
my $rm31=$rmz*$rmx*$rmC - $rmy*$rms;

my $rm12=$rmx*$rmy*$rmC - $rmz*$rms;
my $rm22=$rmy*$rmy*$rmC + $rmc;
my $rm32=$rmy*$rmz*$rmC + $rmx*$rms;

my $rm13=$rmz*$rmx*$rmC + $rmy*$rms;
my $rm23=$rmy*$rmz*$rmC - $rmx*$rms;
my $rm33=$rmz*$rmz*$rmC + $rmc;

my $rmvecx = vector($rm11,$rm12,$rm13);
my $rmvecy = vector($rm21,$rm22,$rm23);
my $rmvecz = vector($rm31,$rm32,$rm33);

# rotation matrix.
# Each of the three arguments to vector_matrix should be row vectors.
my $rmat = vector_matrix( $rmvecx, $rmvecy, $rmvecz );

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

## align the helix vector which is currently along the z-axis
## along the template helix vector

# unit vector of the input helix axis at origin currently along z-axis
$ihelvec = $thelvec;

if ( ($helixid+1)%2 ) {
    $theltheta = 180.0 - $theltheta;
}

# unit vector of the template helix axis at origin
$thelvecx = sin($theltheta*$pi/180.0)*cos($thelphi*$pi/180.0);
$thelvecy = sin($theltheta*$pi/180.0)*sin($thelphi*$pi/180.0);
$thelvecz = cos($theltheta*$pi/180.0);
$thelvec = vector($thelvecx,$thelvecy,$thelvecz);

# unit vector perpendicular to the input and template helix axis vectors
$normvec = $thelvec x $ihelvec;

# angle between the input and template helix axis vectors
$anghels = acos($thelvec . $ihelvec)*180.0/$pi;

# rotation matrix construction that will rotate the input helix axis vector
# to align with the template helix axis vector
$rmc = cos($anghels*$pi/180.0);
$rms = sin($anghels*$pi/180.0);
$rmC = 1.0-$rmc;
$rmx = $normvec . X;
$rmy = $normvec . Y;
$rmz = $normvec . Z;

$rm11=$rmx*$rmx*$rmC + $rmc;
$rm21=$rmx*$rmy*$rmC + $rmz*$rms;
$rm31=$rmz*$rmx*$rmC - $rmy*$rms;

$rm12=$rmx*$rmy*$rmC - $rmz*$rms;
$rm22=$rmy*$rmy*$rmC + $rmc;
$rm32=$rmy*$rmz*$rmC + $rmx*$rms;

$rm13=$rmz*$rmx*$rmC + $rmy*$rms;
$rm23=$rmy*$rmz*$rmC - $rmx*$rms;
$rm33=$rmz*$rmz*$rmC + $rmc;

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
    $allatom_z[$i] = $allatom_z[$i] + $thelz;
    $allatom_y[$i] = $allatom_y[$i] + $thely;
    $allatom_x[$i] = $allatom_x[$i] + $thelx;
}
for ($i=0;$i<$num_bbatoms;$i++) {
    $bbatom_z[$i] = $bbatom_z[$i] + $thelz;
    $bbatom_y[$i] = $bbatom_y[$i] + $thely;
    $bbatom_x[$i] = $bbatom_x[$i] + $thelx;
}

#for ($i = 0; $i < $num_bbatoms; $i++) {
#   print "$i $bbatom_mass[$i] $bbatom_x[$i] $bbatom_y[$i] $bbatom_z[$i]\n";
#}

writebgf_coord($inputbgf,$outputbgf,\@allatom_x,\@allatom_y,\@allatom_z);

print "aligned helix $helixid\n";
undef @bbatom_x;
undef @bbatom_y;
undef @bbatom_z;
undef @allatom_x;
undef @allatom_y;
undef @allatom_z;

reset;

}

1;
