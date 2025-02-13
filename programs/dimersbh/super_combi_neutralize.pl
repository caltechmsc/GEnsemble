#!/usr/bin/perl

use Getopt::Long;
use Cwd;

GetOptions ('h|help'         => \$help,
            'b|bgf=s'        => \$bgf,
            'm|mfta=s'       => \$mfta,
            'n1|number1=i'   => \$num_str1,
            'n2|number2=i'   => \$num_str2,
            'p|proc=i'       => \$proc,
            'f|fin=i'        => \$fin,
            'r|ref=s'        => \$ref,
            'bio=s'          => \$bio,
            'md=s'           => \$masterdir,
            'mach=s'         => \$machine,
            'n|neutralize=s' => \$neut,
            );

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

if (not defined $neut){$neut = "neut1";}
($tag,$bg) = split /\.bgf/, $bgf; 

$totin = "Super_Bihelix_TotalE_withrank.out";
open(TOTIN,"<$totin");
<TOTIN>;
<TOTIN>;
@totin = <TOTIN>;
close(TOTIN);

$bundle = $tag . "_initial_bundle.bgf";
$template = $tag . "_temp.template";
$tempnew = $tag . "_temp_new.template";
$pdb = $tag . ".pdb"; 

$out = "Super_CombiHelix_" . $proc . ".out";
open(OUT,">$out");

### NEUTRALIZE ###
$outneut = "Super_Neutralize_" . $proc . ".out";
open(OUTNEUT,">$outneut");
### NEUTRALIZE ###

