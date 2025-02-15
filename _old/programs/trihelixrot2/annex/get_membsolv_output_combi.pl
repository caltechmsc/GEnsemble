#!/usr/bin/perl -w

($#ARGV >=0 ) or die "Program to pull out membrane solvation numbers from memb_scream output.\n Usage: get_membsolv_output.pl protein_prefix iscream\n Output: prefix_combirot_membsolv.out.\n";

$prefix = $ARGV[0];
$iscream = $ARGV[1];
$outfile = "$prefix"."combirot_membsolv.out";
open (OUT, ">".$outfile);
printf OUT "  H1  H2  H3  H4  H5  H6  H7   PolMemb5(E1)   PolWater(E2)   NonPolar(E3)   E1-E2+E3(Es)\n";

my $memb5;
my $water;
my $nonpol;
my $fscream;

if ($iscream == 1) {
    $fscream = "scream_";
} else {
    $fscream = "";
}

$dir1 = "membsolv_combi";
chdir($dir1) || die "cannot enter dir\n";
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

$dirmemb=$prefix . "." . $struct . ".combirot_" . "$fscream" . "memb5";
chdir($dirmemb);
$filememb5=$prefix . "." . $struct . ".combirot_" . "$fscream" . "memb5_delphi.out";
open (MEMB,$filememb5);
   while ($lines = <MEMB>) {
       chomp ($lines);
       if ($lines =~ /corr/) {
         @strmemb = split(/ /, $lines);
         $memb5 = $strmemb[7]*0.5925;
}
}
   close MEMB;

   chdir("..");
   $dirwater=$prefix . "." . $struct . ".combirot_" . "$fscream" . "water";
   chdir($dirwater);
   $filewater=$prefix . "." . $struct . ".combirot_" . "$fscream" . "water_delphi.out";
   open (WATER,$filewater);
     while ($lines = <WATER>) {
       chomp ($lines);
       if ($lines =~/corr/) {
         @strwater = split(/ /, $lines);
         $water = $strwater[7] * 0.5925;
       }
     }
   close WATER;

   chdir("..");
   $dirnonpol=$prefix . "." . $struct . ".combirot_" . "$fscream" . "nonpol";
   chdir($dirnonpol);

     $filenonpol=$prefix . "." . $struct . ".combirot_" . "$fscream" . "nonpol.out";
   open (NONPOL,$filenonpol);
      while ($lines = <NONPOL>) {
      chomp ($lines);
       if ($lines =~/Energy/) {
         @strnonpol = split(/ /, $lines);
         $nonpol= $strnonpol[8];
       }
     }
    close NONPOL;

     chdir("..");
     $Es=$memb5-$water+$nonpol;
   printf OUT "%4i%4i%4i%4i%4i%4i%4i%15.1f%15.1f%15.1f%15.1f\n",$helixname{$tm1,1},$helixname{$tm2,2},$helixname{$tm3,3},$helixname{$tm4,4},$helixname{$tm5,5},$helixname{$tm6,6},$helixname{$tm7,7},$memb5,$water,$nonpol,$Es;

}
}
}
}
}
}
}
