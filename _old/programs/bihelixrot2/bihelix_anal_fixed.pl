#!/usr/local/bin/perl -w

$prefix = $ARGV[0];
$nostruc = $ARGV[1];
$spe = $ARGV[2];

if (!$prefix | !$nostruc)
{die "\nProgram to analyze output from bihelixrot_scream.
October 2, 2007 Jenelle Bray (jenelle@wag.caltech.edu)

Usage: bihelix_anal.pl {prefix} {number of outputted structures} {specific structures}

Example: bihelix_anal.pl 5ht2b 100 \"0_0_0_0_0_0_0 180_30_60_0_150_30_90\"

This script will calculate the total energy (TotalE), the energy excluding van 
der Waals (NoAllVDW), and the energy excluding interhelical van der Waals 
(NoInterHelVDW) of all 12^7 structures whose pairwise energies were calculated 
with the bihelixrot_scream script.  The prefix is the prefix from the protein 
bgf file whose helices were rotated.  This script will access all 12 directories
created by bihelixrot_scream, so it must be run in the directory where these 12
directories are found.  It will output the best user specified number of 
outputted structures by each type of energy.  In addition, it will calculate the
energy of any specific structures specified by the user even if they are not in
the top structures.  The specific structures must be inputted in the form 
\"0_0_0_0_0_0_0 90_0_300_150_0_30_60 30_60_120_150_0_0_300\"       

Output: prefix.bihelix_TotalE.out
	prefix.bihelix_NoInterHelVDW.out
	prefix.bihelix_NoAllVDW.out
	prefix.bihelix_specific.out
	
These contain the top user specified number of structures by each type of energy
in addition to the interhelical hydrogen bond energy.  The energies of any user
specified structures are given in prefix.bihelix_specific.out bond energies of 
any specified structures.\n"
}

@specs = split / +/, $spe;

$f1_2_d = $prefix . "_H1-H2_bihelixrot";
$f1_2_dir = <$f1_2_d*/>;
chomp $f1_2_dir;
chdir($f1_2_dir);
$f1_2 = $prefix . "_H1-H2_bihelixrot_scream.out";
if (! -e $f1_2)
{die "File $f1_2 cannot be found \n"}
open (F12, "<$f1_2");
@f12 = <F12>;
close (F12);
chdir("..");

$f1_7_d = $prefix . "_H1-H7_bihelixrot";
$f1_7_dir = <$f1_7_d*/>;
chomp $f1_7_dir;
chdir($f1_7_dir);
$f1_7 = $prefix . "_H1-H7_bihelixrot_scream.out";
if (! -e $f1_7)
{die "File $f1_7 cannot be found \n"}
open (F17, "<$f1_7");
@f17 = <F17>;
close (F17);
chdir("..");

$f2_3_d = $prefix . "_H2-H3_bihelixrot";
$f2_3_dir = <$f2_3_d*/>;
chomp $f2_3_dir;
chdir($f2_3_dir);
$f2_3 = $prefix . "_H2-H3_bihelixrot_scream.out";
if (! -e $f2_3)
{die "File $f2_3 cannot be found \n"}
open (F23, "<$f2_3");
@f23 = <F23>;
close (F23);
chdir("..");

$f2_4_d = $prefix . "_H2-H4_bihelixrot";
$f2_4_dir = <$f2_4_d*/>;
chomp $f2_4_dir;
chdir($f2_4_dir);
$f2_4 = $prefix . "_H2-H4_bihelixrot_scream.out";
if (! -e $f2_4)
{die "File $f2_4 cannot be found \n"}
open (F24, "<$f2_4");
@f24 = <F24>;
close (F24);
chdir("..");

$f2_7_d = $prefix . "_H2-H7_bihelixrot";
$f2_7_dir = <$f2_7_d*/>;
chomp $f2_7_dir;
chdir($f2_7_dir);
$f2_7 = $prefix . "_H2-H7_bihelixrot_scream.out";
if (! -e $f2_7)
{die "File $f2_7 cannot be found \n"}
open (F27, "<$f2_7");
@f27 = <F27>;
close (F27);
chdir("..");

$f3_4_d = $prefix . "_H3-H4_bihelixrot";
$f3_4_dir = <$f3_4_d*/>;
chomp $f3_4_dir; 
chdir($f3_4_dir);
$f3_4 = $prefix . "_H3-H4_bihelixrot_scream.out";
if (! -e $f3_4)
{die "File $f3_4 cannot be found \n"}
open (F34, "<$f3_4");
@f34 = <F34>;
close (F34);
chdir("..");

