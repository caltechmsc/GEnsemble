#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
}

use strict;
use warnings;
use Cwd;
use Data::Dumper;
use File::Basename;
use File::Copy;
use File::Path;
use File::Spec;
use Getopt::Long qw(:config no_ignore_case);
use List::Util qw(min max);
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

# Data::Dumper settings
$Data::Dumper::Indent   = 1;
$Data::Dumper::Terse    = 1;
$Data::Dumper::Sortkeys = 1;

sub testdie {
    if ($_[0]) {
	die "died here: $_[0]\n";
    } else {
	die "died\n";
    }
}

################################################################################
### Globals ###
################################################################################

# Set up the BLOSUM62 Similarity Matrix
our @blosumAA =
    qw(A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V  B  Z  X  -);

our @blosum62txt =
    ([ 4,-1,-2,-2, 0,-1,-1, 0,-2,-1,-1,-1,-1,-2,-1, 1, 0,-3,-2, 0,-2,-1, 0,-4],
     [-1, 5, 0,-2,-3, 1, 0,-2, 0,-3,-2, 2,-1,-3,-2,-1,-1,-3,-2,-3,-1, 0,-1,-4],
     [-2, 0, 6, 1,-3, 0, 0, 0, 1,-3,-3, 0,-2,-3,-2, 1, 0,-4,-2,-3, 3, 0,-1,-4],
     [-2,-2, 1, 6,-3, 0, 2,-1,-1,-3,-4,-1,-3,-3,-1, 0,-1,-4,-3,-3, 4, 1,-1,-4],
     [ 0,-3,-3,-3, 9,-3,-4,-3,-3,-1,-1,-3,-1,-2,-3,-1,-1,-2,-2,-1,-3,-3,-2,-4],
     [-1, 1, 0, 0,-3, 5, 2,-2, 0,-3,-2, 1, 0,-3,-1, 0,-1,-2,-1,-2, 0, 3,-1,-4],
     [-1, 0, 0, 2,-4, 2, 5,-2, 0,-3,-3, 1,-2,-3,-1, 0,-1,-3,-2,-2, 1, 4,-1,-4],
     [ 0,-2, 0,-1,-3,-2,-2, 6,-2,-4,-4,-2,-3,-3,-2, 0,-2,-2,-3,-3,-1,-2,-1,-4],
     [-2, 0, 1,-1,-3, 0, 0,-2, 8,-3,-3,-1,-2,-1,-2,-1,-2,-2, 2,-3, 0, 0,-1,-4],
     [-1,-3,-3,-3,-1,-3,-3,-4,-3, 4, 2,-3, 1, 0,-3,-2,-1,-3,-1, 3,-3,-3,-1,-4],
     [-1,-2,-3,-4,-1,-2,-3,-4,-3, 2, 4,-2, 2, 0,-3,-2,-1,-2,-1, 1,-4,-3,-1,-4],
     [-1, 2, 0,-1,-3, 1, 1,-2,-1,-3,-2, 5,-1,-3,-1, 0,-1,-3,-2,-2, 0, 1,-1,-4],
     [-1,-1,-2,-3,-1, 0,-2,-3,-2, 1, 2,-1, 5, 0,-2,-1,-1,-1,-1, 1,-3,-1,-1,-4],
     [-2,-3,-3,-3,-2,-3,-3,-3,-1, 0, 0,-3, 0, 6,-4,-2,-2, 1, 3,-1,-3,-3,-1,-4],
     [-1,-2,-2,-1,-3,-1,-1,-2,-2,-3,-3,-1,-2,-4, 7,-1,-1,-4,-3,-2,-2,-1,-2,-4],
     [ 1,-1, 1, 0,-1, 0, 0, 0,-1,-2,-2, 0,-1,-2,-1, 4, 1,-3,-2,-2, 0, 0, 0,-4],
     [ 0,-1, 0,-1,-1,-1,-1,-2,-2,-1,-1,-1,-1,-2,-1, 1, 5,-2,-2, 0,-1,-1, 0,-4],
     [-3,-3,-4,-4,-2,-2,-3,-2,-2,-3,-2,-3,-1, 1,-4,-3,-2,11, 2,-3,-4,-3,-2,-4],
     [-2,-2,-2,-3,-2,-1,-2,-3, 2,-1,-1,-2,-1, 3,-3,-2,-2, 2, 7,-1,-3,-2,-1,-4],
     [ 0,-3,-3,-3,-1,-2,-2,-3,-3, 3, 1,-2, 1,-1,-2,-2, 0,-3,-1, 4,-3,-2,-1,-4],
     [-2,-1, 3, 4,-3, 0, 1,-1, 0,-3,-4, 0,-3,-3,-2, 0,-1,-4,-3,-3, 4, 1,-1,-4],
     [-1, 0, 0, 1,-3, 3, 4,-2, 0,-3,-3, 1,-1,-3,-1, 0,-1,-3,-2,-2, 1, 4,-1,-4],
     [ 0,-1,-1,-1,-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2, 0, 0,-2,-1,-1,-1,-1,-1,-4],
     [-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4, 1]);

our %blosum62;
our %simmat;
for (my $i = 0; $i < @blosumAA; $i++) {
    for (my $j = 0; $j < @blosumAA; $j++) {
	my $a = $blosumAA[$i];
	my $b = $blosumAA[$j];

	$blosum62{$a}{$b} = $blosum62txt[$i][$j];
	if ($a eq $b) {
	    if ($a eq "-") { $simmat{$a}{$b} = " "; }
	    $simmat{$a}{$b} = "*";
	} elsif ($blosum62{$a}{$b} > 0) {
	    $simmat{$a}{$b} = ":";
	} else {
	    $simmat{$a}{$b} = " ";
	}
    }
}

our $biogroup    = "/project/Biogroup";
our $biosoft     = "${biogroup}/Software";
our $ge          = "${biosoft}/GEnsemble/programs";
our $clustal     = "${ge}/thirdparty/clustal/clustalw";
our $pwb         = "${ge}/utilities/playWithBGF/playWithBGF";
our $runmpsim    = "${ge}/utilities/runMPSim.pl";
our $scream      = "${biosoft}/scream3/programs/scream3_wrap.pl";
our $ff          = "${biogroup}/FF/dreiding-0.3.par";
our $merge       = "${biogroup}/scripts/BGFtools/mergeBGFs.py";
our $mafft_bin   = "${biosoft}/GEnsemble/programs/thirdparty/mafft/lib/mafft";
our $mafft_exe   = "${biosoft}/GEnsemble/programs/thirdparty/mafft/mafft";
our $getinp      = "${biosoft}/GEnsemble/programs/GetTemplate-3.pl";
our $alninp      = "${biosoft}/GEnsemble/programs/Align2Template-3.pl";
our $bgfcheck    = "${biogroup}/scripts/perl/BGFCheck.pl";
our $fastasource = "/ul/griffith/dev/Homologize/fasta/";
our $polyalasrc  = "/ul/griffith/dev/Homologize/polyala/";

################################################################################

my ($help, $tgtmfta, $hombgf, $hommfta, $tgtpfx, $hompfx, $pfx, $debug);
my $pair    = "";
my $overlap = 8;
my $trunc   = 2;

if (@ARGV == 0) { help(); }

#ABCDEFGHIJKLMNOPQRSTUVWXYZ
#abcdefghijklmnopqrstuvwxyz

#ABCDEFGHIJKLMNOPQRSTUVWXYZ
#abcdefg ijklmnopqrstuvwxyz
GetOptions ('h|help'          => \$help,
	    'm|mfta|tgt=s'    => \$tgtmfta,
	    't|temp|hom=s'    => \$hompfx,
	    'p|pfx=s'         => \$pfx,
	    'pair=i'          => \$pair,
	    'overlap=i'       => \$overlap,
	    'trunc=i'         => \$trunc,
	    'debug'           => \$debug);

if ($help) { help(); }

# Target Protein
if (! $tgtmfta) {
    die "Homologize :: Must provide MFTA file for target protein!\n";
} elsif (! -e $tgtmfta) {
    die "Homologize :: Could not find MFTA file for target protein: $tgtmfta\n";
}
($tgtpfx = $tgtmfta) =~ s/.mfta$//;

