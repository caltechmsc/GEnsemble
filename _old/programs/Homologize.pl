#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
}

use strict;
use warnings;
use Cwd;
use File::Basename;
use File::Copy;
use File::Path;
use File::Spec;
use Getopt::Long qw(:config no_ignore_case);
use List::Util qw(min max);
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

#use HomTools::HomTools;

################################################################################
### Globals ###
################################################################################

# Set up the BLOSUM62 Similarity Matrix
our @blosumAA =
    qw(A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V  B  Z  X  gap);

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
for (my $i = 0; $i < @blosumAA; $i++) {
    for (my $j = 0; $j < @blosumAA; $j++) {
		$blosum62{$blosumAA[$i]}{$blosumAA[$j]} = $blosum62txt[$i][$j];
    }
}

our $biogroup = "/project/Biogroup";
our $biosoft  = "${biogroup}/Software";
our $ge       = "${biosoft}/GEnsemble/programs";
our $clustal  = "${ge}/thirdparty/clustal/clustalw";
our $pwb      = "${ge}/utilities/playWithBGF/playWithBGF";
our $runmpsim = "${ge}/utilities/runMPSim.pl";
our $scream   = "${biosoft}/scream3/programs/scream3_wrap.pl";
our $ff       = "${biogroup}/FF/dreiding-0.3.par";
our $merge    = "${biogroup}/scripts/BGFtools/mergeBGFs.py";
our $mafft_bin   = "${biosoft}/GEnsemble/programs/thirdparty/mafft/lib/mafft";
our $mafft_exe   = "${biosoft}/GEnsemble/programs/thirdparty/mafft/mafft";
our $getinp      = "${biosoft}/GEnsemble/programs/GetTemplate-3.pl";
our $alninp      = "${biosoft}/GEnsemble/programs/Align2Template-3.pl";
our $bgfcheck    = "${biogroup}/scripts/perl/BGFCheck.pl";
#our $fastasource = "${Bin}/fasta/";
#our $polyalasrc  = "${Bin}/polyala/";
our $fastasource = "/ul/griffith/dev/Homologize/fasta/";
our $polyalasrc  = "/ul/griffith/dev/Homologize/polyala/";

################################################################################

my ($help, $mfta, $hom, $hompfx, $hombgf, $hommfta, $pfx, $debug);
my $pair    = 1;
my $overlap = 8;
my $trunc   = 2;

if (@ARGV == 0) { help(); }

#ABCDEFGHIJKLMNOPQRSTUVWXYZ
#abcdefghijklmnopqrstuvwxyz

#ABCDEFGHIJKLMNOPQRSTUVWXYZ
#abcdefg ijklmnopqrstuvwxyz
GetOptions ('h|help'          => \$help,
	    'm|mfta=s'        => \$mfta,
	    't|temp=s'        => \$hom,
	    'p|pfx=s'         => \$pfx,
	    'pair=i'          => \$pair,
	    'overlap=i'       => \$overlap,
	    'trunc=i'         => \$trunc,
	    'debug'           => \$debug);

if ($help) { help(); }

# Target Protein
if (! $mfta) {
    die "Homologize :: Must provide MFTA/FTA file for target protein!\n";
} elsif (! -e $mfta) {
    die "Homologize :: Could not find MFTA/FTA file for target protein: $mfta\n";
}

# Homology Protein
if (! $hom) {
    die "Homologize :: Must specify a template protein!\n";
} else {
    # Homology BGF
    if ($hom =~ /.bgf$/) {
	$hombgf = $hom;
	($hompfx = $hombgf) =~ s/.bgf$//;
	$hommfta = "${hompfx}.mfta";
    }

    # Homology MFTA
    elsif ($hom =~ /.mfta$/) {
	$hommfta = $hom;
	($hompfx = $hommfta) =~ s/.mfta$//;
	$hombgf = "${hompfx}.bgf";
    }

    # Homology Prefix
    else {
	$hom =~ s/\.$//;
	$hompfx  = $hom;
	$hombgf  = "${hompfx}.bgf";
	$hommfta = "${hompfx}.mfta";
    }

    # Check for files
    if ((! -e $hombgf) || (! -e $hommfta)) {
	my $str = "Homologize :: Based on template input '-t $hom' could not find:\n";
	if (! -e $hombgf) {
	    $str .= " :: Template BGF  :: $hombgf\n";
	}
	if (! -e $hommfta) {
	    $str .= " :: Template MFTA :: $hommfta\n";
	}
	die $str;
    }
}

# Output Prefix
if (!$pfx) {
    $pfx = "";
}
if ($pfx eq "") {
    (my $pfx1 = $mfta) =~ s/.(mfta|fta)$//;
    $pfx1 =~ s/\./\_/g;
    $pfx = "${pfx1}.${hompfx}";
}

############################################################
### Main Routine                                         ###
############################################################

# Input Options
# 1) Target:
#    A) MFTA
#    B) FTA
# 2) Homology:
#    B) files   (eg beta1.2vt4.bgf, beta1.2vt4.mfta)

# Directory setup
mkdir "${pfx}";
copy($mfta,    $pfx);
copy($hombgf,  $pfx);
copy($hommfta, $pfx);
chdir "${pfx}";

# Generate Alignment, Condense, Map
my @ret    = alignment($mfta, $hompfx, $pfx);
my @aln    = @{$ret[0]};
my %map    = %{$ret[1]};
my $alnlen =   $ret[2];
my $tgtlen =   $ret[3];
my $homlen =   $ret[4];

# Load Homology Info (Start/Stop/HPC/Eta)
@ret    = loadHomologyData($hompfx, \@aln, \%map, $alnlen, $tgtlen, $homlen);
my %dat = %{$ret[0]};
my @tms = @{$ret[1]};