$f3_5_d = $prefix . "_H3-H5_bihelixrot";
$f3_5_dir = <$f3_5_d*/>;
chomp $f3_5_dir;
chdir($f3_5_dir);
$f3_5 = $prefix . "_H3-H5_bihelixrot_scream.out";
if (! -e $f3_5)
{die "File $f3_5 cannot be found \n"}
open (F35, "<$f3_5");
@f35 = <F35>;
close (F35);
chdir("..");

$f3_6_d = $prefix . "_H3-H6_bihelixrot";
$f3_6_dir = <$f3_6_d*/>;
chomp $f3_6_dir;
chdir($f3_6_dir);
$f3_6 = $prefix . "_H3-H6_bihelixrot_scream.out";
if (! -e $f3_6)
{die "File $f3_6 cannot be found \n"}
open (F36, "<$f3_6");
@f36 = <F36>;
close (F36);
chdir("..");

$f3_7_d = $prefix . "_H3-H7_bihelixrot";
$f3_7_dir = <$f3_7_d*/>;
chomp $f3_7_dir;
chdir($f3_7_dir);
$f3_7 = $prefix . "_H3-H7_bihelixrot_scream.out";
if (! -e $f3_7)
{die "File $f3_7 cannot be found \n"}
open (F37, "<$f3_7");
@f37 = <F37>;
close (F37);
chdir("..");

$f4_5_d = $prefix . "_H4-H5_bihelixrot";
$f4_5_dir = <$f4_5_d*/>;
chomp $f4_5_dir;
chdir($f4_5_dir);
$f4_5 = $prefix . "_H4-H5_bihelixrot_scream.out";
if (! -e $f4_5)
{die "File $f4_5 cannot be found \n"}
open (F45, "<$f4_5");
@f45 = <F45>;
close (F45);
chdir("..");

$f5_6_d = $prefix . "_H5-H6_bihelixrot";
$f5_6_dir = <$f5_6_d*/>;
chomp $f5_6_dir;
chdir($f5_6_dir);
$f5_6 = $prefix . "_H5-H6_bihelixrot_scream.out";
if (! -e $f5_6)
{die "File $f5_6 cannot be found \n"}
open (F56, "<$f5_6");
@f56 = <F56>;
close (F56);
chdir("..");

$f6_7_d = $prefix . "_H6-H7_bihelixrot";
$f6_7_dir = <$f6_7_d*/>;
chomp $f6_7_dir;
chdir($f6_7_dir);
$f6_7 = $prefix . "_H6-H7_bihelixrot_scream.out";
if (! -e $f6_7)
{die "File $f6_7 cannot be found \n"}
open (F67, "<$f6_7");
@f67 = <F67>;
close (F67);
chdir("..");

@f1 = (1,1,2,2,2,3,3,3,3,4,5,6);
@f2 = (2,7,3,4,7,4,5,6,7,5,6,7);

for ($m = 0; $m < 12; $m++)
{
$n1 = $f1[$m] . $f2[$m];
$n2 = $f2[$m] . $f1[$m];

$file = f . $f1[$m] . $f2[$m]; 

foreach $line (@$file)
{
if ($line !~ /Intra/)
	{
	$an2 = a . $f2[$m];
        $an1 = a . $f1[$m];
	($sp,$$an1,$$an2,$intr1,$intr2,$inter,$tot1,$intr1v,$intr2v,$interv,$totnov,$interh) = split / +/, $line;
	($tot,$line) = split /\n/, $totl;
	$func = tot . $n1 . "_$$an1";
	$func2 = tot . $n2 . "_$$an2";
	$funb = intr . $n1 . "_$$an1";
	$funb2 = intr . $n2 . "_$$an2";

	$funh = hbon . $n1 . "_$$an1";
	$funh2 = hbon . $n2 . "_$$an2";

	$funcv = totv . $n1 . "_$$an1";
        $func2v = totv . $n2 . "_$$an2";
        $funbv = intrv . $n1 . "_$$an1";
        $funb2v = intrv . $n2 . "_$$an2";
 
	$$func{$$an2} = $inter;
	$$func2{$$an1} = $inter;
	$$funb{$$an2} = $intr1;
	$$funb2{$$an1} = $intr2;

	$$funh{$$an2} = $interh;
	$$funh2{$$an1} = $interh;

	$$funcv{$$an2} = $inter - $interv;
        $$func2v{$$an1} = $inter - $interv;
        $$funbv{$$an2} = $intr1 - $intr1v;
        $$funb2v{$$an1} = $intr2 - $intr2v;
	}
} 
}

