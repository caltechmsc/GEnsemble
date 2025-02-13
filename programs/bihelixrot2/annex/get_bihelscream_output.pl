#!/usr/bin/perl -w

($#ARGV >=0 ) or die "Program to pull out protein energy after SCREAM from memb_scream output.\n Usage: get_scream_output_combi.pl protein_prefix\n Output: prefix_combirot_scream.out.\n";

$prefix = $ARGV[0];
$helix_i = $ARGV[1];
$helix_j = $ARGV[2];
$outfile = $prefix."_H".$helix_i."-H".$helix_j."_bihelixrot_scream.out";
open (OUT, ">".$outfile);

$title = "   H${helix_i}   H${helix_j}  Tot_${helix_i}${helix_i}_Intra  Tot_${helix_j}${helix_j}_Intra  Tot_${helix_i}${helix_j}_Inter  TotalE_H${helix_i}-H${helix_j}  VDW_${helix_i}${helix_i}_Intra  VDW_${helix_j}${helix_j}_Intra  VDW_${helix_i}${helix_j}_Inter  NoVDWE_H${helix_i}-H${helix_j}  HBE_${helix_i}${helix_j}_Inter\n";

printf OUT $title;

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

	$energyp=$prefix . "." . $struct . ".combirot_BiHelical-E.txt";
 
        open (ENER,$energyp);
        readline(ENER);
        while ($lines = <ENER>) {
            chomp ($lines);
            @strenergy = split(/\s+/, $lines);
            $tot_aa_intra=$strenergy[1];
            $tot_bb_intra=$strenergy[6];
            $tot_ab_inter=$strenergy[11];
            $tot_all=$strenergy[15];
            $vdw_aa_intra=$strenergy[3];
            $vdw_bb_intra=$strenergy[8];
            $vdw_ab_inter=$strenergy[12];
            $tot_vdw=$vdw_aa_intra+$vdw_bb_intra+$vdw_ab_inter;
            $tot_novdw=$tot_all-$tot_vdw;
            $hbe_ab_inter=$strenergy[14];
        }
        close ENER;
    printf OUT "%5i%5i %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f\n",$helixname{$tm1,1},$helixname{$tm2,2},$tot_aa_intra,$tot_bb_intra,$tot_ab_inter,$tot_all,$vdw_aa_intra,$vdw_bb_intra,$vdw_ab_inter,$tot_novdw,$hbe_ab_inter;

}
}
