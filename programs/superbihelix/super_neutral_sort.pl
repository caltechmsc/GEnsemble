#!/usr/bin/perl

use Cwd;
use Getopt::Long;

GetOptions ('h|help'         => \$help,
            'b|bgf=s'        => \$bgf,
            'm|mfta=s'       => \$mfta,
            'p|proc=i'       => \$tot,
            'bio=s'          => \$bio,
            'md=s'           => \$masterdir,
            'range=s'        => \$range,
            'sortrank=s'     => \$sortrank,
            'ppn=i'          => \$ppn,
            );

if ($bgf eq "")
{die "super_neutral_sort.pl

Bartosz Trzaskowski (trzask@wag), May 22, 2010

This program takes a run_super_combi_neutralize.pl output and sorts the complexes according to one of rankings. Optionally, it can also build the corresponding bgfs. There are several different modes in which it can run (depending on --range and --bio options), so please read carefully.

Program: /project/Biogroup/Software/GEnsemble/programs/superbihelix/super_neutral_sort.pl

Usage: super_neutral_sort.pl -b {bgf} -m {mfta} -p  {# of processors used for super_combi_neutralize} --bio {bioscratch directory where super_neutral_sort job was run; optinal} -md {job directory; optional} -r {range; optional} --sortrank {sorting rank} --ppn {# of processors to use; optional} 

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
Cih  - rank of charged interhelical energy (identical to CInterH)
Ctl  - rank of charged total energy (identical to CTotal)
Nih  - rank of neutral interhelical energy (identical to NInterH)
Ntl  - rank of total interhelical energy (identical to NTotal)
Cti  - rank of average of charged total and interhelical energy
Nti  - rank of average of neutral total and interhelical energy
CNi  - rank of average of charged and neutral interhelical energy
CNt  - rank of average of charged and neutral total energy
CNti - rank of average of charged and neutral total and charged and neutral interhelical energy

If you DON'T specify range the script will only sort the complexes according to the requested ranking (--sortrank) and output a text file. You should run the jobs from the directory from which you sumbitted super_combi_neutralize jobs. This jobs takes ~seconds.

If you DO specify the range, the script will try to either copy or create the bgfs of the given range:

a) if you run super_combi_neutralize on bioscratch you should specify --bio {diretory} option. The script will then copy the requested bgfs back to your starting directory.
b) if you run super_combi_neutralize NOT on bioscratch (locally) you shouldn' specify --bio option. The script will then submit the job to the queue in which it will create the requested bgfs (both charged and neutral).

Output:

Super_Neutralize_rank{sort ranking}.out - text file with all structures from super_combi_neutralize sorted by a given ranking.
Super_Neutralize_rank{sort ranking}.csv - same but in csv format
super_rank{sort ranking}_{range} - directory with requested bgfs