# Homology Protein
if (! $hompfx) {
    die "Homologize :: Must provide prefix for homology protein!\n";
}
($hombgf  = $hompfx) .= ".bgf";
($hommfta = $hompfx) .= ".mfta";
if (! -e $hombgf) {
    die "Homologize :: Could not find BGF file for homology protein: $hombgf\n";
}
if (! -e $hommfta) {
    die "Homologize :: Could not find MFTA file for homology protein: $hommfta\n";
}

# Output Prefix
if (!$pfx) {
    $pfx = "";
}
if ($pfx eq "") {
    $pfx = "${tgtpfx}.${hompfx}";
}

############################################################
### Main Routine                                         ###
############################################################

# Input
# 1) Target:
#    Target MFTA
# 2) Homology:
#    Homology BGF
#    Homology MFTA

# TM Data
my %dat = ();
my @tms = ();
my @ret = ();
my $tgtseq;
my $homseq;

# Load Target Sequence
@ret = loadTargetData(\%dat, $tgtmfta, $pair);
%dat    = %{$ret[0]};
@tms    = @{$ret[1]};
$tgtseq =   $ret[2];
@tms = sort {$a <=> $b} @tms;

# Load Homology Sequence
@ret = loadHomologyData(\%dat, $hommfta, $hombgf, $hompfx);
%dat    = %{$ret[0]};
$homseq =   $ret[1];

# Find initial alignment by sequence similarity
foreach my $i (@tms) {
    @ret = sequenceSimilarityAlignment(\%dat, $tgtseq, $homseq, $i);
    %dat = %{$ret[0]};
}

# Query user about modifying TMs
@ret = queryTMs(\%dat, $tgtseq, $homseq, \@tms);
%dat = %{$ret[0]};

# Generate BGF
@ret = homologyBGF(\%dat, \@tms, $tgtseq, $tgtmfta, $hompfx, $homseq, $hombgf, $hommfta,
		   $overlap, $trunc, $pfx);
%dat        = %{$ret[0]};
my $finmfta =   $ret[1];

# Final Print
printFinal(\%dat, \@tms, $tgtmfta, $hompfx, $overlap, $trunc, $pfx);

# Done
print "Finished\n\n";

exit;

################################################################################
### Get Target TM Data
################################################################################
sub loadTargetData {
    my %dat     = %{$_[0]};
    my $tgtmfta =   $_[1];
    my $pair    =   $_[2];

    my $tgtseq   = " ";

    # Determine TM Pair to use
    if ($pair eq "") {

	# Target Sequence
	my %tmpdat   = ();
	my %tmppairs = ();
	my $tmplen   = 0;
	open MFTA, "$tgtmfta";
	while (<MFTA>) {
	    my $line = $_;
	    chomp $line;
	    $line =~ s/\r//g;

	    # Sequence
	    if ($line =~ /^[ACDEFGHIKLMNPQRSTVWY]/) {
		$tgtseq .= $line;
	    }

	    # TM start/stop
	    elsif ($line =~ /^\*\s+(\d+)tm/) {
		my $i = $1;
		my @split = split(/\s+/, $line);

		push @tms, $i;

		$tmpdat{$i}{1}{start} = $split[2];
		$tmpdat{$i}{1}{stop}  = $split[3];
		$tmpdat{$i}{1}{len}   = $tmpdat{$i}{1}{stop} - $tmpdat{$i}{1}{start} + 1;
		$tmppairs{1} = 1;
		if ($tmpdat{$i}{1}{len} > $tmplen) { $tmplen = $tmpdat{$i}{1}{len}; }

		if ($split[4] =~ /^\d+$/) {
		    $tmpdat{$i}{2}{start} = $split[4];
		    $tmpdat{$i}{2}{stop}  = $split[5];
		    $tmpdat{$i}{2}{len}   = $tmpdat{$i}{2}{stop} - $tmpdat{$i}{2}{start} + 1;
		    if ($tmpdat{$i}{2}{len} > $tmplen) { $tmplen = $tmpdat{$i}{2}{len}; }
		    $tmppairs{2} = 1;
		}

		if ($split[6] =~ /^\d+$/) {
		    $tmpdat{$i}{3}{start} = $split[6];
		    $tmpdat{$i}{3}{stop}  = $split[7];
		    $tmpdat{$i}{3}{len}   = $tmpdat{$i}{3}{stop} - $tmpdat{$i}{3}{start} + 1;
		    if ($tmpdat{$i}{3}{len} > $tmplen) { $tmplen = $tmpdat{$i}{3}{len}; }
		    $tmppairs{3} = 1;
		}

		if ($split[8] =~ /^\d+$/) {
		    $tmpdat{$i}{4}{start} = $split[8];
		    $tmpdat{$i}{4}{stop}  = $split[9];
		    $tmpdat{$i}{4}{len}   = $tmpdat{$i}{4}{stop} - $tmpdat{$i}{4}{start} + 1;
		    if ($tmpdat{$i}{4}{len} > $tmplen) { $tmplen = $tmpdat{$i}{4}{len}; }
		    $tmppairs{4} = 1;
		}
	    }
	}
	close MFTA;

	# More than one pair available
	my @pairlist = sort {$a <=> $b} keys %tmppairs;
	if (@pairlist > 1) {
	    # Ask user to select TM Pairs
	    $pair = queryPairs(\%tmpdat, \@pairlist, $tgtseq, $tmplen);
	}

	# Only first pair available
	else {
	    $pair = $pairlist[0];
	}
    }

    # Target Sequence
    @tms = ();
    open MFTA, "$tgtmfta";
    while (<MFTA>) {
	my $line = $_;
	chomp $line;
	$line =~ s/\r//g;

	# TM start/stop
	if ($line =~ /^\*\s+(\d+)tm/) {
	    my $i = $1;
	    my @split = split(/\s+/, $line);

	    # Start/stop/length/eta
	    $dat{tgt}{$i}{start}  = $split[$pair * 2];
	    $dat{tgt}{$i}{stop}   = $split[$pair * 2 + 1];
	    $dat{tgt}{$i}{len}    = $dat{tgt}{$i}{stop} - $dat{tgt}{$i}{start} + 1;
	    push @tms, $i;

	    # Sequence
	    $dat{tgt}{$i}{seq} = substr($tgtseq, $dat{tgt}{$i}{start}, $dat{tgt}{$i}{len});
	}
    }
    close MFTA;

    # Return
    return (\%dat, \@tms, $tgtseq);
}

