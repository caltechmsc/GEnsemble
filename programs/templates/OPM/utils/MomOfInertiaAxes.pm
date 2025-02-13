package utils::MomOfInertiaAxes;

use strict;
use warnings;
use myMath::MatrixReal;
use myMath::MinMax;

our $VERSION = '1.00';

use base 'Exporter';

our @EXPORT = qw(MomOfInertiaAxes);

# define the function

sub MomOfInertiaAxes {

my ($num_bbatoms,$bbatom_mass_ref,$bbatom_x_ref,$bbatom_y_ref,$bbatom_z_ref) = @_;

my @m=@$bbatom_mass_ref;
my @x=@$bbatom_x_ref;
my @y=@$bbatom_y_ref;
my @z=@$bbatom_z_ref;

my @moim = ();

my $k = 0;

my $totm   = 0.0;
my $totmx  = 0.0;
my $totmy  = 0.0;
my $totmz  = 0.0;
my $totmxx = 0.0;
my $totmyy = 0.0;
my $totmzz = 0.0;
my $totmxy = 0.0;
my $totmxz = 0.0;
my $totmyz = 0.0;

for ($k = 0; $k < $num_bbatoms; $k++) {

    $totm   = $totm   + $m[$k];
    $totmx  = $totmx  + $m[$k]*$x[$k];
    $totmy  = $totmy  + $m[$k]*$y[$k];
    $totmz  = $totmz  + $m[$k]*$z[$k];
    $totmxx = $totmxx + $m[$k]*$x[$k]*$x[$k];
    $totmyy = $totmyy + $m[$k]*$y[$k]*$y[$k];
    $totmzz = $totmzz + $m[$k]*$z[$k]*$z[$k];
    $totmxy = $totmxy + $m[$k]*$x[$k]*$y[$k];
    $totmxz = $totmxz + $m[$k]*$x[$k]*$z[$k];
    $totmyz = $totmyz + $m[$k]*$y[$k]*$z[$k];

}

my $xcom = $totmx/$totm;
my $ycom = $totmy/$totm;
my $zcom = $totmz/$totm;

$moim[1][1] = $totmyy + $totmzz - ($ycom*$ycom + $zcom*$zcom)*$totm;
$moim[2][1] = -$totmxy + $xcom*$ycom*$totm;
$moim[3][1] = -$totmxz + $xcom*$zcom*$totm;

$moim[1][2] = $moim[2][1];
$moim[2][2] = $totmxx + $totmzz - ($xcom*$xcom + $zcom*$zcom)*$totm;
$moim[3][2] = -$totmyz + $ycom*$zcom*$totm;

$moim[1][3] = $moim[3][1];
$moim[2][3] = $moim[3][2];
$moim[3][3] = $totmxx + $totmyy - ($xcom*$xcom + $ycom*$ycom)*$totm;

#print "$moim[1][1] $moim[1][2] $moim[1][3]\n";
#print "$moim[2][1] $moim[2][2] $moim[2][3]\n";
#print "$moim[3][1] $moim[3][2] $moim[3][3]\n";

my $matrix = myMath::MatrixReal->new_from_cols( [ [$moim[1][1],$moim[2][1],$moim[3][1]], [$moim[1][2],$moim[2][2],$moim[3][2]], [$moim[1][3],$moim[2][3],$moim[3][3]] ] );

my ($l, $V) = $matrix->sym_diagonalize();

#print "$l\n";
#print "$V\n";

my $i = 0;
my $j = 0;
my @eigval = ();
my @eigvec = ();
for ($i = 1; $i <= 3; $i++) {
    $eigval[$i-1]=$l->element($i,1);
    for ($j = 1; $j <= 3; $j++) {
        $eigvec[$j-1][$i-1] = $V->element($j,$i);
    }
}

#print "$eigval[0]   $eigvec[0][0] $eigvec[1][0] $eigvec[2][0]\n";
#print "$eigval[1]   $eigvec[0][1] $eigvec[1][1] $eigvec[2][1]\n";
#print "$eigval[2]   $eigvec[0][2] $eigvec[1][2] $eigvec[2][2]\n";

#print "$xcom  $ycom  $zcom\n";

#my ($minindex, $minvalue) = argmin(@eigval);
my ($minindex, $minvalue) = argmin { $_ } @eigval;

#print "$minindex $minvalue\n";

my $eigx = $eigvec[0][$minindex];
my $eigy = $eigvec[1][$minindex];
my $eigz = $eigvec[2][$minindex];

return ($xcom,$ycom,$zcom,$eigx,$eigy,$eigz);
}

1;
