#!/usr/bin/perl

use Cwd;

$tot = @ARGV[0];
$bgf = @ARGV[1];
$mfta = @ARGV[2];
$sortrank = @ARGV[3];
$range = @ARGV[4];
$proc = @ARGV[5];
$name = @ARGV[6];
$curdir = @ARGV[7];

if ($tot eq "")
{die "super_neutral_sort.pl

Bartosz Trzaskowski (trzask@wag), May 22, 2010

This program takes a run_super_combi_neutralize.pl output and sorts the complexes according to one of rankings. Optionally, it can also build the corresponding bgfs. There are 3 modes in which it can run, so please read carefully.

Program: /project/Biogroup/Software/GEnsemble/programs/superbihelix/super_neutral_sort.pl

Usage: super_neutral_sort.pl {# of processors used for super_combi_neutralize} {bgf file} {mfta file} {sort ranking} {range; optional} {# of processors to use; optional} {directory name; optional}

Required files:

bgf file - A bgf file used for the super_combi_neutralize job.

mfta file - The mfta file used for the super_combi_neutralize job.

super_combihelix_* directories with the complete output from the super_combi_neutralize job.

Options:

The possible values for {sort ranking} are:

CIntraH  - charged intrahelical energy
CInterH  - charged interhelical energy
CTotal   - charged total energy
NIntraH  - neutral intrahelical energy
NInterH  - neutral interhelical energy
NTotal   - neutral total energy
rankCih  - rank of charged interhelical energy (identical to CInterH)
rankCtl  - rank of charged total energy (identical to CTotal)
rankNih  - rank of neutral interhelical energy (identical to NInterH)
rankNtl  - rank of total interhelical energy (identical to NTotal)
rankCti  - rank of average of charged total and interhelical energy
rankNti  - rank of average of neutral total and interhelical energy
rankCNi  - rank of average of charged and neutral interhelical energy
rankCNt  - rank of average of charged and neutral total energy
rankCNti - rank of average of charged and neutral total and charged and neutral interhelical energy

MODE 1:

Usage: super_neutral_sort.pl {# of processors used for super_combi_neutralize} {bgf file} {mfta file} {sort ranking}

If you specify only FOUR FIRST VARIABLES the script will only sort the complexes according to the request {sort ranking} and output a text file. You should run the jobs from the directory where super_combihelix_* directories are. This jobs takes ~seconds.

Output:

Super_Neutralize_{sort ranking} - All structures from super_combi_neutralize sorted by a given ranking.

Example: super_neutral_sort.pl 24 beta2.bgf beta2.mfta rankCNti

MODE 2:

Usage: super_neutral_sort.pl {# of processors used for super_combi_neutralize} {bgf file} {mfta file} {sort ranking} {range} {# of processors to use} 

If you did run super_combi_neutralize in your home directory (not on bioscratch) and want to create additional bgf files you should use SIX FIRST VARIABLES. You should run the jobs from the directory where super_combihelix_* directories are. This job takes ~2 hours per 25 complexes so consider splitting it into mutliple processors for larger jobs.

Output:

Super_Neutralize_{sort ranking} - Text file with all structures from super_combi_neutralize sorted by a given ranking.

super_sbhrank_{sort ranking} directory - directory with bgfs (both charged and neutral) from the requested ranking and in the requested range.

Example: super_neutral_sort.pl 24 beta2.bgf beta2.mfta rankCNti '1-200' 8

MODE 3:

Usage: super_neutral_sort.pl {# of processors used for super_combi_neutralize} {bgf file} {mfta file} {sort ranking} {range} {# of processors to use} {directory name}

If you did run super_combi_neutralize on bioscratch (not in your home directory) and want to get bgf files you should use SEVEN VARIABLES. You should run the jobs from the directory where you started super_combi_neutralize (not on bioscratch). {directory name} is the name of the directory on bioscratch where you run the super_combi_neutralize job. This job only copies the bgf files back to your home directory, so takes ~seconds to run.

Output:

Super_Neutralize_{sort ranking} - Text file with all structures from super_combi_neutralize sorted by a given ranking.

super_sbhrank_{sort ranking} directory - directory with bgfs (both charged and neutral) from the requested ranking and in the requested range.

Example: super_neutral_sort.pl 24 beta2.bgf beta2.mfta rankCNti '1-200' 1 beta2

"}


if    ($sortrank eq "CIntraH") {$sortbase = 33;}
elsif ($sortrank eq "CInterH") {$sortbase = 34;}
elsif ($sortrank eq "CTotal")  {$sortbase = 35;}
elsif ($sortrank eq "NIntraH") {$sortbase = 36;}
elsif ($sortrank eq "NInterH") {$sortbase = 37;}
elsif ($sortrank eq "NTotal")  {$sortbase = 38;}
elsif ($sortrank eq "rankCih") {$sortbase = 41;}
elsif ($sortrank eq "rankCtl") {$sortbase = 42;}
elsif ($sortrank eq "rankNih") {$sortbase = 43;}
elsif ($sortrank eq "rankNtl") {$sortbase = 44;}
elsif ($sortrank eq "rankCti") {$sortbase = 45;}
elsif ($sortrank eq "rankNti") {$sortbase = 46;}
elsif ($sortrank eq "rankCNi") {$sortbase = 47;}
elsif ($sortrank eq "rankCNt") {$sortbase = 48;}
elsif ($sortrank eq "rankCNti"){$sortbase = 49;}
else  {$sortrank = "rankCNti"; $sortbase = 49;}
($sortrank_cap = $sortrank) =~ s/\b(\w)/\U$1/g;

($pre,$post) = split /\.bgf/, $bgf;

# if running on bioscratch #
if (defined $name){
  if (not defined $curdir){$curdir = cwd();}
  system("mkdir $curdir/super_sbhrank_$sortrank-$range");
  system("whoami > whoami");
  open(WHOAMI,"<whoami");
  @whoami = <WHOAMI>;
  close(WHOAMI);
  ($who = $whoami[0]) =~ s/\n//g;
  chdir("/project/bioscratch/$who/$name/");
  }
# if running on bioscratch end #

$j = 0;
for ($i = 1; $i <= $tot; $i++)
{
  $file = "super_combihelix_$i/Super_Neutralize_$i.out";
  open (FILE,"<$file");
  @file = <FILE>;
  close(FILE);
  foreach $line (@file)
  {
    $fudge = $j * 0.000001;
    ($struc,$helixEng,$interHelEng,$aftminx,$neutHelixEng,$neutInterHel,$neutEng,$rmsd,$bhrankx) = split /\ +/, $line;
#    ($rmsd,$nl) = split /\n/, $rmsdx;
    ($bhrank,$nl) = split /\n/, $bhrankx;
#    print $bhrank;
    $aftmin[$j] = $aftminx + $fudge;
    $struc{$aftmin[$j]} = $struc;
    $helixEng{$aftmin[$j]} = $helixEng;
    $interHelEng{$aftmin[$j]} = $interHelEng;
    $neutHelixEng{$aftmin[$j]} = $neutHelixEng; 
    $neutInterHel{$aftmin[$j]} = $neutInterHel;
    $neutEng{$aftmin[$j]} = $neutEng;
    $rmsd{$aftmin[$j]} = $rmsd;
    $bhrank{$aftmin[$j]} = $bhrank;
    $j++;
  }
}

#$out = "Super_Neutralize_TotalE_temp.out";
#open (OUT,">$out");
@mins = sort { $a <=> $b } @aftmin;
#print OUT ("Thet   H1   H2   H3   H4   H5   H6   H7  Phi   H1   H2   H3   H4   H5   H6   H7  Eta   H1   H2   H3   H4   H5   H6   H7  HPM    H1    H2    H3    H4    H5    H6    H7       HBondE      ScreamE      PreMinE     PostMinE      RMSD\n");

foreach $min (@mins)
{
  ($prf,$rest) = split /$pre\./, $struc{$min};
  ($mid,$aft) = split /\.min\.bgf/, $rest;
  ($thets,$phis,$etas,$hpms) = split /x/, $mid;
  ($the1,$the2,$the3,$the4,$the5,$the6,$the7) = split /_/, $thets;
  ($phi1,$phi2,$phi3,$phi4,$phi5,$phi6,$phi7) = split /_/, $phis;
  ($eta1,$eta2,$eta3,$eta4,$eta5,$eta6,$eta7) = split /_/, $etas;
  ($hpm1,$hpm2,$hpm3,$hpm4,$hpm5,$hpm6,$hpm7) = split /_/, $hpms;
  push @final_lines, "Thet " . $the1 . " " . $the2 . " " . $the3 . " " . $the4 . " " . $the5 . " " . $the6 . " " . $the7 . " " . "Phi " . $phi1 . " " . $phi2 . " " . $phi3 . " " . $phi4 . " " . $phi5 . " " . $phi6 . " " . $phi7 . " " . "Eta " . $eta1 . " " . $eta2 . " " . $eta3 . " " . $eta4 . " " . $eta5 . " " . $eta6 . " " . $eta7 . " " . "HPM " . $hpm1 . " " . $hpm2 . " " . $hpm3 . " " . $hpm4 . " " . $hpm5 . " " . $hpm6 . " " . $hpm7 . " " . $helixEng{$min} . " " . $interHelEng{$min} . " " . $min . " " . $neutHelixEng{$min} . " " . $neutInterHel{$min} . " " . $neutEng{$min} . " " . $rmsd{$min} . " " . $bhrank{$min};
}
close(OUT);

$length_input = scalar(@final_lines)-1;
$num = $length_input;

######------------------------------------------######
######   Main part - sorting versus 5 columns   ######
######   and addding ranking numbers.           ######
######------------------------------------------######

@sorted1 = map  {$_->[0]}
           sort { $a->[34] <=> $b->[34] }
           map  {chomp;[$_,split(/ /)]} @final_lines;

for ($i = 0; $i < $num+1; $i++){
                               @split = split(" ", $sorted1[$i]);
                               push(@split, $i+1);
                               push(@add1, join(" ",@split));
                               @split = ();
                               }

@sorted2 = map  {$_->[0]}
           sort { $a->[35] <=> $b->[35] }
           map  {chomp;[$_,split(/ /)]} @add1;

for ($i = 0; $i < $num+1; $i++){
                               @split = split(" ", $sorted2[$i]);
                               push(@split, $i+1);
                               push(@add2, join(" ",@split));
                               @split = ();
                               }

@sorted3 = map  {$_->[0]}
           sort { $a->[37] <=> $b->[37] }
           map  {chomp;[$_,split(/ /)]} @add2;

for ($i = 0; $i < $num+1; $i++){
                               @split = split(" ", $sorted3[$i]);
                               push(@split, $i+1);
                               push(@add3, join(" ",@split));
                               @split = ();
                               }

@sorted4 = map  {$_->[0]}
           sort { $a->[38] <=> $b->[38] }
           map  {chomp;[$_,split(/ /)]} @add3;

for ($i = 0; $i < $num+1; $i++){
                               @split = split(" ", $sorted4[$i]);
                               push(@split, $i+1);
                               $rankMC = sprintf("%.1f",($split[40]+$split[41])/2);
                               $rankMN = sprintf("%.1f",($split[42]+$split[43])/2);
                               $rankMT = sprintf("%.1f",($split[41]+$split[43])/2); 
                               $rankMI = sprintf("%.1f",($split[40]+$split[42])/2);
                               $rankM  = sprintf("%.1f",($split[40]+$split[41]+$split[42]+$split[43])/4);
                               push(@split, ($rankMC,$rankMN,$rankMI,$rankMT,$rankM));
                               push(@add4, join(" ",@split));
                               @split = ();
                               }

@sorted_mean = map  {$_->[0]}
               sort { $a->[$sortbase] <=> $b->[$sortbase] }
               map  {chomp;[$_,split(/ /)]} @add4;
for ($i = 0; $i < $num+1; $i++){
                               @split = split(" ", $sorted_mean[$i]);
                               push(@split, $i+1);
                               push(@add_mean, join(" ",@split));
                               @split = ();
                               }

$output_final = "Super_Neutralize_$sortrank.out";
open(OUTPUT,">$output_final");
printf OUTPUT "Ordered by %8s\n",$sortrank_cap;
printf OUTPUT "Thet   H1   H2   H3   H4   H5   H6   H7  Phi   H1   H2   H3   H4   H5   H6   H7  Eta   H1   H2   H3   H4   H5   H6   H7  HPM    H1    H2    H3    H4    H5    H6    H7  CIntraH  CInterH   CTotal  NIntraH  NInterH   NTotal  RMSD  rankCih  rankCtl  rankNih  rankNtl  rankCti  rankNti  rankCNi  rankCNt rankCNti %8s   SBHrank\n",$sortrank_cap;
foreach $flines (@add_mean){
                             ($t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$n5,$n6,$rm,$bh,$r1,$r2,$r3,$r4,$r5,$r6,$r7,$r8,$r9,$n0) = split / /, $flines;
printf OUTPUT "%4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f %5.2f %8s %8s %8s %8s %8.1f %8.1f %8.1f %8.1f %8.1f %8s %9s\n",$t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$n5,$n6,$rm,$r1,$r2,$r3,$r4,$r5,$r6,$r7,$r8,$r9,$n0,$bh;
                           }
close OUTPUT;
                               
if (defined($range)) {
                     if (not defined $name){
                                           `/project/Biogroup/Software/GEnsemble/programs/superbihelix/run_super_sbhrank.pl $bgf $mfta $proc $bgf $output_final $range`
                                           }
                     else {
                          system("cp Super_Neutralize_$sortrank.out $curdir/super_sbhrank_$sortrank-$range");
                          if ($range =~ m/-/){
                          @split_range = split("-", $range);
                          $start_range = $split_range[0];
                          $end_range   = $split_range[1];
                                             }
                          else {$start_range = $end_range = $range};
                          for ($i = $start_range-1; $i < $end_range; $i++){
                                                                           $curmin = ();
                                                                           $curneut = ();
                                                                           ($t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$n5,$n6,$rm,$bh,$r1,$r2,$r3,$r4,$r5,$r6,$r7,$r8,$r9,$n0) = split / /, $add_mean[$i];
                                                                           $curmin = $pre . "." . $t1 . "_" . $t2 . "_" . $t3 . "_" . $t4 . "_" . $t5 . "_" . $t6 . "_" . $t7 . "x" . $p1 . "_" . $p2 . "_" . $p3 . "_" . $p4 . "_" . $p5 . "_" . $p6 . "_" . $p7 . "x" . $e1 . "_" . $e2 . "_" . $e3 . "_" . $e4 . "_" . $e5 . "_" . $e6 . "_" . $e7 . "x" . $h1 . "_" . $h2 . "_" . $h3 . "_" . $h4 . "_" . $h5 . "_" . $h6 . "_" . $h7 . ".min.bgf";
                                                                           $curneut = $pre . "." . $t1 . "_" . $t2 . "_" . $t3 . "_" . $t4 . "_" . $t5 . "_" . $t6 . "_" . $t7 . "x" . $p1 . "_" . $p2 . "_" . $p3 . "_" . $p4 . "_" . $p5 . "_" . $p6 . "_" . $p7 . "x" . $e1 . "_" . $e2 . "_" . $e3 . "_" . $e4 . "_" . $e5 . "_" . $e6 . "_" . $e7 . "x" . $h1 . "_" . $h2 . "_" . $h3 . "_" . $h4 . "_" . $h5 . "_" . $h6 . "_" . $h7 . "-neut.bgf"; 
                                                                           $command_copymin  = "find super_combihelix_* -name $curmin  -exec cp {} $curdir/super_sbhrank_$sortrank-$range " . '\;';
                                                                           $command_copyneut = "find . -name $curneut -exec cp {} $curdir/super_sbhrank_$sortrank-$range " . '\;';
                                                                           system($command_copymin);
                                                                           system($command_copyneut);
                                                                           }
                         print "\nFiles copied from bioscratch to super_sbhrank_$sortrank-$range\n\n";
                         }
                      }
else {print "\nRange undefined, stopping without creation of bgfs\n\n";}

