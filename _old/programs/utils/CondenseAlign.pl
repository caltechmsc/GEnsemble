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

$target = 1;

GetOptions ('h|help'          => \$help,
	    'a|alignment=s'   => \$alignment,
	    'k|keywords=s'    => \$seq_keys,
	    'm|mfta=s'        => \$mfta,
	    't|target=i'      => \$target,
	    'o|out=s'         => \$prefix);

if ($help) { help(); }
$target--;

#
# Two modes of operation:
# * Condense Alignment, and/or
# * Percent Identities
#
# Condense Alignment requires:
# 1) Alignment File
# 2) Keywords
#
# Percent Identities requires:
# 1) Alignment File
# 2) MFTA File

# Must have an alignment file
if (! $alignment) {
    die "MultiAlignTool :: Alignment file not specified!\n".
	"               :: Use -h for help.\n\n";
}
if (! -e $alignment) {
    die "MultiAlignTool :: Alignment file not found! :: $alignment\n".
	"               :: Use -h for help.\n\n";
}
if    ($alignment =~ /.aln$/)    { $alntype = "aln"; }
elsif ($alignment =~ /.pir$/)    { $alntype = "pir"; }
else {
    die "MultiAlignTool :: Alignment file type not recognized as\n".
	"               :: either ALN or PIR.  Use -h for help.\n\n";
}

# Must have keywords or mfta file
if ((!$seq_keys) && (!$mfta)) {
    die "MultiAlignTool :: Must specify either keywords (-k) or mfta\n".
	"               :: file (-m) or both.  Use -h for help.\n\n";
}

if ($mfta) {
    if (! -e $mfta) {
	die "MultiAlignTool :: MFTA file not found! :: $mfta\n".
	    "               :: Use -h for help.\n\n";
    }
}

if (! $prefix) {
    $prefix = $alignment;
    $prefix =~ s/.aln$//;
    $prefix =~ s/.pir$//;
    $prefix =~ s/.txt$//;
    $prefix .= ".condensed";
}
if ($prefix =~ /.pir$/) {
    $prefix =~ s/.pir$//;
}
if ($prefix =~ /.aln$/) {
    $prefix =~ s/.aln$//;
}
if ($prefix =~ /.txt$/) {
    $prefix =~ s/.txt$//;
}
$prefix2 = $prefix;
$prifix2 =~ s/.condensed//;

###
### Main Routine
###

my $numseq, $alnlength;
my @headers, @alignment, @aln, @matches;
parseAlignment();
if ($numseq < $target) {
    die "MultiAlignTool :: Target sequence ($target) outside of\n".
	"               :: sequence range: 0 <= target < $numseq.\n";
}
if ($seq_keys) {
    identifyKeys();
    condenseAlignment();
}
if ($mfta) {
    sequenceIdentity();
}

print "Output Files\n";
if ($seq_keys) {
    print
	" :: $prefix.aln\n".
	" :: $prefix.pir\n".
	" :: $prefix.map.csv\n";
}
if ($mfta) {
    for ($tmtype = 1; $tmtype <= 4; $tmtype++) {
	if ($tms{1}{$tmtype}{start} =~ /\d+/) {
	    print " :: ${prefix2}.$tmtypes[$tmtype].full.ident.csv\n";
	    print " :: ${prefix2}.$tmtypes[$tmtype].full.ident.txt\n";
	    if ($seq_keys) {
		print " :: ${prefix2}.$tmtypes[$tmtype].part.ident.csv\n";
		print " :: ${prefix2}.$tmtypes[$tmtype].part.ident.txt\n";
	    }
	}
    }
}

###
### Parse Alignment
###

