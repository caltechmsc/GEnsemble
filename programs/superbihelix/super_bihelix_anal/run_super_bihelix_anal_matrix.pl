#!/usr/bin/perl

$lst = @ARGV[0];
$nm = @ARGV[1];
$numba = @ARGV[2]; 

if (! -e 'angles.txt')
{die "Could not find angles.txt \n"}

system("rm -f Interhelical_Energy_* Consensus* Interhelical_Hbond_* No_Interhelical_VDW_* Total_Energy_*");

if ($lst eq "")
{die "run_super_bihelix_anal_matrix.pl

Jenelle Bray (jenelle), August 4, 2009

This is a program to run the SuperBiHelix? analysis standalone. It is automatically run in run_super_bihelix.pl, but one may want to run the analysis over again with different options. This program only runs on hive. To run it on borg or matrix, use run_super_bihelix_anal_matrix.pl instead of run_super_bihelix_anal.pl. Be forewarned that it will overwrite the Super_Bihelix_TotalE.out file from a previous analysis run.

Program: /project/Biogroup/Software/GEnsemble/programs/superbihelix/super_bihelix_anal/run_super_bihelix_anal.pl

Usage run_super_bihelix_anal.pl {number of output structures} {completeness level for analysis} {number of structures from each quadhelix bundle used to determine helical conformations for final analysis}

Required files:

This needs to be run in a directory that that contains the super_bihelix_H#_H# directories.

The directory must also include the angles.txt file that was used to run super_bihelix.

Options:

The number of output structures is the number that will be in the output file Super_Bihelix_TotalE.out, which is subsequently used for super_combihelix. A suggested value is 2000.

For the completeness level of the analysis, select option 1 for 24 conformations of each helix to be tested in the analysis step, or 2 for 36 conformations, or 3 for 48 conformations. Option 2 is the default. Option 3 will take significantly more time than option 2. Option 1 will be much faster, but is less complete.

The number of structures structures from each quadhelix bundle that are used determine the helical conformations for the final bihelical analysis can be specified. The default is 2000 structures from each quadhelix bundle (the bundles are the 1-2-3-7 bundle, the 2-3-4-5 bundle and the 3-5-6-7 bundle).

Output:

Super_Bihelix_TotalE.out - This gives the top structures by total bihelical energy. This file will be used to build the full bundles when you run the combihelix step.

Super_Bihelix_HBondE.out - The top structures by total bihelical hydrogen bonding energy.

Super_Bihelix_InterHelE.out - The top structures by total bihelical interhelical energy.

Super_Bihelix_NoInterVDW.out - The top structures by total bihelical energy excluding interhelical VDW energies.

TM#_configs.out - The ranking of helical conformations for each helix, determined from the quadhelix bundles, that is subsequently used for the analysis.

Example: run_super_bihelix_anal.pl 5000 3 3000\n\n"}

if ($nm == "")
{$nm = 2;}

if ($numba == "")
{$numba = 2000;}

@tm1 = (1,1,2,2,2,3,3,3,3,4,5,6);
@tm2 = (2,7,3,4,7,4,5,6,7,5,6,7);

for ($i = 0; $i < 12; $i++)
{
  $pbs = "super_bihelix_anal_" . $i . ".pbs";
  open(PBS,">$pbs");
  print PBS "#PBS -l nodes=1,walltime=400:00:00\n";
  print PBS "#PBS -j oe\n";
  print PBS "#PBS -N super_bihelix_anal_$i \n";
  print PBS "#PBS -m e\n";
  print PBS "#PBS -S /bin/csh\n\n";
  print PBS "set SCRATCH = /temp1/\$USER/\$PBS_JOBID\n\n";
  print PBS "mkdir -p \$SCRATCH\n";
  print PBS "cd \$PBS_O_WORKDIR\n\n";
  print PBS "echo the job started at ::: `date`\n\n";
  print PBS "/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_bihelix_anal/super_bihelix_anal_matrix.pl $tm1[$i] $tm2[$i] $nm $lst $numba > \$SCRATCH/\${PBS_JOBNAME}.output\n\n";
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
}
 