@anglex = keys (%$func);
@angles = sort { $a <=> $b } @anglex;

$nost = 12;
$j = 0;
for ($tm1 = 0; $tm1 < $nost; $tm1++)
{
for ($tm2 = 0; $tm2 < $nost; $tm2++)
{
for ($tm3 = 0; $tm3 < $nost; $tm3++)
{
for ($tm4 = 0; $tm4 < $nost; $tm4++)
{
for ($tm5 = 0; $tm5 < $nost; $tm5++) 
{
for ($tm6 = 0; $tm6 < $nost; $tm6++)
{
for ($tm7 = 0; $tm7 < $nost; $tm7++)
{
	$j++;
	$tm1a = $angles[$tm1];
	$tm2a = $angles[$tm2];
	$tm3a = $angles[$tm3];
	$tm4a = $angles[$tm4];
	$tm5a = $angles[$tm5];
	$tm6a = $angles[$tm6];
	$tm7a = $angles[$tm7];

	$fc32 = tot32 . "_$tm3a";
	$fc34 = tot34 . "_$tm3a";
	$fc35 = tot35 . "_$tm3a";
	$fc36 = tot36 . "_$tm3a";
	$fc37 = tot37 . "_$tm3a";
	$fc71 = tot71 . "_$tm7a";
	$fc72 = tot72 . "_$tm7a";
	$fc76 = tot76 . "_$tm7a";
	$fc12 = tot12 . "_$tm1a";
	$fc65 = tot65 . "_$tm6a";
	$fc24 = tot24 . "_$tm2a";
	$fc54 = tot54 . "_$tm5a";

	$fh32 = hbon32 . "_$tm3a";
        $fh34 = hbon34 . "_$tm3a";
        $fh35 = hbon35 . "_$tm3a";
        $fh36 = hbon36 . "_$tm3a";
        $fh37 = hbon37 . "_$tm3a";
        $fh71 = hbon71 . "_$tm7a";
        $fh72 = hbon72 . "_$tm7a";
        $fh76 = hbon76 . "_$tm7a";
        $fh12 = hbon12 . "_$tm1a";
        $fh65 = hbon65 . "_$tm6a";
        $fh24 = hbon24 . "_$tm2a";
        $fh54 = hbon54 . "_$tm5a";

	$fv32 = totv32 . "_$tm3a";
        $fv34 = totv34 . "_$tm3a";
        $fv35 = totv35 . "_$tm3a";
        $fv36 = totv36 . "_$tm3a";
        $fv37 = totv37 . "_$tm3a";
        $fv71 = totv71 . "_$tm7a";
        $fv72 = totv72 . "_$tm7a";
        $fv76 = totv76 . "_$tm7a";
        $fv12 = totv12 . "_$tm1a";
        $fv65 = totv65 . "_$tm6a";
	$fv24 = totv24 . "_$tm2a";
        $fv54 = totv54 . "_$tm5a";

	$fb12 = intr12 . "_$tm1a"; 
	$fb17 = intr17 . "_$tm1a";
	$tot_1 = ($$fb12{$tm2a} + $$fb17{$tm7a})/2;

	$fbv12 = intrv12 . "_$tm1a";
        $fbv17 = intrv17 . "_$tm1a";
        $totv_1 = ($$fbv12{$tm2a} + $$fbv17{$tm7a})/2;

	$fb21 = intr21 . "_$tm2a";
	$fb23 = intr23 . "_$tm2a";
	$fb24 = intr24 . "_$tm2a";
	$fb27 = intr27 . "_$tm2a";
	$tot_2 = ($$fb21{$tm1a} + $$fb23{$tm3a} + $$fb24{$tm4a} +$$fb27{$tm7a})/4;

	$fbv21 = intrv21 . "_$tm2a";
        $fbv23 = intrv23 . "_$tm2a";
        $fbv24 = intrv24 . "_$tm2a";
        $fbv27 = intrv27 . "_$tm2a";
        $totv_2 = ($$fbv21{$tm1a} + $$fbv23{$tm3a} + $$fbv24{$tm4a} + $$fbv27{$tm7a})/4;

	$fb32 = intr32 . "_$tm3a";
	$fb34 = intr34 . "_$tm3a";
	$fb35 = intr35 . "_$tm3a";
	$fb36 = intr36 . "_$tm3a";
	$fb37 = intr37 . "_$tm3a";
	$tot_3 = ($$fb32{$tm2a} + $$fb34{$tm4a} + $$fb35{$tm5a} + $$fb36{$tm6a} + $$fb37{$tm7a})/5;

	$fbv32 = intrv32 . "_$tm3a";
        $fbv34 = intrv34 . "_$tm3a";
        $fbv35 = intrv35 . "_$tm3a";
        $fbv36 = intrv36 . "_$tm3a";
        $fbv37 = intrv37 . "_$tm3a";
        $totv_3 = ($$fbv32{$tm2a} + $$fbv34{$tm4a} + $$fbv35{$tm5a} + $$fbv36{$tm6a} + $$fbv37{$tm7a})/5;

	$fb42 = intr42 . "_$tm4a";
	$fb43 = intr43 . "_$tm4a";
	$fb45 = intr45 . "_$tm4a"; 
	$tot_4 = ($$fb42{$tm2a} + $$fb43{$tm3a} + $$fb45{$tm5a})/3;

	$fbv42 = intrv42 . "_$tm4a";
        $fbv43 = intrv43 . "_$tm4a";
        $fbv45 = intrv45 . "_$tm4a";
        $totv_4 = ($$fbv42{$tm2a} + $$fbv43{$tm3a} + $$fbv45{$tm5a})/3;

	$fb53 = intr53 . "_$tm5a";
	$fb54 = intr54 . "_$tm5a";
	$fb56 = intr56 . "_$tm5a";
	$tot_5 = ($$fb53{$tm3a} + $$fb54{$tm4a} + $$fb56{$tm6a})/3;

	$fbv53 = intrv53 . "_$tm5a";
        $fbv54 = intrv54 . "_$tm5a";
        $fbv56 = intrv56 . "_$tm5a";
        $totv_5 = ($$fbv53{$tm3a} + $$fbv54{$tm4a} + $$fbv56{$tm6a})/3;

	$fb63 = intr63 . "_$tm6a";
	$fb65 = intr65 . "_$tm6a";
	$fb67 = intr67 . "_$tm6a";
	$tot_6 = ($$fb63{$tm3a} + $$fb65{$tm5a} + $$fb67{$tm7a})/3;

	$fbv63 = intrv63 . "_$tm6a";
        $fbv65 = intrv65 . "_$tm6a";
        $fbv67 = intrv67 . "_$tm6a";
        $totv_6 = ($$fbv63{$tm3a} + $$fbv65{$tm5a} + $$fbv67{$tm7a})/3;

	$fb71 = intr71 . "_$tm7a";
	$fb72 = intr72 . "_$tm7a";
	$fb73 = intr73 . "_$tm7a";
	$fb76 = intr76 . "_$tm7a";
	$tot_7 = ($$fb71{$tm1a} + $$fb72{$tm2a} + $$fb73{$tm3a} + $$fb76{$tm6a})/4;
	 
	$fbv71 = intrv71 . "_$tm7a";
        $fbv72 = intrv72 . "_$tm7a";
        $fbv73 = intrv73 . "_$tm7a";
        $fbv76 = intrv76 . "_$tm7a";
        $totv_7 = ($$fbv71{$tm1a} + $$fbv72{$tm2a} + $$fbv73{$tm3a} + $$fbv76{$tm6a})/4;

	$fudge = $j * 0.00000001;

	$tot_al = $$fc32{$tm2a} + $$fc34{$tm4a} + $$fc35{$tm5a} + $$fc36{$tm6a} + $$fc37{$tm7a} + $$fc71{$tm1a} + $$fc72{$tm2a} + $$fc76{$tm6a} + $$fc12{$tm2a} + $$fc65{$tm5a} + $$fc24{$tm4a} + $$fc54{$tm4a} - $fudge;
	$tot_all = $tot_al + $tot_1 + $tot_2 + $tot_3 + $tot_4 + $tot_5 + $tot_6 + $tot_7;

	$tot_alv = $$fv32{$tm2a} + $$fv34{$tm4a} + $$fv35{$tm5a} + $$fv36{$tm6a} + $$fv37{$tm7a} + $$fv71{$tm1a} + $$fv72{$tm2a} + $$fv76{$tm6a} + $$fv12{$tm2a} + $$fv65{$tm5a} + $$fv24{$tm4a} + $$fv54{$tm4a} - $fudge;
        $tot_allv = $tot_alv + $totv_1 + $totv_2 + $totv_3 + $totv_4 + $totv_5 + $totv_6 + $totv_7;

	$tot_some = $tot_alv + $tot_1 + $tot_2 + $tot_3 + $tot_4 + $tot_5 + $tot_6 + $tot_7;

	$hbond = $$fh32{$tm2a} + $$fh34{$tm4a} + $$fh35{$tm5a} + $$fh36{$tm6a} + $$fh37{$tm7a} + $$fh71{$tm1a} + $$fh72{$tm2a} + $$fh76{$tm6a} + $$fh12{$tm2a} + $$fh65{$tm5a} + $$fh24{$tm4a} + $$fh54{$tm4a} - $fudge;
	$strc = $tm1a . "_$tm2a" . "_$tm3a" . "_$tm4a" . "_$tm5a" . "_$tm6a" . "_$tm7a";
	foreach $spec (@specs)
	{
		if ($strc eq $spec)
		{
			$tot_all_sp{$spec} = $tot_all;
			$tot_allv_sp{$spec} = $tot_allv;
			$tot_some_sp{$spec} = $tot_some;
			$hbond_sp{$spec} = $hbond;
		}
	} 	

	if ($j <= $nostruc)
	{
		$tot_all{$strc} = $tot_all;
		$tot_allx{$strc} = $tot_all;
		$tot_alls{$strc} = $tot_all;
		$tot_allv{$strc} = $tot_allv;
		$tot_allvx{$strc} = $tot_allv;
		$tot_allvs{$strc} = $tot_allv;
		$tot_some{$strc} = $tot_some;
		$tot_somex{$strc} = $tot_some;
		$tot_somev{$strc} = $tot_some;
		$hbond{$strc} = $hbond;
		$hbondv{$strc} = $hbond;
		$hbonds{$strc} = $hbond;
		$struc{$tot_all{$strc}} = $strc;
		$strucv{$tot_allv{$strc}} = $strc;
		$strucs{$tot_some{$strc}} = $strc;
	}
	
	if ($j eq $nostruc)
	{
		@energ = values (%tot_all);
		@energv = values (%tot_allv);
		@energs = values (%tot_some);
		@energy = reverse sort { $a <=> $b } @energ;
		@energyv = reverse sort { $a <=> $b } @energv;
		@energys = reverse sort { $a <=> $b } @energs;
		$max = $energy[0];
		$maxv = $energyv[0];
		$maxs = $energys[0];
		$maxstr = $struc{$max};
		$maxstrv = $strucv{$maxv};
		$maxstrs = $strucs{$maxs};
	} 

	if ($j > $nostruc && $tot_all < $max)
	{
		$tot_all{$strc} = $tot_all;
		$tot_allvx{$strc} = $tot_allv;
		$tot_somex{$strc} = $tot_some;
		$hbond{$strc} = $hbond;
		$struc{$tot_all{$strc}} = $strc;
		delete $tot_all{$maxstr};
		delete $tot_allvx{$maxstr};
		delete $tot_somex{$maxstr};
		delete $hbond{$maxstr};
		delete $struc{$max};
		@energ = values (%tot_all);
                @energy = reverse sort { $a <=> $b } @energ;
                $max = $energy[0];
                $maxstr = $struc{$max};
	}

	if ($j > $nostruc && $tot_allv < $maxv)
        {
                $tot_allv{$strc} = $tot_allv;
		$tot_allx{$strc} = $tot_all;
		$tot_somev{$strc} = $tot_some;
                $hbondv{$strc} = $hbond;
                $strucv{$tot_allv{$strc}} = $strc;
                delete $tot_allv{$maxstrv};
		delete $tot_allx{$maxstrv};
		delete $tot_somev{$maxstrv};
                delete $hbondv{$maxstrv};
                delete $strucv{$maxv};
                @energv = values (%tot_allv);
                @energyv = reverse sort { $a <=> $b } @energv;
                $maxv = $energyv[0];
                $maxstrv = $strucv{$maxv};
        }

	if ($j > $nostruc && $tot_some < $maxs)
        {
                $tot_allvs{$strc} = $tot_allv;
                $tot_alls{$strc} = $tot_all;
                $tot_some{$strc} = $tot_some;
                $hbonds{$strc} = $hbond;
                $strucs{$tot_some{$strc}} = $strc;
                delete $tot_allvs{$maxstrs};
                delete $tot_alls{$maxstrs};
                delete $tot_some{$maxstrs};
                delete $hbonds{$maxstrs};
                delete $strucs{$maxs};
                @energs = values (%tot_some);
                @energys = reverse sort { $a <=> $b } @energs;
                $maxs = $energys[0];
                $maxstrs = $strucs{$maxs};
        }

}
}
}
}
}
}
}