sub parseAlignment {
    open ALN, "$alignment";
    @lines = <ALN>;
    close ALN;

    # Read in the alignment in string form
    if ($alntype eq "aln") {
	# Remove header info
	if ($lines[0] =~ /CLUSTAL W/) {
	    shift @lines;
	}
	while ($lines[0] !~ /^\S/) {
	    shift @lines;
	}

	# Find out the number of sequences
	$i = 0;
	$maxhdrlen = 0;
	while ($lines[$i] =~ /^\S/) {
	    $line = $lines[$i];
	    chomp $line;
	    $line =~ /^(\S+)\s+(\S+)/;
	    $headers[$i] = $1;
	    if (length($headers[$i]) > $maxhdrlen) {
		$maxhdrlen = length($headers[$i]);
	    }
	    $i++;
	}
	$numseq = $i;

	# Read the alignment
	$i = 0;
	foreach $line (@lines) {
	    chomp $line;
	    if ($line =~ /^(\S+)\s+(\S+)/) {
		$alignment[$i] .= $2;
		$i++;
	    }
	    if ($i == $numseq) { $i = 0; }
	}

    } elsif ($alntype eq "pir") {
	# Split into individual sequences
	$numseq = 0;
	foreach $line (@lines) {
	    chomp $line;

	    # Read headers
	    if ($line =~ /^\>/) {
		$line =~ /^(\S+)/;
		$headers[$numseq] = $1;
		$headers[$numseq] =~ s/^\>P1;//;
		if (length($headers[$numseq]) > $maxhdrlen) {
		    $maxhdrlen = length($headers[$numseq]);
		}

	    # Read alignment
	    } elsif ($line =~ /^[ABCDEFGHIJKLMNOPQRSTUVWXYZ-]/) {
		$alignment[$numseq] .= $line;

	    # Update number of sequences
	    } elsif ($line =~ /^\*/) {
		$numseq++;
	    }
	}

    }

    # Parse the alignment into arrays
    $alnlength = length($alignment[0]);
    for ($i = 0; $i < $numseq; $i++) {
	for ($j = 0; $j < $alnlength; $j++) {
	    $aln[$i][$j] = substr($alignment[$i], $j, 1);
	}
    }

}

###
### Identify Keywords
###

sub identifyKeys {
    @keys = split(/ /,$seq_keys);
    for ($i = 0; $i < @keys; $i++) {
	$tmpky = $keys[$i];
	$keys[$i] =~ s/\*/\.\*/;
	$printkey{$keys[$i]} = $tmpky;
    }

    $keylength = 0;
    foreach $key (@keys) {
	if ($keylength < length($printkey{$key})) {
	    $keylength = length($printkey{$key});
	}
    }

    for ($i = 0; $i < $numseq; $i++) {
	# Check for match
	$matched_true = 0;
	foreach $key (@keys) {
	    if ($headers[$i] =~ /$key/) {
		$matched{$key} += 1;
		$matched_true   = 1;
	    }
	}

	# Log the sequence that matches
	if ($matched_true) {
	    push @matches, $i;
	}
    }

    # Make sure that the target is the first in the list
    foreach $match (@matches) {
	if ($match != $target) {
	    push @tmp_matches, $match;
	}
    }
    undef @matches;
    @matches = @tmp_matches;
    unshift @matches, $target;

    print "Keywords/Sequences to Find :: Number of Matches\n";
    foreach $key (@keys) {
	printf " :: %-${keylength}s :: %3d\n", $key, $matched{$key};
    }
    print "\n";
}

###
### Sequence Identity
###

