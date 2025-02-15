#!/usr/bin/perl -w

($#ARGV >=0 ) or die "Program to pull out protein energy after SCREAM from memb_scream output.\n Usage: get_scream_output_combi.pl protein_prefix\n Output: prefix_combirot_scream.out.\n";

$prefix = $ARGV[0];
$helix_i = $ARGV[1];
$helix_j = $ARGV[2];

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

$tmi = "tm$helix_i";
$tmj = "tm$helix_j";

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

$struct0 = $helixname{$tm1,1} . "_" . $helixname{$tm2,2} . "_" . $helixname{$tm3,3} . "_" . $helixname{$tm4,4} . "_" . $helixname{$tm5,5} . "_" . $helixname{$tm6,6} . "_" . $helixname{$tm7,7};

$angi = $helixname{$$tmi,$helix_i};
$angj = $helixname{$$tmj,$helix_j};
$struct1 = $angi . "_" . $angj;

$file0 = $prefix . "." . $struct0 . ".combirot.bgf";
$file1 = $prefix . "." . $struct1 . ".combirot.bgf";

system("mv -f $file0 $file1");

}
}
}
}
}
}
}