@energyx = sort { $a <=> $b } @energy;
@energyxv = sort { $a <=> $b } @energyv;
@energyxs = sort { $a <=> $b } @energys;

$outx1 = $prefix . ".bihelix_TotalE.out";
open (OUT1,">$outx1");
$outx2 = $prefix . ".bihelix_NoInterHelVDW.out";
open (OUT2,">$outx2");
$outx3 = $prefix . ".bihelix_NoAllVDW.out";
open (OUT3,">$outx3");

if ($spe)
{
$outx4 = $prefix . ".bihelix_specific.out";
open (OUT4,">$outx4");
}

print OUT1 "                                    Ordered by\n";
print OUT1 "                    Structure         TotalE     NoInterHelVDW     NoAllVDW        InterHB\n";

print OUT2 "                                                  Ordered by\n";
print OUT2 "                    Structure         TotalE     NoInterHelVDW     NoAllVDW        InterHB\n";

print OUT3 "                                                                  Ordered by\n";
print OUT3 "                    Structure         TotalE     NoInterHelVDW     NoAllVDW        InterHB\n";

if ($spe)
{
print OUT4 "                    Structure         TotalE     NoInterHelVDW     NoAllVDW        InterHB\n";
}

foreach $energyx (@energyx)
{
	$energyr = sprintf("%.1f",$energyx);
	$energyvxr = sprintf("%.1f",$tot_allvx{$struc{$energyx}});  
	$energysxr = sprintf("%.1f",$tot_somex{$struc{$energyx}});
	$hbondx = sprintf("%.1f",$hbond{$struc{$energyx}});
	printf OUT1 "%29s %14.1f %14.1f %14.1f %14.1f\n",$struc{$energyx},$energyr,$energysxr,$energyvxr,$hbondx;
}