################################################################################
### Get Homology TM Data
################################################################################
sub loadHomologyData {
    my %dat     = %{$_[0]};
    my $hommfta =   $_[1];
    my $hombgf  =   $_[2];
    my $hompfx  =   $_[3];

    # Get Start/Stop info from BGF
    my %hombgftmdat = ();
    open HOMBGF, "$hombgf";
    while (<HOMBGF>) {
	my $line = $_;
	chomp $line;
	$line =~ s/\r//g;

	if ($line =~ /^ATOM/) {
	    my @split = split(/\s+/, $line);
	    my $chain = $split[4];
	    my $rnum  = $split[5];
	    push @{$hombgftmdat{$chain}}, $rnum;
	}
    }
    close HOMBGF;

    # Homology Sequence
    my $homseq = " ";
    open MFTA, "$hommfta";
    while (<MFTA>) {
	my $line = $_;
	chomp $line;
	$line =~ s/\r//g;

	# Sequence
	if ($line =~ /^[ACDEFGHIKLMNPQRSTVWY]/) {
	    $homseq .= $line;
	}

	# TM start/stop
	elsif ($line =~ /^\*\s+(\d+)tm/) {
	    my $i = $1;
	    my @split = split(/\s+/, $line);

	    # start/stop pair
	    my $start = $hombgftmdat{$i}[0];
	    my $stop  = $hombgftmdat{$i}[-1];

	    # Start/stop/length/eta
	    $dat{hom}{$i}{start}  = $start;
	    $dat{hom}{$i}{stop}   = $stop;
	    $dat{hom}{$i}{len}    = $dat{hom}{$i}{stop} - $dat{hom}{$i}{start} + 1;
	    $dat{hom}{$i}{etanum} = $split[11];

	    # Sequence
	    $dat{hom}{$i}{seq} = substr($homseq, $dat{hom}{$i}{start}, $dat{hom}{$i}{len});

	    # Offset
	    $dat{$i}{offset_l} = 0;
	    $dat{$i}{offset_r} = $dat{tgt}{$i}{len} - $dat{hom}{$i}{len};
	}
    }
    close MFTA;

    # Generate INP File
    `$getinp -b $hombgf -m $hommfta`;
    my $inp = "${hompfx}.inp";
    if (! -e $inp) {
	die "Homologize :: Failed to generate INP from user templates:\n".
	    "           :: ${hombgf} and ${hommfta}\n";
    }

    # Get HPC & Eta Residue info from INP
    open INP, "$inp";
    while (<INP>) {
	my @split = split(/\s+/, $_);
	if ($split[1] =~ /^(\d+)tmpl/) {
	    my $i   = $1;
	    my $hpc  = $split[4];

	    # Hydrophobic Center
	    $hpc =~ /^(\d+)\.(\d+)$/; # XXX.YY
	    $dat{hom}{$i}{hpcnum} = $1;
	    $dat{hom}{$i}{hpcdec} = $hpc - $1;
	    my $hpcoffset = $dat{hom}{$i}{hpcnum} - $dat{hom}{$i}{start};
	    $dat{tgt}{$i}{hpcnum} = $dat{tgt}{$i}{start} + $hpcoffset;
	    $dat{tgt}{$i}{hpcdec} = $dat{hom}{$i}{hpcdec};

	    # Eta Residue
	    my $etaoffset = $dat{hom}{$i}{etanum} - $dat{hom}{$i}{start};
	    $dat{tgt}{$i}{etanum} = $dat{tgt}{$i}{start} + $etaoffset;
	}
    }
    close INP;

    # Return
    return (\%dat, $homseq);
}

################################################################################
### Sequence similarity alignment
################################################################################
sub sequenceSimilarityAlignment {
    my %dat    = %{$_[0]};
    my $tgtseq =   $_[1];
    my $homseq =   $_[2];
    my $i      =   $_[3];

    my $range_start = $dat{$i}{offset_l} - 3;
    my $range_stop  = $dat{$i}{offset_l} + 3;
    my $offset_l    = $dat{$i}{offset_l};
    my $offset_r    = $dat{$i}{offset_r};
    my $hpcnum      = $dat{tgt}{$i}{hpcnum};
    my $etanum      = $dat{tgt}{$i}{etanum};
    my $fin_o       = -10;
    my $max_sim     = -100;

    # Cycle through offsets
    for (my $o = -20; $o <= 20; $o++) {
	$dat{$i}{offset_l}    = $offset_l + $o;
	$dat{$i}{offset_r}    = $offset_r + $o;
	$dat{tgt}{$i}{hpcnum} = $hpcnum - $o;

	# Left/Right sequence offsets
	my $tgt_l = max($dat{$i}{offset_l}, 0);
	my $tgt_r = abs(min($dat{$i}{offset_r}, 0));
	my $hom_l = abs(min($dat{$i}{offset_l}, 0));
	my $hom_r = max($dat{$i}{offset_r}, 0);

	# Sequence strings
	my $tgtstr = sprintf "%s%s%s", " " x $tgt_l, $dat{tgt}{$i}{seq}, " " x $tgt_r;	
	my $homstr = sprintf "%s%s%s", " " x $hom_l, $dat{hom}{$i}{seq}, " " x $hom_r;

	# Sequence identity
	my $ovlp   = 0;
	my $id     = 0;
	my $sim    = 0;
	for (my $j = 0; $j < length($tgtstr); $j++) {
	    my $tgt_aa = substr($tgtstr,$j,1);
	    my $hom_aa = substr($homstr,$j,1);

	    # Not gap
	    if (($tgt_aa ne " ") && ($hom_aa ne " ")) {
		$ovlp++;

		# Identical
		if ($tgt_aa eq $hom_aa) {
		    $id++;
		    $sim++;
		}

		# Similar
		elsif ($blosum62{$tgt_aa}{$hom_aa} > 0) {
		    $sim++;
		}
	    }
	}
	if ($sim > $max_sim) {
	    $max_sim = $sim;
	    $fin_o   = $o;
	}
    }

    # Finalize
    $dat{$i}{offset_l}    = $offset_l + $fin_o;
    $dat{$i}{offset_r}    = $offset_r + $fin_o;
    $dat{tgt}{$i}{hpcnum} = $hpcnum - $fin_o;
    $dat{tgt}{$i}{etanum} = $etanum - $fin_o;

    # Return
    return (\%dat);
}

################################################################################
### Print TM
################################################################################
sub printTM {
    my %dat    = %{$_[0]};
    my $tgtseq =   $_[1];
    my $homseq =   $_[2];
    my $i      =   $_[3];
    my $show   =   $_[4];

    # Left/Right sequence offsets
    my $tgt_l = max($dat{$i}{offset_l}, 0);
    my $tgt_r = abs(min($dat{$i}{offset_r}, 0));
    my $hom_l = abs(min($dat{$i}{offset_l}, 0));
    my $hom_r = max($dat{$i}{offset_r}, 0);

    # Sequence strings
    my $tgtstr = sprintf "%s%s%s", " " x $tgt_l, $dat{tgt}{$i}{seq}, " " x $tgt_r;	
    my $homstr = sprintf "%s%s%s", " " x $hom_l, $dat{hom}{$i}{seq}, " " x $hom_r;

    # Sequence identity
    my $ovlp   = 0;
    my $id     = 0;
    my $sim    = 0;
    my $simstr = "";
    my $prostr = "";
    for (my $j = 0; $j < length($tgtstr); $j++) {
	my $tgt_aa = substr($tgtstr,$j,1);
	my $hom_aa = substr($homstr,$j,1);

	# Not gap
	if (($tgt_aa ne " ") && ($hom_aa ne " ")) {
	    $ovlp++;

	    # Identical
	    if ($tgt_aa eq $hom_aa) {
		$id++;
		$sim++;
		$simstr .= "*";
	    }

	    # Similar
	    elsif ($blosum62{$tgt_aa}{$hom_aa} > 0) {
		$sim++;
		$simstr .= ":";
	    }

	    # Mismatch
	    else {
		$simstr .= " ";
	    }

	    # Prolines
	    if ((($tgt_aa eq "P") && ($hom_aa ne "P")) ||
		(($tgt_aa ne "P") && ($hom_aa eq "P"))) {
		$prostr .= "p";
	    } else {
		$prostr .= " ";
	    }
	}

	# Gap
	else {
	    $simstr .= " ";

	    # Prolines
	    if ((($tgt_aa eq "P") && ($hom_aa ne "P")) ||
		(($tgt_aa ne "P") && ($hom_aa eq "P"))) {
		$prostr .= "p";
	    } else {
		$prostr .= " ";
	    }
	}
    }

    # Target eta/hpc
    my $tgt_eh = "";
    for (my $j = $dat{tgt}{$i}{start}; $j <= $dat{tgt}{$i}{stop}; $j++) {
	if (($j == $dat{tgt}{$i}{etanum}) && ($j == $dat{tgt}{$i}{hpcnum})) {
	    $tgt_eh .= "#";
	} elsif ($j == $dat{tgt}{$i}{etanum}) {
	    $tgt_eh .= "e";
	} elsif ($j == $dat{tgt}{$i}{hpcnum}) {
	    $tgt_eh .= "h";
	} else {
	    $tgt_eh .= " ";
	}
    }
    $tgt_eh = sprintf "%s%s%s", " " x $tgt_l, $tgt_eh, " " x $tgt_r;
    my $tgt_hpc_show = floor($dat{tgt}{$i}{hpcnum}+$dat{tgt}{$i}{hpcdec}+0.5);

    # Homology eta/hpc
    my $hom_eh = "";
    for (my $j = $dat{hom}{$i}{start}; $j <= $dat{hom}{$i}{stop}; $j++) {
	if (($j == $dat{hom}{$i}{etanum}) && ($j == $dat{hom}{$i}{hpcnum})) {
	    $hom_eh .= "#";
	} elsif ($j == $dat{hom}{$i}{etanum}) {
	    $hom_eh .= "e";
	} elsif ($j == $dat{hom}{$i}{hpcnum}) {
	    $hom_eh .= "h";
	} else {
	    $hom_eh .= " ";
	}
    }
    $hom_eh = sprintf "%s%s%s", " " x $hom_l, $hom_eh, " " x $hom_r;
    my $hom_hpc_show = floor($dat{hom}{$i}{hpcnum}+$dat{hom}{$i}{hpcdec}+0.5);

    # Lengths
    my $tgt_r2 = 42 - ($tgt_l + $tgt_r + $dat{tgt}{$i}{len});
    my $hom_r2 = 42 - ($hom_l + $hom_r + $dat{hom}{$i}{len});
    my $sim_r2 = 42 - length($simstr);

    # Percent ID/Sim
    my $pct_id  = 100 * ($id  / $ovlp);
    my $pct_sim = 100 * ($sim / $ovlp);

    # Print
    my $tmtxt = sprintf
	"  --- tm %d ---------------\n".
	"         pro   %s%s\n".
	"         e/h   %s%s - eta: %s %d - hpc: %s %.2f\n".
	"  tgt - %4d - %s%s - %4d [len %2d] - id:  %4.1f %% [%2d \#]\n".
	"  hom - %4d - %s%s - %4d [len %2d] - sim: %4.1f %% [%2d \#]\n".
	"         sim   %s%s - overlap: %d\n".
	"         e/h   %s%s - eta: %s %d - hpc: %s %.2f\n\n",
	$i,
	$prostr, " " x $sim_r2,
	$tgt_eh, " " x $sim_r2,
	substr($tgtseq, $dat{tgt}{$i}{etanum}, 1), $dat{tgt}{$i}{etanum},
	substr($tgtseq, $tgt_hpc_show, 1), ($dat{tgt}{$i}{hpcnum} + $dat{tgt}{$i}{hpcdec}),

	$dat{tgt}{$i}{start}, $tgtstr, " " x $tgt_r2, $dat{tgt}{$i}{stop}, $dat{tgt}{$i}{len},
	$pct_id, $id,
	$dat{hom}{$i}{start}, $homstr, " " x $hom_r2,  $dat{hom}{$i}{stop}, $dat{hom}{$i}{len},
	$pct_sim, $sim,
	$simstr, " " x $sim_r2, $ovlp,
	$hom_eh, " " x $sim_r2,

	substr($homseq, $dat{hom}{$i}{etanum}, 1), $dat{hom}{$i}{etanum},
	substr($homseq, $hom_hpc_show, 1), ($dat{hom}{$i}{hpcnum}+$dat{hom}{$i}{hpcdec});
    if ($show) {
	print $tmtxt;
    }

    # Return
    return $tmtxt;
}

