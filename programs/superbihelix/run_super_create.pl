#!/usr/bin/perl

use Cwd;
use Getopt::Long;

GetOptions ('h|help'         => \$help,
            'b|bgf=s'        => \$bgf,
            'm|mfta=s'       => \$mfta,
            'range=s'        => \$range,
            'i|input=s'      => \$file,
            'ppn=i'          => \$numproc,
            );


if ($bgf eq "")
{die "run_super_sbhrank.pl

Bartosz Trzaskowski (trzask@wag), May 22, 2010

Usage: run_super_create.pl -b {bgf} -m {mfta file} --range {range} -i {input} --ppn

"}


if (not defined $numproc){$numproc = 1;}

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
  $dir = "super_" . $split_totin2[0] . "_" . $i;
  system ("mkdir $dir");
  system ("cp $bgf $mfta $totin3 $dir");
  chdir($dir);
  $pbs = "super_$currank" . "_" . $i . ".pbs";
  open (PBS,">$pbs");
  print PBS "#PBS -l nodes=1,walltime=48:00:00\n";
  print PBS "#PBS -q workq\n";
  print PBS "#PBS -j oe\n";
  print PBS "#PBS -N super_$split_totin2[0]" . "_" . "$i\n";
  print PBS "#PBS -m e\n";
  print PBS "#!/bin/csh\n\n";
  print PBS "cd \$PBS_O_WORKDIR\n\n";
  print PBS "echo the job started at ::: `date`\n\n";
  print PBS "/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_create.pl -b $bgf -m $mfta -n1 $num1 -n2 $num2 -p $i -f $fin -i $totin3\n\n";
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
  elsif ($split_line[0] eq "atom\n"){$machine = "atom";}
  elsif ($split_line[0] eq "ion\n"){$machine = "ion";}
   else {$machine = "hive";}
     }
unlink("hostname");

# END OF check #
  print "Submitting super_$split_totin2[0]" . "_" . "$i";
  system("ssh $machine \"cd $curdir;qsub $pbs\""); 
  chdir("..");
}

