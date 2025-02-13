#!/usr/bin/perl -w

($#ARGV >=0 ) or die "Program to pull out mpsim energy after SCREAM from bihelix output.\n Usage: get_bihelmpsim_output.pl protein_prefix helix_i helix_j\n Output: prefix_combirot_scream.out.\n";

$prefix = $ARGV[0];
$helix_i = $ARGV[1];
$helix_j = $ARGV[2];
$outfile1 = $prefix."_H".$helix_i."-H".$helix_j."_bihelixrot_mpsim-befmin.out";
$outfile2 = $prefix."_H".$helix_i."-H".$helix_j."_bihelixrot_mpsim-aftmin.out";
open (OUT1, ">".$outfile1);
open (OUT2, ">".$outfile2);

$title = "   H${helix_i}   H${helix_j}  Tot_${helix_i}${helix_i}_Intra  Tot_${helix_j}${helix_j}_Intra  Tot_${helix_i}${helix_j}_Inter  TotalE_H${helix_i}-H${helix_j}  VDW_${helix_i}${helix_i}_Intra  VDW_${helix_j}${helix_j}_Intra  VDW_${helix_i}${helix_j}_Inter  NoVDWE_H${helix_i}-H${helix_j}  HBE_${helix_i}${helix_j}_Inter\n";

printf OUT1 $title;
printf OUT2 $title;

    $dir1 = "scream_combi";
    chdir($dir1);

$nh=0;
    open (ANG,"../bicombiangles.dat");
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

$struct = $helixname{$tm1,1} . "_" . $helixname{$tm2,2};

	$energyp=$prefix . "." . $struct . ".combirot_mpsimE.out";
 
        open (ENER,$energyp);
        $nline=0;
        while ($lines = <ENER>) {
            $nline++;
            chomp ($lines);
            @strenergy = split(/\s+/, $lines);
            $tot_aa_intra=$strenergy[0];
            $tot_bb_intra=$strenergy[1];
            $tot_ab_inter=$strenergy[2];
            $tot_all=$strenergy[3];
            $vdw_aa_intra=$strenergy[4];
            $vdw_bb_intra=$strenergy[5];
            $vdw_ab_inter=$strenergy[6];
            $tot_novdw=$strenergy[7];
            $hbe_ab_inter=$strenergy[8];
            if ($nline == 1) {
    printf OUT1 "%5i%5i %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f\n",$helixname{$tm1,1},$helixname{$tm2,2},$tot_aa_intra,$tot_bb_intra,$tot_ab_inter,$tot_all,$vdw_aa_intra,$vdw_bb_intra,$vdw_ab_inter,$tot_novdw,$hbe_ab_inter;
            } elsif ($nline == 2) {
    printf OUT2 "%5i%5i %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f\n",$helixname{$tm1,1},$helixname{$tm2,2},$tot_aa_intra,$tot_bb_intra,$tot_ab_inter,$tot_all,$vdw_aa_intra,$vdw_bb_intra,$vdw_ab_inter,$tot_novdw,$hbe_ab_inter;
            }
        }
        close ENER;

}
}
close OUT1;
close OUT2;
if ($nline < 2) { unlink("$outfile2"); }

