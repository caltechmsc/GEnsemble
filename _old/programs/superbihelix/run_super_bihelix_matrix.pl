#!/usr/bin/perl

$bgf = @ARGV[0];
$mfta = @ARGV[1];
$nm = @ARGV[3];
$lst = @ARGV[2];

if ($bgf eq "")
{die "run_super_bihelix_matrix.pl

Jenelle Bray (jenelle@wag), August 4, 2009

This program samples eta, phi, and theta angles and HPM centers in a bgf bundle. It gives the total mpsim bihelical energy of the bundle after each bihelical pair has been minimized for 10 steps. Only the side chains are minimized. It takes 12 processors. On hive, it takes about 3 days when (# of eta angles sampled)*(# of theta angles sampled)*(# of phi angles sampled)*(# of HPM centers sampled) = 81 for one helix. To run it on borg or matrix, use run_super_bihelix_matrix.pl instead of run_super_bihelix.pl.

Program: /project/Biogroup/Software/GEnsemble/programs/superbihelix/run_super_bihelix.pl

Usage: run_super_bihelix.pl {bgf file} {mfta file} {number of ouput structures} {completeness level for analysis step}

Required files:

bgf file - A bgf file with absolute numbering and helices numbered from 1 to 7. The hydrophobic centers need to be aligned to the z axis in this structure. It has been found that alanizing the two residues on each end of each helix for this step gives the best results.

mfta file - The mfta file for the bgf structure. Make sure that you change your mfta file so that the correct starting and ending residues for each helix are in the first two columns.

angles.txt - The file with the changes in the eta, phi, theta angles to test, as well as different HPM centers to test. The angles.txt file should look like the file below for all seven helices:

TM1 eta -30 -15 0 15 30
TM1 HPM 49.77
TM1 phi -30 -15 0 15 30
TM1 theta 0 10 -10
TM2 eta -30 -15 0 15 30 
TM2 HPM 84.04
TM2 phi -30 -15 0 15 30
TM2 theta 0 10 -10

Please make sure there are no extra spaces at the end of each line. For the eta, phi and theta values, these are the changes in the angles to make to the original bgf structure. So, if the input bgf file has TM1 theta of x degrees, the program will sample x, x-15, x+15, x-30 and x+30. For HPM, these are just the values of the HPM centers to test. If you are not sampling HPM centers, do not put the HPM centers in the angles.txt file. If you do not include a degree of freedom, the program will just keep it the same as the input file. For example, if you would just like to sample the eta values, like the old bihelix, your angles.txt file would be:

TM1 eta -90 -75 -60 -45 -30 -15 0 15 30 45 60 75 90
TM2 eta -90 -75 -60 -45 -30 -15 0 15 30 45 60 75 90
TM3 eta -90 -75 -60 -45 -30 -15 0 15 30 45 60 75 90
TM4 eta -90 -75 -60 -45 -30 -15 0 15 30 45 60 75 90
TM5 eta -90 -75 -60 -45 -30 -15 0 15 30 45 60 75 90
TM6 eta -90 -75 -60 -45 -30 -15 0 15 30 45 60 75 90
TM7 eta -90 -75 -60 -45 -30 -15 0 15 30 45 60 75 90

Options:

Select the number of output structures that you would like. The default is 2000. These output structures will be used for the combihelix step.

For the completeness level of the analysis, select option 1 for 24 conformations of each helix to be tested in the analysis step, or 2 for 36 conformations of each helix to be tested in the analysis test. Option 2 is more complete, so is recommended, but option 1 will take less time. The default is option 2. If you would like to use option 1, you must also be sure to put the number of output structures that you would like.

Output:

Super_Bihelix_TotalE.out - This gives the top structures by total bihelical energy. This file will be used to build the full bundles when you run the combihelix step.

Super_Bihelix_HBondE.out - The top structures by total bihelical hydrogen bonding energy.

Super_Bihelix_InterHelE.out - The top structures by total bihelical interhelical energy.

Super_Bihelix_NoInterVDW.out - The top structures by total bihelical energy excluding interhelical VDW energies.

TM#_configs.out - The ranking of helical conformations for each helix, determined from the quadhelix bundles, that is subsequently used for the analysis.

Example: run_super_bihelix.pl beta2.bgf beta2.mfta 2500 2\n\n"}


if (! -e 'angles.txt')
{die "Could not find angles.txt \n"}

if (! -e $bgf)
{die "Could not find bgf file \n"}

if (! -e $mfta)
{die "Could not find mfta file \n"}

system ("/project/Biogroup/scripts/perl/bgf2pdb.pl $bgf > super.pdb");
system ("/project/Biogroup/Software/devel/GEnsemble2/programs/templates/OPM/GetTemplate.pl -m $mfta -p super.pdb >& template_test.out");
open(TEST,"<template_test.out");
@test = <TEST>;
close(TEST);
if ($test[0] !~ /1tmpl/)
{die "GetTemplate.pl failed, showing something is wrong with the mfta or bgf file.  Make sure you have aligned the hydrophobic centers in the bgf file to z=0 \n"}

if ($nm == "")
{$nm = 2;}

if ($lst == "")
{$lst = 2000;}

system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/fix_angles_file_matrix $bgf $mfta");
@tm1 = (1,1,2,2,2,3,3,3,3,4,5,6);
@tm2 = (2,7,3,4,7,4,5,6,7,5,6,7);

for ($i = 0; $i < 12; $i++)
{
  $dir = "super_bihelix_H" . $tm1[$i] . "_H" . $tm2[$i];
  system("mkdir $dir");
  system("cp $bgf $mfta angles.txt $dir");
  chdir($dir);
  $pbs = "super_bihelix_H" . $tm1[$i] . "_H" . $tm2[$i] . ".pbs";
  open(PBS,">$pbs");
  print PBS "#PBS -l nodes=1,walltime=168:00:00\n";
  print PBS "#PBS -j oe\n";
  print PBS "#PBS -N super_H$tm1[$i]_H$tm2[$i]\n";
  print PBS "#PBS -m e\n";
  print PBS "#PBS -S /bin/csh\n\n";
  print PBS "set SCRATCH = /temp1/\$USER/\$PBS_JOBID\n\n";
  print PBS "mkdir -p \$SCRATCH\n";
  print PBS "cd \$PBS_O_WORKDIR\n\n";
  print PBS "echo the job started at ::: `date`\n\n";
  print PBS "source /project/Biogroup/Software/GEnsemble/programs/superbihelix/super.csh\n\n";
  print PBS "/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_bihelix_pl_matrix.pl $bgf $mfta $tm1[$i] $tm2[$i] $nm $lst > \$SCRATCH/\${PBS_JOBNAME}.output\n\n";
  print PBS "echo the job ended at ::: `date`\n\n";
  print PBS "cp -p \$SCRATCH/\${PBS_JOBNAME}.output \$PBS_O_WORKDIR\n";
  print PBS "if (\$status != 0) then\n";
  print PBS "  echo \"Copying results from `hostname`:\$SCRATCH/\${PBS_JOBNAME}.output back to \$PBS_O_WORKDIR failed.\"\n";
  print PBS "  echo \"After fixing the problem be sure to manually remove the file `hostname`:\$SCRATCH/\${PBS_JOBNAME}.output\"\n";
  print PBS "else\n";
  print PBS "  cd \$PBS_O_WORKDIR\n";
  print PBS "  rm -rf \$SCRATCH\n";
  print PBS "endif\n";
  close(PBS);
  system("qsub $pbs"); 
  chdir(".."); 
}
 