sub sequenceIdentity {

    print "Calculating Sequence Identities\n";

    # Condense Alignment based on target sequence
    $resnum = 0;
    for ($j = 0; $j < $alnlength; $j++) {

	# If target does not have a gap here
	if ("$aln[$target][$j]" ne "-") {
	    $resnum++;

	    # Keep this column of the alignment
	    for ($i = 0; $i < $numseq; $i++) {
		$aln_seqid[$i][$resnum] = $aln[$i][$j];
	    }
	}
    }
    $alnlength_seqid = $resnum;

    # Read info from MFTA file
    open MFTA, "$mfta";
    $numtms = 0;
    while (<MFTA>) {
	if (/(\d+)tm\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)/) {
	    $tms{$1}{1}{start}  = $2;
	    $tms{$1}{1}{stop}   = $3;
	    $tms{$1}{2}{start}  = $4;
	    $tms{$1}{2}{stop}   = $5;
	    $tms{$1}{3}{start} = $6;
	    $tms{$1}{3}{stop}  = $7;
	    $tms{$1}{4}{start} = $8;
	    $tms{$1}{4}{stop}  = $9;
	    $numtms++;
	}
    }
    close MFTA;

    # Calculate values for each sequence
    for ($i = 0; $i < $numseq; $i++) {

	# Calculate full-sequence percent identity
	$identical = 0;
	$residues  = 0;
	for ($j = 1; $j <= $alnlength_seqid; $j++) {
	    if ("$aln_seqid[$target][$j]" eq "$aln_seqid[$i][$j]") { $identical++; }
	    $residues++;
	}
	$pct_ident{$i}{all} = ($identical / $residues) * 100;

	# Calculate raw-pred/cap-pred/raw-man/cap-man per-tm percent identity
	for ($tmtype = 1; $tmtype <= 4; $tmtype++) {
	    if ($tms{1}{$tmtype}{start} =~ /\d+/) {
		$tms_avg = 0;
		for ($tm = 1; $tm <= $numtms; $tm++) {
		    $identical = 0;
		    $residues  = 0;
		    
		    for ($j = $tms{$tm}{$tmtype}{start}; $j <= $tms{$tm}{$tmtype}{stop}; $j++) {
			if ("$aln_seqid[$target][$j]" eq "$aln_seqid[$i][$j]") { $identical++; }
			$residues++;
		    }
		    $tms_ident{$i}{$tm}{$tmtype} = ($identical / $residues) * 100;
		    $tms_avg += $tms_ident{$i}{$tm}{$tmtype};
		}
		$tms_ident{$i}{tmavg}{$tmtype} = $tms_avg / $numtms;
	    }
	}

    }

    @tmtypes = ("raw-pred","cap-pred","raw-manual","cap-manual");

    # Print Full Info
    for ($tmtype = 1; $tmtype <= 4; $tmtype++) {
	if ($tms{1}{$tmtype}{start} =~ /\d+/) {
	    open CSV,  ">${prefix2}.$tmtypes[$tmtype].full.ident.csv";
	    open TXT,  ">${prefix2}.$tmtypes[$tmtype].full.ident.txt";

	    print CSV "header,all,tm avg";
	    print TXT sprintf "%-${maxhdrlen}s %6s %6s", "header", "all", "tm avg";
	    for ($tm = 1; $tm <= $numtms; $tm++) {
		print CSV ",TM${tm}";
		print TXT sprintf " %6s", "TM${tm}";
	    }
	    print CSV "\n";
	    print TXT "\n";

	    for ($i = 0; $i < $numseq; $i++) {
		print CSV sprintf
		    "%s,%.2f,%.2f",
		    $headers[$i],
		    $pct_ident{$i}{all},
		    $tms_ident{$i}{tmavg}{$tmtype};
		print TXT sprintf 
		    "%-${maxhdrlen}s %6.2f %6.2f",
		    $headers[$i],
		    $pct_ident{$i}{all},
		    $tms_ident{$i}{tmavg}{$tmtype};

		for ($tm = 1; $tm <= $numtms; $tm++) {
		    print CSV sprintf ",%.2f",  $tms_ident{$i}{$tm}{$tmtype};
		    print TXT sprintf " %6.2f", $tms_ident{$i}{$tm}{$tmtype};
		}
		print CSV "\n";
		print TXT "\n";
	    }
	}
    }

    # Print Partial Info
    if ($seq_keys) {
	for ($tmtype = 1; $tmtype <= 4; $tmtype++) {
	    if ($tms{1}{$tmtype}{start} =~ /\d+/) {
		open CSV,  ">${prefix2}.$tmtypes[$tmtype].part.ident.csv";
		open TXT,  ">${prefix2}.$tmtypes[$tmtype].part.ident.txt";
		
		print CSV "header,all,tm avg";
		print TXT sprintf "%-${maxhdrlen}s %6s %6s", "header", "all", "tm avg";
		for ($tm = 1; $tm <= $numtms; $tm++) {
		    print CSV ",TM${tm}";
		    print TXT sprintf " %6s", "TM${tm}";
		}
		print CSV "\n";
		print TXT "\n";
		
		foreach $i (@matches) {
		    print CSV sprintf
			"%s,%.2f,%.2f",
			$headers[$i],
			$pct_ident{$i}{all},
			$tms_ident{$i}{tmavg}{$tmtype};
		    print TXT sprintf 
			"%-${maxhdrlen}s %6.2f %6.2f",
			$headers[$i],
			$pct_ident{$i}{all},
			$tms_ident{$i}{tmavg}{$tmtype};
		    
		    for ($tm = 1; $tm <= $numtms; $tm++) {
			print CSV sprintf ",%.2f",  $tms_ident{$i}{$tm}{$tmtype};
			print TXT sprintf " %6.2f", $tms_ident{$i}{$tm}{$tmtype};
		    }
		    print CSV "\n";
		    print TXT "\n";
		}
	    }
	}
    }

}

