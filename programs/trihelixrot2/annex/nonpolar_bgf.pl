#!/usr/bin/perl

use File::Basename;
use FindBin ();
use lib "$FindBin::Bin";

$sbin = $FindBin::Bin;

$bgf = $ARGV[0];

if ($bgf !~ /bgf/)
{die "\nThis program calculates the nonpolar solvation of the insertion of a
protein, oriented along the z-axis, into an implicit lipid bilayer.

Usage: /ul/jenelle/codes/other/nonpolar.pl <pdb file>

Required input files: pdb file, HPMCenter.txt\n
"}

$defaultsfile = "${sbin}/../../.gensemble/.bihelix";
open DEF, "<$defaultsfile";
while (<DEF>) {
    if (/^scream_dir\s+(\S+)/)            { $scream_dir        = $1; }
    elsif (/^ff\s+(\S+)/)                 { $ff                = $1; }
    elsif (/^mpsim_data\s+(\S+)/)         { $mpsim_data        = $1; }
#   elsif (/^mpsim_executable\s+(\S+)/)   { $mpsim_executable  = $1; }
    elsif (/^python_executable\s+(\S+)/)  { $python_executable = $1; }
}
close DEF;

################################################################################
##### loadScream                                                           #####
################################################################################
    $ENV{INSTALL_PATH}               = "${sbin}/../../$scream_dir";
    $ENV{SCREAM_MAIN_SCRIPT_PATH}    = "$ENV{INSTALL_PATH}/scripts/";
    $ENV{SCREAM_LIB_PATH}            = "$ENV{INSTALL_PATH}/lib/v3.0/Clustered/lib/";
    $ENV{SCWRL_LIB_PATH}             = "$ENV{INSTALL_PATH}/lib/v3.0/SCWRL/lib/";
    $ENV{SCREAM_CNN_PATH}            = "$ENV{INSTALL_PATH}/lib/v3.0/NtrlAARotConn/";
    $ENV{SCREAM_DELTA_PAR_FILE_PATH} = "$ENV{INSTALL_PATH}/lib/SCREAM_delta_par_files/";
    $ENV{FORCE_FIELD_FILE}           = "${sbin}/../../$ff";
    $ENV{PYTHON_EXE}                 = "${sbin}/../../$python_executable";

    $ENV{PYTHONPATH} =
          "${sbin}/../../$scream_dir/SCREAM/swig/python/build/lib.linux-i686-2.3/".
    ":" . "${sbin}/../../$scream_dir/SCREAM/python/app/".
    ":" . "${sbin}/../../$scream_dir/PythonDeps/";

    $ENV{MPSIM_DATA} = "${sbin}/../../$mpsim_data";
###
# END loadSCREAM
###
$python_exe = "$ENV{PYTHON_EXE}";

$rad_lip = 1.4;
$rad_head = 2.0;
$rad_wat = 1.4;
$dist_lip = 15;
$dist_head = 15;

open (PROG, "<$sbin/Surface_Area_By_Residue.py");
@prog=<PROG>;
close (PROG);

open (PROGWAT, ">Surface_Area_By_Residue_wat.py");
open (PROGHEAD, ">Surface_Area_By_Residue_head.py");
open (PROGLIP, ">Surface_Area_By_Residue_lip.py");

foreach $progline (@prog)
{
        if ($progline =~ /fsm-linux/ && $progline =~ /structure_file/)
        {
        print PROGWAT "    os.system('$sbin/fsm-linux -s ' + structure_file + ' -f ' + forcefield_file + ' -r $rad_wat ' + ' -v 1 > ' + fsm_output_file)\n";
        print PROGHEAD "    os.system('$sbin/fsm-linux -s ' + structure_file + ' -f ' + forcefield_file + ' -r $rad_head ' + ' -v 1 > ' + fsm_output_file)\n";
        print PROGLIP "    os.system('$sbin/fsm-linux -s ' + structure_file + ' -f ' + forcefield_file + ' -r $rad_lip ' + ' -v 1 > ' + fsm_output_file)\n";
        }
        else
        {
        print PROGWAT "$progline";
        print PROGHEAD "$progline";
        print PROGLIP "$progline";
        }
}

close (PROGWAT);
close (PROGHEAD);
close (PROGLIP);

system ("chmod u+x Surface_Area_By_Residue_wat.py");
system ("chmod u+x Surface_Area_By_Residue_head.py");
system ("chmod u+x Surface_Area_By_Residue_lip.py");

($prefix,$stuff) = split /\.bgf/, $bgf;

system ("$sbin/fixchains.pl $bgf");

system ("$python_exe Surface_Area_By_Residue_wat.py $bgf > sasa_wat.out");
system ("mv tmp16584.fsm.out area_wat.out");
system ("$python_exe Surface_Area_By_Residue_head.py $bgf > sasa_head.out");
system ("mv tmp16584.fsm.out area_head.out");
system ("$python_exe Surface_Area_By_Residue_lip.py $bgf > sasa_lip.out");
system ("mv tmp16584.fsm.out area_lip.out");

open (BGF, "<$bgf");
@bgf=<BGF>;
close (BGF);

$atoms = 0;
foreach $bgfline (@bgf)
{
	if ($bgfline =~ /ATOM/ && $bgfline !~ /FORMAT/)
	{
	$atoms++;
	($atom,$atno,$type,$res,$chain,$resno,$xx,$yy,$zz,$rest) = split /\ +/, $bgfline;
	$zz[$atno] = $zz;
	$type[$atno] = $type;
	$res[$atno] = $res;
	$chain[$atno] = $chain;
	$resno[$atno] = $resno;
	}
}

open (AWAT, "<area_wat.out");
@awat=<AWAT>;
close (AWAT);
open (AHEAD, "<area_head.out");
@ahead=<AHEAD>;
close (AHEAD);
open (ALIP, "<area_lip.out");
@alip=<ALIP>;
close (ALIP);

foreach $awatline (@awat)
{
	if ($awatline =~ /Atom/ && $awatline !~ /Breakdown/)
	{
	($at,$atno,$ar,$area_wat) = split /\ +/, $awatline;
	$area_wat[$atno] = $area_wat;
	}
}

foreach $aheadline (@ahead)
{
        if ($aheadline =~ /Atom/ && $aheadline !~ /Breakdown/)
        {
        ($at,$atno,$ar,$area_head) = split /\ +/, $aheadline;
        $area_head[$atno] = $area_head;
        }
}

foreach $alipline (@alip)
{
        if ($alipline =~ /Atom/ && $alipline !~ /Breakdown/)
        {
        ($at,$atno,$ar,$area_lip) = split /\ +/, $alipline;
        $area_lip[$atno] = $area_lip;
        }
}

for ($i = 1; $i < $atoms + 1; $i++)
{
	if (abs $zz[$i] < $dist_lip)
	{
	$area_tot_lip = $area_tot_lip + $area_lip[$i];
	}
	if (abs $zz[$i] > $dist_lip && abs $zz[$i] < $dist_head)
	{
	$area_tot_head = $area_tot_head + $area_head[$i];  
	}
	if (abs $zz[$i] > $dist_head)
	{
	$area_tot_wat = $area_tot_wat + $area_wat[$i];
	}
}

$energy = -0.028 * $area_tot_lip;
$energy_fin = $energy + 1.7;

$out = $prefix . '.nonpolar.out';
open(OUT, ">$out"); 

print OUT "Area available to lipid = $area_tot_lip\nArea available to head groups = $area_tot_head\nArea available to water = $area_tot_wat\n";

print OUT "Energy of insertion from water to lipid is $energy_fin kcal\n"; 