################################################################################
### Query the User about which pair to use
################################################################################
sub queryPairs {
    my %dat   = %{$_[0]};
    my @pairs = @{$_[1]};
    my $seq   =   $_[2];
    my $len   =   $_[3];

    # Options
    my $match = join("|", @pairs);
    my $querymessage =
	"Select TM Pair [" . join(", ", @pairs) . "] ";

    # Clear Screen
    system("clear");

    # Print Pairs
    foreach my $p (@pairs) {
	print " --- Start/Stop $p ---------------\n";
	foreach my $i (@tms) {
	    printf
		" TM %d - %4d - %-${len}s - %4d [ %2d ]\n",
		$i, $dat{$i}{$p}{start},
		substr($seq, $dat{$i}{$p}{start}, $dat{$i}{$p}{len}),
		$dat{$i}{$p}{stop}, $dat{$i}{$p}{len};
	}
	print "\n";
    }

    # Print Options
    print $querymessage;

    # Parse Query
    my $query = 0;
    while ($query !~ /^$match$/) {
	# Get User Input
	$query = <>;
	chomp $query;

	# Unknown option
	if ($query !~ /^$match$/) {
	    print
		"Unknown Option: $query\n\n".
		"$querymessage";
	}
    }

    # Return
    return $query;
}

################################################################################
### Query the User about Modifying the TMs
################################################################################
sub queryTMs {
    my %dat    = %{$_[0]};
    my $tgtseq =   $_[1];
    my $homseq =   $_[2];
    my @tms    = @{$_[3]};

    # Options
    my $tmmatch = join("|", @tms);
    my $querymessage =
	"Options:\n".
	"  Modify TM Region [" . join(", ", @tms) . "]\n".
	"  Finalize BGF     [F]\n".
	"  Quit             [Q]\n\n".
	"Select Option:  ";

    # Print TMs
    system("clear");
    foreach my $i (@tms) {
	printTM(\%dat, $tgtseq, $homseq, $i, 1);
    }

    # Print Options
    print $querymessage;

    # Parse Query
    my $query = "blank";
    while ($query !~ /^F$/i) {
	# Get User Input
	$query = <>;
	chomp $query;

	# Modify TM Region
	if ($query =~ /^($tmmatch)$/) {
	    # Modify TM
	    my @ret = modifyTM(\%dat, $tgtseq, $homseq, $query);
	    %dat = %{$ret[0]};

	    # Print TMs
	    system("clear");
	    foreach my $i (@tms) {
		printTM(\%dat, $tgtseq, $homseq, $i, 1);
	    }

	    # Print Options
	    print $querymessage;
	}

	# Make BGF
	elsif ($query =~ /^F$/i) {
	    # Done with subroutine
	    # Break out of loop to return data
	    last;
	}

	# Quit
	elsif ($query =~ /^Q$/i) {
	    print "\nQuitting!\n\n";
	    exit;
	}

	# Unknown
	else {
	    print
		"Unknown Option: $query\n\n".
		"Select Option:  ";
	}
    }

    # Return
    return (\%dat);
}

################################################################################
### Modify TM Region Parameters
################################################################################
sub modifyTM {
    my %dat    = %{$_[0]};
    my $tgtseq =   $_[1];
    my $homseq =   $_[2];
    my $i      =   $_[3];

    # Options
    my $querymessage =
	"Options:\n".
	"  Move target  left / right [L / R]\n".
	"  Move eta res left / right [E / F]\n".
	"  Move HPC res left / right [H / I]\n".
	"  Finished editing TM       [X]\n\n".
	"Select Option:  ";

    # Clear Screen
    system("clear");

    # Print TM region
    printTM(\%dat, $tgtseq, $homseq, $i, 1);

    # Print Options
    print $querymessage;

    # Parse Query
    my $query = "blank";
    while ($query !~ /^X$/i) {
	# Get User Input
	$query = <>;
	chomp $query;
	my $reprint = 0;

	# Target Left
	if ($query =~ /^L$/i) {
	    $dat{$i}{offset_l}    -= 1;
	    $dat{$i}{offset_r}    -= 1;
	    $dat{tgt}{$i}{hpcnum} += 1;
	    $reprint = 1;
	}

	# Target Right
	elsif ($query =~ /^R$/i) {
	    $dat{$i}{offset_l}      += 1;
	    $dat{$i}{offset_r}      += 1;
	    $dat{tgt}{$i}{hpcnum} -= 1;
	    $reprint = 1;
	}

	# Eta Left
	elsif ($query =~ /^E$/i) {
	    $dat{tgt}{$i}{etanum} -= 1;
	    $reprint = 1;
	}

	# Eta Right
	elsif ($query =~ /^F$/i) {
	    $dat{tgt}{$i}{etanum} += 1;
	    $reprint = 1;
	}

	# HPC Left
	elsif ($query =~ /^H$/i) {
	    $dat{tgt}{$i}{hpcnum} -= 1;
	    $reprint = 1;
	}

	# HPC Right
	elsif ($query =~ /^I$/i) {
	    $dat{tgt}{$i}{hpcnum} += 1;
	    $reprint = 1;
	}

	# Unknown Option
	elsif ($query !~ /^X$/i) {
	    print
		"Unknown Option: $query\n\n".
		"Select Option:  ";
	}

	# Reprint
	if ($reprint) {
	    # Clear Screen
	    system("clear");

	    # Print TM region
	    printTM(\%dat, $tgtseq, $homseq, $i, 1);

	    # Print Options
	    print $querymessage;
	}
    }

    # Return
    return (\%dat);
}

