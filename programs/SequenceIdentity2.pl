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
use List::Util qw(min max);
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

#use AlignTools::AlignTools;

# Set up the BLOSUM62 Similarity Matrix
@blosumAA =
    qw(A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V  B  Z  X  gap);

@blosum62txt =
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

my %blosum62;
for ($i = 0; $i < @blosumAA; $i++) {
    for ($j = 0; $j < @blosumAA; $j++) {
	$blosum62{$blosumAA[$i]}{$blosumAA[$j]} = $blosum62txt[$i][$j];
    }
}

# Set up the GPCR segments
@segments = qw(1 2 3 4 5 6 7 N C I J K E F G);
@tms      = qw(1 2 3 4 5 6 7 );
@loops    = qw(N C I J K E F G);

# Handle Input
if (@ARGV == 0) { help(); }

# Input
# 2 MFTAs
#   1) Create FTA from MFTAs
#   2) Align FTA
#   3) Load Alignment
#   4) Use MFTAs to find segments

#abcdefghijklmnopqrstuvwxyz
#abcdefg ijklmno qrstuvwxyz
GetOptions ('h|help'          => \$help,
	    'm1=s'            => \$m1,
	    'm2=s'            => \$m2,
	    'debug'           => \$debug);

if ($help) { help(); }

############################################################
### Main Routine                                         ###
############################################################

if (!$m1 || !$m2) {
    die "ERROR :: Must provide either one or two MFTA files.\n\n";
}

