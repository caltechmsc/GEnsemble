#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
}

use Cwd;
use File::Basename;
use File::Copy;
use File::Path;
use File::Spec;
use Getopt::Long;
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

if (@ARGV == 0) { help(); }

$centers_string  = "area rawmid";
$alanize_types   = "none standard onlycap";
$template_string = "bovrhod_1gzm humbeta2_2rh1 turbeta1_2vt4 bovopsin_3cap";
$opthelix_types  = "minrmsd.cap.min mineng.cap.min";

GetOptions ('h|help'        => \$help,
            'd|opthelix=s'  => \$opt_dir,
	    'm|mfta=s'      => \$mfta,
	    's|skip=s'      => \$skip_residues,
	    'man'           => \$man,
	    'pred'          => \$pred,
	    't|templates=s' => \$template_string,
	    'oc=s'          => \$opthelix_types,
	    'c|centers=s'   => \$centers_string,
	    'p|prefix=s'    => \$prefix,
	    'a|alanize=s'   => \$alanize_types
	    );

if ($help) { help(); }

@templates = split(/\s+/, $template_string);
@helices   = split(/\s+/, $opthelix_types);
@centers   = split(/\s+/, $centers_string);
@alanize   = split(/\s+/, $alanize_types);
@skip      = split(/\s+/, $skip_residues);
if ($skip_residues && ($alanize_types !~ /skip/)) { push @alanize, "skip"; }
if (($man && $pred) || (!$man && !$pred)) {
    die "Must use _either_ --pred _or_ --man.\n";
}
if (!$mfta) {
    die "Must provide a MFTA file.\n";
} elsif (! -e $mfta) {
    die "Could not find MFTA file :: $mfta\n";
}

if (!$opt_dir) {
    die "Must provide an OptHelix directory.\n";
} elsif (! -e $opt_dir) {
    die "Could not find OptHelix directory :: $opt_dir\n";
}

print "Performing alignments and alanization.\nThis may take a minute or two.\n\n";

$cwd = cwd;

