#!/usr/bin/perl

$bgf = @ARGV[0];
$mfta = @ARGV[1];
$line = @ARGV[2];

($tag,$bg) = split /\.bgf/, $bgf;  
$pdb = $tag . ".pdb"; 
$template = $tag . "_temp.template"; 
system("/project/Biogroup/scripts/perl/bgf2pdb.pl $bgf > $pdb");
system("/project/Biogroup/Software/devel/GEnsemble2/programs/templates/OPM/GetTemplate.pl -m $mfta -p $pdb > $template");
system("/project/Biogroup/scripts/playWithBGF/playWithBGF $bgf -c 1 -o temp1.bgf > play_with_bgf.out");
system("/project/Biogroup/scripts/playWithBGF/playWithBGF $bgf -c 2 -o temp2.bgf > play_with_bgf.out");
system("/project/Biogroup/scripts/playWithBGF/playWithBGF $bgf -c 3 -o temp3.bgf > play_with_bgf.out");
system("/project/Biogroup/scripts/playWithBGF/playWithBGF $bgf -c 4 -o temp4.bgf > play_with_bgf.out");
system("/project/Biogroup/scripts/playWithBGF/playWithBGF $bgf -c 5 -o temp5.bgf > play_with_bgf.out");
system("/project/Biogroup/scripts/playWithBGF/playWithBGF $bgf -c 6 -o temp6.bgf > play_with_bgf.out");
system("/project/Biogroup/scripts/playWithBGF/playWithBGF $bgf -c 7 -o temp7.bgf > play_with_bgf.out");
open(TEMPLATE,"<$template");
@template = <TEMPLATE>;
close(TEMPLATE);

$i = 0;
foreach $templine (@template)
{ 
  $i++;
  if ($templine !~ /EtaRes/)
  {
    ($st,$tmno,$xx,$yy,$hpc,$tht,$phi,$eta,$etares,$etaresno) = split /\ +/, $templine; 
    $tmno[$i] = $tmno;
    $xx[$i] = $xx;
    $yy[$i] = $yy;
    $hpc[$i] = $hpc;
    $tht[$i] = $tht;
    $phi[$i] = $phi;
    $eta[$i] = $eta;
    $etares[$i] = $etares;
    $etaresno[$i] = $etaresno; 
  }
}
($thtx,$thtx[1],$thtx[2],$thtx[3],$thtx[4],$thtx[5],$thtx[6],$thtx[7],$phix,$phix[1],$phix[2],$phix[3],$phix[4],$phix[5],$phix[6],$phix[7],$etax,$etax[1],$etax[2],$etax[3],$etax[4],$etax[5],$etax[6],$etax[7],$hpcx,$hpcx[1],$hpcx[2],$hpcx[3],$hpcx[4],$hpcx[5],$hpcx[6],$hpcx[7],$rest) = split /\ +/, $line;

$tempnew = $tag . "_temp_new.template";
open(TEMPNEW,">$tempnew");

for ($j = 1; $j < 8; $j++)
{
  $thtnew = $tht[$j] + $thtx[$j];
  $phinew = $phi[$j] + $phix[$j];
  $etanew = $eta[$j] + $etax[$j];
  $hpcnew = $hpcx[$j];
  print TEMPNEW ("*  $tmno[$j]   $xx[$j]   $yy[$j]   $hpcnew   $thtnew   $phinew   $etanew   $etares[$j]  $etaresno[$j]");
} 

print TEMPNEW ("* TM          X        Y       HPC     Theta      Phi      Eta    EtaRes");

system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/Align2Template-2.pl -t $tempnew -m $mfta -p $tag");
system("rm -f super_temp.mfta play_with_bgf.out temp1.bgf temp2.bgf temp3.bgf temp4.bgf temp5.bgf temp6.bgf temp7.bgf aligned_helix1.bgf aligned_helix2.bgf aligned_helix3.bgf aligned_helix4.bgf aligned_helix5.bgf aligned_helix6.bgf aligned_helix7.bgf");
