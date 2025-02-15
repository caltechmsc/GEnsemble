package Modules::Align2z;

use strict;
use warnings;
use Math::Complex;
use Math::Trig;
use POSIX qw(ceil floor);
use myMath::VectorReal qw(:all);
use myMath::MatrixReal qw(:all);

our $VERSION = '1.00';

use base 'Exporter';

our @EXPORT = qw(Align2z);

# define the function

sub Align2z {

my ($num_allatoms,$allatom_x_ref,$allatom_y_ref,$allatom_z_ref,$num_bbatoms,$bbatom_x_ref,$bbatom_y_ref,$bbatom_z_ref,$helixid,$nter,$zout,$eigx,$eigy,$eigz,$helz0x,$helz0y) = @_;

my $halfpi = pi/2;
my $twopi = 2*pi;

my ($i,$j);

my @allatom_x=();
my @allatom_y=();
my @allatom_z=();
@allatom_x=@{$allatom_x_ref};
@allatom_y=@{$allatom_y_ref};
@allatom_z=@{$allatom_z_ref};

my @bbatom_x=();
my @bbatom_y=();
my @bbatom_z=();
@bbatom_x=@{$bbatom_x_ref};
@bbatom_y=@{$bbatom_y_ref};
@bbatom_z=@{$bbatom_z_ref};

my $helvecx = 0.0;
my $helvecy = 0.0;
my $helvecz = 1.0;
#  +z for odd helices and -z for even helices if nter is out and zout is plus
#  -z for odd helices and +z for even helices if nter is in and zout in plus
#  ...
#  ...
if (($nter eq 'out' and $zout eq 'plus') or ($nter eq 'in' and $zout eq 'minus')) {
  if ($helixid % 2) {
    if ($eigz > 0.0) { $eigz = -$eigz; $eigy = -$eigy; $eigx = -$eigx;}
    $helvecz = -1.0;
  } else {
    if ($eigz < 0.0) { $eigz = -$eigz; $eigy = -$eigy; $eigx = -$eigx; }
  }
} elsif (($nter eq 'out' and $zout eq 'minus') or ($nter eq 'in' and $zout eq 'plus')) {
  if ($helixid % 2) {
    if ($eigz < 0.0) { $eigz = -$eigz; $eigy = -$eigy; $eigx = -$eigx; }
  } else {
    if ($eigz > 0.0) { $eigz = -$eigz; $eigy = -$eigy; $eigx = -$eigx; }
    $helvecz = -1.0;
  }
}

# unit vector of the input helix axis at origin
my $ihelvec = vector($eigx,$eigy,$eigz);
my $normihel = sqrt($eigx**2 + $eigy**2 + $eigz**2);

# unit vector of the z-axis
my $thelvec = vector($helvecx,$helvecy,$helvecz);
my $normthel = sqrt($helvecx**2 + $helvecy**2 + $helvecz**2);


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

#if ($helixid == 3) {print "normi,normz,normn= $normihel,$normthel,$normnorm\n";}

# angle between the input and +z axis is
my $anghels = acos($thelvec . $ihelvec);
my $anghelsd = rad2deg($anghels);
my $pival = pi;
my $anghelsd2 = $anghels*180.0/pi;

# rotation matrix construction that will rotate the input helix axis vector
# to align with the z-axis
my $rmc = $thelvec . $ihelvec;
my $rms = sin($anghels);
my $rmC = 1.0 - $rmc;
my $rmx = $normvecx;
my $rmy = $normvecy;
my $rmz = $normvecz;

my $rm11 = $rmx*$rmx*$rmC + $rmc;
my $rm21 = $rmx*$rmy*$rmC + $rmz*$rms;
my $rm31 = $rmz*$rmx*$rmC - $rmy*$rms;

my $rm12 = $rmx*$rmy*$rmC - $rmz*$rms;
my $rm22 = $rmy*$rmy*$rmC + $rmc;
my $rm32 = $rmy*$rmz*$rmC + $rmx*$rms;

my $rm13 = $rmz*$rmx*$rmC + $rmy*$rms;
my $rm23 = $rmy*$rmz*$rmC - $rmx*$rms;
my $rm33 = $rmz*$rmz*$rmC + $rmc;

my $rmvecx = vector($rm11,$rm12,$rm13);
my $rmvecy = vector($rm21,$rm22,$rm23);
my $rmvecz = vector($rm31,$rm32,$rm33);

# rotation matrix.
# Each of the three arguments to vector_matrix should be row vectors.
my $rmat = vector_matrix( $rmvecx, $rmvecy, $rmvecz );

for ($j=0;$j<$num_bbatoms;$j++) {
    my $scoord = vector($bbatom_x[$j]-$helz0x,$bbatom_y[$j]-$helz0y,$bbatom_z[$j]);
    my $rcoord = $scoord * $rmat;
    $bbatom_x[$j] = $rcoord . X + $helz0x;
    $bbatom_y[$j] = $rcoord . Y + $helz0y;
    $bbatom_z[$j] = $rcoord . Z;
}
for ($j=0;$j<$num_allatoms;$j++) {
    my $scoord = vector($allatom_x[$j]-$helz0x,$allatom_y[$j]-$helz0y,$allatom_z[$j]);
    my $rcoord = $scoord * $rmat;
    $allatom_x[$j] = $rcoord . X + $helz0x;
    $allatom_y[$j] = $rcoord . Y + $helz0y;
    $allatom_z[$j] = $rcoord . Z;
}

return (\@allatom_x,\@allatom_y,\@allatom_z,\@bbatom_x,\@bbatom_y,\@bbatom_z);

@bbatom_x =();
@bbatom_y =();
@bbatom_z =();

reset;

}

1;