###
### Condense Alignment
###

sub condenseAlignment {

    print "Condensing Alignment\n";

    # Mark columns to keep
    foreach $i (@matches) {
	for ($j = 0; $j < $alnlength; $j++) {
	    if ("$aln[$i][$j]" ne "-") {
		$keep[$j] = 1;
	    }
	}
    }

    # Condense alignment
    foreach $i (@matches) {
	$resnum = 0;
	$alnnum = -1;

	# Go through the full alignment
	for ($j = 0; $j < $alnlength; $j++) {

	    # If this column is to be kept
	    if ($keep[$j]) {

		$alnnum++;

		# Keep track of the new alignment
		$condensed[$i][$alnnum] = $aln[$i][$j];

		# Make a map of the residues and resnums
		if ($aln[$i][$j] ne "-") {
		    $resnum++;
		    $map_rn[$i][$alnnum] = $resnum;
		    $map_aa[$i][$alnnum] = $aln[$i][$j];
		} else {
		    $map_rn[$i][$alnnum] = ".";
		    $map_aa[$i][$alnnum] = ".";
		}

		$condlength = $alnnum;
	    }
	}
    }

    # Split condensed alignment into 60 character lines
    undef @lines;
    foreach $i (@matches) {
	$linenum = -1;
	
	for ($j = 0; $j < $condlength; $j++) {
	    if (($j % 60) == 0) { $linenum++; }
	    $lines[$i][$linenum] .= $condensed[$i][$j];
	}
    }

    # Print PIR
    open PIR, ">$prefix.pir";
    foreach $i (@matches) {
	print PIR ">$headers[$i]\n\n";
	for ($ln = 0; $ln <= $linenum; $ln++) {
	    print PIR "$lines[$i][$ln]\n";
	}
	print PIR "*\n";
    }
    close PIR;

    # Print ALN
    $clustal = "/project/Biogroup/Software/GEnsemble/programs/thirdparty/clustal/clustalw";
    `$clustal -infile=${prefix}.pir -convert -outfile=${prefix}.aln`;

    # Print MAP
    open CSV, ">$prefix.map.csv";
    foreach $i (@matches) {
	print CSV "$headers[$i],$headers[$i],";
    }
    print CSV "\n";

    for ($j = 0; $j < $condlength; $j++) {
	foreach $i (@matches) {
	    print CSV "$map_aa[$i][$j],$map_rn[$i][$j],";
	}
	print CSV "\n";
    }
    close CSV;
}

