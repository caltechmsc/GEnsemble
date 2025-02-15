#!/usr/bin/perl

use List::Util qw(max);
use Math::Trig;

$bgf = @ARGV[0];
$mfta = @ARGV[1];
$angl = @ARGV[2];

if ($bgf eq "")
{die "run_angles_local2abs.pl

Ravi Abrol (abrol\@wag), 16 Sept 2014

Program: /project/Biogroup/Software/GEnsemble/programs/superbihelix/run_angles_local2abs.pl

Usage: run_angles_local2abs.pl {bgf file} {mfta file} {local angles file}

Required files:

bgf file - A bgf file with absolute numbering and helices numbered from 1 to 7.
The hydrophobic centers need to be aligned to the z axis in this structure.
It has been found that alanizing the two residues on each end of each helix for
this step gives the best results.

mfta file - The mfta file for the bgf structure. Make sure that you change your
mfta file so that the correct starting and ending residues for each helix are
in the first two columns.

Conditional files:

If the angles_local.txt file is not specified, then the script will print
the template of the input bgf file in absolute coordinate system and exit.
This can help you decide (based on Theta values) what phi_grid values
to use, if you don't want the script to chose them for you.

angles_local.txt - The file with the local changes in theta, phi, and eta
angles. The angles_local.txt file should look like the file below, but with
entries for all seven helices:

TM1 theta_grid 10 2
TM1 phi_grid 30
TM1 eta -30 -15 0 15 30
TM2 theta_grid 10 2
TM2 phi_grid 30
TM2 eta -30 -15 0 15 30

In this example angles_local.txt file,
theta_grid entry of \"10 2\" means that 2 non-zero theta_local values will be
sampled on a 10deg grid. So, theta_local will sample 0 deg, 10deg, and 20deg.
phi_grid entry of \"30\" means that for non-zero theta_local, phi_local will
sample the full 2*pi range on a 30deg grid. So, phi_local will sample:
0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330.
If phi_grid is not specified, then it will be automatically chosen based
on theta_local. Smaller theta_local needs bigger strides in phi_local and vice
versa. 
If theta_local ~  7.5deg, phi_grid = 120deg ( 3 values).
If theta_local ~ 10.0deg, phi_grid =  90deg ( 4 values).
If theta_local ~ 15.0deg, phi_grid =  60deg ( 6 values).
If theta_local ~ 22.5deg, phi_grid =  40deg ( 9 values).
If theta_local ~ 30.0deg, phi_grid =  30deg (12 values).
If theta_local ~ 45.0deg, phi_grid =  20deg (18 values).
If theta_local ~ 60.0deg, phi_grid =  15deg (24 values).
If theta_local ~ 90.0deg, phi_grid =  10deg (36 values).

Please make sure there are no extra spaces at the end of each line.
For any HPM entries, these are just the values of the HPM centers to test.
If you are not sampling HPM centers, do not put the HPM centers in this file.

Output:

angles.txt file - This file should then be used for input for
run_super_bihelix.pl script.

Example: run_angles_local2abs.pl beta2.bgf beta2.mfta angles_local.txt\n\n"}

if (! -e $bgf)
{die "Could not find bgf file \n"}

if (! -e $mfta)
{die "Could not find mfta file \n"}

system ("/project/Biogroup/scripts/perl/bgf2pdb.pl $bgf > super.pdb");
system ("/project/Biogroup/Software/devel/GEnsemble2/programs/templates/OPM/GetTemplate.pl -m $mfta -p super.pdb >& template_test.out");
open(TDEF,"<template_test.out");
@tmplf = <TDEF>;
close(TDEF);
if ($tmplf[0] !~ /1tmpl/)
{die "GetTemplate.pl failed, showing something is wrong with the mfta or bgf file.  Make sure you have aligned the hydrophobic centers in the bgf file to z=0 \n"} 
if (! -e $angl)
{print "\n@tmplf\n";
die "\n"}

#
$pi=3.14159265359;
$rad=$pi/180;
#
foreach $line (@tmplf) {
    chomp $line;
    if ($line =~ /1tmpl/) {
        @tdef=split(/\s+/,$line);
#       print "$tdef[5]\n";
        $t_abs[1]=$tdef[5];
        $p_abs[1]=$tdef[6];
    } elsif ($line =~ /2tmpl/) {
        @tdef=split(/\s+/,$line); 
        $t_abs[2]=$tdef[5];
        $p_abs[2]=$tdef[6];
    } elsif ($line =~ /3tmpl/) {
        @tdef=split(/\s+/,$line); 
        $t_abs[3]=$tdef[5];
        $p_abs[3]=$tdef[6];
    } elsif ($line =~ /4tmpl/) {
        @tdef=split(/\s+/,$line); 
        $t_abs[4]=$tdef[5];
        $p_abs[4]=$tdef[6];
    } elsif ($line =~ /5tmpl/) {
        @tdef=split(/\s+/,$line); 
        $t_abs[5]=$tdef[5];
        $p_abs[5]=$tdef[6];
    } elsif ($line =~ /6tmpl/) {
        @tdef=split(/\s+/,$line); 
        $t_abs[6]=$tdef[5];
        $p_abs[6]=$tdef[6];
    } elsif ($line =~ /7tmpl/) {
        @tdef=split(/\s+/,$line); 
        $t_abs[7]=$tdef[5];
        $p_abs[7]=$tdef[6];
    }
}

open(ANGL,"<$angl");
@anglf = <ANGL>;
close(ANGL);

#phi
foreach $line (@anglf) {
    chomp $line;
    @adef=split(/\s+/,$line);
    if ($line =~ /phi_grid/) {
       $tm=substr($adef[0],2,1);
       $phi_local_delta=$adef[2];
       $rem=360%$phi_local_delta;
       if ($rem != 0) {
          die "phi_grid not evenly able to cover full 360deg for TM $tm\n";
       } else {
          $phi_local_ngrid=360/$phi_local_delta;
          for ($k=0; $k < $phi_local_ngrid; $k++) {
              $p_local[$tm,$k]=$k*$phi_local_delta;
          }
       }
    }
}

#theta
foreach $line (@anglf) {
    chomp $line;
    @adef=split(/\s+/,$line);
    if ($line =~ /theta_grid/) {
       $tm=substr($adef[0],2,1);
       $theta_local_delta=$adef[2];
       $theta_local_ngrid=$adef[3];
       for ($j=0; $j < $theta_local_ngrid; $j++) {
           $t_local[$tm,$j]=$theta_local_delta*($j+1);
       $t_localmax = $t_local[$tm,$j]; 
       }
       if (not defined($phi_local_delta) ) {
          if ($t_localmax <= 8.75) {
             $phi_local_delta=120.0; $phi_local_ngrid=3; }
          if ($t_localmax > 8.75 and $t_localmax <= 12.5) {
             $phi_local_delta=90.0; $phi_local_ngrid=4; }
          if ($t_localmax > 12.5 and $t_localmax <= 18.75) {
             $phi_local_delta=60.0; $phi_local_ngrid=6; }
          if ($t_localmax > 18.75 and $t_localmax <= 26.25) {
             $phi_local_delta=40.0; $phi_local_ngrid=9; }
          if ($t_localmax > 26.25 and $t_localmax <= 37.5) {
             $phi_local_delta=30.0; $phi_local_ngrid=12; }
          if ($t_localmax > 37.5 and $t_localmax <= 52.5) {
             $phi_local_delta=20.0; $phi_local_ngrid=18; }
          if ($t_localmax > 52.5 and $t_localmax <= 75.0) {
             $phi_local_delta=15.0; $phi_local_ngrid=24; }
          if ($t_localmax > 75.0) {
             $phi_local_delta=10.0; $phi_local_ngrid=36; }
          for ($k=0; $k < $phi_local_ngrid; $k++) {
              $p_local[$tm,$k]=$k*$phi_local_delta;
          }
       }
    } 
}

#eta/HPM
foreach $line (@anglf) {
    chomp $line;
    @adef=split(/\s+/,$line);
    $tm=substr($adef[0],2,1);
    if ($line =~ /eta/) {
       $etaline[$tm]=$line;
    }
    if ($line =~ /HPM/) {
       $hpmline[$tm]=$line;
    }
}

for ($tm=1; $tm <= 7; $tm++) {
    $tm_str="TM".$tm;
    $theta_str=$tm_str." theta 0.00";
    $phi_str=$tm_str." phi 0.00";
#   print "t_abs, p_abs: $t_abs[$tm],$p_abs[$tm]\n";
    $sinta=sin($t_abs[$tm]*$rad);
    $costa=cos($t_abs[$tm]*$rad);
    $sinpa=sin($p_abs[$tm]*$rad);
    $cospa=cos($p_abs[$tm]*$rad);
    
    for ($j=0; $j < $theta_local_ngrid; $j++) {
        $thel=$t_local[$tm,$j]*$rad;
        for ($k=0; $k < $phi_local_ngrid; $k++) {
            $phil=$p_local[$tm,$k]*$rad;
#           print "thel,phil: $thel $phil\n";
#
            $xp=sin($thel)*cos($phil);
            $yp=sin($thel)*sin($phil);
            $zp=cos($thel);
#
            $xa=($xp*$costa*$cospa)-($yp*$sinpa)+($zp*$sinta*$cospa);
            $ya=($xp*$costa*$sinpa)+($yp*$cospa)+($zp*$sinta*$sinpa);
            $za=-($xp*$sinta)+($zp*$costa);
#           print "xa,ya,za: $xa,$ya,$za\n";
#
            $thea=(acos($za)-($t_abs[$tm]*$rad))/$rad;
            $phia=(atan2($ya,$xa)-($p_abs[$tm]*$rad))/$rad;
            if ($phia < -179.9) {$phia=360+$phia;}
            $theta_str=sprintf("$theta_str %.2f", $thea);
            $phi_str=sprintf("$phi_str %.2f", $phia);
         }
     }
     print "$theta_str\n";
     print "$phi_str\n";
     if (defined $etaline[$tm]) { print "$etaline[$tm]\n"; }
     if (defined $hpmline[$tm]) { print "$hpmline[$tm]\n"; }
}