################################################################################
### Generate Homology BGF & MFTA
################################################################################
sub homologyBGF {
    my %dat     = %{$_[0]};
    my @tms     = @{$_[1]};
    my $tgtseq  =   $_[2];
    my $tgtmfta =   $_[3];
    my $hompfx  =   $_[4];
    my $homseq  =   $_[5];
    my $hombgf  =   $_[6];
    my $hommfta =   $_[7];
    my $overlap =   $_[8];
    my $trunc   =   $_[9];
    my $pfx     =   $_[10];

    # Generating Homology BGF
    # 1) Copy template BGF
    # 2) For each TM:
    #    A) Renumber TM residues
    #    B) Resolve any N-term Pro->Non Pro mutations
    #    C) Scream to AGPST
    #    D) Minimize to 0.5
    #    E) Scream to final residues
    # 3) Merge TM Bundle
    # 4) Realign TMs

    system("clear");
    print
	"Building Homology BGF:\n\n".
	"  --- Orienting Template ---------------\n";
    
    # Copy template BGF
    copy("${hompfx}.bgf",  "template.bgf");
    copy("${hompfx}.mfta", "template.mfta");
    copy("${hompfx}.inp",  "template.inp");

    # Make sure template BGF is properly oriented
    `$alninp -b template.bgf -m template.mfta -i template.inp >& /dev/null`;
    move("template.aligned.bgf", "template.bgf");
    print "\n";

    # For each TM region
    my $mergecmd = "$merge";
    foreach my $i (@tms) {
     	$mergecmd .= " tm.${i}.fin.bgf";

	# Print TM region
	printTM(\%dat, $tgtseq, $homseq, $i, 1);

     	# Chop off TM region
     	`$pwb template.bgf -c $i -o tm.${i}.bgf`;

     	# Renumber TM region
     	print "  ...renumbering...\n";
     	renumber(\%dat, $i, "tm.${i}.bgf", "tm.${i}.renum.bgf");

	# Extend/truncate
	print "  ...extend/truncate...\n";
	applySS(\%dat, $i, "tm.${i}.renum.bgf", "tm.${i}.ss.bgf", $overlap, $trunc);

	# Scream to AGPST
	print "  ...alanize [AGPST]...\n";
	screamAGPST(\%dat, $i, $tgtseq, $homseq, "tm.${i}.ss.bgf", "tm.${i}.agpst.bgf");

	# Minimize to 0.5
	print "  ...minimize...\n";
	minimize(\%dat, $i, "tm.${i}.agpst.bgf", "tm.${i}.min.bgf");

	# Scream to final residues
	print "  ...scream...\n";
	screamFinal(\%dat, $i, $tgtseq, "tm.${i}.min.bgf", "tm.${i}.fin.bgf");

	print "\n";

     	# Cleanup
	unlink "tm.${i}.bgf";
	unlink "tm.${i}.renum.bgf";
	unlink "tm.${i}.ss.bgf";
	unlink "tm.${i}.agpst.bgf";
	unlink "tm.${i}.min.bgf";
    }

    # Merge BGF
    print " --- Merging TMs into Bundle ---------------\n";
    `$mergecmd -o target.bgf`;
    print "\n";

    # Cleanup
    foreach my $i (@tms) {
	unlink "tm.${i}.fin.bgf";
    }

    # INP File
    my $newinp = "";
    open INP, "template.inp";
    while (<INP>) {
	my $line = $_;
	chomp $line;
	$line =~ s/\r//g;

	if ($line =~ /^\*\s+(\d+)/) {
	    my $i = $1;
	    my @split = split(/\s+/, $line);
	    $split[4] = $dat{tgt}{$i}{hpcnum} + $dat{tgt}{$i}{hpcdec};
	    $split[8] = substr($tgtseq, $dat{tgt}{$i}{etanum}, 1);
	    $split[9] = $dat{tgt}{$i}{etanum};
	    $line = sprintf "%1s %6s %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f %4s %4d\n", @split;
	}
	$newinp .= $line;
    }
    close INP;
    open INP, ">target.inp";
    print INP $newinp;
    close INP;

    # MFTA File
    my $finmfta = printMFTA(\%dat, \@tms, $tgtseq, $tgtmfta, "target.mfta");

    # Align
    print " --- Realigning Helices in Bundle ---------------\n";
    `$alninp -b target.bgf -m target.mfta -i target.inp`;
    print "\n";

    # Move target files
    move("target.aligned.bgf", "${pfx}.bgf");
    move("target.inp",         "${pfx}.inp");
    move("target.mfta",        "${pfx}.mfta");

    # Cleanup
    unlink "target.bgf";
    unlink "template.bgf";
    unlink "template.inp";
    unlink "template.mfta";

    # Return
    return (\%dat, $finmfta);
}

################################################################################
### P->NonP Mutation
################################################################################
sub pro2ala {
    my $in  = $_[0];
    my $n   = $_[1];

    #0         10        20        30        40        50        60        70
    #01234567890123456789012345678901234567890123456789012345678901234567890
    #ATOM       1  N    PRO 7  309    3.38035 -19.41013  16.93745 N_R    3 0 -0.29000
    #ATOM       2 HN    PRO 7  309    2.37977 -19.14869  16.85590 H___A  1 0  0.00000
    #ATOM       3  CA   PRO 7  309    4.34423 -18.63016  17.66910 C_3    4 0  0.02000
    #ATOM       4 HCA   PRO 7  309    3.98299 -18.48641  18.69034 H_     1 0  0.09000
    #ATOM       5  CB   PRO 7  309    5.57243 -19.56221  17.73116 C_3    4 0 -0.18000
    #ATOM       6 HCB   PRO 7  309    6.50530 -19.00436  17.72022 H_     1 0  0.09000
    #ATOM       7 HCB   PRO 7  309    5.52631 -20.17977  18.63131 H_     1 0  0.09000
    #ATOM       8  CG   PRO 7  309    5.43608 -20.45073  16.49419 C_3    4 0 -0.18000
    #ATOM       9 HCG   PRO 7  309    5.81171 -19.92916  15.61117 H_     1 0  0.09000
    #ATOM      10 HCG   PRO 7  309    5.94471 -21.40970  16.60991 H_     1 0  0.09000
    #ATOM      11  CD   PRO 7  309    3.92194 -20.61701  16.39275 C_3    4 0  0.00000
    #ATOM      12 HCD   PRO 7  309    3.63725 -20.77198  15.35143 H_     1 0  0.09000
    #ATOM      13 HCD   PRO 7  309    3.59997 -21.47050  16.99361 H_     1 0  0.09000
    #ATOM      14  C    PRO 7  309    4.71004 -17.32737  17.11572 C_2    3 0  0.51000
    #ATOM      15  O    PRO 7  309    5.05385 -17.22041  15.94561 O_2    1 2 -0.51000
	
    #ATOM     107  N    ALA 7  315    8.81692 -13.84430  11.31998 N_R    3 0 -0.47000
    #ATOM     108 HN    ALA 7  315    8.81092 -14.37952  12.12987 H___A  1 0  0.31000
    #ATOM     109  CA   ALA 7  315    9.36602 -14.42770  10.12610 C_3    4 0  0.07000
    #ATOM     110 HCA   ALA 7  315   10.35749 -13.99640   9.96861 H_     1 0  0.09000
    #ATOM     111  CB   ALA 7  315    9.55658 -15.94135  10.35400 C_3    4 0 -0.27000
    #ATOM     112 HCB   ALA 7  315   10.07481 -16.38564   9.50295 H_     1 0  0.09000
    #ATOM     113 HCB   ALA 7  315   10.14742 -16.11676  11.25449 H_     1 0  0.09000
    #ATOM     114 HCB   ALA 7  315    8.58913 -16.42626  10.46347 H_     1 0  0.09000
    #ATOM     115  C    ALA 7  315    8.55655 -14.18184   8.90026 C_R    3 0  0.51000
    #ATOM     116  O    ALA 7  315    9.09736 -13.70911   7.87010 O_2    1 2 -0.51000
	
    # CG --> HCB
    # HCG --> delete
    # HCG --> delete
    # HCD --> delete
    # HCD --> delete
    # CD --> HN

    # Parse BGF
    my $txt = "";
    my ($hcb_atom, $hn_atom, $n_atom, $cb_atom);
    my @hcg_atoms;
    my @hcd_atoms;
    open BGF, "$in";
    while (<BGF>) {
	my $line = $_;

	# Atom Lines
	if ($line =~ /^ATOM\s+(\d+)\s+(\S+)\s+\S+\s+\S+\s+$n\s+/) {
	    my $anum  = $1;
	    my $aname = $2;

	    # PRO->ALA
	    substr($line,19,3) = "ALA";

	    # CG  --> HCB
	    if ($aname eq "CG") {
		substr($line,13,3) = "HCB";
		substr($line,61,5) = "H_   ";
		$hcb_atom = $anum;
	    }

	    # HCG --> Delete
	    elsif ($aname eq "HCG") {
		$line = "";
		push @hcg_atoms, $anum;
	    }

	    # HCD --> Delete
	    elsif ($aname eq "HCD") {
		$line = "";
		push @hcd_atoms, $anum;
	    }

	    # CD  --> HN
	    elsif ($aname eq "CD") {
		substr($line,13,3) = "HN ";
		substr($line,61,5) = "H___A";
		$hn_atom = $anum;
	    }

	    # N
	    elsif ($aname eq "N") {
		$n_atom = $anum;
	    }

	    # CB
	    elsif ($aname eq "CB") {
		$cb_atom = $anum;
	    }
	}

	# Conect Lines
	if ($line =~ /^CONECT\s+(\d+)/) {
	    my $anum = $1;

	    # HCG -> Delete
	    for (my $j = 0; $j < @hcg_atoms; $j++) {
		if ($anum == $hcg_atoms[$j]) {
		    $line = "";
		}
	    }

	    # HCD -> Delete
	    for (my $j = 0; $j < @hcd_atoms; $j++) {
		if ($anum == $hcd_atoms[$j]) {
		    $line = "";
		}
	    }

	    # HCB
	    if ($anum == $hcb_atom) {
		$line = sprintf "CONECT%6d%6d\n", $hcb_atom, $cb_atom;
	    }

	    # HN
	    if ($anum == $hn_atom) {
		$line = sprintf "CONECT%6d%6s\n", $hn_atom, $n_atom;
	    }
	}

	$txt .= $line;
    }
    close BGF;

    # Print new BGF
    open BGF, ">$in";
    print BGF $txt;
    close BGF;

    # Renumber
    `$pwb $in -no $in`;

    # Clean up BGF
    `$bgfcheck -b $in`;
    (my $bak = $in) =~ s/.bgf$/.bak/;
    unlink $bak;

    # Done
}