foreach $template (@templates) {
    if (! -e "$template") {
	mkdir "$template";
    }
    chdir "$template";

    foreach $hel (@helices) {
	foreach $ctr (@centers) {

	    copy("$cwd/$mfta",".");
	    `/project/Biogroup/Software/devel/GEnsemble/programs/Align2Template.pl -t $template -d $opt_dir -m $mfta -oc $hel -c $ctr`;
	    unlink glob "*.gz";
	    unlink glob "protein.mfta";

	    foreach $ala (@alanize) {
		if ($ala eq "none") {
		    if (! -e "${template}.${hel}.${ctr}.noala") {
			mkdir "${template}.${hel}.${ctr}.noala";
			chdir "${template}.${hel}.${ctr}.noala";
			print "${template}.${hel}.${ctr}.noala\n";

			copy("../protein_initial_bundle.bgf",".");
			copy("../$mfta",".");
			if ($prefix) {
			    move("protein_initial_bundle.bgf", "${prefix}.${template}.${hel}.${ctr}.noala.bgf");
			    `ln -s ${prefix}.${template}.${hel}.${ctr}.noala.bgf ${prefix}.bgf`;
			} else {
			    move("protein_initial_bundle.bgf", "${template}.${hel}.${ctr}.noala.bgf");
			    `ln -s ${template}.${hel}.${ctr}.noala.bgf protein.bgf`;
			}

			chdir "..";
		    } else {
			print "Template already exists :: ${template}.${hel}.${ctr}.noala\n";
		    }

		} elsif ($ala eq "standard") {
		    if (! -e "${template}.${hel}.${ctr}.alastd") {
			mkdir "${template}.${hel}.${ctr}.alastd";
			chdir "${template}.${hel}.${ctr}.alastd";
			print "${template}.${hel}.${ctr}.alastd\n";

			copy("../protein_initial_bundle.bgf",".");
			copy("../$mfta",".");

			$alacmd = "/project/Biogroup/scripts/perl/alanize_bgf_2.pl ".
			    "-b protein_initial_bundle.bgf ".
			    "-m $mfta ".
			    "-o protein_initial_bundle.bgf ";

			if ($hel =~ /cap/) {
			    $alacmd .= "--cap all --raw nonpolar ";
			} elsif ($hel =~ /raw/) {
			    $alacmd .= "--raw nonpolar ";
			}

			if ($man) { $alacmd .= "--man"; } else { $alacmd .= "--pred"; }

			`$alacmd`;

			if ($prefix) {
			    move("protein_initial_bundle.bgf", "${prefix}.${template}.${hel}.${ctr}.alastd.bgf");
			    `ln -s ${prefix}.${template}.${hel}.${ctr}.alastd.bgf ${prefix}.bgf`;
			} else {
			    move("protein_initial_bundle.bgf", "${template}.${hel}.${ctr}.alastd.bgf");
			    `ln -s ${template}.${hel}.${ctr}.alastd.bgf protein.bgf`;
			}

			chdir "..";
		    } else {
			print "Template already exists :: ${template}.${hel}.${ctr}.alastd\n";
		    }

        } elsif ($ala eq "onlycap") {
            if (! -e "${template}.${hel}.${ctr}.alacap") {
            mkdir "${template}.${hel}.${ctr}.alacap";
            chdir "${template}.${hel}.${ctr}.alacap";
            print "${template}.${hel}.${ctr}.alacap\n";

            copy("../protein_initial_bundle.bgf",".");
            copy("../$mfta",".");

            $alacmd = "/project/Biogroup/scripts/perl/alanize_bgf_2.pl ".
                "-b protein_initial_bundle.bgf ".
                "-m $mfta ".
                "-o protein_initial_bundle.bgf ";

            if ($hel =~ /cap/) {
                $alacmd .= "--cap all --raw none ";
            } elsif ($hel =~ /raw/) {
                $alacmd .= "--raw none ";
            }

            if ($man) { $alacmd .= "--man"; } else { $alacmd .= "--pred"; }

            `$alacmd`;

            if ($prefix) {
                move("protein_initial_bundle.bgf", "${prefix}.${template}.${hel}.${ctr}.alacap.bgf");
                `ln -s ${prefix}.${template}.${hel}.${ctr}.alacap.bgf ${prefix}.bgf`;
            } else {
                move("protein_initial_bundle.bgf", "${template}.${hel}.${ctr}.alacap.bgf");
                `ln -s ${template}.${hel}.${ctr}.alacap.bgf protein.bgf`;
            }

            chdir "..";
            } else {
            print "Template already exists :: ${template}.${hel}.${ctr}.alacap\n";
            }

		} elsif ($ala eq "skip") {
		    @skip2 = @skip;
		    $string = "$skip2[0]"; shift @skip2; foreach (@skip2) { $string .= "_$_"; }

		    if (! -e "${template}.${hel}.${ctr}.skip_${string}") {
			mkdir "${template}.${hel}.${ctr}.skip_${string}";
			chdir "${template}.${hel}.${ctr}.skip_${string}";
			print "${template}.${hel}.${ctr}.skip_${string}\n";

			copy("../protein_initial_bundle.bgf",".");
			copy("../$mfta",".");

			$alacmd = "/project/Biogroup/scripts/perl/alanize_bgf_2.pl ".
			    "-b protein_initial_bundle.bgf ".
			    "-m $mfta ".
			    "-o protein_initial_bundle.bgf ";

			if ($hel =~ /cap/) {
			    $alacmd .= "--cap all --raw nonpolar ";
			} elsif ($hel =~ /raw/) {
			    $alacmd .= "--raw nonpolar ";
			}

			if ($man) { $alacmd .= "--man "; } else { $alacmd .= "--pred "; }

			$alacmd .= "--skip \"";

			foreach (@skip) { $alacmd .= " $_"; }
			$alacmd .= "\"";

			`$alacmd`;

			if ($prefix) {
			    move("protein_initial_bundle.bgf", "${prefix}.${template}.${hel}.${ctr}.skip_${string}.bgf");
			    `ln -s ${prefix}.${template}.${hel}.${ctr}.skip_${string}.bgf ${prefix}.bgf`;
			} else {
			    move("protein_initial_bundle.bgf", "${template}.${hel}.${ctr}.skip_${string}.bgf");
			    `ln -s ${template}.${hel}.${ctr}.skip_${string}.bgf protein.bgf`;
			}

			chdir "..";
		    } else {
			print "Template already exists :: ${template}.${hel}.${ctr}.skip_${string}\n";
		    }
		}
	    }

	    unlink "protein_initial_bundle.bgf";
	}
    }

    chdir "..";
}





