#!/usr/bin/perl

use Cwd;
use Getopt::Long;

#if (@ARGV == 0) { help(); }

GetOptions ('h|help'        => \$help,
            'b|bgf=s'       => \$bgf,
            'm|mfta=s'      => \$mfta,
            'n|number=i'    => \$totnum,
            'p|proc=i'      => \$numproc,
            'r|ref=s'       => \$ref,
            'bio|bioscratch=s'  => \$bio,
            'w|wall=i'      => \$walltime,
            'mach=s'        => \$machine,
            'i|input=s'     => \$totin,
            'neut=s'        => \$neut,
            );

if ($bgf eq "")
{die "run_super_combi_neutralize.pl

Jenelle Bray (jenelle@wag), August 4, 2009
Bartosz Trzaskowski (trzask@wag), May 22, 2010

This program builds the best clusters from super_bihelix that sample eta, phi, theta and HPM values. After building, it minimizes the entire bundle for 10 steps and neutralizes it. There are two modes in which this program can run, so please read carefully.

Program: /project/Biogroup/Software/GEnsemble/programs/superbihelix/run_super_combi_neutralize.pl

Usage: run_super_combi_neutralize.pl -b {bgf file} -m {mfta file} -n {# of bundles to build} -p {# of processors to use} -r {reference bgf} --bio {bioscratch directory} -w {walltime} --mach {machine} -i {input} --neut {neutralization scheme}

Required files:

bgf file - A bgf file with absolute numbering and helices numbered from 1 to 7. The hydrophobic centers need to be aligned to the z axis in this structure. It has been found that using a bgf file with the terminis alanized works well for the superbihelix step, but the original dealanized structure is best for this combihelix step.
mfta file - The mfta file for the bgf structure. Make sure that you change the mfta file so that the correct starting and ending residues for each helix are in the first two columns.
Super_Bihelix_TotalE.out - The output file from super_bihelix that gives the best structures by total bihelical energy.

Options:

For the number of bundles to build, choose up to the number of structures that are in Super_Bihelix_TotalE.out, the output file from Super_BiHelix.
You must enter the number of processors to perform the calculation in parallel. 
The reference bgf file is a file for which each bundle that is built will be compared to, with backbone RMSD. This is not required and will default to the input bgf file. Also, RMSD will only be calculated on hive or matrix (if you request borg the job will run fine, but all RMSD values will be 0.0).
There are currently 3 neutralization schemes:
- neut1 = Neutral-Prep-06-16-09.pl (default, don't have to specified)
- neut2 = Neutral-Prep/Neutral-Prep.pl (old default, may crash for some cases)
- neut3 = /project/Biogroup/Software/Neutralize/neutralize.py (new Vaclav's code)

MODE 1:

Usage: run_super_combi_neutralize.pl -b {bgf file} -m {mfta file} -n {# of bundles to build} -p {# of processors to use}

If you DON'T specify --bio variable the job will run in the directory you run it from. All bgf files will be deleted on the fly to save disk space. After the job combi helix neutralize job finishes it will also order the bundles by minimized mpsim energy and by a mean rank (rankNCti) consisting of intrahelical charged (rankCih) and neutral (rankNih) energies and total charged (rankCtl) and neutral (rankNtl) energies. After that step it will submit 5 additional jobs to create to 100 bgfs from rankCNti ranking and top 25 bgfs from each of rankCih, rankNih, rankCtl and rank Ntl rankings. After the job finishes and bgfs are created you will have an option to sort the results by any other energy ranking and produce as many bgfs as you wish using super_neutral_sort.pl script.

MODE 2:

Usage: run_super_combi_neutralize.pl -b {bgf file} -m {mfta file} -n {# of bundles to build} -p {# of processors to use} --bio {some_directory}

If you DO specify --bio {directory name} the job will run in /project/bioscratch/username/{directory name}/ directory (make sure that you have access to /project/bioscratch/username/ and that {directory name} is unique). All bgf files will be kept on bioscratch in the corresponding super_combihelix_* directories together with partial SuperCombihelix and SuperNeutralize rankings. After that step it will copy 100 bgfs from rankCNti ranking and top 25 bgfs from each of rankCih, rankNih, rankCtl and rank Ntl rankings to your home directory to corresponding directories. After the job finishes and bgfs are created you will have an option to sort the results by any other energy ranking and copy as mnay bgfs as you wish using super_neutral_sort.pl script.

Output (of both modes, it's the same):

Super_CombiHelix_TotalE.out - This gives the top structures by total mpsim energy of the bundle after 10 steps of minimization, as well as the their backbone RMSD to the reference bgf.
super_combihelix_* directories - with all partial SuperCombihelix and SuperNeutralize rankings (don't delete them!); in MODE 1 they will be created in your home directory, in MODE 2 they will be created and left on bioscratch.
Super_Neutralize_rankCNti.out - This gives the top structures by rankNCti. Top 100 bgfs by this ranking will be produced in super_sbhrank_rankCNti directory.
Super_Neutralize_rankCih.out - This gives the top structures by rankCih. Top 25 bgfs by this ranking will be produced in super_sbhrank_rankCih directory.
Super_Neutralize_rankNih.out - This gives the top structures by rankNih. Top 25 bgfs by this ranking will be produced in super_sbhrank_rankNih directory.
Super_Neutralize_rankCtl.out - This gives the top structures by rankCtl. Top 25 bgfs by this ranking will be produced in super_sbhrank_rankCtl directory.
Super_Neutralize_rankCtl.out - This gives the top structures by rankNtl. Top 25 bgfs by this ranking will be produced in super_sbhrank_rankNtl directory.

Example: run_super_combi_neutralize.pl beta2.bgf beta2.mfta 1000 24\n\n"}

# chek whereami - if not defined machine #
if (not defined $machine){
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
}
# END OF whereami check #

$masterdir = cwd();

if (not defined $ref) {$ref = $bgf;}
if (not defined $neut){$neut = "neut1"};
if (not defined $walltime){$walltime = 48;}

$fin = 0;
$jump = int($totnum/$numproc) + 1;
$top = ($numproc - 1)*$jump + 1;
$proc = $numproc;
if ($top > $totnum)
{
  $proc = $numproc - 1;
}

### added ###
if (not defined $totin){$totin = "Super_Bihelix_TotalE.out";}
open(TOTIN,"<$totin");
@totin = <TOTIN>;
close(TOTIN);

### add bihelix rank ###
$length_totin = scalar(@totin);
@totin2 = ();
$totin2[0] = $totin[0];
@split = split(" ", $totin[1]);
push(@split, "    BHrank");
push(@totin2, join(" ",@split));
@split = ();
for ($i = 2; $i < $length_totin; $i++){
                                        @split = split(" ", $totin[$i]);
                                        push(@split, $i-1);
                                        push(@totin2, join(" ",@split));
                                        @split = ();
                                        }
$totin3 = "Super_Bihelix_TotalE_withrank.out";
open(TOTIN2,">$totin3");
print TOTIN2 $totin2[0];
print TOTIN2 "Thet   H1   H2   H3   H4   H5   H6   H7 Phi   H1   H2   H3   H4   H5   H6   H7 Eta   H1   H2   H3   H4   H5   H6   H7 HPM    H1    H2    H3    H4    H5    H6    H7        TotalE     InterHelE  NoInterVDW     HBond    SBHrank\n";
for ($i = 2; $i < $length_totin; $i++){
     ($t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$r1) = split /\ +/, $totin2[$i];
     printf TOTIN2 "%4s %4s %4s %4s %4s %4s %4s %4s %3s %4s %4s %4s %4s %4s %4s %4s %3s %4s %4s %4s %4s %4s %4s %4s %3s %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f %13.1f %13.1f %11.1f %9.1f %10s\n",$t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$r1;
                                         }

close TOTIN2;

# if running on bioscratch #
if (defined $bio){ 
  system("whoami > whoami");
  open(WHOAMI,"<whoami");
  @whoami = <WHOAMI>;
  close(WHOAMI);
  ($who = $whoami[0]) =~ s/\n//g;
  if (-d "/project/bioscratch/$who/$bio/"){die "\n/project/bioscratch/$who/$bio/ directory exists, dying\n\n";}
  system ("mkdir /project/bioscratch/$who/$bio/");
  }
else {$bio = 0;}
# if running on bioscratch end #


for ($i = 1; $i <= $proc; $i++)
{
  $num1 = ($i - 1)*$jump + 1;
  $num2 = $i*$jump;
  if ($i == $proc)
  {
    $num2 = $totnum;
    $fin = 1;
  }
  if ($bio eq "0"){$dir = "super_combihelix_" . $i;}
else {$dir = "/project/bioscratch/$who/$bio/super_combihelix_" . $i;}  # if running on bioscratch #
  system ("mkdir $dir");
  system ("cp $bgf $mfta Super_Bihelix_TotalE_withrank.out $dir");
  chdir($dir);
  $curdir = cwd();
  $pbs = "super_combi_" . $i . ".pbs";
  open (PBS,">$pbs");
  print PBS "#PBS -l nodes=1,walltime=$walltime:00:00\n";
  print PBS "#PBS -q workq\n";
  print PBS "#PBS -j oe\n";
  print PBS "#PBS -N super_combin_$i\n";
  print PBS "#PBS -m e\n";
  print PBS "#!/bin/csh\n\n";
  print PBS "cd \$PBS_O_WORKDIR\n\n";
  print PBS "echo the job started at ::: `date`\n\n";
  print PBS "/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_combi_neutralize_dev.pl -b $bgf -m $mfta -n1 $num1 -n2 $num2 -p $i -f $fin -r $ref --bio $bio -md $masterdir --mach $machine -n $neut \n\n";
  print PBS "echo the job ended at ::: `date`\n";
  close(PBS);
  print "Submitting super_combin_$i\t";
  system("ssh $machine \"cd $curdir;qsub $pbs;exit\"");
  chdir($masterdir);
}