################################################################################
### Renumber TM
################################################################################
sub renumber {
    my %dat = %{$_[0]};
    my $i   =   $_[1];
    my $in  =   $_[2];
    my $out =   $_[3];

    # Overlap = -3
    # 30 XXXYYYYYYYY
    # 50    YYYYYYYYXXX
    # Renumbering starts at hom 50 = tgt 33

    # Overlap = 3
    # 30    YYYYYYYYYYY
    # 50 YYYYYYYYXXX
    # Renumbering starts at hom 50 = tgt 27

    # Find renumbering offset
    my $offset     = $dat{$i}{offset_l};
    my $tgtstart   = $dat{tgt}{$i}{start};
    my $renumstart = $tgtstart - $offset;
    my $homstart   = $dat{hom}{$i}{start};

    # Difference
    my $d = $renumstart - $homstart;

    # Parse BGF
    my $txt = "";
    open BGF, "$in";
    while (<BGF>) {
	my $line = $_;

	# Change residue number
	if ($line =~ /^ATOM\s+\d+\s+\S+\s+\S+\s\S\s+(\d+)/) {
	    substr($line,25,4) = sprintf "%4d", $1 + $d;
	}
	$txt .= $line;
    }
    close BGF;

    # Print BGF
    open BGF, ">$out";
    print BGF $txt;
    close BGF;

    # Done
}

sub quickrenum {
    my $in    = $_[0];
    my $out   = $_[1];
    my $start = $_[2];

    # Difference
    my $d = $start - 1;

    # Parse BGF
    my $txt = "";
    open BGF, "$in";
    while (<BGF>) {
	my $line = $_;

	# Change residue number
	if ($line =~ /^ATOM\s+\d+\s+\S+\s+\S+\s\S\s+(\d+)/) {
	    substr($line,25,4) = sprintf "%4d", $1 + $d;
	}
	$txt .= $line;
    }
    close BGF;

    # Print BGF
    open BGF, ">$out";
    print BGF $txt;
    close BGF;

    # Done
}

sub quickrechain {
    my $in  = $_[0];
    my $chn = $_[1];

    #0         10        20        30        40        50        60        70        80
    #0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
    #ATOM       1  N    ALA 1   30   26.14118  -7.52623  15.30267 N_R    3 0 -0.47000 0   0

    # Parse BGF
    my $txt = "";
    open BGF, "$in";
    while (<BGF>) {
	my $line = $_;

	# Change residue number
	if ($line =~ /^ATOM\s+\d+\s+\S+\s+\S+\s\S\s+(\d+)/) {
	    substr($line,23,1) = $chn;
	}
	$txt .= $line;
    }
    close BGF;

    # Print BGF
    open BGF, ">$in";
    print BGF $txt;
    close BGF;

    # Done
}

################################################################################
### Scream to AGPST
################################################################################
sub screamAGPST {
    my %dat    = %{$_[0]};
    my $i      =   $_[1];
    my $tgtseq =   $_[2];
    my $homseq =   $_[3];
    my $in     =   $_[4];
    my $out    =   $_[5];

    # Read in BGF
    my $pro2alaflag = 0;
    open IN, "$in";
    while (<IN>) {
    	my $line = $_;

	# Change residue number
	if ($line =~ /^ATOM\s+\d+\s+N+\s+(\S+)\s\S\s+(\d+)/) {
	    my $res3 = $1;
	    my $resn = $2;

	    # N-term Proline --> Non Proline
	    # 1) res = PRO
	    # 2) res num = TM start
	    # 3) TM start res != PRO
	    if (($res3 eq "PRO") &&
		($resn == $dat{tgt}{$i}{start}) &&
		(substr($tgtseq, $dat{tgt}{$i}{start}, 1) ne "P")) {
		$pro2alaflag = 1;
	    }
	}
    }
    close IN;

    # If $tgtres = !P and $homres = P
    if ($pro2alaflag) {
	print "       N-term P -> Non-P Mutation\n";
	pro2ala($in, $dat{tgt}{$i}{start});
    }

    # Generate SCREAM list
    my $scr = "";
    for (my $j = $dat{tgt}{$i}{start}; $j <= $dat{tgt}{$i}{stop}; $j++) {
     	my $aa = substr($tgtseq, $j, 1);
	
     	if ($aa =~ /^[AGPST]$/) {
     	    $scr .= " ${aa}${j}_${i}";
     	} else {
     	    $scr .= " A${j}_${i}";
     	}
    }

    ###
    ### Scream
    ###
    `$scream -b $in -r '$scr' >& /dev/null`;

    # Check Output
    if (! -e "best_1.bgf") {
    	die "Homologize :: Alanization failed for TM $i.\n";
    } else {
     	move("best_1.bgf", "$out");
     	unlink "scream.out";
     	unlink "scream.par";
    }

    # Done
}

################################################################################
### Minimize
################################################################################
sub minimize {
    my %dat = %{$_[0]};
    my $i   =   $_[1];
    my $in  =   $_[2];
    my $out =   $_[3];

    # MPSim
    `$runmpsim $in -l 0 -f $ff -s 100 -t 0.5 minvac`;

    # Cleanup
    (my $pfx = $in) =~ s/.bgf//;
    unlink glob "${pfx}_minvac.snap*";
    unlink "${pfx}_minvac.ctl";
    unlink "${pfx}_minvac.out";
    unlink "${pfx}_minvac.traj1";
    move("${pfx}_minvac.fin.bgf", $out);

    # Done
}