# Map Homology Info onto Target
@ret = mapHomologyData(\@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
%dat = %{$ret[0]};

# Modify TM Regions
@ret = queryTMs(\@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen, $mfta);
%dat = %{$ret[0]};

# Generate BGF
@ret = homologyBGF(\@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen, $mfta, $hompfx,
		   $pair, $overlap, $trunc, $pfx);
%dat       = %{$ret[0]};
my $use_ss =   $ret[1];

# Final Print
chdir "..";
printFinal(\@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen, $mfta, $hompfx,
	   $pair, $overlap, $trunc, $pfx, $use_ss);

print "\nFinished\n\n";

exit;



################################################################################
### Generate and Parse Alignment
################################################################################
sub alignment {
    my $mfta   = $_[0];
    my $hompfx = $_[1];
    my $pfx    = $_[2];

    # Fasta Text
    my $fta = "";
    my $tgthdr = ""; # Target Fasta Header
    my $tgtseq = ""; # Target Sequence
    my $homhdr = ""; # Homology Fasta Header
    my $homseq = ""; # Homology Sequence
    my $othfta = ""; # Other Fasta Input
    my $othhdr = ""; # Other Fasta Header
    my $othseq = ""; # Other Sequence

    # Parse Target MFTA
    open MFTA, "$mfta";
    while (<MFTA>) {
	my $line = $_;
	chomp $line;
	$line =~ s/\r//g;

	if ($line =~ /^\>/) {
	    if ($line =~ /^\>P1;/) { $line =~ s/^\>P1;/\>/; }
	    if ($line !~ /^\>sp\|/) { $line =~ s/^\>/\>sp\|/; }
	    $tgthdr = $line;
	} elsif ($line =~ /^[ACDEFGHIKLMNPQRSTVWY]/) {
	    $tgtseq .= $line;
	}
    }
    close MFTA;
    $fta .= $tgthdr . "\n" . $tgtseq . "\n";

    # Parse Homology MFTA
    open MFTA, "${hompfx}.mfta";
    while (<MFTA>) {
	my $line = $_;
	chomp $line;
	$line =~ s/\r//g;

	if ($line =~ /^\>/) {
	    if ($line =~ /^\>P1;/) { $line =~ s/^\>P1;/\>/; }
	    if ($line !~ /^\>sp\|/) { $line =~ s/^\>/\>sp\|/; }
	    $homhdr = $line;
	} elsif ($line =~ /^[ACDEFGHIKLMNPQRSTVWY]/) {
	    $homseq .= $line;
	}
    }
    close MFTA;
    $fta .= $homhdr . "\n" . $homseq . "\n";

    # Parse Other FTAs
    my @known = glob "${fastasource}/*.fta";
    foreach my $file (@known) {
	$othhdr = "";
	$othseq = "";

	open FTA, "$file";
	while (<FTA>) {
	    my $line = $_;
	    chomp $line;
	    $line =~ s/\r//g;

	    if ($line =~ /^\>/) {
		$othhdr = $line;
	    } elsif ($line =~ /^[ACDEFGHIKLMNPQRSTVWY]/) {
		$othseq .= $line;
	    }
	}
	close FTA;

	# Make sure this sequence isn't the same as the
	# target or homology sequences
	if (($othseq ne $tgtseq) && ($othseq ne $homseq)) {
	    $fta .= $othhdr . "\n" . $othseq . "\n";
	}
    }

    # FTA to Align
    open FTA, ">${pfx}.fta";
    print FTA $fta;
    close FTA;

    # MAFFT Align (--genafpair since few sequences)
    my ($pir, $aln) = mafft("${pfx}.fta");

    # Condense/Map Alignment
    my @ret    = condense($pir, $pfx);
    my @cnd    = @{$ret[0]};
    my %map    = %{$ret[1]};
    my $len    =   $ret[2];
    my $tgtlen =   $ret[3];
    my $homlen =   $ret[4];

    # Return
    return (\@cnd, \%map, $len, $tgtlen, $homlen);
}

################################################################################
### MAFFT Alignment
################################################################################
sub mafft {
    my $fta = $_[0];

    (my $pfx = $fta) =~ s/.fta$//;

    # Set up MAFFT Environment
    $ENV{MAFFT_BINARIES} = "$mafft_bin";

    # MAFFT
    my $command =
	"(${mafft_exe} --genafpair --op 10.0 --ep 0.2 $fta".
	" > ${pfx}.pir) >& ${pfx}.mafft.out";
    `$command`;
    my $pir = "${pfx}.pir";
    my $aln = pir2aln($pir);
    unlink "${pfx}.mafft.out";
    return ($pir,$aln);
}

################################################################################
### PIR to ALN conversion
################################################################################
sub pir2aln {
    my $f = $_[0]; # PIR alignment file

    my $txt = "";
    open PIR, $f; my @lines = <PIR>; close PIR;
    for (my $i = 0; $i < @lines; $i++) {
	my $line = $lines[$i];
	if ($i == 0) {
	    $txt .= $line . "\n";
	} elsif ($line =~ /^\>/) {
	    $txt .= "*\n" . $line . "\n";
	} else {
	    $txt .= $line;
	}
    }
    $txt .= "*\n";
    open PIR, ">tmp.pir"; print PIR $txt; close PIR;
    
    (my $nf = $f) =~ s/.pir$/.aln/;
    `$clustal -infile=tmp.pir -convert -outfile=${nf}`;
    unlink "tmp.pir";
    return $nf;
}

################################################################################
### Condense Alignment
################################################################################
sub condense {
    my $pir = $_[0]; # PIR File
    my $pfx = $_[1]; # Output Prefix

    # Load Pir
    my $txt = "";
    open PIR, "$pir"; while (<PIR>) { $txt .= $_; } close PIR;
    my @split = split(/\n\>/, $txt);

    my $tgt      = $split[0];
    my @tgtsplit = split(/\n/, $tgt);
    my $tgthdr   = shift @tgtsplit;
    $tgt         = join("", @tgtsplit);

    my $hom      = ">" . $split[1];
    my @homsplit = split(/\n/, $hom);
    my $homhdr   = shift @homsplit;
    $hom         = join("", @homsplit);
    
    my $len = length($tgt);
    
    # Parse Sequences
    my $cndlen = 0;
    my $tgtlen = 0;
    my $cndtgt = "";
    my $homlen = 0;
    my $cndhom = "";
    my $numid  = 0;
    my $numsim = 0;
    my @cnd    = ();
    my %map    = ();
    $cnd[1][0] = $tgthdr;
    $cnd[2][0] = $homhdr;
    for (my $i = 0; $i < $len; $i++) {
	my $a = substr($tgt,$i,1);
	my $b = substr($hom,$i,1);

	# Sequence similarity:
	# $a = $b             --> Identical: '*'
	# $blosum{$a}{$b} > 0 --> Similar:   ':'
	# $a or $b == '-'     --> Mismatch:  ' '
	my $s = $blosum62{$a}{$b};
	if (($a eq "-") || ($b eq "-")) { $s = -1; }

	# Condense & Similarity
	if (($a ne "-") || ($b ne "-")) {
	    $cndlen++;

	    # Mapping
	    # Target: no gap
	    if ($a ne "-") {
		$tgtlen++;
		$map{tgt}{res2aln}{$tgtlen} = $cndlen;
		$map{tgt}{aln2res}{$cndlen} = $tgtlen;
	    }

	    # Template: no gap
	    if ($b ne "-") {
		$homlen++;
		$map{hom}{res2aln}{$homlen} = $cndlen;
		$map{hom}{aln2res}{$cndlen} = $homlen;
	    }

	    # Similarity
	    if ($a eq $b) {
		$cnd[0][$cndlen] = "*";
		$numid++;
		$numsim++;
	    } elsif ($s > 0) {
		$cnd[0][$cndlen] = ":";
		$numsim++;
	    } else {
		$cnd[0][$cndlen] = " ";
	    }

	    # Record sequence info
	    $cnd[1][$cndlen] = $a;
	    $cnd[2][$cndlen] = $b;
	    $cndtgt .= $a;
	    $cndhom .= $b;
	}
    }

    # Generate Condensed PIR/ALN
    my $pirtxt = "${tgthdr}\n${cndtgt}\n${homhdr}\n${cndhom}\n";
    open PIR, ">${pfx}.cnd.pir";
    print PIR $pirtxt;
    close PIR;
    my $alntxt = pir2aln("${pfx}.cnd.pir");

    # Return
    return (\@cnd, \%map, $cndlen, $tgtlen, $homlen);
}

################################################################################
### Get Homology Data
################################################################################
sub loadHomologyData {
    my $hom     =   $_[0];
    my @aln     = @{$_[1]};
    my %map     = %{$_[2]};
    my $alnlen  =   $_[3];
    my $tgtlen  =   $_[4];
    my $homlen  =   $_[5];

    # Homology Template
    my %dat  = ();
    my $bgf  = "${hom}.bgf";
    my $mfta = "${hom}.mfta";
    my $inp  = "${hom}.inp";

    # Generate INP File
    `$getinp -b $bgf -m $mfta`;
    if (! -e $inp) {
	die "Homologize :: Failed to generate INP from user templates:\n".
	    "           :: ${hom}.bgf and ${hom}.mfta\n";
    }

    # Get HPC & Eta Residue info from INP
    my @tms = ();
    open INP, "$inp";
    while (<INP>) {
	my @split = split(/\s+/, $_);
	if ($split[1] =~ /^(\d+)tmpl/) {
	    my $tm   = $1; push @tms, $tm;
	    my $hpc  = $split[4];
	    my $eres = $split[8];
	    my $enum = $split[9];

	    # Eta residue
	    $dat{hom}{$tm}{eres}      = $eres;
	    $dat{hom}{$tm}{enum}{res} = $enum;
	    $dat{hom}{$tm}{enum}{aln} = $map{hom}{res2aln}{$enum};

	    # Hydrophobic Center
	    $hpc =~ /^(\d+)\.(\d+)$/; # XXX.YY
	    $dat{hom}{$tm}{hpcnum}{res} = $1;
	    $dat{hom}{$tm}{hpcnum}{aln} = $map{hom}{res2aln}{$1};
	    $dat{hom}{$tm}{hpcdec}      = $2;
	    $dat{tgt}{$tm}{hpcdec}      = $2;
	    $dat{tgt}{$tm}{hpcres}      = $aln[2][$dat{hom}{$tm}{hpcnum}{aln}];
	}
    }
    close INP;

    # Get Start/Stop info from BGF
    my %hombgftmdat = ();
    open HOMBGF, "$bgf";
    while (<HOMBGF>) {
	my $line = $_;
	if ($line =~ /^ATOM/) {
	    my @split = split(/\s+/, $line);
	    my $chain = $split[4];
	    my $rnum  = $split[5];
	    push @{$hombgftmdat{$chain}}, $rnum;
	}
    }
    close HOMBGF;

    # Get Start/Stop info from MFTA
    my $minreslen = 0;
    my $minalnlen = 0;
    open MFTA, "$mfta";
    while (<MFTA>) {
	my $line = $_;
	if ($line =~ /^\*\s+(\d+)tm/) {
	    my $tm = $1;
	    my @split = split(/\s+/, $line);

	    # start/stop pair
	    my $start = $hombgftmdat{$tm}[0];
	    my $stop  = $hombgftmdat{$tm}[-1];

	    # Start
	    $dat{hom}{$tm}{start}{res} = $start;
	    $dat{hom}{$tm}{start}{aln} = $map{hom}{res2aln}{$start};

	    # Stop
	    $dat{hom}{$tm}{stop}{res} = $stop;
	    $dat{hom}{$tm}{stop}{aln} = $map{hom}{res2aln}{$stop};

	    # Length
	    $dat{hom}{$tm}{length}{res} = $stop - $start + 1;
	    $dat{hom}{$tm}{length}{aln} =
		$map{hom}{res2aln}{$stop} - $map{hom}{res2aln}{$start} + 1;

	    $minreslen = max($minreslen, $dat{hom}{$tm}{length}{res});
	    $minalnlen = max($minalnlen, $dat{hom}{$tm}{length}{aln});

	    # Sequence
	    for (my $i = $map{hom}{res2aln}{$start}; $i <= $map{hom}{res2aln}{$stop}; $i++) {
		$dat{hom}{$tm}{seq}{aln} .= $aln[2][$i];
		if ($aln[2][$i] ne "-") {
		    $dat{hom}{$tm}{seq}{res} .= $aln[2][$i];
		}
	    }
	}
    }
    close MFTA;
    $dat{hom}{minreslen} = $minreslen;
    $dat{hom}{minalnlen} = $minalnlen;

    # Return
    return (\%dat, \@tms);
}

################################################################################
### Map Homology Data to Target
################################################################################
sub mapHomologyData {
    my @aln    = @{$_[0]};
    my %map    = %{$_[1]};
    my %dat    = %{$_[2]};
    my @tms    = @{$_[3]};
    my $alnlen =   $_[4];
    my $tgtlen =   $_[5];
    my $homlen =   $_[6];

    my $minreslen = 0;
    my $minalnlen = 0;

    # For each TM region
    for (my $i = 1; $i <= @tms; $i++) {

	### Begin with eta residue
	# If there is a gap in the target alignment for the homolgy eta residue
	# move backward until we find a non-gap.  If that doesn't work, move
	# forward until we find a non-gap
	$dat{flags}{$i}{aln} = "";
	my $e = $dat{hom}{$i}{enum}{aln};
	while (! defined $map{tgt}{aln2res}{$e}) {
	    $dat{flags}{$i}{aln} = "Possible sequence misalignment\n";
	    $e--;
	    if ($e == 0) {
		$e++;
		while (! defined $map{tgt}{alnres}{$e}) {
		    $e++;
		    if ($e >= $alnlen) {
			die "Homologize :: Error mapping eta residue for TM $i\n";
		    }
		}
		last;
	    }
	}
	$dat{tgt}{$i}{enum}{aln} = $e;
	$dat{tgt}{$i}{enum}{res} = $map{tgt}{aln2res}{$e};
	$dat{tgt}{$i}{eres}      = $aln[1][$e];

	### Find start residue
	# Expand left until the needed number of residues is found
	my $d = $dat{hom}{$i}{enum}{res} - $dat{hom}{$i}{start}{res};
	$dat{tgt}{$i}{start}{res} = $dat{tgt}{$i}{enum}{res} - $d;
	$dat{tgt}{$i}{start}{aln} = $map{tgt}{res2aln}{$dat{tgt}{$i}{start}{res}};

	### Find stop residue
	# Expand right until the needed number of residues is found
	$d = $dat{hom}{$i}{stop}{res} - $dat{hom}{$i}{enum}{res};
	$dat{tgt}{$i}{stop}{res} = $dat{tgt}{$i}{enum}{res} + $d;
	$dat{tgt}{$i}{stop}{aln} = $map{tgt}{res2aln}{$dat{tgt}{$i}{stop}{res}};

	### Hydrophobic center
	# Same thing
	$d = $dat{hom}{$i}{enum}{res} - $dat{hom}{$i}{hpcnum}{res};
	$dat{tgt}{$i}{hpcnum}{res} = $dat{tgt}{$i}{enum}{res} - $d;
	$dat{tgt}{$i}{hpcnum}{aln} = $map{tgt}{res2aln}{$dat{tgt}{$i}{hpcnum}{res}};
	$dat{tgt}{$i}{hpcres}      = $aln[1][$dat{tgt}{$i}{hpcnum}{aln}];

	### Length
	$dat{tgt}{$i}{length}{aln} =
	    $dat{tgt}{$i}{stop}{res} - $dat{tgt}{$i}{start}{res} + 1;
	$dat{tgt}{$i}{length}{res} =
	    $dat{tgt}{$i}{stop}{res} - $dat{tgt}{$i}{start}{res} + 1;
	$minreslen = max($minreslen, $dat{tgt}{$i}{length}{res});
	$minalnlen = max($minalnlen, $dat{tgt}{$i}{length}{aln});

	### Sequence
	for (my $j = $dat{tgt}{$i}{start}{aln}; $j <= $dat{tgt}{$i}{stop}{aln}; $j++) {
	    $dat{tgt}{$i}{seq}{aln} .= $aln[1][$j];
	    if ($aln[1][$j] ne "-") {
		$dat{tgt}{$i}{seq}{res} .= $aln[1][$j];
	    }
	}
    }
    $dat{tgt}{minreslen} = $minreslen;
    $dat{tgt}{minalnlen} = $minalnlen;
    $dat{all}{minreslen} = max($dat{tgt}{minreslen}, $dat{hom}{minreslen});
    $dat{all}{minalnlen} = max($dat{tgt}{minalnlen}, $dat{hom}{minalnlen});

    # Return
    return (\%dat);
}

################################################################################
### Query the User about Modifying the TMs
################################################################################
sub queryTMs {
    my @aln    = @{$_[0]};
    my %map    = %{$_[1]};
    my %dat    = %{$_[2]};
    my @tms    = @{$_[3]};
    my $alnlen =   $_[4];
    my $tgtlen =   $_[5];
    my $homlen =   $_[6];
    my $mfta   =   $_[7];

    # Options
    my $tmmatch = join("|", @tms);
    my $querymessage =
	"Options:\n".
	"  Modify TM Region [" . join(", ", @tms) . "]\n".
	"  Finalize BGF     [F]\n\n".
	"Select Option:  ";

    # Clear Screen
    system("clear");

    # For each TM region
    for (my $i = 1; $i <= @tms; $i++) {
	# Print TM regions
	printTM_short($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
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
	    my @ret = modifyTM($query, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
	    %dat = %{$ret[0]};

	    # Reprint Full TM info
	    system("clear");

	    # For each TM region
	    for (my $i = 1; $i <= @tms; $i++) {
		# Print TM regions
		printTM_short($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
	    }

	    # Print Options
	    print $querymessage;
	}

	# Unknown option
	elsif ($query !~ /^F$/i) {
	    print
		"Unknown Option: $query\n".
		"Select Option:  ";
	}
    }

    # Return
    return (\%dat);
}

################################################################################
### Print Short TM info
################################################################################
sub printTM_short {
    my $i      =   $_[0];
    my @aln    = @{$_[1]};
    my %map    = %{$_[2]};
    my %dat    = %{$_[3]};
    my @tms    = @{$_[4]};
    my $alnlen =   $_[5];
    my $tgtlen =   $_[6];
    my $homlen =   $_[7];

    # Get Percent ID / Similarity
    my $pctid  = 0; my $numid  = 0;
    my $pctsim = 0; my $numsim = 0;
    my $tgtseq = $dat{tgt}{$i}{seq}{res};
    my $homseq = $dat{hom}{$i}{seq}{res};
    my $simstr = "";
    my $prostr = "";
    $dat{flags}{$i}{pro} = "";
    for (my $j = 0; $j < length($tgtseq); $j++) {
	my $a = substr($tgtseq,$j,1);
	my $b = substr($homseq,$j,1);
	if ($a eq $b)              { $numid++;  }
	if ($blosum62{$a}{$b} > 0) { $numsim++; }
	
	if    ($a eq $b)              { $simstr .= "*"; }
	elsif ($blosum62{$a}{$b} > 0) { $simstr .= ":"; }
	else                          { $simstr .= " "; }

	if (($a eq "P") && ($b eq "P")) { $prostr .= "p"; }
	elsif (($a eq "P") && ($b ne "P")) {
	    $prostr .= "^";
	    my $tmp1 = $dat{tgt}{$i}{start}{res} + $j;
	    my $tmp2 = $dat{hom}{$i}{start}{res} + $j;
	    my $tmp3 = $map{hom}{res2aln}{$tmp2};
	    my $tmp4 = $aln[2][$tmp3];
	    $dat{flags}{$i}{pro} .=
		"  WARNING: Proline mismatch at: tgt P${tmp1} / hom ${tmp4}${tmp2}\n";
	}
	elsif (($a ne "P") && ($b eq "P")) {
	    $prostr .= "v";
	    my $tmp1 = $dat{tgt}{$i}{start}{res} + $j;
	    my $tmp2 = $dat{hom}{$i}{start}{res} + $j;
	    my $tmp3 = $map{tgt}{res2aln}{$tmp1};
	    my $tmp4 = $aln[1][$tmp3];
	    $dat{flags}{$i}{pro} .=
		"  WARNING: Proline mismatch at: tgt ${tmp4}${tmp1} / hom P${tmp2}\n";
	}
	else { $prostr .= " "; }

    }
    $pctid  = 100 * $numid  / length($tgtseq);
    $pctsim = 100 * $numsim / length($tgtseq);

    # Header Line
    my $txt = sprintf
	"TM %d | Length %d | EtaRes %s %d | HPC %s %d.%d | ".
	"Pct ID %.1f %% [%d \#] | Pct Sim %.1f %% [%d \#]\n",
	$i, $dat{tgt}{$i}{length}{res}, $dat{tgt}{$i}{eres}, $dat{tgt}{$i}{enum}{res},
	$dat{tgt}{$i}{hpcres}, $dat{tgt}{$i}{hpcnum}{res}, $dat{tgt}{$i}{hpcdec},
	$pctid, $numid, $pctsim, $numsim;

    # Warnings
    if ($dat{flags}{$i}{aln} ne "") { $txt .= "  WARNING: " . $dat{flags}{$i}{aln}; }
    if ($dat{flags}{$i}{pro} ne "") { $txt .= $dat{flags}{$i}{pro}; }

    # Proline Line
    $txt .= sprintf "                  pro   %s\n", $prostr;

    # Target E/H - No Gaps
    my $e = $dat{tgt}{$i}{enum}{res};
    my $h = $dat{tgt}{$i}{hpcnum}{res};
    $txt .= sprintf "                  e/h   ";
    for (my $j = $dat{tgt}{$i}{start}{res}; $j <= $dat{tgt}{$i}{stop}{res}; $j++) {
	if (($j == $e) && ($j == $h)) {
	    $txt .= "\#";
	} elsif ($j == $e) {
	    $txt .= "e";
	} elsif ($j == $h) {
	    $txt .= "h";
	} else {
	    $txt .= " ";
	}
    }
    $txt .= "\n";

    # Target Line - No Gaps
    $txt .= sprintf
	"    target tm %d - %3d - %s - %3d\n",
	$i, $dat{tgt}{$i}{start}{res}, $dat{tgt}{$i}{seq}{res},
	$dat{tgt}{$i}{stop}{res};

    # Homology Line - No Gaps
    $txt .= sprintf
	"  homology tm %d - %3d - %s - %3d\n",
	$i, $dat{hom}{$i}{start}{res}, $dat{hom}{$i}{seq}{res},
	$dat{hom}{$i}{stop}{res};

    # Similarity Line - No Gaps
    $txt .= sprintf "                  sim   %s\n", $simstr;

    # Homology E/H - No Gaps
    $e = $dat{hom}{$i}{enum}{res};
    $h = $dat{hom}{$i}{hpcnum}{res};
    $txt .= sprintf "                  e/h   ";
    for (my $j = $dat{hom}{$i}{start}{res}; $j <= $dat{hom}{$i}{stop}{res}; $j++) {
	if (($j == $e) && ($j == $h)) {
	    $txt .= "\#";
	} elsif ($j == $e) {
	    $txt .= "e";
	} elsif ($j == $h) {
	    $txt .= "h";
	} else {
	    $txt .= " ";
	}
    }
    $txt .= "\n\n";

    print $txt;
}

################################################################################
### Print Long TM info
################################################################################
sub printTM_long {
    my $i      =   $_[0];
    my @aln    = @{$_[1]};
    my %map    = %{$_[2]};
    my %dat    = %{$_[3]};
    my @tms    = @{$_[4]};
    my $alnlen =   $_[5];
    my $tgtlen =   $_[6];
    my $homlen =   $_[7];

    # Get Percent ID / Similarity
    my $pctid  = 0; my $numid  = 0;
    my $pctsim = 0; my $numsim = 0;
    my $tgtseq = $dat{tgt}{$i}{seq}{res};
    my $homseq = $dat{hom}{$i}{seq}{res};
    my $simstr = "";
    my $prostr = "";
    $dat{flags}{$i}{pro} = "";
    for (my $j = 0; $j < length($tgtseq); $j++) {
	my $a = substr($tgtseq,$j,1);
	my $b = substr($homseq,$j,1);
	if ($a eq $b)              { $numid++;  }
	if ($blosum62{$a}{$b} > 0) { $numsim++; }
	
	if    ($a eq $b)              { $simstr .= "*"; }
	elsif ($blosum62{$a}{$b} > 0) { $simstr .= ":"; }
	else                          { $simstr .= " "; }

	if (($a eq "P") && ($b eq "P")) { $prostr .= "p"; }
	elsif (($a eq "P") && ($b ne "P")) {
	    $prostr .= "^";
	    my $tmp1 = $dat{tgt}{$i}{start}{res} + $j;
	    my $tmp2 = $dat{hom}{$i}{start}{res} + $j;
	    my $tmp3 = $map{hom}{res2aln}{$tmp2};
	    my $tmp4 = $aln[2][$tmp3];
	    $dat{flags}{$i}{pro} .=
		"  warning: Proline mismatch at: tgt P${tmp1} / hom ${tmp4}${tmp2}\n";
	}
	elsif (($a ne "P") && ($b eq "P")) {
	    $prostr .= "v";
	    my $tmp1 = $dat{tgt}{$i}{start}{res} + $j;
	    my $tmp2 = $dat{hom}{$i}{start}{res} + $j;
	    my $tmp3 = $map{tgt}{res2aln}{$tmp1};
	    my $tmp4 = $aln[1][$tmp3];
	    $dat{flags}{$i}{pro} .=
		"  warning: Proline mismatch at: tgt ${tmp4}${tmp1} / hom P${tmp2}\n";
	}
	else { $prostr .= " "; }

    }
    $pctid  = 100 * $numid  / length($tgtseq);
    $pctsim = 100 * $numsim / length($tgtseq);

    # Header Line
    my $txt = "";
    $txt .= sprintf
	"TM %d | Length %d | EtaRes %s %d | HPC %s %d.%d | ".
	"Pct ID %.1f %% [%d \#] | Pct Sim %.1f %% [%d \#]\n\n",
	$i, $dat{tgt}{$i}{length}{res}, $dat{tgt}{$i}{eres}, $dat{tgt}{$i}{enum}{res},
	$dat{tgt}{$i}{hpcres}, $dat{tgt}{$i}{hpcnum}{res}, $dat{tgt}{$i}{hpcdec},
	$pctid, $numid, $pctsim, $numsim;

    # Sequence Alignment
    my $tgtalnstr = "";
    my $homalnstr = "";
    my $simalnstr = "";
    my $markstr1  = "";
    my $markstr2  = "";
    my $alnstart = max(1, min($dat{tgt}{$i}{start}{aln},
			      $dat{hom}{$i}{start}{aln}) - 5);
    my $alnstop  = min($alnlen, max($dat{tgt}{$i}{stop}{aln},
				    $dat{hom}{$i}{stop}{aln}) + 5);
    for (my $j = $alnstart; $j <= $alnstop; $j++) {
	$tgtalnstr .= $aln[1][$j];
	$homalnstr .= $aln[2][$j];
	$simalnstr .= $aln[0][$j];

	if (($j == $dat{tgt}{$i}{start}{aln}) || ($j == $dat{tgt}{$i}{stop}{aln})) {
	    $markstr1 .= "|";
	} else {
	    $markstr1 .= " ";
	}
	if (($j == $dat{hom}{$i}{start}{aln}) || ($j == $dat{hom}{$i}{stop}{aln})) {
	    $markstr2 .= "|";
	} else {
	    $markstr2 .= " ";
	}

    }

    $txt .= "Original Sequence Alignment:\n";
    $txt .= sprintf "                          %s\n", $markstr1;
    $txt .=
	sprintf "      target tm %d - %3d - %s - %3d\n",
	$i, $dat{tgt}{$i}{start}{aln}, $tgtalnstr, $dat{tgt}{$i}{stop}{aln}; 
    $txt .= sprintf "                          %s\n", $simalnstr;
    $txt .=
	sprintf "    homology tm %d - %3d - %s - %3d\n",
	$i, $dat{hom}{$i}{start}{aln}, $homalnstr, $dat{hom}{$i}{stop}{aln};
    $txt .= sprintf "                          %s\n\n", $markstr2;

    $txt .= "Homology Alignment:\n";

    # Proline Line
    $txt .= sprintf "                    pro   %s\n", $prostr;

    # Target E/H - No Gaps
    my $e = $dat{tgt}{$i}{enum}{res};
    my $h = $dat{tgt}{$i}{hpcnum}{res};
    $txt .= sprintf "                    e/h   ";
    for (my $j = $dat{tgt}{$i}{start}{res}; $j <= $dat{tgt}{$i}{stop}{res}; $j++) {
	if (($j == $e) && ($j == $h)) {
	    $txt .= "\#";
	} elsif ($j == $e) {
	    $txt .= "e";
	} elsif ($j == $h) {
	    $txt .= "h";
	} else {
	    $txt .= " ";
	}
    }
    $txt .= "\n";

    # Target Line - No Gaps
    $txt .= sprintf
	"      target tm %d - %3d - %s - %3d\n",
	$i, $dat{tgt}{$i}{start}{res}, $dat{tgt}{$i}{seq}{res},
	$dat{tgt}{$i}{stop}{res};
    
    # Similarity Line - No Gaps
    $txt .= sprintf "                    sim   %s\n", $simstr;

    # Homology Line - No Gaps
    $txt .= sprintf
	"    homology tm %d - %3d - %s - %3d\n",
	$i, $dat{hom}{$i}{start}{res}, $dat{hom}{$i}{seq}{res},
	$dat{hom}{$i}{stop}{res};

    # Homology E/H - No Gaps
    $e = $dat{hom}{$i}{enum}{res};
    $h = $dat{hom}{$i}{hpcnum}{res};
    $txt .= sprintf "                    e/h   ";
    for (my $j = $dat{hom}{$i}{start}{res}; $j <= $dat{hom}{$i}{stop}{res}; $j++) {
	if (($j == $e) && ($j == $h)) {
	    $txt .= "\#";
	} elsif ($j == $e) {
	    $txt .= "e";
	} elsif ($j == $h) {
	    $txt .= "h";
	} else {
	    $txt .= " ";
	}
    }
    $txt .= "\n\n";

    # Warnings
    if (($dat{flags}{$i}{aln} ne "") || ($dat{flags}{$i}{pro} ne "")) {
	$txt .= "Warnings:\n";
    }
    if ($dat{flags}{$i}{aln} ne "") { $txt .= "  warning: ". $dat{flags}{$i}{aln}; }
    if ($dat{flags}{$i}{pro} ne "") { $txt .= $dat{flags}{$i}{pro}; }
    if (($dat{flags}{$i}{aln} ne "") || ($dat{flags}{$i}{pro} ne "")) {
	$txt .= "\n";
    }

    print $txt;
    return $txt;
}

################################################################################
### Print Long TM info
################################################################################
sub printTM_long_final {
    my $i      =   $_[0];
    my @aln    = @{$_[1]};
    my %map    = %{$_[2]};
    my %dat    = %{$_[3]};
    my @tms    = @{$_[4]};
    my $alnlen =   $_[5];
    my $tgtlen =   $_[6];
    my $homlen =   $_[7];
    my $use_ss =   $_[8];

    # Get Percent ID / Similarity
    my $pctid  = 0; my $numid  = 0;
    my $pctsim = 0; my $numsim = 0;
    my $tgtseq = $dat{tgt}{$i}{seq}{res};
    my $homseq = $dat{hom}{$i}{seq}{res};
    my $simstr = "";
    my $prostr = "";
    my $DUM = "  ";
    $dat{flags}{$i}{pro} = "";
    for (my $j = 0; $j < length($tgtseq); $j++) {
	my $a = substr($tgtseq,$j,1);
	my $b = substr($homseq,$j,1);
	if ($a eq $b)              { $numid++;  }
	if ($blosum62{$a}{$b} > 0) { $numsim++; }
	
	if    ($a eq $b)              { $simstr .= "*"; }
	elsif ($blosum62{$a}{$b} > 0) { $simstr .= ":"; }
	else                          { $simstr .= " "; }

	if (($a eq "P") && ($b eq "P")) { $prostr .= "p"; }
	elsif (($a eq "P") && ($b ne "P")) {
	    $prostr .= "^";
	    my $tmp1 = $dat{tgt}{$i}{start}{res} + $j;
	    my $tmp2 = $dat{hom}{$i}{start}{res} + $j;
	    my $tmp3 = $map{hom}{res2aln}{$tmp2};
	    my $tmp4 = $aln[2][$tmp3];
	    $dat{flags}{$i}{pro} .=
		"  ${DUM}warning: Proline mismatch at: tgt P${tmp1} / hom ${tmp4}${tmp2}\n";
	}
	elsif (($a ne "P") && ($b eq "P")) {
	    $prostr .= "v";
	    my $tmp1 = $dat{tgt}{$i}{start}{res} + $j;
	    my $tmp2 = $dat{hom}{$i}{start}{res} + $j;
	    my $tmp3 = $map{tgt}{res2aln}{$tmp1};
	    my $tmp4 = $aln[1][$tmp3];
	    $dat{flags}{$i}{pro} .=
		"  ${DUM}warning: Proline mismatch at: tgt ${tmp4}${tmp1} / hom P${tmp2}\n";
	}
	else { $prostr .= " "; }

    }
    $pctid  = 100 * $numid  / length($tgtseq);
    $pctsim = 100 * $numsim / length($tgtseq);

    # Header Line
    my $txt = "";
    $txt .= sprintf "%s %s %s %s %s\n\n", "-"x5, "-"x5, "-"x5, "-"x5, "-"x5;
    $txt .= sprintf
	"TM %d | Length %d | EtaRes %s %d | HPC %s %d.%d | ".
	"Pct ID %.1f %% [%d \#] | Pct Sim %.1f %% [%d \#]\n",
	$i, $dat{tgt}{$i}{length}{res}, $dat{tgt}{$i}{eres}, $dat{tgt}{$i}{enum}{res},
	$dat{tgt}{$i}{hpcres}, $dat{tgt}{$i}{hpcnum}{res}, $dat{tgt}{$i}{hpcdec},
	$pctid, $numid, $pctsim, $numsim;
    if (! $use_ss) { $txt .= "\n"; }

    # Sequence Alignment
    my $tgtalnstr = "";
    my $homalnstr = "";
    my $simalnstr = "";
    my $markstr1  = "";
    my $markstr2  = "";
    my $alnstart = max(1, min($dat{tgt}{$i}{start}{aln},
			      $dat{hom}{$i}{start}{aln}) - 5);
    my $alnstop  = min($alnlen, max($dat{tgt}{$i}{stop}{aln},
				    $dat{hom}{$i}{stop}{aln}) + 5);
    for (my $j = $alnstart; $j <= $alnstop; $j++) {
	$tgtalnstr .= $aln[1][$j];
	$homalnstr .= $aln[2][$j];
	$simalnstr .= $aln[0][$j];

	if (($j == $dat{tgt}{$i}{start}{aln}) || ($j == $dat{tgt}{$i}{stop}{aln})) {
	    $markstr1 .= "|";
	} else {
	    $markstr1 .= " ";
	}
	if (($j == $dat{hom}{$i}{start}{aln}) || ($j == $dat{hom}{$i}{stop}{aln})) {
	    $markstr2 .= "|";
	} else {
	    $markstr2 .= " ";
	}

    }

    $txt .= "  Original Sequence Alignment:\n";
    $txt .=
	sprintf "        target tm %d - %3d - %s - %3d\n",
	$i, $dat{tgt}{$i}{start}{aln}, $tgtalnstr, $dat{tgt}{$i}{stop}{aln}; 
    $txt .= sprintf "                            %s\n", $simalnstr;
    $txt .=
	sprintf "      homology tm %d - %3d - %s - %3d\n\n",
	$i, $dat{hom}{$i}{start}{aln}, $homalnstr, $dat{hom}{$i}{stop}{aln};

    # Secondary Structure
    if ($use_ss) {
	$txt .= "  Homology Alignment:\n";

	my ($DUM1, $DUM2, $DUM3, $DUM4) = (0,0,0,0);

	# Buffer tgt & hom
	if ($dat{tgt}{$i}{ss_start}{res} <= $dat{tgt}{$i}{start}{res}) {
	    $DUM1 = $dat{tgt}{$i}{start}{res} - $dat{tgt}{$i}{ss_start}{res};
	    $DUM3 = 0;
	}

	# Buffer ss
	else {
	    $DUM1 = 0;
	    $DUM3 = $dat{tgt}{$i}{ss_start}{res} - $dat{tgt}{$i}{start}{res};
	}

	# Buffer tgt & hom
	if ($dat{tgt}{$i}{ss_stop}{res} >= $dat{tgt}{$i}{stop}{res}) {
	    $DUM2 = $dat{tgt}{$i}{ss_stop}{res} - $dat{tgt}{$i}{stop}{res};
	    $DUM4 = 0;
	}

	# Buffer ss
	else {
	    $DUM2 = 0;
	    $DUM4 = $dat{tgt}{$i}{stop}{res} - $dat{tgt}{$i}{ss_stop}{res};
	}

	# Proline Line
	$txt .= sprintf "                      pro   %s%s\n", " " x $DUM1, $prostr;

	# Target E/H - No Gaps
	my $e = $dat{tgt}{$i}{enum}{res};
	my $h = $dat{tgt}{$i}{hpcnum}{res};
	$txt .= sprintf "                      e/h   %s", " " x $DUM1;
	for (my $j = $dat{tgt}{$i}{start}{res}; $j <= $dat{tgt}{$i}{stop}{res}; $j++) {
	    if (($j == $e) && ($j == $h)) {
		$txt .= "\#";
	    } elsif ($j == $e) {
		$txt .= "e";
	    } elsif ($j == $h) {
		$txt .= "h";
	    } else {
		$txt .= " ";
	    }
	}
	$txt .= "\n";

	# SS Target Line - No Gaps
	$txt .= sprintf
	    "     ss target tm %d - %3d - %s%s%s - %3d\n",
	    $i, $dat{tgt}{$i}{ss_start}{res}, " " x $DUM3, $dat{tgt}{$i}{ss_seq}{res},
	    " " x $DUM4, $dat{tgt}{$i}{ss_stop}{res};

	# Target Line - No Gaps
	$txt .= sprintf
	    "        target tm %d - %3d - %s%s%s - %3d\n",
	    $i, $dat{tgt}{$i}{start}{res}, " " x $DUM1, $dat{tgt}{$i}{seq}{res},
	    " " x $DUM2, $dat{tgt}{$i}{stop}{res};

	# Similarity Line - No Gaps
	$txt .= sprintf "                      sim   %s%s\n", " " x $DUM1, $simstr;

	# Homology Line - No Gaps
	$txt .= sprintf
	    "      homology tm %d - %3d - %s%s%s - %3d\n",
	    $i, $dat{hom}{$i}{start}{res}, " " x $DUM1, $dat{hom}{$i}{seq}{res},
	    " " x $DUM2, $dat{hom}{$i}{stop}{res};

	# Homology E/H - No Gaps
	$e = $dat{hom}{$i}{enum}{res};
	$h = $dat{hom}{$i}{hpcnum}{res};
	$txt .= sprintf "                      e/h   %s", " " x $DUM1;
	for (my $j = $dat{hom}{$i}{start}{res}; $j <= $dat{hom}{$i}{stop}{res}; $j++) {
	    if (($j == $e) && ($j == $h)) {
		$txt .= "\#";
	    } elsif ($j == $e) {
		$txt .= "e";
	    } elsif ($j == $h) {
		$txt .= "h";
	    } else {
		$txt .= " ";
	    }
	}
	$txt .= "\n\n";
    }

    # No Secondary Structure
    else {
	$txt .= "  Homology Alignment:\n";

	# Proline Line
	$txt .= sprintf "                      pro   %s\n", $prostr;

	# Target E/H - No Gaps
	my $e = $dat{tgt}{$i}{enum}{res};
	my $h = $dat{tgt}{$i}{hpcnum}{res};
	$txt .= sprintf "                      e/h   ";
	for (my $j = $dat{tgt}{$i}{start}{res}; $j <= $dat{tgt}{$i}{stop}{res}; $j++) {
	    if (($j == $e) && ($j == $h)) {
		$txt .= "\#";
	    } elsif ($j == $e) {
		$txt .= "e";
	    } elsif ($j == $h) {
		$txt .= "h";
	    } else {
		$txt .= " ";
	    }
	}
	$txt .= "\n";

	# Target Line - No Gaps
	$txt .= sprintf
	    "        target tm %d - %3d - %s - %3d\n",
	    $i, $dat{tgt}{$i}{start}{res}, $dat{tgt}{$i}{seq}{res},
	    $dat{tgt}{$i}{stop}{res};

	# Similarity Line - No Gaps
	$txt .= sprintf "                      sim   %s\n", $simstr;

	# Homology Line - No Gaps
	$txt .= sprintf
	    "      homology tm %d - %3d - %s - %3d\n",
	    $i, $dat{hom}{$i}{start}{res}, $dat{hom}{$i}{seq}{res},
	    $dat{hom}{$i}{stop}{res};

	# Homology E/H - No Gaps
	$e = $dat{hom}{$i}{enum}{res};
	$h = $dat{hom}{$i}{hpcnum}{res};
	$txt .= sprintf "                      e/h   ";
	for (my $j = $dat{hom}{$i}{start}{res}; $j <= $dat{hom}{$i}{stop}{res}; $j++) {
	    if (($j == $e) && ($j == $h)) {
		$txt .= "\#";
	    } elsif ($j == $e) {
		$txt .= "e";
	    } elsif ($j == $h) {
		$txt .= "h";
	    } else {
		$txt .= " ";
	    }
	}
	$txt .= "\n\n";
    }

    # Warnings
    if (($dat{flags}{$i}{aln} ne "") || ($dat{flags}{$i}{pro} ne "")) {
	$txt .= "  Warnings:\n";
    }
    if ($dat{flags}{$i}{aln} ne "") { $txt .= "  warning: ". $dat{flags}{$i}{aln}; }
    if ($dat{flags}{$i}{pro} ne "") { $txt .= $dat{flags}{$i}{pro}; }
    if (($dat{flags}{$i}{aln} ne "") || ($dat{flags}{$i}{pro} ne "")) {
	$txt .= "\n";
    }

    print $txt;
    return $txt;
}

################################################################################
### Modify TM Region Parameters
################################################################################
sub modifyTM {
    my $i      =   $_[0];
    my @aln    = @{$_[1]};
    my %map    = %{$_[2]};
    my %dat    = %{$_[3]};
    my @tms    = @{$_[4]};
    my $alnlen =   $_[5];
    my $tgtlen =   $_[6];
    my $homlen =   $_[7];

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
    printTM_long($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen, 0);

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
	    my @ret = moveTargetLeft($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
	    %dat = %{$ret[0]};
	    $reprint = 1;
	}

	# Target Right
	elsif ($query =~ /^R$/i) {
	    my @ret = moveTargetRight($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
	    %dat = %{$ret[0]};
	    $reprint = 1;
	}

	# Eta Left
	elsif ($query =~ /^E$/i) {
	    my @ret = moveEtaLeft($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
	    %dat = %{$ret[0]};
	    $reprint = 1;
	}

	# Eta Right
	elsif ($query =~ /^F$/i) {
	    my @ret = moveEtaRight($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
	    %dat = %{$ret[0]};
	    $reprint = 1;
	}

	# HPC Left
	elsif ($query =~ /^H$/i) {
	    my @ret = moveHPCLeft($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
	    %dat = %{$ret[0]};
	    $reprint = 1;
	}

	# HPC Right
	elsif ($query =~ /^I$/i) {
	    my @ret = moveHPCRight($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
	    %dat = %{$ret[0]};
	    $reprint = 1;
	}

	# Unknown Option
	elsif ($query !~ /^X$/i) {
	    print
		"Unknown Option: $query\n".
		"Select Option:  ";
	}

	# Reprint
	if ($reprint) {
	    # Clear Screen
	    system("clear");

	    # Print TM region
	    printTM_long($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen, 0);

	    # Print Options
	    print $querymessage;
	}
    }

    # Return
    return (\%dat);
}

################################################################################
### Move Start/Stop, ETA, HPC Right/Left
################################################################################
sub moveTargetLeft {
    my $i      =   $_[0];
    my @aln    = @{$_[1]};
    my %map    = %{$_[2]};
    my %dat    = %{$_[3]};
    my @tms    = @{$_[4]};
    my $alnlen =   $_[5];
    my $tgtlen =   $_[6];
    my $homlen =   $_[7];

    # New Start/Stop
    my $start_res = $dat{tgt}{$i}{start}{res} + 1;
    my $start_aln = $map{tgt}{res2aln}{$start_res};
    my $stop_res  = $dat{tgt}{$i}{stop}{res} + 1;
    my $stop_aln  = $map{tgt}{res2aln}{$stop_res};

    # New HPC
    my $h_res  = $dat{tgt}{$i}{hpcnum}{res} + 1;
    my $h_aln  = $map{tgt}{res2aln}{$h_res};
    my $h_name = $aln[1][$h_aln];

    # New Eta
    my $e_res  = $dat{tgt}{$i}{enum}{res} + 1;
    my $e_aln  = $map{tgt}{res2aln}{$e_res};
    my $e_name = $aln[1][$e_aln];

    # Check Boundary
    if ($stop_res <= $tgtlen) {
	$dat{tgt}{$i}{start}{res}  = $start_res;
	$dat{tgt}{$i}{start}{aln}  = $start_aln;
	$dat{tgt}{$i}{stop}{res}   = $stop_res;
	$dat{tgt}{$i}{stop}{aln}   = $stop_aln;
	$dat{tgt}{$i}{hpcnum}{res} = $h_res;
	$dat{tgt}{$i}{hpcnum}{aln} = $h_aln;
	$dat{tgt}{$i}{hpcres}      = $h_name;
	$dat{tgt}{$i}{enum}{res}   = $e_res;
	$dat{tgt}{$i}{enum}{aln}   = $e_aln;
	$dat{tgt}{$i}{eres}        = $e_name;

	# Redo TM length / sequence
	$dat{tgt}{$i}{length}{res} =
	    $dat{tgt}{$i}{stop}{res} - $dat{tgt}{$i}{start}{res} + 1;
	$dat{tgt}{$i}{length}{aln} =
	    $dat{tgt}{$i}{stop}{aln} - $dat{tgt}{$i}{start}{aln} + 1;
	$dat{tgt}{$i}{seq}{res} = "";
	$dat{tgt}{$i}{seq}{aln} = "";
	for (my $j = $dat{tgt}{$i}{start}{aln}; $j <= $dat{tgt}{$i}{stop}{aln}; $j++) {
	    $dat{tgt}{$i}{seq}{aln} .= $aln[1][$j];
	    if ($aln[1][$j] ne "-") {
		$dat{tgt}{$i}{seq}{res} .= $aln[1][$j];
	    }
	}

	# Move Eta Left
	my @ret = moveEtaLeft($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
	%dat = %{$ret[0]};

	# Move HPC Left
	@ret = moveHPCLeft($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
	%dat = %{$ret[0]};
    }

    # Return
    return (\%dat);
}

sub moveTargetRight {
    my $i      =   $_[0];
    my @aln    = @{$_[1]};
    my %map    = %{$_[2]};
    my %dat    = %{$_[3]};
    my @tms    = @{$_[4]};
    my $alnlen =   $_[5];
    my $tgtlen =   $_[6];
    my $homlen =   $_[7];

    # New Start/Stop
    my $start_res = $dat{tgt}{$i}{start}{res} - 1;
    my $start_aln = $map{tgt}{res2aln}{$start_res};
    my $stop_res  = $dat{tgt}{$i}{stop}{res} - 1;
    my $stop_aln  = $map{tgt}{res2aln}{$stop_res};

    # New HPC
    my $h_res  = $dat{tgt}{$i}{hpcnum}{res} - 1;
    my $h_aln  = $map{tgt}{res2aln}{$h_res};
    my $h_name = $aln[1][$h_aln];

    # New Eta
    my $e_res  = $dat{tgt}{$i}{enum}{res} - 1;
    my $e_aln  = $map{tgt}{res2aln}{$e_res};
    my $e_name = $aln[1][$e_aln];

    # Check Boundary
    if ($start_res >= 1) {
	$dat{tgt}{$i}{start}{res}  = $start_res;
	$dat{tgt}{$i}{start}{aln}  = $start_aln;
	$dat{tgt}{$i}{stop}{res}   = $stop_res;
	$dat{tgt}{$i}{stop}{aln}   = $stop_aln;
	$dat{tgt}{$i}{hpcnum}{res} = $h_res;
	$dat{tgt}{$i}{hpcnum}{aln} = $h_aln;
	$dat{tgt}{$i}{hpcres}      = $h_name;
	$dat{tgt}{$i}{enum}{res}   = $e_res;
	$dat{tgt}{$i}{enum}{aln}   = $e_aln;
	$dat{tgt}{$i}{eres}        = $e_name;

	# Redo TM length / sequence
	$dat{tgt}{$i}{length}{res} =
	    $dat{tgt}{$i}{stop}{res} - $dat{tgt}{$i}{start}{res} + 1;
	$dat{tgt}{$i}{length}{aln} =
	    $dat{tgt}{$i}{stop}{aln} - $dat{tgt}{$i}{start}{aln} + 1;
	$dat{tgt}{$i}{seq}{res} = "";
	$dat{tgt}{$i}{seq}{aln} = "";
	for (my $j = $dat{tgt}{$i}{start}{aln}; $j <= $dat{tgt}{$i}{stop}{aln}; $j++) {
	    $dat{tgt}{$i}{seq}{aln} .= $aln[1][$j];
	    if ($aln[1][$j] ne "-") {
		$dat{tgt}{$i}{seq}{res} .= $aln[1][$j];
	    }
	}

	# Move Eta Right
	my @ret = moveEtaRight($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
	%dat = %{$ret[0]};

	# Move HPC Right
	@ret = moveHPCRight($i, \@aln, \%map, \%dat, \@tms, $alnlen, $tgtlen, $homlen);
	%dat = %{$ret[0]};
    }

    # Return
    return (\%dat);
}

sub moveEtaLeft {
    my $i      =   $_[0];
    my @aln    = @{$_[1]};
    my %map    = %{$_[2]};
    my %dat    = %{$_[3]};
    my @tms    = @{$_[4]};
    my $alnlen =   $_[5];
    my $tgtlen =   $_[6];
    my $homlen =   $_[7];

    # New Eta
    my $e_res  = $dat{tgt}{$i}{enum}{res} - 1;
    my $e_aln  = $map{tgt}{res2aln}{$e_res};
    my $e_name = $aln[1][$e_aln];

    # Check Boundary
    if ($e_res >= $dat{tgt}{$i}{start}{res}) {
	$dat{tgt}{$i}{enum}{res} = $e_res;
	$dat{tgt}{$i}{enum}{aln} = $e_aln;
	$dat{tgt}{$i}{eres}      = $e_name;
    }

    # Return
    return (\%dat);
}

sub moveEtaRight {
    my $i      =   $_[0];
    my @aln    = @{$_[1]};
    my %map    = %{$_[2]};
    my %dat    = %{$_[3]};
    my @tms    = @{$_[4]};
    my $alnlen =   $_[5];
    my $tgtlen =   $_[6];
    my $homlen =   $_[7];

    # New Eta
    my $e_res  = $dat{tgt}{$i}{enum}{res} + 1;
    my $e_aln  = $map{tgt}{res2aln}{$e_res};
    my $e_name = $aln[1][$e_aln];

    # Check Boundary
    if ($e_res <= $dat{tgt}{$i}{stop}{res}) {
	$dat{tgt}{$i}{enum}{res} = $e_res;
	$dat{tgt}{$i}{enum}{aln} = $e_aln;
	$dat{tgt}{$i}{eres}      = $e_name;
    }

    # Return
    return (\%dat);
}

sub moveHPCLeft {
    my $i      =   $_[0];
    my @aln    = @{$_[1]};
    my %map    = %{$_[2]};
    my %dat    = %{$_[3]};
    my @tms    = @{$_[4]};
    my $alnlen =   $_[5];
    my $tgtlen =   $_[6];
    my $homlen =   $_[7];

    # New HPC
    my $h_res  = $dat{tgt}{$i}{hpcnum}{res} - 1;
    my $h_aln  = $map{tgt}{res2aln}{$h_res};
    my $h_name = $aln[1][$h_aln];

    # Check Boundary
    if ($h_res >= $dat{tgt}{$i}{start}{res}) {
	$dat{tgt}{$i}{hpcnum}{res} = $h_res;
	$dat{tgt}{$i}{hpcnum}{aln} = $h_aln;
	$dat{tgt}{$i}{hpcres}      = $h_name;
    }

    # Return
    return (\%dat);
}

sub moveHPCRight {
    my $i      =   $_[0];
    my @aln    = @{$_[1]};
    my %map    = %{$_[2]};
    my %dat    = %{$_[3]};
    my @tms    = @{$_[4]};
    my $alnlen =   $_[5];
    my $tgtlen =   $_[6];
    my $homlen =   $_[7];

    # New HPC
    my $h_res = $dat{tgt}{$i}{hpcnum}{res} + 1;
    my $h_aln = $map{tgt}{res2aln}{$h_res};
    my $h_name = $aln[1][$h_aln];

    # Check Boundary
    if ($h_res <= $dat{tgt}{$i}{stop}{res}) {
	$dat{tgt}{$i}{hpcnum}{res} = $h_res;
	$dat{tgt}{$i}{hpcnum}{aln} = $h_aln;
	$dat{tgt}{$i}{hpcres}      = $h_name;
    }

    # Return
    return (\%dat);
}

################################################################################
### Generate Homology BGF & MFTA
################################################################################
sub homologyBGF {
    my @aln     = @{$_[0]};
    my %map     = %{$_[1]};
    my %dat     = %{$_[2]};
    my @tms     = @{$_[3]};
    my $alnlen  =   $_[4];
    my $tgtlen  =   $_[5];
    my $homlen  =   $_[6];
    my $mfta    =   $_[7];
    my $hompfx  =   $_[8];
    my $pair    =   $_[9];
    my $overlap =   $_[10];
    my $trunc   =   $_[11];
    my $pfx     =   $_[12];

    # Generating Homology BGF
    # 1) Copy template BGF
    # 2) If any etas or hpcs have been changed, rotate/shift TMs
    # 2) For each TM:
    #    A) Renumber TM residues
    #    B) Resolve any N-term Pro->Non Pro mutations
    #    C) Scream to AGPST
    #    D) Minimize to 0.5
    #    E) Scream to final residues
    # 3) Merge TM Bundle
    # 4) Output MFTA

    system("clear");
    print
	"Building Homology BGF:\n".
	" :: Orienting Template\n";
    
    # Copy template BGF
    copy("${hompfx}.bgf",  "template.bgf");
    copy("${hompfx}.mfta", "template.mfta");
    copy("${hompfx}.inp",  "template.inp");

    # Make sure template BGF is properly oriented
    `$alninp -b template.bgf -m template.mfta -i template.inp >& /dev/null`;
    move("template.aligned.bgf", "template.bgf");

    # Check if etas or hpcs have been changed
    my $changed = 0;
    my $newinp  = "";
    my %changes = ();
    open INP, "template.inp";
    while (<INP>) {
	my $line = $_;
	if ($line =~ /^\*\s+(\d+)tmpl/) {
	    my $i = $1;
	    my @split = split(/\s+/, $line);

	    # Compare target eta-start to homology eta-start
	    $changes{$i}{enum} = 0;
	    $changes{$i}{eres} = $dat{hom}{$i}{eres};
	    my $rel_eta =
		($dat{tgt}{$i}{enum}{res} - $dat{tgt}{$i}{start}{res}) -
		($dat{hom}{$i}{enum}{res} - $dat{hom}{$i}{start}{res});
	    my $rel_eta_homres = $dat{hom}{$i}{enum}{res} + $rel_eta;
	    my $rel_eta_homaln = $map{hom}{res2aln}{$rel_eta_homres};
	    my $rel_etares     = $aln[2][$rel_eta_homaln];
	    if ($rel_eta != 0) {
		$split[8]  = $rel_etares;
		$split[9] += $rel_eta;
		$changes{$i}{eres} = $split[8];
		$changes{$i}{enum} = $rel_eta;
		$changed = 1;
	    }

	    # Compare target hpc-start to homology hpc-start
	    my $rel_hpc =
		($dat{tgt}{$i}{hpcnum}{res} - $dat{tgt}{$i}{start}{res}) -
		($dat{hom}{$i}{hpcnum}{res} - $dat{hom}{$i}{start}{res});
	    $changes{$i}{hpc}  = $split[4];
	    if ($rel_hpc != 0) {
		$split[4] += $rel_hpc;
		$changes{$i}{hpc} = $split[4];
		$changed = 1;
	    }

	    # New line
	    $line = sprintf "%1s %6s %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f %4s %4d\n", @split;
	}
	$newinp .= $line;
    }
    close INP;

    # If etas or hpcs have been changed, adjust template
    if ($changed) {
	print " :: Reorienting Helices\n";
	# Modify MFTA
	my $newmfta = "";
	open MFTA, "template.mfta";
	while (<MFTA>) {
	    my $line = $_;
	    if ($line =~ /^\*\s+(\d+)tm/) {
		my $i = $1;
		my @split = split(/\s+/, $line);
		$split[10]  = $changes{$i}{eres};
		$split[11] += $changes{$i}{enum};
		$line =
		    sprintf "%1s %4s  %4d %4d  %4s %4s  %4s %4s  %4s %4s %4s %4d %4s\n",
		    @split;
	    } elsif ($line =~ /^\*\s+(\d+)hpc/) {
		my $i = $1;
		$line =
		    sprintf "%1s %2dhpc  %7.2f  X.00  X.00  X.00  X.00  X.00\n",
		    "*", $i, $changes{$i}{hpc};
	    }
	    $newmfta .= $line;
	}
	close MFTA;

	# Print MFTA & INP
	open INP,  ">template.2.inp";  print INP  $newinp;  close INP;
	open MFTA, ">template.2.mfta"; print MFTA $newmfta; close MFTA;

	# Align
	`$alninp -b template.bgf -m template.2.mfta -i template.2.inp`;
	move("template.bgf", "template.orig.bgf");
	move("template.aligned.bgf", "template.bgf");
	move("template.inp", "template.orig.inp");
	move("template.2.inp", "template.inp");
	move("template.mfta", "template.orig.mfta");
	move("template.2.mfta", "template.mfta");
    }

    # Load Secondary Structure info from MFTA
    my $use_ss = 0;
    if ($mfta =~ /.mfta$/) {
	open MFTA, "../$mfta";
	while (<MFTA>) {
	    my $line = $_;

	    # TM start/stop line
	    if ($line =~ /^\*\s+(\d+)tm/) {
		my $i = $1;
		my @split = split(/\s+/, $line);

		# start/stop pair
		my $start = $split[2 * $pair];
		my $stop  = $split[2 * $pair + 1];

		# Make sure they're integers
		if (($start =~ /^\d+$/) && ($stop =~ /^\d+$/)) {
		    $use_ss = 1;
		    $dat{tgt}{$i}{ss_start}{res} = $start;
		    $dat{tgt}{$i}{ss_stop}{res}  = $stop;
		    $dat{tgt}{$i}{ss_start}{aln} = $map{tgt}{res2aln}{$start};
		    $dat{tgt}{$i}{ss_stop}{aln}  = $map{tgt}{res2aln}{$stop};
		    $dat{tgt}{$i}{ss_seq}{res} = "";
		    for (my $k = $dat{tgt}{$i}{ss_start}{aln};
			 $k <= $dat{tgt}{$i}{ss_stop}{aln}; $k++) {
			if ($aln[1][$k] ne "-") {
			    $dat{tgt}{$i}{ss_seq}{res} .= $aln[1][$k];
			}
		    }
		}
	    }
	}
	close MFTA;
    }

    # For each TM region
    my $mergecmd = "$merge";
    my $mergess  = "$merge";
    for (my $i = 1; $i <= @tms; $i++) {
	$mergecmd .= " tm.${i}.fin.bgf";
	$mergess  .= " tm.${i}.fin.ss.bgf";
	print " :: TM $i\n";

	# Chop off TM region
	`$pwb template.bgf -c $i -o tm.${i}.bgf >& /dev/null`;

	# Renumber TM region
	print "    Renumber\n";
	renumber(\%dat, $i, "tm.${i}.bgf", "tm.${i}.renum.bgf");

	###
	### Non-secondary structure TMs
	###
	if (1) {
	    # Scream to AGPST
	    print "    Alanize (AGPST)\n";
	    screamAGPST(\%dat, \@aln, \%map, $i, "tm.${i}.renum.bgf", "tm.${i}.agpst.bgf", 0);

	    # Minimize to 0.5
	    print "    Minimize\n";
	    minimize(\%dat, \@aln, \%map, $i, "tm.${i}.agpst.bgf", "tm.${i}.min.bgf", 0);

	    # Scream to final residues
	    print "    Final Scream\n";
	    screamFinal(\%dat, \@aln, \%map, $i, "tm.${i}.min.bgf", "tm.${i}.fin.bgf", 0);
	}

	###
	### Secondary structure TMs
	###
	if ($use_ss) {
	    # Extend/truncate
	    print "    Apply Secondary Structure\n";
	    applySS(\%dat, \@aln, \%map, $i, "tm.${i}.renum.bgf", "tm.${i}.renum.ss.bgf",
		    $overlap, $trunc);

	    # Scream to AGPST
	    print "    SS Alanize (AGPST)\n";
	    screamAGPST(\%dat, \@aln, \%map, $i, "tm.${i}.renum.ss.bgf",
			"tm.${i}.agpst.ss.bgf", 1);

	    # Minimize to 0.5
	    print "    SS Minimize\n";
	    minimize(\%dat, \@aln, \%map, $i, "tm.${i}.agpst.ss.bgf", "tm.${i}.min.ss.bgf", 1);

	    # Scream to final residues
	    print "    SS Final Scream\n";
	    screamFinal(\%dat, \@aln, \%map, $i, "tm.${i}.min.ss.bgf", "tm.${i}.fin.ss.bgf", 1);
	}

	# Cleanup
	unlink "tm.${i}.bgf";
	unlink "tm.${i}.renum.bgf";
	unlink "tm.${i}.agpst.bgf";
	unlink "tm.${i}.min.bgf";
	if ($use_ss) {
	    unlink "tm.${i}.renum.ss.bgf";
	    unlink "tm.${i}.agpst.ss.bgf";
	    unlink "tm.${i}.min.ss.bgf";
	}
    }

    # Merge BGF
    print " :: Merging TMs into Bundle\n";
    `$mergecmd -o target.bgf`;
    if ($use_ss) {
	`$mergess -o target.ss.bgf`;
    }

    # Cleanup
    unlink glob "tm.*.*";

    # MFTA Files
    system("clear");
    printMFTA(\%dat, \@aln, \%map, \@tms, $mfta, $use_ss, $pfx);

    # Copy Files
    move("target.bgf", "${pfx}.hom.bgf");
    copy("${pfx}.hom.bgf", "..");
    copy("${pfx}.hom.mfta", "..");
    if ($use_ss) {
	move("target.ss.bgf", "${pfx}.hom.ss.bgf");
	copy("${pfx}.hom.ss.bgf", "..");
	copy("${pfx}.hom.ss.mfta", "..");
    }

    # Return
    return (\%dat, $use_ss);
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
    `$pwb $in -no $in >& /dev/null`;

    # Clean up BGF
    `$bgfcheck -b $in`;

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

    # Target start number
    my $tgtstart = $dat{tgt}{$i}{start}{res};

    # Homology start number
    my $homstart = $dat{hom}{$i}{start}{res};

    # Difference
    my $d = $tgtstart - $homstart;

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
    my %dat = %{$_[0]};
    my @aln = @{$_[1]};
    my %map = %{$_[2]};
    my $i   =   $_[3];
    my $in  =   $_[4];
    my $out =   $_[5];
    my $ss  =   $_[6];

    # 6 of SCREAM residues
    my $scr = "";

    ###
    ### Non-secondary structure
    ###
    if (!$ss) {
	# Check for N-term Proline -> Non Proline Mutation
	my $ntermaln = $dat{tgt}{$i}{start}{aln};
	my $ntermtgt = substr($dat{tgt}{$i}{seq}{res},0,1);
	my $ntermhom = substr($dat{hom}{$i}{seq}{res},0,1);

	# If $tgtres = !P and $homres = P
	if (($ntermtgt ne "P") && ($ntermhom eq "P")) {
	    print "    N-term P -> NP Mutation\n";
	    pro2ala($in, $dat{tgt}{$i}{start}{res});
	}

	# Generate SCREAM list
	for (my $j = $dat{tgt}{$i}{start}{res}; $j <= $dat{tgt}{$i}{stop}{res}; $j++) {
	    my $aa = $aln[1][$map{tgt}{res2aln}{$j}];

	    if ($aa =~ /^[AGPST]$/) {
		$scr .= " ${aa}${j}_${i}";
	    } else {
		$scr .= " A${j}_${i}";
	    }
	}
    }

    ###
    ### Secondary Structure
    ###
    elsif ($ss) {
	# N-term extension: no need to check for P->NP mutation, extension is already alanine
	# N-term same or truncated: MUST CHECK
	if ($dat{tgt}{$i}{ss_start}{aln} >= $dat{tgt}{$i}{start}{aln}) {
	    # Check for N-term Proline -> Non Proline Mutation
	    my $ntermaln = $dat{tgt}{$i}{ss_start}{aln};
	    my $ntermtgt = $aln[1][$ntermaln];
	    my $ntermhom = $aln[2][$ntermaln];

	    # If $tgtres = !P and $homres = P
	    if (($ntermtgt ne "P") && ($ntermhom eq "P")) {
		print "    N-term P -> NP Mutation\n";
		pro2ala($in, $dat{tgt}{$i}{ss_start}{res});
	    }
	}

	# Generate SCREAM list
	for (my $j = $dat{tgt}{$i}{ss_start}{res}; $j <= $dat{tgt}{$i}{ss_stop}{res}; $j++) {
	    my $aa = $aln[1][$map{tgt}{res2aln}{$j}];

	    if ($aa =~ /^[AGPST]$/) {
		$scr .= " ${aa}${j}_${i}";
	    } else {
		$scr .= " A${j}_${i}";
	    }
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
	unlink "Anneal-Energies.txt";
	unlink "Field1.bgf";
	unlink "Residue-E.txt";
	unlink "scream.out";
	unlink "scream.par";
	unlink "timing.txt";
    }

    # Done
}

################################################################################
### Minimize
################################################################################
sub minimize {
    my %dat = %{$_[0]};
    my @aln = @{$_[1]};
    my %map = %{$_[2]};
    my $i   =   $_[3];
    my $in  =   $_[4];
    my $out =   $_[5];
    my $ss  =   $_[6];

    # Hydrophobic Center
    my $tgthpc = $dat{tgt}{$i}{hpcnum}{res};
    my $homhpc = $dat{hom}{$i}{hpcnum}{res};
    my $dec = $dat{tgt}{$i}{hpcdec};
    if ($dec > 50) { $tgthpc++; $homhpc++; }

    # Core Residues
    my $pnp = 0;
    my $fix = "";
    for (my $j = -2; $j <= 2; $j++) {
	my $tgt_aa  = $aln[1][$map{tgt}{res2aln}{$tgthpc + $j}];
	my $hom_aa  = $aln[2][$map{hom}{res2aln}{$homhpc + $j}];
	my $tgt_num = $tgthpc + $j;

	# Check for P<->Non-P mutation
	if ((($tgt_aa eq "P") && ($hom_aa ne "P")) ||
	    (($tgt_aa ne "P") && ($hom_aa eq "P"))) {
	    $pnp = 1;
	}

	# Residue to keep fixed
	$fix .= " -r ${tgt_num}${i}";
    }

    # No P<->Non-P Mutation = Fix Core of Helix
    if (!$pnp) {
	$fix .= " -b -V off -L -o $in";
	`$pwb $in $fix >& /dev/null`;
    }

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
    my %dat = %{$_[0]};
    my @aln = @{$_[1]};
    my %map = %{$_[2]};
    my $i   =   $_[3];
    my $in  =   $_[4];
    my $out =   $_[5];
    my $ss  =   $_[6];

    # List of SCREAM residues
    my $scr = "";

    ###
    ### Non-secondary structure
    ###
    if (!$ss) {
	for (my $j = $dat{tgt}{$i}{start}{res}; $j <= $dat{tgt}{$i}{stop}{res}; $j++) {
	    my $aa = $aln[1][$map{tgt}{res2aln}{$j}];

	    if ($aa !~ /^[AGP]$/) {
		$scr .= " ${aa}${j}_${i}";
	    }
	}
    }

    ###
    ### Secondary Structure
    ###
    elsif ($ss) {
	for (my $j = $dat{tgt}{$i}{ss_start}{res}; $j <= $dat{tgt}{$i}{ss_stop}{res}; $j++) {
	    my $aa = $aln[1][$map{tgt}{res2aln}{$j}];

	    if ($aa !~ /^[AGP]$/) {
		$scr .= " ${aa}${j}_${i}";
	    }
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
	unlink "Anneal-Energies.txt";
	unlink "Field1.bgf";
	unlink "Residue-E.txt";
	unlink "scream.out";
	unlink "scream.par";
	unlink "timing.txt";
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
    `$pwb $in -r '${start}...${stop}${chn}' +H -no $out >& /dev/null`;

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
    `$pwb $in -r '${start}...${stop}${chn}' +H -no $out >& /dev/null`;

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
	`$pwb ext.aligned.bgf -r '${newstart}...${exttrunc}${chn}' -no ext.trunc.bgf >& /dev/null`;

	# Trim N-term
	`$pwb $in -r '${oldstart}...${stop}${chn}' -no ${mergeto} >& /dev/null`;
    }

    # Not trimming end of helix
    else {
	# Truncate Extension Overlap
	`$pwb ext.aligned.bgf -r '${newstart}...${exttrunc}${chn}' -no ext.trunc.bgf >& /dev/null`;

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
	`$pwb ext.aligned.bgf -r '${exttrunc}...${newstop}${chn}' -no ext.trunc.bgf >& /dev/null`;

	# Trim C-term
	`$pwb $in -r '${start}...${oldstop}${chn}' -no ${mergeto} >& /dev/null`;
    }

    # Not trimming end of helix
    else {
	# Truncate Overlap
	`$pwb ext.aligned.bgf -r '${exttrunc}...${newstop}${chn}' -no ext.trunc.bgf >& /dev/null`;

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
    my @aln     = @{$_[1]};
    my %map     = %{$_[2]};
    my $i       =   $_[3];
    my $in      =   $_[4];
    my $out     =   $_[5];
    my $overlap =   $_[6];
    my $trunc   =   $_[7];

    # Old/new start/stop values
    my $newnterm = $dat{tgt}{$i}{ss_start}{res};
    my $oldnterm = $dat{tgt}{$i}{start}{res};
    my $ndiff    = $newnterm - $oldnterm;
    my $newcterm = $dat{tgt}{$i}{ss_stop}{res};
    my $oldcterm = $dat{tgt}{$i}{stop}{res};
    my $cdiff    = $newcterm - $oldcterm;
    (my $ntermout = $in) =~ s/.bgf$/.N.bgf/;

    # N-term Extension
    if ($ndiff < 0) {
	printf "      N-term: %3d to %3d (extend)\n", $oldnterm, $newnterm;
	nTermExtend($in, $ntermout, $i, $oldnterm, $newnterm, $oldcterm, $overlap, $trunc);    }

    # N-term Truncation
    elsif ($ndiff > 0) {
	printf "      N-term: %3d to %3d (truncate)\n", $oldnterm, $newnterm;
	nTermTruncate($in, $ntermout, $i, $newnterm, $oldcterm);
    }

    # N-term Same
    else {
	copy($in, $ntermout);
	printf "      N-term: %3d (keep)\n", $oldnterm;
    }

    # C-term Extension
    if ($cdiff > 0) {
	printf "      C-term: %3d to %3d (extend)\n", $oldcterm, $newcterm;
	cTermExtend($ntermout, $out, $i, $newnterm, $oldcterm, $newcterm, $overlap, $trunc)
    }

    # C-term Truncation
    elsif ($cdiff < 0) {
	printf "      C-term: %3d to %3d (truncate)\n", $oldcterm, $newcterm;
	cTermTruncate($ntermout, $out, $i, $newnterm, $newcterm);
    }

    # C-term Same
    else {
	copy($ntermout, $out);
	printf "      C-term: %3d (keep)\n", $oldcterm;
    }

    # Cleanup
    unlink $ntermout;
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
    my @aln     = @{$_[1]};
    my %map     = %{$_[2]};
    my @tms     = @{$_[3]};
    my $oldmfta =   $_[4];
    my $use_ss  =   $_[5];
    my $prefix  =   $_[6];

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
    my $mftatxt   = $txt;
    my $mftasstxt = $txt;
    for (my $i = 1; $i <= @tms; $i++) {
	$mftatxt .=
	    sprintf "* %dtm   %4d %4d   X X   X X   X X   %s %4d   A\n",
	    $i, $dat{tgt}{$i}{start}{res}, $dat{tgt}{$i}{stop}{res},
	    $dat{tgt}{$i}{eres}, $dat{tgt}{$i}{enum}{res};
	if ($use_ss) {
	    $mftasstxt .=
		sprintf "* %dtm   %4d %4d   X X   X X   X X   %s %4d   A\n",
		$i, $dat{tgt}{$i}{ss_start}{res}, $dat{tgt}{$i}{ss_stop}{res},
		$dat{tgt}{$i}{eres}, $dat{tgt}{$i}{enum}{res};
	}
    }

    # HPC
    for (my $i = 1; $i <= @tms; $i++) {
	my $tmpdec = $dat{tgt}{$i}{hpcdec};
	if ($tmpdec < 10) { $tmpdec = "0" . $tmpdec; }
	$mftatxt .=
	    sprintf "* %dhpc   %4d.%2s   X.00   X.00   X.00   X.00   X.00\n",
	    $i, $dat{tgt}{$i}{hpcnum}{res}, $tmpdec;
	if ($use_ss) {
	    $mftasstxt .=
		sprintf "* %dhpc   %4d.%2s   X.00   X.00   X.00   X.00   X.00\n",
		$i, $dat{tgt}{$i}{hpcnum}{res}, $tmpdec;
	}
    }

    # Print
    open MFTA, ">${prefix}.hom.mfta";
    print MFTA $mftatxt;
    close MFTA;
    if ($use_ss) {
	open MFTA, ">${prefix}.hom.ss.mfta";
	print MFTA $mftasstxt;
	close MFTA;
    }

    # Done
}

################################################################################
### Final printing
################################################################################
sub printFinal {
    my @aln     = @{$_[0]};
    my %map     = %{$_[1]};
    my %dat     = %{$_[2]};
    my @tms     = @{$_[3]};
    my $alnlen  =   $_[4];
    my $tgtlen  =   $_[5];
    my $homlen  =   $_[6];
    my $mfta    =   $_[7];
    my $temp    =   $_[8];
    my $pair    =   $_[9];
    my $overlap =   $_[10];
    my $trunc   =   $_[11];
    my $prefix  =   $_[12];
    my $use_ss  =   $_[13];

    my $cwd = cwd();
    my $finaltxt = "";
    $finaltxt .= sprintf
	"Homologize :: Final Report :: " . localtime() . "\n".
	" :: Log File :: ${prefix}.log\n\n".
	" :: Target\n".
	"    File    :: $mfta\n".
	"    Length  :: $tgtlen\n";
    if ($use_ss) {
	$finaltxt .= sprintf
	    "    SS Pair :: $pair\n\n";
    } else {
	$finaltxt .= sprintf "\n";
    }
    $finaltxt .= sprintf
	" :: Homology Template\n".
	"    BGF File  :: ${cwd}/${temp}.bgf\n".
	"    MFTA File :: ${cwd}/${temp}.mfta\n".
	"    Length    :: $homlen\n\n";
    $finaltxt .= sprintf
	" :: Full Alignment\n".
	"    PIR :: ${prefix}.pir\n".
	"    ALN :: ${prefix}.aln\n\n".
	" :: Condensed Alignment\n".
	"    Length :: $alnlen\n".
	"    PIR :: ${prefix}.cnd.pir\n".
	"    ALN :: ${prefix}.cnd.aln\n\n".
	" :: Output\n".
	"    Homology Start/Stop\n".
	"      BGF  :: ${prefix}.hom.bgf\n".
	"      MFTA :: ${prefix}.hom.mfta\n";
    if ($use_ss) {
	$finaltxt .= sprintf
	    "    Secondary Structure Start/Stop\n".
	    "      BGF      :: ${prefix}.hom.ss.bgf\n".
	    "      MFTA     :: ${prefix}.hom.ss.mfta\n".
	    "      Overlap  :: $overlap\n".
	    "      Truncate :: $trunc\n\n";
    }

    foreach my $tm (@tms) {
	$finaltxt .= printTM_long_final($tm, \@aln, \%map, \%dat, \@tms, $alnlen,
				  $tgtlen, $homlen, $use_ss);
    }

    print $finaltxt;
    open LOG, ">${prefix}.log";
    print LOG $finaltxt;
    close LOG;
}

############################################################
### Help                                                 ###
############################################################

sub help {

    my $help = "
Program:
 :: Homologize.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: Homologize.pl -m {mfta} -t {template file prefix}

Input:
 :: -m | --mfta        :: Filename
 :: MFTA or FTA for the target protein.
 :: Use FTA if secondary structure changes not needed.

 :: -t | --temp        :: File / File Prefix
 :: Homology template.  The program needs both a BGF and
 :: an MFTA with the same file prefix:
 :: Example: -t tBeta1_2vt4_xray
 ::  * program will expect:
 ::        tBeta1_2vt4_xray.bgf
 ::        tBeta1_2vt4_xray.mfta

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
 :: 1) Aligns target sequence with homology template sequence
 ::    and other selected GPCR sequences (crystal templates,
 ::    prediced structures, in-progress proteins)
 ::    Sequences used: ${Bin}/fasta/*.fta
 :: 2) Identifies transmembrane regions
 :: 3) Allows the user to adjust:
 ::    a) The alignment profile (helix shape)
 ::    b) The hydrophobic center
 ::    c) The eta residue
 :: 4) Rotates and shifts helices as needed
 :: 5) Mutates residues to the final target
 :: 6) Applies secondary structure extensions or truncations
 ::
 :: Helix preparation:
 :: 1) Applies secondary structure extensions or truncations
 :: 2) Screams the template helix to AGPST
 :: 3) Minimizes helix to 0.5 RMS Force
 :: 4) Screams to final residues
 ::
 :: Helix extensions:
 :: 1) Aligns a polyalanine helix to the end of the target helix
 ::    with an overlap of 8 residues
 :: 2) Trims 2 residues from the old helix
 :: 3) Connects the extension to the helix

Usage:
 :: Homologize.pl -m {mfta} -t {template file prefix}

";

    die "$help";
}