exit;

sub help {

    my $help = "
Program:
 :: MultiTemplate.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: MultiTemplate.pl -m {mfta} -d {opthelix directory}
 ::                  {--man or --pred}
 ::                  --oc \"{opthelix helix types}\"
 ::                  -t \"{templates}\"
 ::                  -c \"{center types}\"
 ::                  -a \"{alanization types}\"
 ::                  -s \"{residues to skip}\"
 ::                  -p {filename prefix}

Input:
 :: -m | --mfta      :: Filename (New style MFTA)

 :: -d | --opthelix  :: Directory
 :: Absolute path to the OptHelix output directory.

 :: --oc             :: OptHelix Keywords
 :: OptHelix output types.  Options are ::
 :: * minrmsd.cap.min  (default)
 :: * mineng.cap.min   (default)
 :: * minrmsd.cap
 :: * minrmsd.raw
 :: * mineng.cap
 :: * mineng.raw
 :: * minrmsd.raw.min
 :: * mineng.raw.min
 :: Example :: --oc \"minrmsd.cap.min mineng.cap.min\"

 :: -t | --templates :: Keywords
 :: The template that your helices should be aligned to.
 :: * bovrhod_1gzm  (default)
 :: * humbeta2_2rh1 (default)
 :: * (see Align2Template.pl help info for others)
 :: Example :: -t \"bovrhod_1gzm humbeta2_2rh1\"

 :: -c | --centers   :: Keywords
 :: Hydrophobic centers to use.
 :: * area (default), rawmid (default), peak, capmid
 :: Example :: -c \"area rawmid\"

 :: -a | --alanize   :: Keywords
 :: Types of alanization to perform.
 :: * none (default)
 :: * standard (default) - cap all, raw nonpolar
 :: * skip (must be used in conjuction with -s option)
 :: Example :: -a \"none standard skip\"

 :: -s | --skip      :: Integers
 :: Residues that should NOT be alanized when performing
 :: the \"standard\" alanization.
 :: It should be a list of residues in quotes:
 :: Ex: -s \"35 54 104\"

 :: -p | --prefix    :: String
 :: Prefix to be added to all output files.

 :: --man            :: No Input
 :: Use the Manual raw/cap start/stop information

 :: --pred           :: No Input
 :: Use the Predicted raw/cap start/stop information

Description:
 :: This program takes various template and alanization
 :: options and performs all of them in one command.
 ::
 :: One subdirectory is created for each protein template
 :: used (i.e. bovrhod_1gzm, humbeta2_2rh1, turbeta1_2vt4, bovopsin_3cap).
 ::
 :: A sub-subdirectory is created for each individual
 :: bundle combination.
 ::
 :: Alignment Program
 :: /project/Biogroup/Software/GEnsemble/programs/Align2Template.pl
 :: See the help info for Align2Template.pl for help
 :: with alignment options.
 ::
 :: Alanization Program
 :: /project/Biogroup/scripts/perl/alanize_bgf_2.pl
 :: See the help info for alanize_bgf_2.pl for help
 :: with alanization options.

Usage (repeated):
 :: MultiTemplate.pl -m {mfta} -d {opthelix directory}
 ::                  {--man or --pred}
 ::                  --oc \"{opthelix helix types}\"
 ::                  -t \"{templates}\"
 ::                  -c \"{center types}\"
 ::                  -a \"{alanization types}\"
 ::                  -s \"{residues to skip}\"
 ::                  -p {filename prefix}

";

    die "$help";


}
