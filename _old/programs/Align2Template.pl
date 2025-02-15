#!/usr/bin/env perl

use warnings;
use FindBin ();
use lib "$FindBin::Bin";
use Cwd;
use File::Copy;
use File::Basename;
use Getopt::Long;
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;
use Modules::AlignHelix;

our $VERSION = '1.10';

$sbin = $FindBin::Bin;

GetOptions ('h|help'                 => \$help,
        't|template=s'               => \$template,
        'd|opthelixdir=s'            => \$opthelixdir,
        'oc|opthelixcriteria=s'      => \$opthelixcriteria,
        'm|mftafile=s'               => \$mftafile,
        'c|hpcenter=s'               => \$hpcenter,
        'p|proteintag=s'             => \$proteintag,
        'nt|nter=s'                  => \$nter,
        'zo|zout=s'                  => \$zout,
        'tmo|tmatorigin=i'           => \$tmatorigin,
        'tmx|tmalongx=i'             => \$tmalongx);

if ($help)       { &help; }
#if ($numargv == 0) { &help; }
if (not defined $template and not defined $opthelixdir and not defined $opthelixcriteria and not defined $mftafile and not defined $hpcenter and not defined $proteintag and not defined $nter and not defined $zout and not defined $tmatorigin and not defined $tmalongx) { &help; }
if (not defined $template) { die "specify the template to use for aligning helices\n"; }
if (not defined $opthelixdir) { die "specify the directory with optimized helices\n"; }
if (not defined $mftafile) { die "specify the modified fasta file (.mfta) from PredicTM output\n"; }
if (not defined $opthelixcriteria) {
    print "Using default OptHelix Criteria of minrmsd.cap.min!\n";
    $opthelixcriteria = "minrmsd.cap.min";
}
if (not defined $hpcenter) { die "specify whether rawmid/capmid/peak/area/manual1/manual2 hydrophobic center should be used\n"; }

if (!$proteintag) { $proteintag = "protein"; }
my $templatespecfile = "$template"."_template.inp";
my $templatelocation = "$sbin\/templates\/$templatespecfile";
if (! -e $templatelocation) {die "Could not find Template for :: $template\n\n";}
system("cp -r $templatelocation .");


my $my_mftafile = "$proteintag".".mfta";
system("cp -f $mftafile $my_mftafile");

open (TMPL, "<$templatespecfile");
my @tmpl = <TMPL>;
close (TMPL);

open (MFTA, "<$my_mftafile");
my @mfta = <MFTA>;
close (MFTA);

#system("cp -f $opthelixdir/*helix*fin.$opthelixcriteria.bgf .");

#Makes N-terminal point out of the cell by default (e.g., GPCRs)
if (not defined $nter) {
$nter = 'out';
}
if (($nter ne 'out') and ($nter ne 'in')) { die "specify in or out for nter\n"; }

# Makes the outside of the cell as +z direction from lipid middle by default
if (not defined $zout) {
$zout = 'plus';
}
if (($zout ne 'plus') and ($zout ne 'minus')) { die "specify plus or minus for zout\n"; }

# Translate the bundle so that helical axis of a specified helix (tmatorigin)
# passes through origin.
# If a zero value is given then make origin the geometric center of
# intersection points of all helical axes with the z=0 plane.
# If a negative value is given, then don't do any alignment.

if (not defined $tmatorigin) {
$tmatorigin=3; # Useful for Class A GPCRs as TM3 is in the middle
}


# Once the origin is set, rotate the helical bundle in x-y plane such that
# the axis of a specified helix (tmalongx) passes through the x-axis.
# If a negative value is given, then don't do any alignment.
if (not defined $tmalongx) {
    $tmalongx=2; # Useful convention for Class A GPCRs
}

if (($tmatorigin == $tmalongx) && ($tmatorigin > 0)) {
die "Specify different TM helices for positioning at origin and along x-axis\n";
}

my ($i,$j,$k,$dum1,$dum2,$dum3,$dum4,$dum5,$dum6,$dum7,$dum8,$dumx,$dumy,$dumz);
my ($dum,$thelx,$thely,$thelz,$theltheta,$thelphi,$theleta,$etadum1,$etadum2);
my @etaresid = ();

# Get eta angle residue information
my $ihel = 0;
foreach my $mftaline (@mfta) {
    if ($mftaline =~ /\* / and $mftaline =~ /tm /) {
    $ihel++;
    $helixid = $ihel;
    ($dum1,$dum2,$dum3,$dum4,$dum5,$dum6,$dum7,$dum8,$dumx,$dumy,$dumz,$etaresid[$helixid],$dum) = split /\ +/, $mftaline;
    }
}


