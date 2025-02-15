#!/usr/bin/perl

$bgf = @ARGV[0];
$mfta = @ARGV[1];
$num_str1 = @ARGV[2] + 2;
$num_str2 = @ARGV[3] + 2; 
$proc = @ARGV[4];
$fin = @ARGV[5]; 
$ref = @ARGV[6];

################################################################################
##### loadScream                                                           #####
################################################################################
    $ENV{INSTALL_PATH}               = "/project/Biogroup/Software/devel/GEnsemble/programs/scream2";
    $ENV{SCREAM_MAIN_SCRIPT_PATH}    = "$ENV{INSTALL_PATH}/scripts/";
    $ENV{SCREAM_LIB_PATH}            = "$ENV{INSTALL_PATH}/lib/v3.0/Clustered/lib/";
    $ENV{SCWRL_LIB_PATH}             = "$ENV{INSTALL_PATH}/lib/v3.0/SCWRL/lib/";
    $ENV{SCREAM_CNN_PATH}            = "$ENV{INSTALL_PATH}/lib/v3.0/NtrlAARotConn/";
    $ENV{SCREAM_DELTA_PAR_FILE_PATH} = "$ENV{INSTALL_PATH}/lib/SCREAM_delta_par_files/";
    $ENV{FORCE_FIELD_FILE}           = "/project/Biogroup/Software/devel/GEnsemble/programs/FF/dreiding-0.3.par";
    $ENV{PYTHON_EXE}                 = "/exec/python/python-2.4.2/bin/python";

    $ENV{PYTHONPATH} =
          "/project/Biogroup/Software/devel/GEnsemble/programs/scream2/SCREAM/swig/python/build/lib.linux-i686-2.3/".
    ":" . "/project/Biogroup/Software/devel/GEnsemble/programs/scream2/SCREAM/python/app/".
    ":" . "/project/Biogroup/Software/devel/GEnsemble/programs/scream2/PythonDeps/";

    $ENV{MPSIM_DATA} = "/project/Biogroup/Software/devel/GEnsemble/programs/mpsim/";
###
# END loadSCREAM
###

($tag,$bg) = split /\.bgf/, $bgf; 

$totin = "Super_Bihelix_TotalE.out";
open(TOTIN,"<$totin");
@totin = <TOTIN>;
close(TOTIN);
$bundle = $tag . "_initial_bundle.bgf";
$template = $tag . "_temp.template";
$tempnew = $tag . "_temp_new.template";
$pdb = $tag . ".pdb"; 

$out = "Super_CombiHelix_" . $proc . ".out";
open(OUT,">$out");

$i = 0; 
foreach $totinline (@totin)
{
  $i++;
  if ($i >= $num_str1 && $i <= $num_str2)  
  {
    ($thtx,$thtx[1],$thtx[2],$thtx[3],$thtx[4],$thtx[5],$thtx[6],$thtx[7],$phix,$phix[1],$phix[2],$phix[3],$phix[4],$phix[5],$phix[6],$phix[7],$etax,$etax[1],$etax[2],$etax[3],$etax[4],$etax[5],$etax[6],$etax[7],$hpmx,$hpmx[1],$hpmx[2],$hpmx[3],$hpmx[4],$hpmx[5],$hpmx[6],$hpmx[7],$rest) = split /\ +/, $totinline;
    $finbgf = $tag . "." . $thtx[1] . "_" . $thtx[2] . "_" . $thtx[3] . "_" . $thtx[4] . "_" . $thtx[5] . "_" . $thtx[6] . "_" . $thtx[7] . "x" . $phix[1] . "_" . $phix[2] . "_" . $phix[3] . "_" . $phix[4] . "_" . $phix[5] . "_" . $phix[6] . "_" . $phix[7] . "x" . $etax[1] . "_" . $etax[2] . "_" . $etax[3] . "_" . $etax[4] . "_" . $etax[5] . "_" . $etax[6] . "_" . $etax[7] . "x" . $hpmx[1] . "_" . $hpmx[2] . "_" . $hpmx[3] . "_" . $hpmx[4] . "_" . $hpmx[5] . "_" . $hpmx[6] . "_" . $hpmx[7] . ".min.bgf";
    system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/make-bgf-for-combi.pl $bgf $mfta \"$totinline\"");
    system ("/exec/python/python-2.4.2/bin/python /project/Biogroup/Software/devel/GEnsemble/programs/scream2/scripts/SCREAM_all_no_AGP_CYX.py $bundle 05 FULL 0.0");
    system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/Combi_MPSim.pl -b best_1.bgf -s 10 > mpsim.out");
    system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/rmsd_matrix.pl $ref best_1.min.bgf rmsd_super.out");
    system ("cp best_1.min.bgf $finbgf");
    open (MPSIM,"<mpsim.out");
    @mpsim = <MPSIM>;
    close (MPSIM);
    ($premin,$hbondminx) = split /\ /, $mpsim[0];
    ($hbondmin,$nl) = split /\n/, $hbondminx;
    ($postmin,$hbondpostx) = split /\ /, $mpsim[1];
    ($hbond,$nl) = split /\n/, $hbondpostx; 
    open (SCREAM,"<Residue-E.txt");
    @scream = <SCREAM>;
    close (SCREAM);
    ($all,$intern,$el,$vel,$cel,$hel,$tsc,$vsc,$csc,$hsc,$totscream) = split /\ +/, $scream[1];
    open (RMSD,"<rmsd_super.out");
    @rmsd = <RMSD>;
    close (RMSD);
    ($sp,$rmsdx) = split /\ /, $rmsd[0];
    print OUT ("$finbgf  $hbond  $totscream  $premin  $postmin  $rmsdx");  
    system ("rm -f Residue-E.txt best_1.bgf best_1.min.bgf $bundle Anneal-Energies.txt rmsd_super.out mpsim.out scream.par scream.out.gz timing.txt $template $tempnew  Field1.bgf.gz");
  }
}

