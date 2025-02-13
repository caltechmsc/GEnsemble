#!/usr/bin/perl -w

($#ARGV >=0 ) or die "Program to pull out protein energy after MPSim from memb_scream output.\n Usage: get_mpsim_output_combi.pl protein_prefix\n Output: prefix_combirot_mpsim.out.\n";

$prefix = $ARGV[0];
$outfile = $prefix."combirot_mpsim.out";
open (OUT, ">".$outfile);


    $dir1 = "scream_combi";
    chdir($dir1);

$nh=0;
    open (ANG,"../my_combiangles.dat");
    while ($angle = <ANG>) {
        chomp $angle;
        $nh++;
        $helixname="helix"."$nh";
        @helix_ang=split(/\s+/, $angle);
        $i=1;
        foreach (@helix_ang) {
            $helixname{$i,$nh}=$_;
            $i++;
        }
        $angno[$nh]=$i-1;
    }
close ANG;

for ($tm1 = 1; $tm1 < $angno[1] + 1; $tm1++)
{
for ($tm2 = 1; $tm2 < $angno[2] + 1; $tm2++)
{
for ($tm3 = 1; $tm3 < $angno[3] + 1; $tm3++)
{
for ($tm4 = 1; $tm4 < $angno[4] + 1; $tm4++)
{
for ($tm5 = 1; $tm5 < $angno[5] + 1; $tm5++)
{
for ($tm6 = 1; $tm6 < $angno[6] + 1; $tm6++)
{
for ($tm7 = 1; $tm7 < $angno[7] + 1; $tm7++)
{

$struct = $helixname{$tm1,1} . "_" . $helixname{$tm2,2} . "_" . $helixname{$tm3,3} . "_" . $helixname{$tm4,4} . "_" . $helixname{$tm5,5} . "_" . $helixname{$tm6,6} . "_" . $helixname{$tm7,7};

	$energyp=$prefix . "." . $struct . ".combirot_mpsimE.out";
 
        open (ENER,$energyp);
        $nline = 0;
        while ($lines = <ENER>) {
            $nline++;
            chomp ($lines);
            @strenergy = split(/\s+/, $lines);
            if ($nline == 1) {$ebefmin=$strenergy[0];}
            if ($nline == 2) {$eaftmin=$strenergy[0];}
        }
        close (ENER);

        if ($nline == 1) {
            printf OUT "  H1  H2  H3  H4  H5  H6  H7      MPSimE-BefMin\n";
            printf OUT "%4i%4i%4i%4i%4i%4i%4i %11.1f\n",$helixname{$tm1,1},$helixname{$tm2,2},$helixname{$tm3,3},$helixname{$tm4,4},$helixname{$tm5,5},$helixname{$tm6,6},$helixname{$tm7,7},$ebefmin;
        } elsif ($nline == 2) {
            printf OUT "  H1  H2  H3  H4  H5  H6  H7    MPSim-BefMin  MPSim-AftMin\n";
            printf OUT "%4i%4i%4i%4i%4i%4i%4i %11.1f %11.1f\n",$helixname{$tm1,1},$helixname{$tm2,2},$helixname{$tm3,3},$helixname{$tm4,4},$helixname{$tm5,5},$helixname{$tm6,6},$helixname{$tm7,7},$ebefmin,$eaftmin;
        }

}
}
}
}
}
}
}