### MAIN LOOP TO ALIGN EACH HELIX
$ihel = 0;
my $remarkhpc = "";
unlink <aligned*bgf*>;
foreach my $mftaline (@mfta) {
    if ($mftaline =~ /\* / and $mftaline =~ /hpc /) {
    $ihel++;
    $helixid = $ihel;
    my ($dum1,$dum2,$hpcrawmid,$hpccapmid,$hpcpeak,$hpcarea,$hpcman1,$hpcman2) = split /\ +/, $mftaline;
    if ($hpcenter =~ /rawmid/) {
        $helixhpc = $hpcrawmid;
    } elsif ($hpcenter =~ /capmid/) {
        $helixhpc = $hpccapmid;
    } elsif ($hpcenter =~ /peak/) {
        $helixhpc = $hpcpeak;
    } elsif ($hpcenter =~ /area/) {
        $helixhpc = $hpcarea;
    } elsif ($hpcenter =~ /manual1/) {
        $helixhpc = $hpcman1;
    } elsif ($hpcenter =~ /manual2/) {
        $helixhpc = $hpcman2;
    }
    if ($tmpl[$ihel-1] =~ /\* / and $tmpl[$ihel-1] =~ /tmpl /) {
    ($dum1,$dum2,$thelx,$thely,$thelz,$theltheta,$thelphi,$theleta,$etadum1,$etadum2) = split /\ +/, $tmpl[$ihel-1];
    }

    my $inputbgf = "myhelix".$helixid.".".$opthelixcriteria.".bgf";
    system("cp -f $opthelixdir/*helix$helixid*$opthelixcriteria*bgf $inputbgf");
#   print "$helixid $inputbgf $helixhpc  $thelx,$thely,$thelz,$theltheta,$thelphi,$theleta\n";
    AlignHelix($helixid,$inputbgf,$helixhpc,$thelx,$thely,$theltheta,$thelphi,$theleta,$etaresid[$helixid],$nter,$zout);
    $remarkhpc = $remarkhpc."REMARK HPC HELIX$helixid $helixhpc\n";
    }
}
### END OF MAIN LOOP
unlink <myhelix*bgf>;

# NOW MERGE ALL ALIGNED HELICES INTO A BUNDLE
system("$sbin/thirdparty/python-2.4.2/bin/python $sbin/utilities/mergeBGFs.py aligned_helix1.bgf aligned_helix2.bgf aligned_helix3.bgf aligned_helix4.bgf aligned_helix5.bgf aligned_helix6.bgf aligned_helix7.bgf -o ${proteintag}_initial_bundle.bgf");

open (BUNDLE, "<${proteintag}_initial_bundle.bgf");
my @bundle = <BUNDLE>;
close (BUNDLE);

my $descrpline = "DESCRP ${proteintag}\n";
my $remarklines = "REMARK Bundle created by using $template as a template
REMARK Bundle created with $opthelixcriteria helices and $hpcenter hydrophobic centers
$remarkhpc";

$nrem=0;
open (OBGF, ">${proteintag}_initial_bundle.bgf");
foreach $bundleline (@bundle) {
	if ($bundleline =~ /DESCRP/) {
		print OBGF "$descrpline";
	} elsif ($bundleline =~ /REMARK/) {
        if ($nrem == 0) {
		    print OBGF "$remarklines";
            $nrem=1;
        }
	} else {
		print OBGF "$bundleline";
	}
}
close (OBGF);
system("gzip aligned*bgf");


sub help {
    @tempavail = `ls -1 $sbin/templates`;
    foreach $temp (@tempavail) {
        chomp $temp;
        if ($temp =~ /template.inp/) {
           {local $/ = "_template.inp"; chomp $temp};
            $temp = "\n"."$temp";
            push(@templates,$temp);
        }
    }

    $help_message = "

Program:
 :: Align2Template.pl

Location:
 :: /project/Biogroup/scripts/Align2Template/Align2Template.pl

Release:
 :: Version 1.1 (29 Mar 2008)

Authors:
 :: Ravi Abrol (abrol\@wag.caltech.edu)

Usage:
 :: Align2Template.pl -t {humbeta2_2rh1 or bovrhod_1gzm} -d {opthelix directory} -m {modified fasta file} -oc {minrmsd.cap or minrmsd.raw or minrmsd.cap.min or minrmsd.raw.min or mineng.cap or mineng.raw or mineng.cap.min or mineng.raw.min} -c {area or peak or rawmid or capmid or manual1 or manual2 hydrophobic centers} -p {protein tag optional}

Options:
 :: -h | --help             :: Optional    :: No Input
 :: Prints this help message.

 :: -t | --template         :: Required
 :: Specify one of the following templates:
@templates

Description:
Takes your relaxed helices from OptHelix and orients them into a template
of your choice (currently two available: humbeta2_2rh1 or bovrhod_1gzm).
Requires a new mfta file so that you can specify which hydrophobic centers
to use. Also uses the eta residue information from the mfta file. 

Example Usage:
 :: Align2Template.pl -t humbeta2_2rh1 -d example_opthelix -m example_opthelix/P59533.nf_global.mfta -oc minrmsd.cap.min -c area

";
    die $help_message;
}