sub help {

    my $help = "
Program:
 :: MultiAlignTool.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: MultiAlignTool.pl -a {alignment file} -k {keywords}
 ::                   -m {mfta file} -o {output prefix}
 ::                   -t {target sequence number}

Input:
 :: -a | --alignment   :: Filename
 :: Either an ALN or PIR multiple sequence alignment file
 :: with corresponding file extension (.aln or .pir).

 :: -k | --keywords    :: String
 :: Keywords to identify the sequences to be kept in the
 :: condensed alignment.  The first sequence in the
 :: alignment will always be kept.  Other sequences can
 :: be kept by using a unique identifier.  When multiple
 :: keywords are used, they should be put in single
 :: quotes and separated by spaces.  Note that anything
 :: other than spaces will be considered part of a
 :: keyword.  In other words, don't use commas or
 :: semicolons, etc., if you want things to work.
 :: Examples ::
 ::
 :: * Identifying sequences based on Swiss-Prot ID:
 ::   This grabs ADRB2_HUMAN, ADRB1_HUMAN, AA2AR_HUMAN,
 ::   and OPSD_BOVIN.
 ::
 ::   -s 'P07550 P08588 P29274 P02699'
 ::
 :: * Identifying sequences based on protein type:
 ::   This grabs all ADRB2 proteins regardless of species.
 ::
 ::   -s 'ADRB2'
 ::
 :: * Identifying using species:
 ::   -s 'HUMAN'
 ::
 :: * Using a wildcard (\*): Note that keywords including
 ::   a wildcard must always be in quotes, even if there
 ::   is only one keyword being used.
 ::   This will grab ADRB1_HUMAN, ADRB2_HUMAN, and ADRB3_HUMAN
 ::
 ::   -s 'ADR\*_HUMAN'
 ::
 :: * Identifying using mixed keywords:
 ::   -s 'DRD\* ADR\*_HUMAN P02699'

 :: -m | --mfta        :: Filename
 :: MFTA file containing TM information for percent identity
 :: calculations based on the multiple sequence alignment.

 :: -t | --target      :: Integer
 :: If the target sequence isn't the first in the alignment
 :: then specify the correct number in the alignment here.

 :: -o | --out         :: Filename Prefix
 :: Filename prefix for the two output files.  The files
 :: will be named {prefix}.aln and {prefix}.pir.

 :: -h | --help        :: No Input
 :: Displays this help message.

Description:
 :: MultiAlignTool allows you to quickly take a multiple
 :: sequence alignment file with thousands of sequences
 :: and condense it down to a handful of relevant sequences.
 ::
 :: Any sequence alignment in the PIR or ALN input file that
 :: matches at least one of the keywords will be kept.  All
 :: other sequences are discarded.
 ::
 :: Once the matching sequences have been extracted, all
 :: 100% conserved gap positions will be removed from the
 :: alignments, leaving only alignment positions with at
 :: least one non-gap amino acid.
 ::
 :: The resulting condensed alignment is the output to both
 :: PIR and ALN output files.
 ::
 :: Additionally, when a MFTA file is provided with TM
 :: start/stop information, the program will calculate
 :: percent identity values for the TMs based on the
 :: multiple sequence alignment.  The value is calculated
 :: using the formula:
 ::
 ::   # identical matches / length of TM
 ::
 :: or
 ::
 ::   # identical matches / length of target sequence
 ::
 :: The sequence identities can be calculated without
 :: condensing the alignment if the -k option is not
 :: used.  Similarly, without using the -m option, no
 :: percent identities will not be calculated.

Usage:
 :: MultiAlignTool.pl -a {alignment file} -k {keywords}
 ::                   -m {mfta file} -o {output prefix}
 ::                   -t {target sequence number}

";

    die "$help";
}
