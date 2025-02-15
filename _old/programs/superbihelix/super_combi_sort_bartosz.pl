#!/usr/bin/perl

$tot = @ARGV[0];
$bgf = @ARGV[1];
$prefix = @ARGV[2];

($pre,$post) = split /\.bgf/, $bgf;
$j = 0;
system("mkdir super_combihelix");
for ($i = 1; $i <= $tot; $i++)
{
  $file = "super_combihelix_$i/Super_CombiHelix_$i.out";
  open (FILE,"<$file");
  @file = <FILE>;
  close(FILE);
  foreach $line (@file)
  {
    $fudge = $j * 0.000001;
    ($struc,$hbond,$scream,$premin,$aftminx,$rmsdx) = split /\ +/, $line;
    ($rmsd,$nl) = split /\n/, $rmsdx;    
    $aftmin[$j] = $aftminx + $fudge;
    $struc{$aftmin[$j]} = $struc;
    $scream{$aftmin[$j]} = $scream;
    $premin{$aftmin[$j]} = $premin;
    $hbond{$aftmin[$j]} = $hbond; 
    $rmsd{$aftmin[$j]} = $rmsd;
    $j++;
  }
  system("find super_combihelix_$i/ -name '*'bgf.gz -exec mv {} super_combihelix \\;");
  system("find super_combihelix_$i/ -name Super_CombiHelix_$i.out -exec mv {} super_combihelix \\;");
  system("find super_combihelix_$i/ -name super_combi_$i.o'*' -exec mv {} super_combihelix \\;");
  system("rm -fr super_combihelix_$i");
}

$out = "Super_CombiHelix_TotalE.out";
open (OUT,">$out");
@mins = sort { $a <=> $b } @aftmin;
print OUT ("                                                                                                                                                                                                                Ordered by\n");
print OUT ("Thet   H1   H2   H3   H4   H5   H6   H7  Phi   H1   H2   H3   H4   H5   H6   H7  Eta   H1   H2   H3   H4   H5   H6   H7  HPM    H1    H2    H3    H4    H5    H6    H7       HBondE      ScreamE      PreMinE     PostMinE      RMSD\n"); 

foreach $min (@mins)
{
  ($prf,$rest) = split /$pre\./, $struc{$min};
  ($mid,$aft) = split /\.min\.bgf/, $rest;
  ($thets,$phis,$etas,$hpms) = split /x/, $mid;
  ($the1,$the2,$the3,$the4,$the5,$the6,$the7) = split /_/, $thets;
  ($phi1,$phi2,$phi3,$phi4,$phi5,$phi6,$phi7) = split /_/, $phis;
  ($eta1,$eta2,$eta3,$eta4,$eta5,$eta6,$eta7) = split /_/, $etas;
  ($hpm1,$hpm2,$hpm3,$hpm4,$hpm5,$hpm6,$hpm7) = split /_/, $hpms;
  printf OUT "Thet %4s %4s %4s %4s %4s %4s %4s  Phi %4s %4s %4s %4s %4s %4s %4s  Eta %4s %4s %4s %4s %4s %4s %4s  HPM %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f %12.1f %12.1f %12.1f %12.1f %9.1f\n",$the1,$the2,$the3,$the4,$the5,$the6,$the7,$phi1,$phi2,$phi3,$phi4,$phi5,$phi6,$phi7,$eta1,$eta2,$eta3,$eta4,$eta5,$eta6,$eta7,$hpm1,$hpm2,$hpm3,$hpm4,$hpm5,$hpm6,$hpm7,$hbond{$min},$scream{$min},$premin{$min},$min,$rmsd{$min};  
} 

close(OUT);

if (defined $prefix){
system("cp Super_CombiHelix_TotalE.out super_combihelix");
chdir("super_combihelix");
system("/ul/trzask/scripts/super_neutralize.pl -p $prefix -s -m hive -t 10");
}
