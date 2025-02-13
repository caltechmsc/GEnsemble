#!/usr/bin/perl

$ener = @ARGV[0];
$nstr = @ARGV[1];
$tag  = @ARGV[2];
$tago = @ARGV[3];

if (@ARGV == 0) { help(); }

if (!$tago) {
    $tago=$tag;
}

$enerout=$tago . "_ener.dat";

open(ENERIN,"<$ener");
@enerin = <ENERIN>;
close(ENERIN);

open(ENEROUT,">$enerout");

$i = 0; 
foreach $enerinline (@enerin)
{
  if ($enerinline !~ /Rank/) {
  $i++;
  if ($i <= $nstr)  
  {
    ($thtx,$thtx[1],$thtx[2],$thtx[3],$thtx[4],$thtx[5],$thtx[6],$thtx[7],$phix,$phix[1],$phix[2],$phix[3],$phix[4],$phix[5],$phix[6],$phix[7],$etax,$etax[1],$etax[2],$etax[3],$etax[4],$etax[5],$etax[6],$etax[7],$hpmx,$hpmx[1],$hpmx[2],$hpmx[3],$hpmx[4],$hpmx[5],$hpmx[6],$hpmx[7],$enc[1],$enc[2],$enc[3],$enn[1],$enn[2],$enn[3],$rmsd,$rnk[1],$rnk[2],$rnk[3],$rnk[4],$rnk[5],$rnk[6],$rnk[7],$rnk[8],$rnk[9],$rnk[10],$rnk[11]) = split /\ +/, $enerinline;
    $curbgf = $tag . "." . $thtx[1] . "_" . $thtx[2] . "_" . $thtx[3] . "_" . $thtx[4] . "_" . $thtx[5] . "_" . $thtx[6] . "_" . $thtx[7] . "x" . $phix[1] . "_" . $phix[2] . "_" . $phix[3] . "_" . $phix[4] . "_" . $phix[5] . "_" . $phix[6] . "_" . $phix[7] . "x" . $etax[1] . "_" . $etax[2] . "_" . $etax[3] . "_" . $etax[4] . "_" . $etax[5] . "_" . $etax[6] . "_" . $etax[7] . "x" . $hpmx[1] . "_" . $hpmx[2] . "_" . $hpmx[3] . "_" . $hpmx[4] . "_" . $hpmx[5] . "_" . $hpmx[6] . "_" . $hpmx[7] . ".min.bgf";
    $finbgf = "rank" . $i . "_" . $tago . ".bgf";
    system ("cp -f $curbgf $finbgf");
  $avge=0.25*($enc[2]+$enc[3]+$enn[2]+$enn[3]);
  print ENEROUT "$i $enc[1] $enc[2] $enc[3] $enn[1] $enn[2] $enn[3] $avge\n";
  }
  }
}
close(ENEROUT);


sub help {
 
     my $help = "
     Usage example: add_erank_get_ener.pl Super_Neutralize_rankCNti.out 25 L209A
\n";

     print "$help";
     exit(1);

}
