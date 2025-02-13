#!/usr/bin/perl

use Cwd;

$bgf = @ARGV[0];
$mfta = @ARGV[1];
$numproc = @ARGV[2];
$ref = @ARGV[3];
$file = @ARGV[4];
$range = @ARGV[5];

if ($bgf eq "")
{die "run_super_sbhrank.pl

Bartosz Trzaskowski (trzask@wag), May 22, 2010

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

if ($range =~ m/-/){
                   @split_range = split("-", $range);
                   $start_range = $split_range[0];
                   $end_range   = $split_range[1];
                   }
else {$start_range = $end_range = $range};

$totnum = $end_range - $start_range + 1;

$fin = 0;
$jump = int($totnum/$numproc) + 1;
$top = ($numproc - 1)*$jump + 1;
$proc = $numproc;
if ($top > $totnum)
{
  $proc = $numproc - 1;
}

### added ###

open(TOTIN,"<$file");
@lines = <TOTIN>;
close(TOTIN);

### add bihelix rank ###
$length_lines = scalar(@lines);
@lines2 = ();
$lines2[0] = $lines[0];
$lines2[1] = $lines[1];
@split_totin = split("_", $file);
@split_totin2 = split /\./, $split_totin[2];
$currank = $split_totin2[0]; 
$totin3 =  "Super_Bihelix_sbhrank_" . $split_totin2[0] . ".out";
open(TOTIN2,">$totin3");
print TOTIN2 $lines2[0];
print TOTIN2 $lines2[1];
for ($i = $start_range+1; $i < $end_range+2; $i++){
                                        $lines2[$i] = $lines[$i];
                                        print TOTIN2 $lines2[$i];
                                        }
close TOTIN2;
### END ###

for ($i = 1; $i <= $proc; $i++)
{
  $num1 = ($i - 1)*$jump + 1;
  $num2 = $i*$jump;
  if ($i == $proc)
  {
    $num2 = $totnum;
    $fin = 1;
  }
  $dir = "super_sbhrank_" . $split_totin2[0] . "_" . $i;
  system ("mkdir $dir");
  system ("cp $bgf $mfta $totin3 $dir");
  chdir($dir);
  $pbs = "super_sbhrank_$currank" . "_" . $i . ".pbs";
  open (PBS,">$pbs");
  print PBS "#PBS -l nodes=1,walltime=100:00:00\n";
  print PBS "#PBS -q workq\n";
  print PBS "#PBS -j oe\n";
  print PBS "#PBS -N sbhrank_$split_totin2[0]" . "_" . "$i\n";
  print PBS "#PBS -m e\n";
  print PBS "#!/bin/csh\n\n";
  print PBS "cd \$PBS_O_WORKDIR\n\n";
  print PBS "echo the job started at ::: `date`\n\n";
  print PBS "/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_sbhrank_n.pl $bgf $mfta $num1 $num2 $i $fin $ref $totin3\n\n";
  print PBS "echo the job ended at ::: `date`\n";
  close(PBS);
  $curdir = cwd();

# chek whereami #
system("hostname > hostname");
open(HOSTNAME,"<hostname");
@line = <HOSTNAME>;
close(HOSTNAME);

if ($line[0] =~ m/-/){
                     @split_line = split("-", $line[0]);
                     if ($split_line[0] eq "node"){$machine = "hive";}
                  elsif ($split_line[0] eq "node6"){$machine = "matrix";}
                  elsif ($split_line[0] eq "node5"){$machine = "matrix";}
                  elsif ($split_line[0] eq "node4"){$machine = "borg";}
                  elsif ($split_line[0] eq "node3"){$machine = "borg";}
                  elsif ($split_line[0] eq "node2"){$machine = "borg";}
                   else {$machine = "hive";}
                     }
else {
     @split_line = split(/\./, $line[0]);
     if ($split_line[0] eq "hive"){$machine = "hive";}
  elsif ($split_line[0] eq "matrix\n"){$machine = "matrix";}
  elsif ($split_line[0] eq "borg\n"){$machine = "borg";}
   else {$machine = "hive";}
     }
unlink("hostname");

# END OF check #

  system("ssh $machine \"cd $curdir;qsub $pbs\""); 
  chdir("..");
}