$i = 0; 
foreach $totinline (@totin)
{
  $i++;
  if ($i >= $num_str1 && $i <= $num_str2)  
  {
    ($thtx,$thtx[1],$thtx[2],$thtx[3],$thtx[4],$thtx[5],$thtx[6],$thtx[7],$phix,$phix[1],$phix[2],$phix[3],$phix[4],$phix[5],$phix[6],$phix[7],$etax,$etax[1],$etax[2],$etax[3],$etax[4],$etax[5],$etax[6],$etax[7],$hpmx,$hpmx[1],$hpmx[2],$hpmx[3],$hpmx[4],$hpmx[5],$hpmx[6],$hpmx[7],$enx[1],$enx[2],$enx[3],$enx[4],$bhrankx) = split /\ +/, $totinline;
    $finbgf = $tag . "." . $thtx[1] . "_" . $thtx[2] . "_" . $thtx[3] . "_" . $thtx[4] . "_" . $thtx[5] . "_" . $thtx[6] . "_" . $thtx[7] . "x" . $phix[1] . "_" . $phix[2] . "_" . $phix[3] . "_" . $phix[4] . "_" . $phix[5] . "_" . $phix[6] . "_" . $phix[7] . "x" . $etax[1] . "_" . $etax[2] . "_" . $etax[3] . "_" . $etax[4] . "_" . $etax[5] . "_" . $etax[6] . "_" . $etax[7] . "x" . $hpmx[1] . "_" . $hpmx[2] . "_" . $hpmx[3] . "_" . $hpmx[4] . "_" . $hpmx[5] . "_" . $hpmx[6] . "_" . $hpmx[7] . ".min.bgf";
    system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/make-bgf-for-combi.pl $bgf $mfta \"$totinline\"");
    system ("/exec/python/python-2.4.2/bin/python /project/Biogroup/Software/devel/GEnsemble/programs/scream2/scripts/SCREAM_all_no_AGP_CYX.py $bundle 05 FULL 0.0");
    system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/Combi_MPSim.pl -b best_1.bgf -s 10 > mpsim.out");
    if ($machine = "matrix"){system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/rmsd_matrix.pl $ref best_1.min.bgf rmsd_super.out");}
  else {system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/rmsd_hive.pl $ref best_1.min.bgf rmsd_super.out");}
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
    ($sp,$rmsdz) = split /\ /, $rmsd[0];
    ($rmsdx,$nl) = split /\n/, $rmsdz;
    if (-z $finbgf){$premin = "none"; $postmin = "none";}
    print OUT ("$finbgf  $hbond  $totscream  $premin  $postmin  $rmsdx  $bhrankx");  
    system ("rm -f Residue-E.txt best_1.bgf best_1.min.bgf $bundle Anneal-Energies.txt rmsd_super.out mpsim.out scream.par scream.out.gz timing.txt $template $tempnew  Field1.bgf.gz");

    ##### NEUTRALIZE AND GET ENERGIES #####
    open(BGF, $finbgf);
    while (<BGF>){
              while ( /^ATOM       1/g ){push @atom, $_;}
              }
        @split_atom = split (" ", join (" ", @atom));
        if ($split_atom[4] eq 'A') {$type = 1;}
        elsif ($split_atom[4] == 1) {$type = 2;}
        else {die "Wrong chain numbering!\n\n";}
    close BGF;
    $stripbgf = $tag . "." . $thtx[1] . "_" . $thtx[2] . "_" . $thtx[3] . "_" . $thtx[4] . "_" . $thtx[5] . "_" . $thtx[6] . "_" . $thtx[7] . "x" . $phix[1] . "_" . $phix[2] . "_" . $phix[3] . "_" . $phix[4] . "_" . $phix[5] . "_" . $phix[6] . "_" . $phix[7] . "x" . $etax[1] . "_" . $etax[2] . "_" . $etax[3] . "_" . $etax[4] . "_" . $etax[5] . "_" . $etax[6] . "_" . $etax[7] . "x" . $hpmx[1] . "_" . $hpmx[2] . "_" . $hpmx[3] . "_" . $hpmx[4] . "_" . $hpmx[5] . "_" . $hpmx[6] . "_" . $hpmx[7];
    system("cp $finbgf fintmp.bgf");
    my $bundle2 = &spe("fintmp.bgf");
    my ($interHelEng, $helixEng) = &getInterHel("fintmp.bgf",$bundle2,$type);
    my ($neutEng, $neutInterHel, $neutHelixEng);
    if ($neut eq "neut2"){$neutEng = &neutralize2("fintmp.bgf","striptmp");}
 elsif ($neut eq "neut3"){$neutEng = &neutralize3("fintmp.bgf","striptmp");}
  else {$neutEng = &neutralize("fintmp.bgf","striptmp");}
    if (-z "striptmp-neut.bgf"){$neutHelixEng = "none"; $neutInterHel = "none"; $neutEng = "none";}
  else {($neutInterHel, $neutHelixEng) = &getInterHel("striptmp-neut.bgf",$neutEng,$type);}
    system("mv striptmp-neut.bgf $stripbgf-neut.bgf");
    system("mv striptmp-neut.out $stripbgf-neut.out");
    if (-z $finbgf){$helixEng = "none"; $interHelEng = "none"; $postmin = "none";}
    print OUTNEUT ("$finbgf  $helixEng  $interHelEng  $postmin  $neutHelixEng  $neutInterHel  $neutEng  $rmsdx  $bhrankx");
    system ("rm *oneEvac* spe.out play.out fintmp.bgf");
    if (($bio == 0) && (not defined $bio)) {
                          system ("rm $finbgf $stripbgf-neut.bgf"); # if not running on bioscratch
                          }
    #### END #####
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
$bhrank0 = "-1\n";
    $finbgf = $tag . "." . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "x" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "x" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "x" . $hpc[1] . "_" . $hpc[2] . "_" . $hpc[3] . "_" . $hpc[4] . "_" . $hpc[5] . "_" . $hpc[6] . "_" . $hpc[7] . ".min.bgf";
    $totinline = "Thet    0    0    0    0    0    0    0 Phi    0    0    0    0    0    0    0 Eta    0    0    0    0    0    0    0 HPM  " . $hpc[1] . "  " .  $hpc[2] . "  " . $hpc[3] . "  " . $hpc[4] . "  " . $hpc[5] . "  " . $hpc[6] . "  " . $hpc[7] . "         100.0        -100.0       100.0     -100.0";
    system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/make-bgf-for-combi.pl $bgf $mfta \"$totinline\"");
    system ("/exec/python/python-2.4.2/bin/python /project/Biogroup/Software/devel/GEnsemble/programs/scream2/scripts/SCREAM_all_no_AGP_CYX.py $bundle 05 FULL 0.0");
    system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/Combi_MPSim.pl -b best_1.bgf -s 10 > mpsim.out");
    if ($machine = "matrix"){system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/rmsd_matrix.pl $ref best_1.min.bgf rmsd_super.out");}
  else {system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/rmsd_hive.pl $ref best_1.min.bgf rmsd_super.out");}
    system ("/project/Biogroup/Software/GEnsemble/programs/superbihelix/rmsd_hive.pl $ref best_1.min.bgf rmsd_super.out");
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
    ($sp,$rmsdz) = split /\ /, $rmsd[0];
    ($rmsdx,$nl) = split /\n/, $rmsdz;
    if (-z $finbgf){$premin = "none"; $postmin = "none";}
    print OUT ("$finbgf  $hbond  $totscream  $premin  $postmin $rmsdx  $bhrank0");
    system ("rm -f Residue-E.txt best_1.bgf best_1.min.bgf $bundle Anneal-Energies.txt rmsd_super.out mpsim.out scream.par scream.out.gz timing.txt $template $tempnew $pdb Field1.bgf.gz");

    ##### NEUTRALIZE AND GET ENERGIES #####
    open(BGF, $finbgf);
    while (<BGF>){
              while ( /^ATOM       1/g ){push @atom, $_;}
              }
        @split_atom = split (" ", join (" ", @atom));
        if ($split_atom[4] eq A) {$type = 1;}
        elsif ($split_atom[4] == 1) {$type = 2;}
        else {die "Wrong chain numbering!\n\n";}
    close BGF;

    $stripbgf = $tag . "." . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "x" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "x" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "_" . "0" . "x" . $hpc[1] . "_" . $hpc[2] . "_" . $hpc[3] . "_" . $hpc[4] . "_" . $hpc[5] . "_" . $hpc[6] . "_" . $hpc[7];
    system("cp $finbgf fintmp.bgf");
    my $bundle2 = &spe("fintmp.bgf");
    my ($interHelEng, $helixEng) = &getInterHel("fintmp.bgf",$bundle2,$type);
    my ($neutEng, $neutInterHel, $neutHelixEng);
    if ($neut eq "neut2"){$neutEng = &neutralize2("fintmp.bgf","striptmp");}
 elsif ($neut eq "neut3"){$neutEng = &neutralize3("fintmp.bgf","striptmp");}
  else {$neutEng = &neutralize("fintmp.bgf","striptmp");}
    if (-z "striptmp-neut.bgf"){$neutHelixEng = "none"; $neutInterHel = "none"; $neutEng = "none";}
  else {($neutInterHel, $neutHelixEng) = &getInterHel("striptmp-neut.bgf",$neutEng,$type);}
    system("mv striptmp-neut.bgf $stripbgf-neut.bgf");
    system("mv striptmp-neut.out $stripbgf-neut.out");
    print OUTNEUT ("$finbgf  $helixEng  $interHelEng  $postmin  $neutHelixEng  $neutInterHel  $neutEng  $rmsdx  $bhrank0");
    system ("rm *oneEvac* spe.out play.out fintmp.bgf");
    if ($bio eq "0"){
               system ("rm $finbgf $stripbgf-neut.bgf"); # if not running on bioscratch
               }
    #### END #####

}

$done = "combi_done";
open (DONE,">$done");
print DONE ("done");
#system ("gzip *.bgf");
chdir("..");

if (($bio == 0) && (not defined $bio)) {$bio = 0;}

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
  system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_neutral_sort.pl -p $proc -b $bgf -m $mfta --sortrank 'NCti' --range '1-25' --ppn 1 --bio $bio -md $masterdir"); 
  system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_neutral_sort.pl -p $proc -b $bgf -m $mfta --sortrank 'Cih'  --range  '1-25' --ppn 1 --bio $bio -md $masterdir");   
  system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_neutral_sort.pl -p $proc -b $bgf -m $mfta --sortrank 'Ctl'  --range  '1-25' --ppn 1 --bio $bio -md $masterdir");   
  system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_neutral_sort.pl -p $proc -b $bgf -m $mfta --sortrank 'Nih'  --range  '1-25' --ppn 1 --bio $bio -md $masterdir");   
  system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_neutral_sort.pl -p $proc -b $bgf -m $mfta --sortrank 'Ntl'  --range  '1-25' --ppn 1 --bio $bio -md $masterdir");   
}

#######----------------------------------#######
#######         Subroutine spe           #######
#######----------------------------------#######

sub spe {
        my $file = $_[0];
        my $ff = "/project/Biogroup/FF/dreiding-0.3.par";
        my $energy;
        system "/ul/caglar/Perl/runMPSim.pl $file -f $ff oneEvac > spe.out";
        open (SPE, "<spe.out") or die "Can't find spe.out\n";
        while (<SPE>) {
                if (/final energy/) {
                        my @line = split(" ", $_);
                        $energy = $line[6];
                        last;
                }
        }
        close SPE;
        return $energy;
}

#####---------------------------#####
#####   Subroutine neutralize   #####
#####---------------------------#####

sub neutralize {
    my $file = $_[0];
    my $strippedName = $_[1];
    system "/ul/victor/utilities/Neutral-Prep/Neutral-Prep-06-16-09.pl $file $strippedName-neut.bgf /ul/victor/SCREAM/SCREAM_v2.0/SCREAM/src/Neutralize/Standard.def &> $strippedName-neut.out";
    my $NeutEnergy = &spe("$strippedName-neut.bgf","neut");
    system "rm -fr tmp*";   #from NeutralPrep.pl
    return $NeutEnergy;
}

#####-------------------------------#####
#####   Subroutine neutralize old   #####
#####-------------------------------#####

sub neutralize2 {
    my $file = $_[0];
    my $strippedName = $_[1];
    #print "...Neutralizing $file...\n";
    system "/ul/victor/utilities/Neutral-Prep/Neutral-Prep.pl $file $strippedName-neut.bgf /ul/victor/SCREAM/SCREAM_v2.0/SCREAM/src/Neutralize/Standard.def &> $strippedName-neut.out";
    my $NeutEnergy = &spe("$strippedName-neut.bgf","neut");
    system "rm -fr tmp*";   #from NeutralPrep.pl
    return $NeutEnergy;
}

#####-------------------------------#####
#####   Subroutine neutralize vac   #####
#####-------------------------------#####

sub neutralize3 {
    my $file = $_[0];
    my $strippedName = $_[1];
    #print "...Neutralizing $file...\n";
    system "/project/Biogroup/Software/Neutralize/neutralize.py $file $strippedName-neut.bgf /ul/victor/SCREAM/SCREAM_v2.0/SCREAM/src/Neutralize/Standard.def &> $strippedName-neut.out";
    my $NeutEnergy = &spe("$strippedName-neut.bgf","neut");
    system "rm -fr tmp*";   #from NeutralPrep.pl
    return $NeutEnergy;
}


#####----------------------------#####
#####   Subroutine getInterHel   #####
#####----------------------------#####

sub getInterHel {
    my $file = $_[0];
    my $bundle3 = $_[1];
    my $type = $_[2];
    my %tms;

#split into 7 tms, get spe for each helix
    if($type == 2){
    my @chains = ("1", "2", "3", "4", "5", "6", "7");
        foreach (@chains) {
            system "/ul/caglar/Perl/playWithBGF -c $_ -o tm$_.bgf $file > play.out";
            $tms{$_} = &spe("tm$_.bgf");
        }}
    elsif ($type == 1){
    my @chains = ("A", "B", "C", "D", "E", "F", "G");
        foreach (@chains) {
            system "/ul/caglar/Perl/playWithBGF -c $_ -o tm$_.bgf $file > play.out";
            $tms{$_} = &spe("tm$_.bgf");
        }}
#add up helix spe, subtract from bundle
    my $helixEng = 0;
    foreach (keys %tms) {
        $helixEng = $helixEng + $tms{$_};
    }
    my $interHelEng = $bundle3 - $helixEng;
    system "rm -f tm?.bgf play.bgf"; #cleanup

    return ($interHelEng, $helixEng);
}