################################################################################
### Scream to AGPST
################################################################################
sub screamFinal {
    my %dat    = %{$_[0]};
    my $i      =   $_[1];
    my $tgtseq =   $_[2];
    my $in     =   $_[3];
    my $out    =   $_[4];

    # Generate SCREAM list
    my $scr = "";
    for (my $j = $dat{tgt}{$i}{start}; $j <= $dat{tgt}{$i}{stop}; $j++) {
     	my $aa = substr($tgtseq, $j, 1);
	
     	if ($aa !~ /^[AGP]$/) {
     	    $scr .= " ${aa}${j}_${i}";
     	}
    }

    ###
    ### Scream
    ###
    `$scream -b $in -r '$scr' >& /dev/null`;

    # Check Output
    if (! -e "best_1.bgf") {
	die "Homologize :: Alanization failed for TM $i.\n";
    } else {
	move("best_1.bgf", "$out");
	unlink "scream.out";
	unlink "scream.par";
    }

    # Done
}

################################################################################
### N-term Truncate
################################################################################
sub nTermTruncate {
    my $in    = $_[0];
    my $out   = $_[1];
    my $chn   = $_[2];
    my $start = $_[3]; # New N-term
    my $stop  = $_[4]; # Old C-term

    # Truncate
    `$pwb $in -r '${start}...${stop}${chn}' +H -no $out`;

    # Clean
    `$bgfcheck -b $out`;
    (my $tmp = $out) =~ s/.bgf$/.bak/;
    unlink $tmp;

    # Done
}

################################################################################
### C-term Truncate
################################################################################
sub cTermTruncate {
    my $in    = $_[0];
    my $out   = $_[1];
    my $chn   = $_[2];
    my $start = $_[3]; # New N-term
    my $stop  = $_[4]; # New C-term

    # Truncate
    `$pwb $in -r '${start}...${stop}${chn}' +H -no $out`;

    # Clean
    `$bgfcheck -b $out`;
    (my $tmp = $out) =~ s/.bgf$/.bak/;
    unlink $tmp;

    # Done
}

################################################################################
### N-term Extend
################################################################################
sub nTermExtend {
    my $in       = $_[0];
    my $out      = $_[1];
    my $chn      = $_[2];
    my $oldstart = $_[3]; # Old N-term
    my $newstart = $_[4]; # New N-term
    my $stop     = $_[5]; # C-term
    my $overlap  = $_[6]; # Extension overlap
    my $trunc    = $_[7]; # Trim N-term

    # Extension segment: $oldstart - $newstart
    my $extlen   = $oldstart - $newstart + $overlap;
    my $extstop  = $oldstart + $overlap - 1;
    my $exttrunc = $oldstart - 1;
    unlink "ext.bgf";
    copy("${polyalasrc}/ala${extlen}.bgf", "ext.bgf");

    # Renumber Extension
    quickrenum("ext.bgf", "ext.bgf", $newstart);
    quickrechain("ext.bgf", $chn);

    # Align Extension
    my $vmd =
	"mol new $in     type \{bgf\} first 0 last -1 step 1 waitfor 1\n".
	"mol new ext.bgf type \{bgf\} first 0 last -1 step 1 waitfor 1\n".
	"set sel1 \[atomselect 0 \"name CA and resid $oldstart to $extstop\"\]\n".
	"set sel2 \[atomselect 1 \"name CA and resid $oldstart to $extstop\"\]\n".
	"set tmat \[measure fit \$sel2 \$sel1\]\n".
	"set move \[atomselect 1 \"all\"\]\n".
	"\$move move \$tmat\n".
	"animate write bgf ext.aligned.bgf beg 0 end 0 skip 1 1\n".
	"quit\n";
    open VMD, ">vmd.vmd";
    print VMD $vmd;
    close VMD;
    my $lines = `/exec/VMD/bin/vmd -dispdev text -e vmd.vmd`;
    unlink "vmd.vmd";
    `$bgfcheck -b ext.aligned.bgf`;

    # If trimming end of helix
    my $mergeto = "tm.${chn}.mergeto.N.bgf";
    if ($trunc > 0) {
	# New values
	$exttrunc += $trunc;
	$oldstart += $trunc;

	# Truncate Extension Overlap
	`$pwb ext.aligned.bgf -r '${newstart}...${exttrunc}${chn}' -no ext.trunc.bgf`;

	# Trim N-term
	`$pwb $in -r '${oldstart}...${stop}${chn}' -no ${mergeto}`;
    }

    # Not trimming end of helix
    else {
	# Truncate Extension Overlap
	`$pwb ext.aligned.bgf -r '${newstart}...${exttrunc}${chn}' -no ext.trunc.bgf`;

	# Don't Trim N-Term
	copy($in,$mergeto);
    }

    # Merge Extension
    `/ul/caglar/Python/GPCRassembler.py ext.trunc.bgf $mergeto -o $out`;

    # Cleanup BGF
    `$bgfcheck -b $out`;
    if (-e "ext.bgf")         { unlink "ext.bgf"; }
    if (-e "ext.aligned.bak") { unlink "ext.aligned.bak"; }
    if (-e "ext.aligned.bgf") { unlink "ext.aligned.bgf"; }
    if (-e "ext.trunc.bgf")   { unlink "ext.trunc.bgf"; }
    if (-e $mergeto)          { unlink $mergeto; }
    (my $tmp = $out) =~ s/.bgf$/.bak/;
    unlink $tmp;

    # Done
}

################################################################################
### C-term Extend
################################################################################
sub cTermExtend {
    my $in      = $_[0];
    my $out     = $_[1];
    my $chn     = $_[2];
    my $start   = $_[3]; # N-term
    my $oldstop = $_[4]; # Old C-term
    my $newstop = $_[5]; # New C-term
    my $overlap = $_[6]; # Extension overlap
    my $trunc   = $_[7]; # Trim C-term

    # Extension segment: $oldstart - $newstart
    my $extlen   = $newstop - $oldstop + $overlap;
    my $extstart = $oldstop - $overlap + 1;
    my $exttrunc = $oldstop + 1;
    unlink "ext.bgf";
    copy("${polyalasrc}/ala${extlen}.bgf", "ext.bgf");

    # Renumber Extension
    quickrenum("ext.bgf", "ext.bgf", $extstart);
    quickrechain("ext.bgf", $chn);

    # Align Extension
    my $vmd =
	"mol new $in     type \{bgf\} first 0 last -1 step 1 waitfor 1\n".
	"mol new ext.bgf type \{bgf\} first 0 last -1 step 1 waitfor 1\n".
	"set sel1 \[atomselect 0 \"name CA and resid $extstart to $oldstop\"\]\n".
	"set sel2 \[atomselect 1 \"name CA and resid $extstart to $oldstop\"\]\n".
	"set tmat \[measure fit \$sel2 \$sel1\]\n".
	"set move \[atomselect 1 \"all\"\]\n".
	"\$move move \$tmat\n".
	"animate write bgf ext.aligned.bgf beg 0 end 0 skip 1 1\n".
	"quit\n";
    open VMD, ">vmd.vmd";
    print VMD $vmd;
    close VMD;
    my $lines = `/exec/VMD/bin/vmd -dispdev text -e vmd.vmd`;
    unlink "vmd.vmd";
    `$bgfcheck -b ext.aligned.bgf`;

    # If trimming end of helix
    my $mergeto = "tm.${chn}.mergeto.C.bgf";
    if ($trunc > 0) {
	# New values
	$exttrunc -= $trunc;
	$oldstop  -= $trunc;

	# Truncate Overlap
	`$pwb ext.aligned.bgf -r '${exttrunc}...${newstop}${chn}' -no ext.trunc.bgf`;

	# Trim C-term
	`$pwb $in -r '${start}...${oldstop}${chn}' -no ${mergeto}`;
    }

    # Not trimming end of helix
    else {
	# Truncate Overlap
	`$pwb ext.aligned.bgf -r '${exttrunc}...${newstop}${chn}' -no ext.trunc.bgf`;

	# Don't Trim C-Term
	copy($in,$mergeto);
    }

    # Merge Extension
    `/ul/caglar/Python/GPCRassembler.py $mergeto ext.trunc.bgf -o $out`;

    # Cleanup BGF
    `$bgfcheck -b $out`;
    if (-e "ext.bgf")         { unlink "ext.bgf"; }
    if (-e "ext.aligned.bak") { unlink "ext.aligned.bak"; }
    if (-e "ext.aligned.bgf") { unlink "ext.aligned.bgf"; }
    if (-e "ext.trunc.bgf")   { unlink "ext.trunc.bgf"; }
    if (-e $mergeto)          { unlink $mergeto; }
    (my $tmp = $out) =~ s/.bgf$/.bak/;
    unlink $tmp;

    # Done
}

