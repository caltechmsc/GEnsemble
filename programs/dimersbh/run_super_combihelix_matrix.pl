#!/usr/bin/perl

$bgf = @ARGV[0];
$mfta = @ARGV[1];
$totnum = @ARGV[2];
$numproc = @ARGV[3];
$ref = @ARGV[4];

if ($bgf eq "")
{die "run_super_combihelix_matrix.pl

Jenelle Bray (jenelle@wag), August 4, 2009

This program builds the best clusters from super_bihelix that sample eta, phi, theta and HPM values. After building, it minimizes the entire bundle for 10 steps. It orders the bundles by minimized mpsim energy. It runs on hive. To run it on borg or matrix, use run_super_combihelix_matrix.pl instead of run_super_combihelix.pl. On borg, building 1000 structures on 24 processors takes about 4 hours.

Program: /project/Biogroup/Software/GEnsemble/programs/superbihelix/run_super_combihelix.pl

Usage: run_super_combihelix.pl {bgf file} {mfta file} {# of bundles to build} {# of processors to use} {reference bgf}

Required files:

bgf file - A bgf file with absolute numbering and helices numbered from 1 to 7. The hydrophobic centers need to be aligned to the z axis in this structure. It has been found that using a bgf file with the terminis alanized works well for the superbihelix step, but the original dealanized structure is best for this combihelix step.

mfta file - The mfta file for the bgf structure. Make sure that you change the mfta file so that the correct starting and ending residues for each helix are in the first two columns.

Super_Bihelix_TotalE.out - The output file from super_bihelix that gives the best structures by total bihelical energy.

Options:

For the number of bundles to build, choose up to the number of structures that are in Super_Bihelix_TotalE.out, the output file from Super_BiHelix.

You must enter the number of processors to perform the calculation in parallel. Only choose the number of processors that are currently available.

The reference bgf file is a file for which each bundle that is built will be compared to, with backbone RMSD. This is an optional input. The default reference structure is the original bgf file.

Output:

Super_CombiHelix_TotalE.out - This gives the top structures by total mpsim energy of the bundle after 10 steps of minimization, as well as the their backbone RMSD to the reference bgf.

Example: run_super_bihelix.pl beta2.bgf beta2.mfta 1000 24 beta2-ref.bgf\n\n"}

if ($ref == "")
{$ref = $bgf;}

$fin = 0;
$jump = int($totnum/$numproc) + 1;
$top = ($numproc - 1)*$jump + 1;
$proc = $numproc;
if ($top > $totnum)
{
  $proc = $numproc - 1;
}

for ($i = 1; $i <= $proc; $i++)
{
  $num1 = ($i - 1)*$jump + 1;
  $num2 = $i*$jump;
  if ($i == $proc)
  {
    $num2 = $totnum;
    $fin = 1;
  }
  $dir = "super_combihelix_" . $i;
  system ("mkdir $dir");
  system ("cp $bgf $mfta Super_Bihelix_TotalE.out $dir");
  chdir($dir);
  $pbs = "super_combi_" . $i . ".pbs";
  open (PBS,">$pbs");
  print PBS "#PBS -l nodes=1,walltime=48:00:00\n";
  print PBS "#PBS -q workq\n";
  print PBS "#PBS -j oe\n";
  print PBS "#PBS -N super_combi_$i\n";
  print PBS "#PBS -m e\n";
  print PBS "#!/bin/csh\n\n";
  print PBS "cd \$PBS_O_WORKDIR\n\n";
  print PBS "echo the job started at ::: `date`\n\n";
  print PBS "/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_combihelix_matrix.pl $bgf $mfta $num1 $num2 $i $fin $ref\n\n";
  print PBS "echo the job ended at ::: `date`\n";
  close(PBS);
  system("qsub $pbs"); 
  chdir("..");
}