if ($fin == 1)
{
system("/project/Biogroup/Software/devel/GEnsemble2/programs/templates/OPM/GetTemplate.pl -m $mfta -p $pdb > $template");

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
    $hpc[$i] = sprintf("%.1f",$hpc);
  }
}

    $finbgf = $tag . "." . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "x" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "x" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "x" . $hpc[1] . "_" . $hpc[2] . "_" . $hpc[3] . "_" . $hpc[4] . "_" . $hpc[5] . "_" . $hpc[6] . "_" . $hpc[7] . ".min.bgf";
    $totinline = "Thet    0    0    0    0    0    0    0 Phi    0    0    0    0    0    0    0 Eta    0    0    0    0    0    0    0 HPM  " . $hpc[1] . "  " .  $hpc[2] . "  " . $hpc[3] . "  " . $hpc[4] . "  " . $hpc[5] . "  " . $hpc[6] . "  " . $hpc[7] . "         100.0        -100.0       100.0     -100.0";
    system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/make-bgf-for-combi.pl $bgf $mfta \"$totinline\"");
    system ("/exec/python/python-2.4.2/bin/python /project/Biogroup/Software/devel/GEnsemble/programs/scream2/scripts/SCREAM_all_no_AGP_CYX.py $bundle 05 FULL 0.0");
    system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/Combi_MPSim.pl -b best_1.bgf -s 10 > mpsim.out");
    system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/rmsd_matrix.pl $ref best_1.min.bgf rmsd_super.out");
    system ("cp best_1.min.bgf $finbgf");
    open (MPSIM,"<mpsim.out");
    @mpsim = <MPSIM>;
    close (MPSIM);
    ($premin,$hbondminx) = split /\ /, $mpsim[0];
    ($hbondmin,$nl) = split /\n/, $hbondminx;
    ($postmin,$hbondpostx) = split /\ /, $mpsim[1];
    ($hbond,$nl) = split /\n/, $hbondpostx;
    open (SCREAM,"<Residue-E.txt");
    @scream = <SCREAM>;
    close (SCREAM);
    ($all,$intern,$el,$vel,$cel,$hel,$tsc,$vsc,$csc,$hsc,$totscream) = split /\ +/, $scream[1];
    open (RMSD,"<rmsd_super.out");    
    @rmsd = <RMSD>;
    close (RMSD);
    ($sp,$rmsdx) = split /\ /, $rmsd[0];
    print OUT ("$finbgf  $hbond  $totscream  $premin  $postmin  $rmsdx");
    system ("rm -f Residue-E.txt best_1.bgf best_1.min.bgf $bundle Anneal-Energies.txt rmsd_super.out mpsim.out scream.par scream.out.gz timing.txt $template $tempnew $pdb Field1.bgf.gz");
}

$done = "combi_done";
open (DONE,">$done");
print DONE ("done");
system ("gzip *.bgf");
chdir("..");

$dn = 0;
if ($fin == 1)
{
  for ($k = 1; $k <= $proc; $k++)
  {
    $file = "super_combihelix_$k/combi_done";
    while ($dn < $k)
    { 
      if (-e $file)
      {
        $dn++;
      } 
    }      
  }
  system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_combi_sort.pl $proc $bgf"); 
}
