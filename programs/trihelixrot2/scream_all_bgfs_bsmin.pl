#!/usr/bin/env perl

use File::Basename;
use File::Copy;
use FindBin ();
use Getopt::Long;
use lib "$FindBin::Bin";
 
GetOptions ('r|rotadiv=s'                 => \$rotadiv,
            's|mpsim:i'                   => \$mpsim);

if (not defined $rotadiv) { $rotadiv = 10; }

$sbin = $FindBin::Bin;

$defaultsfile = "${sbin}/../.gensemble/.bihelix";
open DEF, "<$defaultsfile";
while (<DEF>) {
    if (/^scream_dir\s+(\S+)/)            { $scream_dir        = $1; }
    elsif (/^ff\s+(\S+)/)                 { $ff                = $1; }
    elsif (/^pwb\s+(\S+)/)                { $pwb               = $1; }
    elsif (/^runmpsim\s+(\S+)/)           { $runmpsim          = $1; }
    elsif (/^mpsim_data\s+(\S+)/)         { $mpsim_data        = $1; }
    elsif (/^mpsim_executable\s+(\S+)/)   { $mpsim_executable  = $1; }
    elsif (/^python_executable\s+(\S+)/)  { $python_executable = $1; }
}
close DEF;
print "scream_dir $scream_dir\n";

################################################################################
##### loadScream                                                           #####
################################################################################
    $ENV{INSTALL_PATH}               = "${sbin}/../$scream_dir";
    $ENV{SCREAM_MAIN_SCRIPT_PATH}    = "$ENV{INSTALL_PATH}/scripts/";
    $ENV{SCREAM_LIB_PATH}            = "$ENV{INSTALL_PATH}/lib/v3.0/Clustered/lib/";
    $ENV{SCWRL_LIB_PATH}             = "$ENV{INSTALL_PATH}/lib/v3.0/SCWRL/lib/";
    $ENV{SCREAM_CNN_PATH}            = "$ENV{INSTALL_PATH}/lib/v3.0/NtrlAARotConn/";
    $ENV{SCREAM_DELTA_PAR_FILE_PATH} = "$ENV{INSTALL_PATH}/lib/SCREAM_delta_par_files/";
    $ENV{FORCE_FIELD_FILE}           = "${sbin}/../$ff";
    $ENV{PYTHON_EXE}                 = "${sbin}/../$python_executable";

    $ENV{PYTHONPATH} =
          "${sbin}/../$scream_dir/SCREAM/swig/python/build/lib.linux-i686-2.3/".
    ":" . "${sbin}/../$scream_dir/SCREAM/python/app/".
    ":" . "${sbin}/../$scream_dir/PythonDeps/";

    $ENV{MPSIM_DATA} = "${sbin}/../$mpsim_data";
###
# END loadSCREAM
###
$ff = "${sbin}/../$ff";
$pwb = "${sbin}/../$pwb";
$runmpsim = "${sbin}/../$runmpsim";

$mpsimmin = "";
if (defined $mpsim and $mpsim > 0) {
$mpsimmin = " -s $mpsim ";
}

@bgfl = `ls wt*.bgf`;
chomp @bgfl;

foreach $bgfl (@bgfl) {
    system("echo $bgfl");
    ( $bgfp, $path, $suffix ) = fileparse( $bgfl, qr/\.[^.]*/ );
    if ($path || $suffix) {}; # Avoid warning
#   system("$sbin/annex/add_GPCR_chains2.pl $bgfl > temp1.bgf");
    system("/project/Biogroup/scripts/python/SCREAM_BindingSite.py $bgfl $rotadiv X 5.0");
    $bgfls = $bgfp.'.s.bgf';
    system("cp -f best_1.bgf $bgfls");
    if (defined $mpsim) {
    $bgfme = $bgfp.'.mpsimE.out';
    system("$runmpsim -f $ff -l 0 -s $mpsim $bgfl minvac > $bgfme");
    }
#   $bgflo = $bgfp.'_scream.out.gz';
#   system("mv -f scream.out.gz $bgflo");
#   $bgflso = $bgfp.'_Scream_Energies.txt';
#   system("cp -f Residue-E.txt $bgflso");
    system("rm -f temp1.bgf temp2.bgf best_1.bgf Residue-E.txt timing.txt *snap* *traj1 *ctl");
}
