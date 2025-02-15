#!/usr/bin/perl

use Cwd;

$bgf = @ARGV[0];
$mfta = @ARGV[1];
$totnum = @ARGV[2];
$numproc = @ARGV[3];
$ref = @ARGV[4];
$name = @ARGV[5];

if ($bgf eq "")
{die "run_super_combi_neutralize.pl

Jenelle Bray (jenelle@wag), August 4, 2009
Bartosz Trzaskowski (trzask@wag), May 22, 2010

This program builds the best clusters from super_bihelix that sample eta, phi, theta and HPM values. After building, it minimizes the entire bundle for 10 steps and neutralizes it. There are two modes in which this program can run, so please read carefully.

Program: /project/Biogroup/Software/GEnsemble/programs/superbihelix/run_super_combi_neutralize.pl

Usage: run_super_combi_neutralize.pl {bgf file} {mfta file} {# of bundles to build} {# of processors to use} {reference bgf} {directory name; optional}

Required files:

bgf file - A bgf file with absolute numbering and helices numbered from 1 to 7. The hydrophobic centers need to be aligned to the z axis in this structure. It has been found that using a bgf file with the terminis alanized works well for the superbihelix step, but the original dealanized structure is best for this combihelix step.

mfta file - The mfta file for the bgf structure. Make sure that you change the mfta file so that the correct starting and ending residues for each helix are in the first two columns.

Super_Bihelix_TotalE.out - The output file from super_bihelix that gives the best structures by total bihelical energy.

Options:

For the number of bundles to build, choose up to the number of structures that are in Super_Bihelix_TotalE.out, the output file from Super_BiHelix.

You must enter the number of processors to perform the calculation in parallel. Only choose the number of processors that are currently available.

The reference bgf file is a file for which each bundle that is built will be compared to, with backbone RMSD. This is a REQUIRED input, if you don't know what to add just repeat the original bgf file.

MODE 1:

Usage: run_super_combi_neutralize.pl {bgf file} {mfta file} {# of bundles to build} {# of processors to use} {reference bgf}

If you DON'T specify the last variable {directory name} the job will run in the directory you run it from. All bgf files will be deleted on the fly to save disk space. After the job combi helix neutralize job finishes it will also order the bundles by minimized mpsim energy and by a mean rank (rankNCti) consisting of intrahelical charged (rankCih) and neutral (rankNih) energies and total charged (rankCtl) and neutral (rankNtl) energies. After that step it will submit 5 additional jobs to create to 100 bgfs from rankCNti ranking and top 25 bgfs from each of rankCih, rankNih, rankCtl and rank Ntl rankings. After the job finishes and bgfs are created you will have an option to sort the results by any other energy ranking and produce as many bgfs as you wish using super_neutral_sort.pl script.

MODE 2:

Usage: run_super_combi_neutralize.pl {bgf file} {mfta file} {# of bundles to build} {# of processors to use} {reference bgf} {directory name}

If you DO specify the last variable {directory name} the job will run in /project/bioscratch/username/{directory name}/ directory (make sure that you have access to /project/bioscratch/username/ and that {directory name} is unique). All bgf files will be kept on bioscratch in the corresponding super_combihelix_* directories together with partial SuperCombihelix and SuperNeutralize rankings. After that step it will copy 100 bgfs from rankCNti ranking and top 25 bgfs from each of rankCih, rankNih, rankCtl and rank Ntl rankings to your home directory to corresponding directories. After the job finishes and bgfs are created you will have an option to sort the results by any other energy ranking and copy as mnay bgfs as you wish using super_neutral_sort.pl script.

Output (of both modes, it's the same):

Super_CombiHelix_TotalE.out - This gives the top structures by total mpsim energy of the bundle after 10 steps of minimization, as well as the their backbone RMSD to the reference bgf.

super_combihelix_* directories - with all partial SuperCombihelix and SuperNeutralize rankings (don't delete them!); in MODE 1 they will be created in your home directory, in MODE 2 they will be created and left on bioscratch.

Super_Neutralize_rankCNti.out - This gives the top structures by rankNCti. Top 100 bgfs by this ranking will be produced in super_sbhrank_rankCNti directory.

Super_Neutralize_rankCih.out - This gives the top structures by rankCih. Top 25 bgfs by this ranking will be produced in super_sbhrank_rankCih directory.

Super_Neutralize_rankNih.out - This gives the top structures by rankNih. Top 25 bgfs by this ranking will be produced in super_sbhrank_rankNih directory.

Super_Neutralize_rankCtl.out - This gives the top structures by rankCtl. Top 25 bgfs by this ranking will be produced in super_sbhrank_rankCtl directory.

Super_Neutralize_rankCtl.out - This gives the top structures by rankNtl. Top 25 bgfs by this ranking will be produced in super_sbhrank_rankNtl directory.


Example: run_super_combi_neutralize.pl beta2.bgf beta2.mfta 1000 24 beta2-ref.bgf beta2\n\n"}

$curdir = cwd();

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

### added ###

$totin = "Super_Bihelix_TotalE.out";
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
for ($i = 2; $i < $length_totin+1; $i++){
     ($t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$r1) = split /\ +/, $totin2[$i];
     printf TOTIN2 "%4s %4s %4s %4s %4s %4s %4s %4s %3s %4s %4s %4s %4s %4s %4s %4s %3s %4s %4s %4s %4s %4s %4s %4s %3s %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f %13.1f %13.1f %11.1f %9.1f %10s\n",$t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$r1;
                                         }

close TOTIN2;

# if running on bioscratch #
if (defined $name){ 
  system("whoami > whoami");
  open(WHOAMI,"<whoami");
  @whoami = <WHOAMI>;
  close(WHOAMI);
  ($who = $whoami[0]) =~ s/\n//g;
  system ("mkdir /project/bioscratch/$who/$name/");
  }
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
  if (defined $name){$dir = "/project/bioscratch/$who/$name/super_combihelix_" . $i;}  # if running on bioscratch #
  else {$dir = "super_combihelix_" . $i;}
  system ("mkdir $dir");
  system ("cp $bgf $mfta Super_Bihelix_TotalE_withrank.out $dir");
  chdir($dir);
  $pbs = "super_combi_" . $i . ".pbs";
  open (PBS,">$pbs");
  print PBS "#PBS -l nodes=1,walltime=240:00:00\n";
  print PBS "#PBS -q workq\n";
  print PBS "#PBS -j oe\n";
  print PBS "#PBS -N super_combin_$i\n";
  print PBS "#PBS -m e\n";
  print PBS "#!/bin/csh\n\n";
  print PBS "cd \$PBS_O_WORKDIR\n\n";
  print PBS "echo the job started at ::: `date`\n\n";
  print PBS "/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_combi_neutralize2.pl $bgf $mfta $num1 $num2 $i $fin $ref $name $curdir\n\n";
  print PBS "echo the job ended at ::: `date`\n";
  close(PBS);
  system("qsub $pbs"); 
  chdir($curdir);
}