################################################################################
### Apply secondary structure
################################################################################
sub applySS {
    my %dat     = %{$_[0]};
    my $i       =   $_[1];
    my $in      =   $_[2];
    my $out     =   $_[3];
    my $overlap =   $_[4];
    my $trunc   =   $_[5];

    # Old & New Start/Stop Values
    my $offset_l = $dat{$i}{offset_l};
    my $old_nterm = $dat{tgt}{$i}{start} - $offset_l;
    my $new_nterm = $dat{tgt}{$i}{start};
    my $offset_r = $dat{$i}{offset_r};
    my $old_cterm = $dat{tgt}{$i}{stop} - $offset_r;
    my $new_cterm = $dat{tgt}{$i}{stop};
    (my $nterm_out = $in) =~ s/.bgf$/.nterm.bgf/;

    ###
    ### N-term side
    ###

    # N-term Extension
    if ($offset_l < 0) {
	printf "       N-term: %d to %d [extend]\n", $old_nterm, $new_nterm;
     	nTermExtend($in, $nterm_out, $i, $old_nterm, $new_nterm, $old_cterm,
		    $overlap, $trunc);
    }

    # N-term Truncation
    elsif ($offset_l > 0) {
	printf "       N-term: %d to %d [truncate]\n", $old_nterm, $new_nterm;
     	nTermTruncate($in, $nterm_out, $i, $new_nterm, $old_cterm);
    }

    # N-term Same
    else {
	printf "       N-term: %d [no change]\n", $old_nterm, $new_nterm;
	copy($in, $nterm_out);
    }

    ###
    ### C-term side
    ###

    # C-term Truncation
    if ($offset_r < 0) {
	printf "       C-term: %d to %d [truncate]\n", $old_cterm, $new_cterm;
     	cTermTruncate($nterm_out, $out, $i, $new_nterm, $new_cterm);
    }

    # C-term Extension
    elsif ($offset_r > 0) {
	printf "       C-term: %d to %d [extend]\n", $old_cterm, $new_cterm;
     	cTermExtend($nterm_out, $out, $i, $new_nterm, $old_cterm, $new_cterm,
		    $overlap, $trunc)
    }

    # C-term Same
    else {
	printf "       C-term: %d [no change]\n", $old_cterm, $new_cterm;
     	copy($nterm_out, $out);
    }

    # Cleanup
    unlink $nterm_out;
    `$bgfcheck -b $out`;
    (my $tmp = $out) =~ s/.bgf$/.bak/;
    unlink $tmp;

    # Done
}

################################################################################
### Print MFTA Files
################################################################################
sub printMFTA {
    my %dat     = %{$_[0]};
    my @tms     = @{$_[1]};
    my $tgtseq  =   $_[2];
    my $oldmfta =   $_[3];
    my $out     =   $_[4];

    # Header & Sequence
    my $txt = "";
    open MFTA, "$oldmfta";
    my @lines = <MFTA>;
    close MFTA;
    foreach my $line (@lines) {
	if ($line !~ /^\s*(\*|\#)/) {
	    $txt .= $line;
	}
    }

    # Start/Stop/Eta
    foreach my $i (@tms) {
	$txt .=
	    sprintf "* %dtm   %4d %4d   X X   X X   X X   %s %4d   A\n",
	    $i, $dat{tgt}{$i}{start}, $dat{tgt}{$i}{stop},
	    substr($tgtseq, $dat{tgt}{$i}{etanum}, 1),
	    $dat{tgt}{$i}{etanum};
    }

    # HPC
    foreach my $i (@tms) {
	my $tmphpc = $dat{tgt}{$i}{hpcnum} + $dat{tgt}{$i}{hpcdec};
	$txt .=
	    sprintf "* %dhpc   %7.2f   X.00   X.00   X.00   X.00   X.00\n",
	    $i, $tmphpc;
    }

    # Print
    open MFTA, ">$out";
    print MFTA $txt;
    close MFTA;

    # Done
    return $txt;
}

################################################################################
### Final printing
################################################################################
sub printFinal {
    my %dat     = %{$_[0]};
    my @tms     = @{$_[1]};
    my $tgtmfta =   $_[2];
    my $hompfx  =   $_[3];
    my $overlap =   $_[4];
    my $trunc   =   $_[5];
    my $pfx     =   $_[6];

    system("clear");
    system("clear");
    my $cwd = cwd();
    my $txt =
	"Homologize2 :: " . localtime() . "\n".
	" :: Target MFTA      :: $tgtmfta\n".
	" :: Homology MFTA    :: ${hompfx}.mfta\n".
	" :: Homology BGF     :: ${hompfx}.bgf\n".
	" :: Overlap Setting  :: $overlap\n".
	" :: Truncate Setting :: $trunc\n".
	" :: Final BGF        :: ${pfx}.bgf\n".
	" :: Final MFTA       :: ${pfx}.mfta\n\n".
	"TM Regions\n";

    foreach my $i (@tms) {
	$txt .= printTM(\%dat, $tgtseq, $homseq, $i, 0);
    }

    open LOG, ">${pfx}.log";
    print LOG $txt;
    close LOG;

    print $txt;
}

############################################################
### Help                                                 ###
############################################################
sub help {

    my $help = "
Program:
 :: Homologize2.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: Homologize2.pl -m {mfta} -t {template file prefix}

Input:
 :: -m | --tgt         :: Filename
 :: MFTA for the target protein.

 :: -t | --hom         :: File Prefix
 :: Prefix for homology template.  The program needs both
 :: a BGF and an MFTA file using this prefix:
 :: Example: -t tBeta1_2vt4_xray
 ::  * program will expect:
 ::    tBeta1_2vt4_xray.bgf
 ::    tBeta1_2vt4_xray.mfta
 :: Note: The start/stop values used from the homology MFTA
 ::       are expected to be the first pair of values.

 :: --pair             :: Integer
 :: Pair of start/stop values in the target MFTA to use for
 :: secondary structure extensions/truncations.

 :: --overlap          :: Integer
 :: Number of residues of overlap to use when extending helices

 :: --trunc            :: Integer
 :: Number of residues to trim off of the helix when extending
 :: helices

 :: -h | --help        :: No Input
 :: Displays this help message.

Description:
 :: This program constructs a target protein from a homology
 :: template.
 ::
 :: 1) Generate initial alignment of TM regions using sequence
 ::    similarity.
 :: 2) Allow user to adjust:
 ::    a) The alignment profile (helix shape)
 ::    b) The hydrophobic center
 ::    c) The eta residue
 :: 3) Align template bundle to guarantee proper orientation
 :: 4) For each TM region:
 ::    a) Extend/truncate TM to proper length
 ::    b) SCREAM to AGPST
 ::    c) Minimize to 0.5 RMS force
 ::    d) SCREAM to final residues
 :: 5) Merge final TM regions into target bundle
 :: 6) Reorient helices in target bundle
 ::
 :: Helix extensions:
 :: 1) Aligns a polyalanine helix to the end of the target helix
 ::    with an overlap of 8 residues
 :: 2) Trims 2 residues from the old helix
 :: 3) Connects the extension to the helix
 ::
 :: NOTES:
 :: Starting Eta and HPC residues are based on the HOMOLOGY sequence.
 :: Eta and HPC values in the TARGET MFTA file are ignored!

Usage:
 :: Homologize2.pl -m {mfta} -t {template file prefix}

";

    die "$help";
}