foreach $energyxs (@energyxs)
{
        $energyss = sprintf("%.1f",$energyxs);
        $energyssx = sprintf("%.1f",$tot_alls{$strucs{$energyxs}});
        $energyssv = sprintf("%.1f",$tot_allvs{$strucs{$energyxs}});
        $hbondss = sprintf("%.1f",$hbonds{$strucs{$energyxs}});
        printf OUT2 "%29s %14.1f %14.1f %14.1f %14.1f\n",$strucs{$energyxs},$energyssx,$energyss,$energyssv,$hbondss;
}

foreach $energyxv (@energyxv)
{
        $energyvr = sprintf("%.1f",$energyxv);
        $energyxx = sprintf("%.1f",$tot_allx{$strucv{$energyxv}});
        $energyvs = sprintf("%.1f",$tot_somev{$strucv{$energyxv}});
        $hbondxx = sprintf("%.1f",$hbondv{$strucv{$energyxv}});
        printf OUT3 "%29s %14.1f %14.1f %14.1f %14.1f\n",$strucv{$energyxv},$energyxx,$energyvs,$energyvr,$hbondxx;
}

if ($spe)
{
foreach $spec (@specs)
{
	$nrgx = sprintf("%.1f",$tot_all_sp{$spec});
	$nrgvx = sprintf("%.1f",$tot_allv_sp{$spec});
	$nrgs = sprintf("%.1f",$tot_some_sp{$spec});
	$hbonx = sprintf("%.1f",$hbond_sp{$spec});
	printf OUT4 "%29s %14.1f %14.1f %14.1f %14.1f\n",$spec,$nrgx,$nrgs,$nrgvx,$hbonx;
}
}