Usage: super_neutral_sort.pl -b {bgf} -m {mfta} -p  {# of processors used for super_combi_neutralize} --bio {bioscratch directory where super_neutral_sort job was run; optinal} -md {job directory; optional} -r {range; optional} --sortrank {sorting rank} --ppn {# of processors to use; optional}

"}


if    ($sortrank eq "CIntraH") {$sortbase = 33;}
elsif ($sortrank eq "CInterH") {$sortbase = 34;}
elsif ($sortrank eq "CTotal")  {$sortbase = 35;}
elsif ($sortrank eq "NIntraH") {$sortbase = 36;}
elsif ($sortrank eq "NInterH") {$sortbase = 37;}
elsif ($sortrank eq "NTotal")  {$sortbase = 38;}
elsif ($sortrank eq "Cih") {$sortbase = 41;}
elsif ($sortrank eq "Ctl") {$sortbase = 42;}
elsif ($sortrank eq "Nih") {$sortbase = 43;}
elsif ($sortrank eq "Ntl") {$sortbase = 44;}
elsif ($sortrank eq "Cti") {$sortbase = 45;}
elsif ($sortrank eq "Nti") {$sortbase = 46;}
elsif ($sortrank eq "CNi") {$sortbase = 47;}
elsif ($sortrank eq "CNt") {$sortbase = 48;}
elsif ($sortrank eq "CNti"){$sortbase = 49;}
else  {$sortrank = "CNti"; $sortbase = 49;}
($sortrank_cap = "rank" . $sortrank) =~ s/\b(\w)/\U$1/g;

($pre,$post) = split /\.bgf/, $bgf;

# if running on bioscratch #
if (($bio != 0) || (defined $bio)){
  system("whoami > whoami");
  open(WHOAMI,"<whoami");
  @whoami = <WHOAMI>;
  close(WHOAMI);
  ($who = $whoami[0]) =~ s/\n//g;
  unlink("whoami");
  }
# if running on bioscratch end #

if (not defined $ppn){$ppn = 1;}
if (not defined $masterdir){$masterdir = cwd();}
if (($bio != 0) || (defined $bio)){chdir("/project/bioscratch/$who/$bio");}
else {chdir($masterdir);}


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
  if (($helixEng{$min} eq "none") || ($interHelEng{$min} eq "none") || ($min eq "none") || ($neutHelixEng{$min} eq "none") || ($neutInterHel{$min} eq "none") || ($neutEng{$min} eq "none")){
       push @none_lines, "Thet " . $the1 . " " . $the2 . " " . $the3 . " " . $the4 . " " . $the5 . " " . $the6 . " " . $the7 . " " . "Phi " . $phi1 . " " . $phi2 . " " . $phi3 . " " . $phi4 . " " . $phi5 . " " . $phi6 . " " . $phi7 . " " . "Eta " . $eta1 . " " . $eta2 . " " . $eta3 . " " . $eta4 . " " . $eta5 . " " . $eta6 . " " . $eta7 . " " . "HPM " . $hpm1 . " " . $hpm2 . " " . $hpm3 . " " . $hpm4 . " " . $hpm5 . " " . $hpm6 . " " . $hpm7 . " " . $helixEng{$min} . " " . $interHelEng{$min} . " " . $min . " " . $neutHelixEng{$min} . " " . $neutInterHel{$min} . " " . $neutEng{$min} . " " . $rmsd{$min} . " " . $bhrank{$min};}
else {
  push @final_lines, "Thet " . $the1 . " " . $the2 . " " . $the3 . " " . $the4 . " " . $the5 . " " . $the6 . " " . $the7 . " " . "Phi " . $phi1 . " " . $phi2 . " " . $phi3 . " " . $phi4 . " " . $phi5 . " " . $phi6 . " " . $phi7 . " " . "Eta " . $eta1 . " " . $eta2 . " " . $eta3 . " " . $eta4 . " " . $eta5 . " " . $eta6 . " " . $eta7 . " " . "HPM " . $hpm1 . " " . $hpm2 . " " . $hpm3 . " " . $hpm4 . " " . $hpm5 . " " . $hpm6 . " " . $hpm7 . " " . $helixEng{$min} . " " . $interHelEng{$min} . " " . $min . " " . $neutHelixEng{$min} . " " . $neutInterHel{$min} . " " . $neutEng{$min} . " " . $rmsd{$min} . " " . $bhrank{$min};
}
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

$output_final = "Super_Neutralize_rank$sortrank.out";
$output_csv = "Super_Neutralize_rank$sortrank.csv";
open(OUTPUT,">$output_final");
printf OUTPUT "Ordered by %8s\n",$sortrank_cap;
printf OUTPUT "Thet   H1   H2   H3   H4   H5   H6   H7  Phi   H1   H2   H3   H4   H5   H6   H7  Eta   H1   H2   H3   H4   H5   H6   H7  HPM    H1    H2    H3    H4    H5    H6    H7  CIntraH  CInterH   CTotal  NIntraH  NInterH   NTotal  RMSD  rankCih  rankCtl  rankNih  rankNtl  rankCti  rankNti  rankCNi  rankCNt rankCNti %8s   SBHrank\n",$sortrank_cap;
foreach $flines (@add_mean){
                           ($t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$n5,$n6,$rm,$bh,$r1,$r2,$r3,$r4,$r5,$r6,$r7,$r8,$r9,$n0) = split / /, $flines;
                           printf OUTPUT "%4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f %5.2f %8s %8s %8s %8s %8.1f %8.1f %8.1f %8.1f %8.1f %8s %9s\n",$t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$n5,$n6,$rm,$r1,$r2,$r3,$r4,$r5,$r6,$r7,$r8,$r9,$n0,$bh;
                           }
foreach $nlines (@none_lines){
                             ($t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$n5,$n6,$rm,$bh) = split / /, $nlines;
                             printf OUTPUT "%4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f %5.2f        -        -        -        -        -        -        -        -        -        - %9s\n",$t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$n5,$n6,$rm,$bh;
                             }
@full_array = (@add_mean,@none_lines);
close OUTPUT;

open(CSV,">$output_csv");
print CSV "Ordered by $sortrank_cap\n";
print CSV "Thet,H1,H2,H3,H4,H5,H6,H7,Phi,H1,H2,H3,H4,H5,H6,H7,Eta,H1,H2,H3,H4,H5,H6,H7,HPM,H1,H2,H3,H4,H5,H6,H7,CIntraH,CInterH,CTotal,NIntraH,NInterH,NTotal,RMSD,rankCih,rankCtl,rankNih,rankNtl,rankCti,rankNti,rankCNi,rankCNt,rankCNti,$sortrank_cap,SBHrank\n";
foreach $flines (@add_mean){
                           ($t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$n5,$n6,$rm,$bh,$r1,$r2,$r3,$r4,$r5,$r6,$r7,$r8,$r9,$n0) = split / /, $flines;
                           print CSV "$t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$n5,$n6,$rm,$r1,$r2,$r3,$r4,$r5,$r6,$r7,$r8,$r9,$n0,$bh\n";
                          }
foreach $nlines (@none_lines){
                             ($t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$n5,$n6,$rm,$bh) = split / /, $nlines;
                             print CSV "$t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$n5,$n6,$rm,-,-,-,-,-,-,-,-,-,-,$bh\n";
                             }
close CSV;

if (defined $range){
if (($bio != 0) || (defined $bio)) {
                          system("cp Super_Neutralize_rank$sortrank.out $masterdir");
                          system("cp Super_Neutralize_rank$sortrank.csv $masterdir");
                          mkdir("$masterdir/super_rank$sortrank-$range");
                          system("cp Super_Neutralize_rank$sortrank.out $masterdir/super_rank$sortrank-$range");
                          if ($range =~ m/-/){
                          @split_range = split("-", $range);
                          $start_range = $split_range[0];
                          $end_range   = $split_range[1];
                                             }
                          else {$start_range = $end_range = $range};
                          for ($i = $start_range-1; $i < $end_range; $i++){
                                                                           $curmin = ();
                                                                           $curneut = ();
                                                                           ($t0,$t1,$t2,$t3,$t4,$t5,$t6,$t7,$p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$e0,$e1,$e2,$e3,$e4,$e5,$e6,$e7,$h0,$h1,$h2,$h3,$h4,$h5,$h6,$h7,$n1,$n2,$n3,$n4,$n5,$n6,$rm,$bh,$r1,$r2,$r3,$r4,$r5,$r6,$r7,$r8,$r9,$n0) = split / /, $full_array[$i];
                                                                           $curmin = $pre . "." . $t1 . "_" . $t2 . "_" . $t3 . "_" . $t4 . "_" . $t5 . "_" . $t6 . "_" . $t7 . "x" . $p1 . "_" . $p2 . "_" . $p3 . "_" . $p4 . "_" . $p5 . "_" . $p6 . "_" . $p7 . "x" . $e1 . "_" . $e2 . "_" . $e3 . "_" . $e4 . "_" . $e5 . "_" . $e6 . "_" . $e7 . "x" . $h1 . "_" . $h2 . "_" . $h3 . "_" . $h4 . "_" . $h5 . "_" . $h6 . "_" . $h7 . ".min.bgf";
                                                                           $curneut = $pre . "." . $t1 . "_" . $t2 . "_" . $t3 . "_" . $t4 . "_" . $t5 . "_" . $t6 . "_" . $t7 . "x" . $p1 . "_" . $p2 . "_" . $p3 . "_" . $p4 . "_" . $p5 . "_" . $p6 . "_" . $p7 . "x" . $e1 . "_" . $e2 . "_" . $e3 . "_" . $e4 . "_" . $e5 . "_" . $e6 . "_" . $e7 . "x" . $h1 . "_" . $h2 . "_" . $h3 . "_" . $h4 . "_" . $h5 . "_" . $h6 . "_" . $h7 . "-neut.bgf";
                                                                           $command_copymin  = "find super_combihelix_* -name $curmin  -exec cp {} $masterdir/super_rank$sortrank-$range " . '\;';
                                                                           $command_copyneut = "find . -name $curneut -exec cp {} $masterdir/super_rank$sortrank-$range " . '\;';
                                                                           system($command_copymin);
                                                                           system($command_copyneut);
                                                                           }
                         print "\nFiles copied from bioscratch to super_$sortrank-$range\n\n";
                         }
if (($bio == 0) && (not defined $bio)) {
`/project/Biogroup/Software/GEnsemble/programs/superbihelix/run_super_create.pl -b $bgf -m $mfta -p $tot -i $output_final --range $range --ppn $ppn`}
                      }
else {
if (($bio != 0) || (defined $bio)) { 
                                   system("cp Super_Neutralize_rank$sortrank.out $masterdir");
                                   system("cp Super_Neutralize_rank$sortrank.csv $masterdir");
                                   }
print "\nRange undefined, stopping without creation of bgfs\n\n";}
exit;