print "\SequenceIdentity.pl :: " . localtime() . "\n";
# Load FTA portion of MFTA 1
# Load TMs portion of MFTA 1
my $fta = "";
my $seq1 = "";
open MFTA, "$m1";
while (<MFTA>) {
    if ((!/^\*/) && (!/^\#/)) {
	$fta  .= $_;
	if (!/^\>/) {
	    $seq1 .= $_;
	}
	chomp $seq1;
    } elsif (/^\*\s+(\d+)tm\s+(\d+)\s+(\d+)/) {
	$mfta{1}{$1}{start} = $2;
	$mfta{1}{$1}{stop}  = $3;
    }
}
close MFTA;
$mfta{1}{N}{start} = 1;
$mfta{1}{N}{stop}  = $mfta{1}{1}{start} - 1;
$mfta{1}{I}{start} = $mfta{1}{1}{stop} + 1;
$mfta{1}{I}{stop}  = $mfta{1}{2}{start} - 1;
$mfta{1}{E}{start} = $mfta{1}{2}{stop} + 1;
$mfta{1}{E}{stop}  = $mfta{1}{3}{start} - 1;
$mfta{1}{J}{start} = $mfta{1}{3}{stop} + 1;
$mfta{1}{J}{stop}  = $mfta{1}{4}{start} - 1;
$mfta{1}{F}{start} = $mfta{1}{4}{stop} + 1;
$mfta{1}{F}{stop}  = $mfta{1}{5}{start} - 1;
$mfta{1}{K}{start} = $mfta{1}{5}{stop} + 1;
$mfta{1}{K}{stop}  = $mfta{1}{6}{start} - 1;
$mfta{1}{G}{start} = $mfta{1}{6}{stop} + 1;
$mfta{1}{G}{stop}  = $mfta{1}{7}{start} - 1;
$mfta{1}{C}{start} = $mfta{1}{7}{stop} + 1;
$mfta{1}{C}{stop}  = length($seq1);

# Load FTA portion of MFTA 2
# Load TMs portion of MFTA 2
open MFTA, "$m2";
my $seq2 = "";
while (<MFTA>) {
    if ((!/^\*/) && (!/^\#/)) {
	$fta  .= $_;
	if (!/^\>/) {
	    $seq2 .= $_;
	}
	chomp $seq2;
    } elsif (/^\*\s+(\d+)tm\s+(\d+)\s+(\d+)/) {
	$mfta{2}{$1}{start} = $2;
	$mfta{2}{$1}{stop}  = $3;
    }
}
close MFTA;
$mfta{2}{N}{start} = 1;
$mfta{2}{N}{stop}  = $mfta{2}{1}{start} - 1;
$mfta{2}{I}{start} = $mfta{2}{1}{stop} + 1;
$mfta{2}{I}{stop}  = $mfta{2}{2}{start} - 1;
$mfta{2}{E}{start} = $mfta{2}{2}{stop} + 1;
$mfta{2}{E}{stop}  = $mfta{2}{3}{start} - 1;
$mfta{2}{J}{start} = $mfta{2}{3}{stop} + 1;
$mfta{2}{J}{stop}  = $mfta{2}{4}{start} - 1;
$mfta{2}{F}{start} = $mfta{2}{4}{stop} + 1;
$mfta{2}{F}{stop}  = $mfta{2}{5}{start} - 1;
$mfta{2}{K}{start} = $mfta{2}{5}{stop} + 1;
$mfta{2}{K}{stop}  = $mfta{2}{6}{start} - 1;
$mfta{2}{G}{start} = $mfta{2}{6}{stop} + 1;
$mfta{2}{G}{stop}  = $mfta{2}{7}{start} - 1;
$mfta{2}{C}{start} = $mfta{2}{7}{stop} + 1;
$mfta{2}{C}{stop}  = length($seq2);

# Print FTA for MAFFT
($pfx[1] = $m1) =~ s/.mfta//;
($pfx[2] = $m2) =~ s/.mfta//;
$tmp = "$pfx[1].$pfx[2]";
open FTA, ">${tmp}.fta";
print FTA "$fta";
close FTA;

# MAFFT
($pir, $aln) = mafft("${tmp}.fta");
print
    " :: Seq 1 MFTA    :: $m1\n".
    " :: Seq 2 MFTA    :: $m2\n".
    " :: FTA Sequences :: ${tmp}.fta\n".
    " :: PIR Alignment :: $pir\n".
    " :: ALN Alignment :: $aln\n\n";

# Load PIR Alignment into Array
@return = pir2alnArray($pir);
$alnlen        =   $return[0];
@{$condaln[3]} = @{$return[1]};
@aln           = @{$return[1]};

# Load ALN Alignment Similarity into Array
@return = aln2simArray($aln);
@{$aln[3]}        = @{$return[0]};
@{$condaln[3][3]} = @{$return[0]};

# For Sequence 1 & 2
for ($i = 1; $i <= 2; $i++) {
    $resnum = 0;

    # For Each Position in the Alignment
    for ($j = 1; $j <= $alnlen; $j++) {
	# If not a gap
	if ($aln[$i][$j] !~ /-/) {
	    # Then we're on a new residue number
	    $resnum++;

	    # Go through each segment
	    foreach $seg (@segments) {
		# If this residue is a segment start, mark the alignment position
		if ($resnum == $mfta{$i}{$seg}{start}) {
		    $map{$i}{$seg}{start} = $j;
		}

		# If this residue is a segment stop, mark the alignment position
		if ($resnum == $mfta{$i}{$seg}{stop}) {
		    $map{$i}{$seg}{stop} = $j;
		}
	    }
	}
    }
}

# Start = max(start 1, start 2)
# Stop  = max(stop  1, stop  2)
for ($seg = 1; $seg <= 7; $seg++) {
    $mfta{3}{$seg}{start} = max($map{1}{$seg}{start}, $map{2}{$seg}{start});
    $mfta{3}{$seg}{stop}  = min($map{1}{$seg}{stop},  $map{2}{$seg}{stop});
}
$mfta{3}{N}{start} = 1;
$mfta{3}{N}{stop}  = $mfta{3}{1}{start} - 1;
$mfta{3}{I}{start} = $mfta{3}{1}{stop} + 1;
$mfta{3}{I}{stop}  = $mfta{3}{2}{start} - 1;
$mfta{3}{E}{start} = $mfta{3}{2}{stop} + 1;
$mfta{3}{E}{stop}  = $mfta{3}{3}{start} - 1;
$mfta{3}{J}{start} = $mfta{3}{3}{stop} + 1;
$mfta{3}{J}{stop}  = $mfta{3}{4}{start} - 1;
$mfta{3}{F}{start} = $mfta{3}{4}{stop} + 1;
$mfta{3}{F}{stop}  = $mfta{3}{5}{start} - 1;
$mfta{3}{K}{start} = $mfta{3}{5}{stop} + 1;
$mfta{3}{K}{stop}  = $mfta{3}{6}{start} - 1;
$mfta{3}{G}{start} = $mfta{3}{6}{stop} + 1;
$mfta{3}{G}{stop}  = $mfta{3}{7}{start} - 1;
$mfta{3}{C}{start} = $mfta{3}{7}{stop} + 1;
$mfta{3}{C}{stop}  = $alnlen;

# Condense to no gaps in sequence 1
@return     = condenseAlignToTarget(\@aln, $alnlen, 1);
$alnlen_1   =   $return[0];
@{$condaln[1]} = @{$return[1]};

# Condense to no gaps in sequence 2
@return     = condenseAlignToTarget(\@aln, $alnlen, 2);
$alnlen_2   =   $return[0];
@{$condaln[2]} = @{$return[1]};

# Percent Identity/Similarity for Sequence 1 & 2 & 3
my %dat;
for ($i = 1; $i <= 3; $i++) {
    foreach $seg (@segments) {
	$same = 0;
	$sim  = 0;

	# Length of segment
	$dat{$i}{$seg}{length} = $mfta{$i}{$seg}{stop} - $mfta{$i}{$seg}{start} + 1;

	# For each position of the segment
	for ($j = $mfta{$i}{$seg}{start}; $j <= $mfta{$i}{$seg}{stop}; $j++) {
	    $aa_1 = $condaln[$i][1][$j]; # AA at this position in sequence 1
	    $aa_2 = $condaln[$i][2][$j]; # AA at this position in sequence 2
	    if ($aa_1 eq $aa_2) { # Identical
		$same++;
	    }
	    if ($blosum62{$aa_1}{$aa_2} > 0) { # Similar
		$sim++;
	    }
	}

	# Number Same / Similar
	$dat{$i}{$seg}{same} = $same;
	$dat{$i}{$seg}{sim}  = $sim;

	# Percent Same / Similar
	$dat{$i}{$seg}{pid}  = ($same / $dat{$i}{$seg}{length}) * 100;
	$dat{$i}{$seg}{psim} = ($sim  / $dat{$i}{$seg}{length}) * 100;
    }

    # Average over TMs
    for ($s = 1; $s <= 7; $s++) {
	$dat{$i}{tms}{length} += $dat{$i}{$s}{length};
	$dat{$i}{tms}{same}   += $dat{$i}{$s}{same};
	$dat{$i}{tms}{sim}    += $dat{$i}{$s}{sim};
    }
    $dat{$i}{tms}{pid}  = ($dat{$i}{tms}{same} / $dat{$i}{tms}{length}) * 100;
    $dat{$i}{tms}{psim} = ($dat{$i}{tms}{sim}  / $dat{$i}{tms}{length}) * 100;

    # Average over All
    foreach $seg (@segments) {
	$dat{$i}{all}{length} += $dat{$i}{$seg}{length};
	$dat{$i}{all}{same}   += $dat{$i}{$seg}{same};
	$dat{$i}{all}{sim}    += $dat{$i}{$seg}{sim};
    }
    $dat{$i}{all}{pid}  = ($dat{$i}{all}{same} / $dat{$i}{all}{length}) * 100;
    $dat{$i}{all}{psim} = ($dat{$i}{all}{sim}  / $dat{$i}{all}{length}) * 100;
}

# Print Identity
open TXT, ">${tmp}.txt";
print "***************************************************************************\n";
$len = max(length("Condensed to $pfx[1]"),length("Condensed to $pfx[2]"),length("Percent Similarity"));
printf     "%-${len}s  All   TMs  ::", "Percent Identity";
printf TXT "%-${len}s  All   TMs  ::", "Percent Identity";
foreach $seg (@tms) {
    printf     "   %s  ", $seg;
    printf TXT "   %s  ", $seg;
}
printf     "\n%s ----- ----- ::", "-" x $len;
printf TXT "\n%s ----- ----- ::", "-" x $len;
foreach $seg (@tms) {
    print      " -----";
    print  TXT " -----";
}
print     "\n";
print TXT "\n";
for ($i = 1; $i <= 3; $i++) {
    if ($i < 3) {
	printf     "%-${len}s", "Condensed to $pfx[$i]";
	printf TXT "%-${len}s", "Condensed to $pfx[$i]";
    } else {
	printf     "%-${len}s", "Uncondensed";
	printf TXT "%-${len}s", "Uncondensed";
    }
    printf     " %5.1f %5.1f ::", $dat{$i}{all}{pid}, $dat{$i}{tms}{pid};
    printf TXT " %5.1f %5.1f ::", $dat{$i}{all}{pid}, $dat{$i}{tms}{pid};
    foreach $seg (@tms) {
	printf     " %5.1f", $dat{$i}{$seg}{pid};
	printf TXT " %5.1f", $dat{$i}{$seg}{pid};
    }
    print     "\n";
    print TXT "\n";
}
print     "\n";
print TXT "\n";

$len = max(length("Condensed to $pfx[1]"),length("Condensed to $pfx[2]"),length("Percent Similarity"));
printf     "%-${len}s", "Percent Identity";
printf TXT "%-${len}s", "Percent Identity";
foreach $seg (@loops) {
    printf     "   %s  ", $seg;
    printf TXT "   %s  ", $seg;
    if (($seg eq "C") || ($seg eq "K")) {
	print     " ::";
	print TXT " ::";
    }
}
printf     "\n%s", "-" x $len;
printf TXT "\n%s", "-" x $len;
foreach $seg (@loops) {
    print     " -----";
    print TXT " -----";
    if (($seg eq "C") || ($seg eq "K")) {
	print     " ::";
	print TXT " ::";
    }
}
print     "\n";
print TXT "\n";
for ($i = 1; $i <= 3; $i++) {
    if ($i < 3) {
	printf     "%-${len}s", "Condensed to $pfx[$i]";
	printf TXT "%-${len}s", "Condensed to $pfx[$i]";
    } else {
	printf     "%-${len}s", "Uncondensed";
	printf TXT "%-${len}s", "Uncondensed";
    }
    foreach $seg (@loops) {
	printf     " %5.1f", $dat{$i}{$seg}{pid};
	printf TXT " %5.1f", $dat{$i}{$seg}{pid};
	if (($seg eq "C") || ($seg eq "K")) {
	    print     " ::";
	    print TXT " ::";
	}
    }
    print     "\n";
    print TXT "\n";
}
print     "\n";
print TXT "\n";

# Print Similarity
print     "***************************************************************************\n";
print TXT "***************************************************************************\n";
$len = max(length("Condensed to $pfx[1]"),length("Condensed to $pfx[2]"),"Percent Similarity");
printf     "%-${len}s  All   TMs  ::", "Percent Similarity";
printf TXT "%-${len}s  All   TMs  ::", "Percent Similarity";
foreach $seg (@tms) {
    printf     "   %s  ", $seg;
    printf TXT "   %s  ", $seg;
}
printf     "\n%s ----- ----- ::", "-" x $len;
printf TXT "\n%s ----- ----- ::", "-" x $len;
foreach $seg (@tms) {
    print     " -----";
    print TXT " -----";
}
print     "\n";
print TXT "\n";
for ($i = 1; $i <= 3; $i++) {
    if ($i < 3) {
	printf     "%-${len}s", "Condensed to $pfx[$i]";
	printf TXT "%-${len}s", "Condensed to $pfx[$i]";
    } else {
	printf     "%-${len}s", "Uncondensed";
	printf TXT "%-${len}s", "Uncondensed";
    }
    printf     " %5.1f %5.1f ::", $dat{$i}{all}{psim}, $dat{$i}{tms}{psim};
    printf TXT " %5.1f %5.1f ::", $dat{$i}{all}{psim}, $dat{$i}{tms}{psim};
    foreach $seg (@tms) {
	printf     " %5.1f", $dat{$i}{$seg}{psim};
	printf TXT " %5.1f", $dat{$i}{$seg}{psim};
    }
    print     "\n";
    print TXT "\n";
}
print     "\n";
print TXT "\n";

$len = max(length("Condensed to $pfx[1]"),length("Condensed to $pfx[2]"),"Percent Similarity");
printf     "%-${len}s", "Percent Similarity";
printf TXT "%-${len}s", "Percent Similarity";
foreach $seg (@loops) {
    printf     "   %s  ", $seg;
    printf TXT "   %s  ", $seg;
    if (($seg eq "C") || ($seg eq "K")) {
	print     " ::";
	print TXT " ::";
    }
}
printf     "\n%s", "-" x $len;
printf TXT "\n%s", "-" x $len;
foreach $seg (@loops) {
    print     " -----";
    print TXT " -----";
    if (($seg eq "C") || ($seg eq "K")) {
	print     " ::";
	print TXT " ::";
    }
}
print     "\n";
print TXT "\n";
for ($i = 1; $i <= 3; $i++) {
    if ($i < 3) {
	printf     "%-${len}s", "Condensed to $pfx[$i]";
	printf TXT "%-${len}s", "Condensed to $pfx[$i]";
    } else {
	printf     "%-${len}s", "Uncondensed";
	printf TXT "%-${len}s", "Uncondensed";
    }
    foreach $seg (@loops) {
	printf     " %5.1f", $dat{$i}{$seg}{psim};
	printf TXT " %5.1f", $dat{$i}{$seg}{psim};
	if (($seg eq "C") || ($seg eq "K")) {
	    print     " ::";
	    print TXT " ::";
	}
    }
    print     "\n";
    print TXT "\n";
}
print     "\n";
print TXT "\n";
close TXT;

# Print CSV Files for Percent Identity/Similarity
open CSV, ">${tmp}.csv";
print CSV "Percent Identity,All,TMs";
foreach $seg (@segments) {
    print CSV ",$seg";
}
print CSV "\n";
for ($i = 1; $i <= 3; $i++) {
    if ($i < 3) {
	print CSV "Condensed to $pfx[$i]";
    } else {
	print CSV "Uncondensed";
    }
    printf CSV ",%.1f,%.1f", $dat{$i}{all}{pid}, $dat{$i}{tms}{pid};
    foreach $seg (@segments) {
	printf CSV ",%.1f", $dat{$i}{$seg}{pid};
    }
    print CSV "\n";
}
print CSV "\n";
print CSV "Percent Similarity,All,TMs";
foreach $seg (@segments) {
    print CSV ",$seg";
}
print CSV "\n";
for ($i = 1; $i <= 3; $i++) {
    if ($i < 3) {
	print CSV "Condensed to $pfx[$i]";
    } else {
	print CSV "Uncondensed";
    }
    printf CSV ",%.1f,%.1f", $dat{$i}{all}{psim}, $dat{$i}{tms}{psim};
    foreach $seg (@segments) {
	printf CSV ",%.1f", $dat{$i}{$seg}{psim};
    }
    print CSV "\n";
}
close CSV;

# Print the alignments
$len2 = max(length($pfx[1]), length($pfx[2]));
for ($i = 1; $i <= 3; $i++) {
    if ($i == 1) {
	print "***************************************************************************\n";
	print "Results based on alignment condensed to have no gaps for sequence $pfx[1]\n\n";
    } elsif ($i == 2) {
	print "***************************************************************************\n";
	print "Results based on alignment condensed to have no gaps for sequence $pfx[2]\n\n";
    } elsif ($i == 3) {
	print "***************************************************************************\n";
	print "Results based on standard MAFFT alignment\n\n";
    }

    foreach $seg (@segments) {
	if ($seg eq "1") {
	    print "***** TMs *********************\n";
	} elsif ($seg eq "N") {
	    print "***** NTerm / CTerm ***********\n";
	} elsif ($seg eq "I") {
	    print "***** Intracellular Loops *****\n";
	} elsif ($seg eq "E") {
	    print "***** Extracellular Loops *****\n";
	}
	printf "Segment $seg :: %5.1f %% identity :: %5.1f %% similarity\n",
	$dat{$i}{$seg}{pid}, $dat{$i}{$seg}{psim};

	$seq1 = ""; $seq2 = ""; $seq3 = "";
	for ($j = $mfta{$i}{$seg}{start}; $j <= $mfta{$i}{$seg}{stop}; $j++) {
	    $seq1 .= $condaln[$i][1][$j];
	    $seq2 .= $condaln[$i][2][$j];
	    $seq3 .= $condaln[$i][3][$j];
	}
	while (length($seq1) > 60) {
	    printf " :: %-${len2}s :: ", $pfx[1];
	    print  substr($seq1,0,60) . "\n";
	    printf " :: %-${len2}s :: ", $pfx[2];
	    print  substr($seq2,0,60) . "\n";
	    printf "    %-${len2}s    ", " ";
	    print  substr($seq3,0,60) . "\n\n";

	    substr($seq1,0,60) = "";
	    substr($seq2,0,60) = "";
	    substr($seq3,0,60) = "";
	}
	if (length($seq1) > 0) {
	    printf " :: %-${len2}s :: $seq1\n", $pfx[1];
	    printf " :: %-${len2}s :: $seq2\n", $pfx[2];
	    printf "    %-${len2}s    $seq3\n\n", " ";
	}
    }
}























exit;

################################################################################
### pir2aln                                                                  ###
################################################################################
sub pir2aln {
    my $f = shift;
    (my $nf = $f) =~ s/.pir$/.aln/;

    # Copy PIR to TMP PIR
    open PIR, "$f";
    my $txt;
    while (<PIR>) {
	$txt .= "$_";
    }
    close PIR;
    $txt =~ s/\>/\*\n\>/g;
    $txt =~ s/^\*\n//;
    $txt .= "*\n";
    my @split = split(/\n/, $txt);
    open TMP, ">tmp.pir";
    for (my $i = 0; $i < @split; $i++) {
	if ($split[$i] =~ /^\>/) {
	    print TMP "$split[$i]\n\n";
	} else {
	    print TMP "$split[$i]\n";
	}
    }
    close TMP;

    # Convert PIR to ALN
    my $bio = "/project/Biogroup/Software/GEnsemble/programs/thirdparty";
    `${bio}/clustal/clustalw -infile=tmp.pir -convert -outfile=${nf}`;

    unlink "tmp.pir";
    return "$nf";
}

################################################################################
### aln2pir                                                                  ###
################################################################################
sub aln2pir {
    my $f = shift;
    (my $nf = $f) =~ s/.aln$/.pir/;

    # Convert PIR to ALN
    my $bio = "/project/Biogroup/Software/GEnsemble/programs/thirdparty";
    `${bio}/clustal/clustalw -infile=${f} -convert -outfile=${nf} -output=PIR`;

    # Remove blank lines and * lines
    move("$nf", "tmp.pir");
    open TMP, "tmp.pir";
    open PIR, ">$nf";
    while (<TMP>) {
	if ((!/^\n/) && (!/^\*/)) {
	    print PIR $_;
	}
    }
    close TMP;
    unlink "tmp.pir";
    close PIR;
    return "$nf";
}

################################################################################
### mafft                                                                    ###
################################################################################
sub mafft {
    my $fastafile  = shift; # Fasta file containing sequences to be aligned

    # Set up MAFFT Environment
    my $bio = "/project/Biogroup/Software/GEnsemble/programs/thirdparty";
    $ENV{MAFFT_BINARIES} = "${bio}/mafft/lib/mafft";

    # Handle Prefix
    my $prefix = $fastafile;
    $prefix =~ s/.fta$//;
    
    # Set up MAFFT Command
    my $command = " --genafpair --op 10.0 --ep 0.2";

    # Run MAFFT if number of sequences is greater than 1
    `(${bio}/mafft/mafft $command $fastafile > ${prefix}.pir) >& ${prefix}.mafft.out`;

    # Convert PIR to ALN
    pir2aln("${prefix}.pir");

    return ("${prefix}.pir", "${prefix}.aln");
}

################################################################################
### pir2alnArray                                                             ###
################################################################################
sub pir2alnArray {
    my $pir = shift; # PIR Alignment File

    my @headers;
    my @alignment;
    my $i = 0;
    open PIR, "$pir";
    while (<PIR>) {
	chomp;

	# We've found a new sequence in the PIR file
	if (/^\>/) {
	    $i++;
	    $headers[$i] = "$_";           # Grab the header line
	    # Change >P1;sp|######|####_##### to >sp|######|####_#####
	    $headers[$i] =~ s/^\>P1\;/\>/;

	# Blank line or * line
	} elsif ((/^\s+/) || (/^\*/)) {
	    # Do nothing

	# We've found an alignment line in the PIR file
	} else {
	    $alignment[$i] .= "$_";       # Grab the alignment line
	}
    }
    close PIR;

    # Convert from 1D to 2D
    my @alignment_2D;
    for (my $i = 1; $i <= 2; $i++) {
	for (my $j = 0; $j < length($alignment[$i]); $j++) {
	    # Sequences: ($i = 1; $i <= 2; $i++)
	    # Positions: ($j = 1; $j <= length(alignment); $j++)
	    $alignment_2D[$i][$j+1] = substr($alignment[$i],$j,1);
	}
    }
    my $alnlen = length($alignment[1]);

    # Return
    return ($alnlen, \@alignment_2D);
}

################################################################################
### aln2simArray                                                             ###
################################################################################
sub aln2simArray {
    my $aln = shift; # ALN Alignment File

    open ALN, "$aln";
    my @lines = <ALN>;
    close ALN;

    my @newlines;
    foreach my $line (@lines) {
	if (($line !~ /^CLUSTAL/) && ($line !~ /^\n$/)) {
	    push @newlines, $line;
	}
    }

    @lines = @newlines;
    my $txt = "";
    for (my $i = 2; $i < @lines; $i += 3) {
	substr($lines[$i],0,36) = "";
	chomp $lines[$i];
	$txt .= $lines[$i];
    }

    my @array = ("");
    for (my $i = 0; $i < length($txt); $i++) {
	push @array, substr($txt,$i,1);
    }

    return (\@array);
}

################################################################################
### condenseAlignToTarget                                                    ###
################################################################################
sub condenseAlignToTarget {
    my @alignment = @{$_[0]}; # The alignment to condense
    my $alnlen    =   $_[1];  # The length of the input alignment
    my $target    =   $_[2];  # The target sequence (1 or 2)

    # New alignment:
    # Sequences: ($i = 1; $i <= 2; $i++)
    # Positions: ($j = 1; $j <= length(target seq); $j++)
    my @newalign; # Condensed Alignment
    my $rn = 0;   # Residue Number

    # For each alignment position
    for (my $j = 1; $j <= $alnlen; $j++) {

	# Target sequence at this alignment position
	my $tgtres = $alignment[$target][$j];

	# If target at this alignment position is NOT a gap
	if ($tgtres !~ /-/) {
	    $rn++;

	    # For each sequence # We go to $i = 3 because the sim markings are in this position
	    for (my $i = 1; $i <= 3; $i++) {
		$newalign[$i][$rn] = $alignment[$i][$j];
	    }
	}
    }
    
    # Alignment length = length of target sequence
    my $newalnlen = $rn;

    # Return (new alignment length, new 1D alignment array, new 2D alignment array, map)
    return ($newalnlen, \@newalign);
}

############################################################
### Help                                                 ###
############################################################

sub help {

    my $help = "
Program:
 :: SequenceIdentity.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: SequenceIdentity.pl -m1 {mfta} -m2 {mfta}

Input:
 :: -m1 :: MFTA File
 :: Corresponds to first sequence.

 :: -m2 :: MFTA File
 :: Corresponds to second sequence.

 :: -h | --help        :: No Input
 :: Displays this help message.

Description:
 :: Performs sequence alignment of the two provided
 :: sequences.  Calculates sequence identity and
 :: sequence similarity.
 ::
 :: There are three values reported for each
 :: calculation based on the three alignments used.
 ::
 :: 1) Alignment 1: Condensed alignment where there are
 ::    no gaps in Sequence 1.
 :: 2) Alignment 2: Condensed alignment where there are
 ::    no gaps in Sequence 2.
 :: 3) Alignment 3: Normal alignment.
 ::
 :: All numerical values are printed out to text and csv
 :: files with the name {m1}.{m2}.txt/csv.

";

    die "$help";
}
