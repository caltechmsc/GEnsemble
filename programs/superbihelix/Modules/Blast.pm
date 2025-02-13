package Modules::Blast;

my $copyright = "
#####################################################################
#                                                                   #
# PredicTM.pl/PredicTM.pm/Blast.pl/Blast.pm/Clustal.pm/Mafft.pm     #
#                                                                   #
# Copyright (c) 2008                                                #
# Adam R. Griffith, Ravinder Abrol, and William A. Goddard III      #
# Materials and Process Simulation Center                           #
# California Institute of Technology                                #
# Pasadena, CA, USA                                                 #
# All Rights Reserved.                                              #
#                                                                   #
# Uses BLAST:                                                       #
# Altschul S.F., Madden T.L., Schaffer A.A., Zhang J., Zhang Z.,    #
# Miller W., Lipman D.J.  Gapped BLAST and PSI-BLAST: a new         #
# generation of protein database search programs. (1997)            #
# _Nucleic Acids Res_ 25:3389-3402.                                 #
#                                                                   #
# BLAST is performed at the SIB using the BLAST network service.    #
# The SIB BLAST network service uses a server developed at SIB and  #
# the NCBI BLAST 2 software.                                        #
#                                                                   #
# Uses the GPCRDB when flagging of cutting potential non-GPCR       #
# sequences: http://www.gpcr.org/7tm/htmls/entries.html             #
#                                                                   #
# Uses libwww-perl-5.808 from the Comprehensive Perl Archive        #
# Network (CPAN).                                                   #
# libwww-perl (c) 1995-2005 Gisle Aas. All rights reserved.         #
# libwww-perl (c) 1995 Martijn Koster. All rights reserved.         #
#                                                                   #
# Uses ClustalW 1.83:                                               #
# Chenna, et al. \"Multiple sequence alignment with the Clustal      #
# series of programs.\" (2003)                                       #
# _Nucleic Acids Res_ 31 (13):3497-500 PubMedID: 12824352           #
#                                                                   #
# Uses MAFFT 6.240:                                                 #
# MAFFT v6.240 (2007/04/04)  Copyright (c) 2006 Kazutaka Katoh      #
# http://align.bmr.kyushu-u.ac.jp/mafft/software/                   #
# NAR 30:3059-3066, NAR 33:511-518                                  #
#                                                                   #
#####################################################################

";

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
    push @INC, "$Bin/thirdparty/libwww/";
}

use strict;
use warnings;
use base 'Exporter';

use Cwd;
use File::Copy;
use File::Path;
use LWP::Simple;
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

use Modules::Clustal;

our $VERSION = 1.25;
our @EXPORT  = qw(blast
		  help
		  checkVersion);

# Global Input Variables
our ($accession, $fasta, $raw, $protdb, $ethreshold, $compiter, $maxseqs, $sequences, $name,
     $prefix, $complete, $flagnongpcr, $help, $filter, $trembl, $cutnongpcr,
     $clustal_executable, $mafft_executable, $mafft_binaries, $quiet, $print_copyright1,
     $print_copyright2);

# Global Internal Variables
our ($blastinput, $run, $fastaprint, $rawprint, $html, $xml, $curated, $filteron, @results,
     @evalues, @fastas, @seqids, $fnpfx, $round, $numhits, $htmllink, $sequence);

################################################################################
##### Version Check                                                        #####
################################################################################
sub checkVersion { return $VERSION; }

################################################################################
##### Main Routine                                                         #####
################################################################################
sub blast {
    # Load Input
    (my $printstring,
     $accession,
     $fasta,
     $raw,
     $protdb,
     $ethreshold,
     $sequences,
     $compiter,
     $maxseqs,
     $name,
     $prefix,
     $complete,
     $flagnongpcr,
     $cutnongpcr,
     $filter,
     $trembl,
     $help,
     $quiet,
     $print_copyright1,
     $print_copyright2,
     $clustal_executable,
     $mafft_executable,
     $mafft_binaries) = @_;

    # Check Help Conditions
    if ($help) { help(); }

    # Check Input
    checkInput();

    # Set up filename
    if ($name) {
	$fnpfx = $name;
    } elsif ($accession && $prefix) {
	$fnpfx = "$prefix" . "." . "$accession";
    } elsif ($accession && !$prefix) {
	$fnpfx = "$accession";
    } elsif (($fasta || $raw) && $prefix) {
	$fnpfx = "$prefix";
    } elsif (($fasta || $raw) && !$prefix) {
	$fnpfx = "blast";
    }

    # Open Output File
    open LOG, ">${fnpfx}.log";
    if ($print_copyright1) { printDuo($copyright, 0); }
    printDuo($printstring, $quiet);

    $printstring =
	"\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\n".
	"\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@ Running Blast v$VERSION \@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\n".
	"\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\@\n\n";
    printDuo($printstring, 0);

    # Print Program Parameters
    $printstring = 
	"Blast :: Running With the Following Parameters ::\n".
	" :: Protein Database                 :: $protdb\n".
	" :: E-Threshold                      :: $ethreshold\n".
	" :: Sequences                        :: $sequences\n".
	" :: Completeness Step                :: $compiter\n".
	" :: Maximum Sequences                :: $maxseqs\n";

    if ($complete)    { $printstring .= " :: Find Completeness                :: Yes\n"; }
    else              { $printstring .= " :: Find Completeness                :: No\n";  }
    if ($flagnongpcr) { $printstring .= " :: Flag Possible Non-GPCRs          :: Yes\n"; }
    else              { $printstring .= " :: Flag Possible Non-GPCRs          :: No\n";  }
    if ($cutnongpcr)  { $printstring .= " :: Cut Possible Non-GPCRs           :: Yes\n"; }
    else              { $printstring .= " :: Cut Possible Non-GPCRs           :: No\n";  }
    if ($filter)      { $printstring .= " :: Use Low-Complexity Region Filter :: Yes\n"; }
    else              { $printstring .= " :: Use Low-Complexity Region Filter :: No\n";  }
    if ($trembl)      { $printstring .= " :: Include TrEMBL Sequences         :: Yes\n"; }
    else              { $printstring .= " :: Include TrEMBL Sequences         :: No\n";  }

    $printstring .= "\n";

    printDuo($printstring, $quiet);

    # Convert input to something that we can give BLAST
    convertInput();

    # Print Settings Info
    printSettings();

    # While completeness has not been obtained
    $run = 1; $round = 1;
    while ($run) {
	if ($complete) {
	    printDuo("Round $round Results ::\n", 0);
	} else {
	    printDuo("Results ::\n", 0);
	    $run = 0;
	}
	
	# Load BLAST HTML
	loadBLAST();

	# Parse Sequences
	my $skip_to_end = parseBLAST();
	
	if ($skip_to_end) {
	    # Print Filter Info
	    if ($filter) {
		printDuo(" :: Low Complexity Region Filter  ::\n");
		while (length($htmllink) > 0) {
		    if (length($htmllink) > 60) {
			printDuo(" :: " . substr($htmllink,0,60) . "\n");
			substr($htmllink,0,60) = "";
		    } else {
			printDuo(" :: " . $htmllink . "\n");
			$htmllink = "";
		    }
		}
	    }
	    
	    if ($print_copyright2) { printDuo($copyright, 0); } else { printDuo("\n", 0); }
	    
	    close LOG;
	    return "$fnpfx";
	}

	# Check Completeness
	checkCompleteness();
    }

    # Flag or Cut Non-GPCRs
    if ($flagnongpcr || $cutnongpcr) {
	flagCutNonGPCR();
    }

    # Load FASTA Sequences
    loadFASTAs();

    # Make sure that target sequence is first sequence
    setTargetOnTop();

    # Calculate Sequence Identities
    calcSeqIds();

    # Output Files
    writeOutput();

    # Print Filter Info
    if ($filter) {
	printDuo(" :: Low Complexity Region Filter  ::\n");
	while (length($htmllink) > 0) {
	    if (length($htmllink) > 60) {
		printDuo(" :: " . substr($htmllink,0,60) . "\n");
		substr($htmllink,0,60) = "";
	    } else {
		printDuo(" :: " . $htmllink . "\n");
		$htmllink = "";
	    }
	}
    }

    if ($print_copyright2) { printDuo($copyright, 0); } else { printDuo("\n", 0); }

    close LOG;
    return "$fnpfx";
}

################################################################################
##### Check Input                                                          #####
################################################################################
sub checkInput {
    if (!$accession && !$fasta && !$raw) {
	die "Blast :: Sequence input not provided.  Must specify either an\n".
	    "      :: accession number, a single-sequence FASTA file, or a\n".
	    "      :: raw amino acid sequence.  Use \"Blast.pl -h\" for help.\n\n";
    }

    if (($accession && $fasta) ||
	($accession && $raw)   ||
	($fasta     && $raw)) {
	die "Blast :: Multiple sequence input provided.  Can only use one\n".
	    "      :: sequence input at a time.  Use \"Blast.pl -h\" for help.\n\n";
    }

    if (($fasta) && (! -e $fasta)) {
	die "Blast :: Could not locate FASTA file :: $fasta\n".
	    "      :: Use \"Blast.pl -h\" for help.\n\n";
    }

    if (($raw) && $raw =~ /[B,J,O,U,X,Z,\d]/) {
	die "Blast :: Nonstandard amino acid found in RAW input.\n".
	    "      :: Use \"Blast.pl -h\" for help.\n\n";
    }

    if ($protdb !~ /[Bacteria_Archaea,Bacteria,Archaea,Viruses,Eukaryota,Viridiplantae,Fungi,Metazoa,Arthropoda,Vertebrata,Mammalia,Rodentia,Primates,Microbial_proteomes,Mitochondrion,ARATH,CAEEL,DROME,ECOLI,HUMAN,MOUSE,RAT,YEAST,SCHPO,PLAFA,Complete]/) {
	die "Blast :: $protdb is not one of the recognized databases.\n".
	    "      :: The following databases are available:\n".
	    "      :: Bacteria_Archaea, Bacteria, Archaea,V iruses, Eukaryota,\n".
	    "      :: Viridiplantae, Fungi, Metazoa, Arthropoda, Vertebrata,\n".
	    "      :: Mammalia, Rodentia, Primates, Microbial_proteomes,\n".
	    "      :: Mitochondrion, ARATH, CAEEL, DROME, ECOLI, HUMAN, MOUSE,\n".
	    "      :: RAT, YEAST, SCHPO, PLAFA, and Complete.\n".
	    "      :: Use \"Blast.pl -h\" for help.\n\n";
    }

    if (($ethreshold !~ /^10*(\.0+)?$/) &&
	($ethreshold !~ /^0*\.0*1$/)) {
	die "Blast :: The E-Value Threshold given ($ethreshold) is not valid.\n".
	    "      :: Must be a power of 10.  Use \"Blast.pl -h\" for help.\n\n";
    }

    if ($compiter !~ /^\d+$/) {
	die "Blast :: The given completeness step size ($compiter) is not valid.\n".
	    "      :: Use \"Blast.pl -h\" for help.\n\n";
    }

    if ($maxseqs !~ /^\d+$/) {
	die "Blast :: The given maximum number of sequences ($maxseqs) is not valid.\n".
	    "      :: Use \"Blast.pl -h\" for help.\n\n";
    }

    if ($sequences !~ /^\d+$/) {
	die "Blast :: The given number of target sequences ($sequences) is not valid.\n".
	    "      :: Use \"Blast.pl -h\" for help.\n\n";
    }

    if (! -e "${Bin}/$clustal_executable") {
	die "Blast :: Could not locate ClustalW executable.  Was expected to be\n".
	    "      :: found here :: ${Bin}/$clustal_executable\n\n";
    }

    if (! -e "${Bin}/$mafft_executable") {
	die "Blast :: Could not locate MAFFT executable.  Was expected to be\n".
	    "      :: found here :: ${Bin}/$mafft_executable\n\n";
    }

    if (! -e "${Bin}/$mafft_binaries") {
	die "Blast :: Could not locate MAFFT binaries.  Was expected to be\n".
	    "      :: found here :: ${Bin}/$mafft_binaries\n\n";
    }

}

################################################################################
##### Convert Input to BLAST Readable Format                               #####
################################################################################
sub convertInput {
    if ($accession) {
	$blastinput = $accession;

    } elsif ($fasta) {
	open FTA, "$fasta";
	while (<FTA>) {
	    chomp;
	    if (!/^\>/) {
		$blastinput .= "$_";
	    }
	}
	close FTA;

    } elsif ($raw) {
	$blastinput = $raw;
    }
}

################################################################################
##### Print Settings                                                       #####
################################################################################
sub printSettings {
    my $printstring =
	"Performing BLAST Search ::\n".
	" :: Date                   :: ".localtime()."\n".
	" :: Database               :: $protdb\n";

    if ($trembl) {
	$printstring .=
	    " :: Include TrEMBL         :: Yes\n";
    } else {
	$printstring .=
	    " :: Include TrEMBL         :: No\n";
    }

    $printstring .=
	" :: E-Threshold            :: $ethreshold\n";

    if ($filter) {
	$printstring .=
	    " :: Filter Low Complexity  :: Yes\n";
    } else {
	$printstring .=
	    " :: Filter Low Complexity  :: No\n";
    }

    if ($accession) {
	$printstring .=
	    " :: Accession Number Input :: $accession\n";
	my $accstring = 
	    "http://www.expasy.org/cgi-bin/get-sprot-raw-list.pl?AC=$accession&format=1";
	undef my $tmp;
	$tmp = get $accstring;
	$sequence = $tmp;
	die "Blast.pl :: Could not load FASTA sequence.\n" unless defined $tmp;
	my @tmps = split(/\n/, $tmp); shift @tmps;
	$tmp = "";
	foreach (@tmps) { $tmp .= "$_"; }
	
	$fastaprint = "$tmp";
	while (length($fastaprint) > 0) {
	    if (length($fastaprint) > 60) {
		$printstring .= " :: " . substr($fastaprint,0,60) . "\n";
		substr($fastaprint,0,60) = "";
	    } else {
		$printstring .= " :: $fastaprint\n\n";
		$fastaprint = "";
	    }
	}
	
    } elsif ($fasta) {
	$printstring .=
	    " :: FASTA File Input       :: $fasta\n";

	$fastaprint = "$blastinput";
	while (length($fastaprint) > 0) {
	    if (length($fastaprint) > 60) {
		$printstring .= " :: " . substr($fastaprint,0,60) . "\n";
		substr($fastaprint,0,60) = "";
	    } else {
		$printstring .= " :: $fastaprint\n\n";
		$fastaprint = "";
	    }
	}
    } elsif ($raw) {
	$printstring .=
	    " :: User RAW Input     ::\n";

	$fastaprint = "$blastinput";
	while (length($fastaprint) > 0) {
	    if (length($fastaprint) > 60) {
		$printstring .= " :: " . substr($fastaprint,0,60) . "\n";
		substr($fastaprint,0,60) = "";
	    } else {
		$printstring .= " :: $fastaprint\n\n";
		$fastaprint = "";
	    }
	}
    }

    printDuo($printstring, 0);
}

################################################################################
##### Run BLAST at http://www.expasy.org/cgi-bin/blast.pl and get HTML/XML #####
################################################################################
sub loadBLAST {
    undef $html; undef $xml; undef $htmllink;

    if ($protdb eq "Complete") { $protdb = ""; }
    if ($trembl) {
	$curated = "";
    } else {
	$curated = "&curated=on";
    }
    if ($filter) {
	$filteron = "T";
    } else {
	$filteron = "F";
    }

    my $url =
 	"http://www.expasy.org/cgi-bin/blast.pl?" .
	"sequence=$blastinput" .
	"&action=Normal" .
	"&dbtype=UniProtKB" .
	"&protdb_section=$protdb" .
	"&Tax=" .
	"&protdb1=" .
	"$curated" .
	"&nofragment=on" .
	"&protdb=EXPASY%2F%2FUniRef100" .
	"&nucltype=embl-sp" .
	"&nucldb=embl-sp" .
	"&nucldb1=" .
	"&email=" .
	"&matrix=auto" .
	"&showsc=$sequences" .
	"&showal=$sequences" .
	"&ethr=$ethreshold" .
	"&Filter=$filteron" .
	"&Gap=T";

    $htmllink = $url;

    $html = get $url;
    die "Blast :: Could not load BLAST HTML results.\n" unless defined $html;

    $url =
	"http://www.expasy.org/cgi-bin/blast.pl?" .
	"sequence=$blastinput" .
	"&action=Xml" .
	"&dbtype=UniProtKB" .
	"&protdb_section=$protdb" .
	"&Tax=" .
	"&protdb1=" .
	"$curated" .
	"&nofragment=on" .
	"&protdb=EXPASY%2F%2FUniRef100" .
	"&nucltype=embl-sp" .
	"&nucldb=embl-sp" .
	"&nucldb1=" .
	"&email=" .
	"&matrix=auto" .
	"&showsc=$sequences" .
	"&showal=$sequences" .
	"&ethr=$ethreshold" .
	"&Filter=$filteron" .
	"&Gap=T";

    $xml = get $url;
    die "Blast.pl :: Could not load BLAST XML results.\n" unless defined $xml;

    open HTML, ">${fnpfx}.html"; print HTML "$html"; close HTML;
    open XML,  ">${fnpfx}.xml";  print XML  "$xml";  close XML;

    if ($protdb eq "") { $protdb = "Complete"; }
}

################################################################################
##### Parse the BLAST XML Output                                           #####
################################################################################
sub parseBLAST {
    my $printstring;
    if ($xml =~ /no hits found/i) {
	$printstring = 
	    " :: WARNING :: No sequences returned by BLAST!\n".
	    " :: Note that this is not an error; BLAST simply did not\n".
	    " :: have any matching sequences for the given E-Value\n".
	    " :: threshold.  You may wish to re-run BLAST with a larger\n".
	    " :: E-Value threshold; however, the program will proceed\n".
	    " :: with just the target sequence.\n";

	if ($filter) {
	    $html =~ /of which (\d+)% low-complexity/;
	    my $pctfiltered = $1;
	    if (!$pctfiltered) { $pctfiltered = "0"; }
	    $printstring .=
		" :: Pct. of Sequence Filtered :: $pctfiltered \%\n";
	}

	if ($accession) {
	    chomp $sequence;
	    open FTA, ">${fnpfx}.fta";
	    print FTA "$sequence\n";
	    close FTA;

	} elsif ($fasta) {
	    open FTA, "$fasta";
	    my $tmp = "";
	    while (<FTA>) { $tmp .= "$_"; }
	    close FTA;
	    open FTA, ">${fnpfx}.fta";
	    print FTA "$tmp";
	    close FTA;

	} elsif ($raw) {
	    open FTA, ">${fnpfx}.fta";
	    print FTA ">User RAW Sequence\n";
	    while (length($blastinput) > 60) {
		print FTA substr($blastinput,0,60) . "\n";
		substr($blastinput,0,60) = "";
	    }
	    print FTA "$blastinput\n";
	    close FTA;
	}
	
	$printstring .= 
	    "\nOutput Files ::\n".
	    " :: BLAST Results FASTA File      :: ${fnpfx}.fta\n".
	    " :: BLAST HTML Output             :: ${fnpfx}.html\n".
	    " :: BLAST XML Output              :: ${fnpfx}.xml\n".
	    " :: Blast.pl Log File             :: ${fnpfx}.log\n";

	printDuo($printstring, 0);
	return 1;
	
    }

    my @hits = split(/<Hit>/, $xml); shift @hits;
    $numhits = @hits;

    my ($normal, $splice, $swissprot, $tremblctr, $maxev) = (0, 0, 0, 0, -1);

    foreach my $hit (@hits) {
	$hit =~ /<Hit_accession>(\S+)<\/Hit_accession>/;
	my $hit_long = $1;
	my $hit_an;
	my $not_splice;
	if ($hit_long =~ /\-/) {
	    $hit_an = $1;
	    $splice++;
	    $not_splice = 0;
	} elsif ($hit_long =~ /^tr!(\S+)\_/) {
	    $hit_an = $1;
	    $normal++;
	    $tremblctr++;
	    $not_splice = 1;
	} else {
	    $hit_long =~ /^sp\!(\S+)\!/;
	    $hit_an = $1;
	    $normal++;
	    $swissprot++;
	    $not_splice = 1;
	}

	$hit =~ /<Hsp_evalue>(\S+)<\/Hsp_evalue>/;
	my $hit_ev = $1;
	if ($hit_ev > $maxev) { $maxev = $hit_ev; }

	if ($not_splice) {
	    push @results, $hit_an;
	    push @evalues, $hit_ev;
	}
    }

    $printstring =
	" :: Number of Sequences Requested  :: $sequences\n".
	" :: Number of Sequences Returned   :: $numhits\n".
	" :: Number of Normal Sequences     :: $normal\n".
	" :: Number of Splice Sequences     :: $splice\n";
    if ($trembl) {
	$printstring .= 
	    " :: Number of Swiss-Prot Sequences :: $swissprot\n".
	    " :: Number of TrEMBL Sequences     :: $tremblctr\n";
    }
    $printstring .= 
	" :: Largest E-Value                :: $maxev\n";
    
    if ($filter) {
	$html =~ /of which (\d+)% low-complexity/;
	my $pctfiltered = $1;
	if (!$pctfiltered) { $pctfiltered = "0"; }
	$printstring .=
	    " :: Pct. of Sequence Filtered      :: $pctfiltered \%\n";
    }
    printDuo($printstring, 0);
    return 0;
}

################################################################################
##### Check to see if we've reached completeness                           #####
################################################################################
sub checkCompleteness {
    my $printstring;

    if ($complete) {
	if (($numhits == $sequences) && ($sequences < $maxseqs)) {
	    $printstring =
		" :: Completeness Not Obtained\n".
		" :: Increase Target By $compiter\n\n";
	    $sequences += $compiter;
	    $round++;

	    undef @results;
	    undef @evalues;
	    undef $html;
	    undef $xml;

	} elsif (($numhits == $sequences) && ($sequences >= $maxseqs)) {
	    $printstring =
		" :: Completeness Not Obtained\n".
		" :: Cannot Increase Target Further\n".
		" :: Proceeding With Current BLAST Results\n\n";
	    $run = 0;

	} else {
	    $printstring =
		" :: Completeness Obtained\n\n";
	    $run = 0;
	}
    } else {
	$printstring = "\n";
    }

    printDuo($printstring, 0);
}

################################################################################
##### Flag/Cut All Sequences that might not be GPCRs                       #####
################################################################################
sub flagCutNonGPCR {
    my $url = "http://www.gpcr.org/7tm/htmls/entries.html";
    my $db  = get "$url";
    die "Blast :: Could not load GPCR Listing :: $url\n" unless defined $db;

    my @dblines = split (/\<li\>/, $db);
    my $dblist  = "";
    my $incr    = 0;
    for (my $i = 0; $i < @dblines; $i++) {
	$dblines[$i] =~ /\&nbsp\;\((\S+)\)\&nbsp\;/;
	if ($1) { $dblist .= "$1\n"; $incr++; }
    }

    my @nongpcr_results;
    my @nongpcr_evalues;
    my @gpcr_results;
    my @gpcr_evalues;
    my $count = 0;

    while (@results) {
	my $result = shift @results;
	my $evalue = shift @evalues;

	if ($dblist !~ /$result/) {
	    if ($flagnongpcr) {
		push @nongpcr_results, $result;
		push @nongpcr_evalues, $evalue;
		push @gpcr_results, $result;
		push @gpcr_evalues, $evalue;
	    } elsif ($cutnongpcr) {
		push @nongpcr_results, $result;
		push @nongpcr_evalues, $evalue;
	    }
	    $count++;
	} else {
	    push @gpcr_results, $result;
	    push @gpcr_evalues, $evalue;
	}
    }

    undef @results; @results = @gpcr_results;
    undef @evalues; @evalues = @gpcr_evalues;

    if (@nongpcr_results > 0) {
	my $printstring = "";

	if ($flagnongpcr) {
	    $printstring .=
		"Potential Non-GPCRs ::\n".
		" :: The following $count sequences were flagged\n".
		" :: because it is possible that they are not GPCRs\n".
		" ::";
	} elsif ($cutnongpcr) {
	    $printstring .=
		"Potential Non-GPCRs ::\n".
		" :: The following $count sequences were cut\n".
		" :: because it is possible that they are not GPCRs\n".
		" ::";
	}
	
	my $iterator = 1;
	while (@nongpcr_results > 0) {
	    my $flag = shift (@nongpcr_results);
	    $printstring .= " $flag";
	    if ($iterator % 8 == 0) {
		$printstring .= "\n ::";
	    }
	    $iterator++;
	}
	$printstring .= "\n\n";
	printDuo($printstring, $quiet);
    }
}

################################################################################
##### Load the final FASTA results                                         #####
################################################################################
sub loadFASTAs {
    my @accnos = @results;
    my $fasta = "";
    while (@accnos > 200) {
	my $accstring = "http://www.expasy.org/cgi-bin/get-sprot-raw-list.pl?AC=$accnos[0]";
	shift @accnos;
	for (my $j = 0; $j < 199; $j++) {
	    $accstring .= "\|$accnos[0]";
	    shift @accnos;
	}
	$accstring .= "&format=1";
	undef my $tmp;
	$tmp = get $accstring;
	die "Blast.pl :: Could not load FASTA results.\n" unless defined $tmp;
	$fasta .= $tmp;
    }

    my $accstring = "http://www.expasy.org/cgi-bin/get-sprot-raw-list.pl?AC=$accnos[0]";
    for (my $j = 1; $j < @accnos; $j++) {
	$accstring .= "\|$accnos[$j]";
    }
    $accstring .= "&format=1";
    undef my $tmp;
    $tmp = get $accstring;
    die "Blast.pl :: Could not load FASTA results.\n" unless defined $tmp;
    $fasta .= $tmp;

    @fastas = split (/\n\>/, $fasta);
    $fastas[0] .= "\n";
    for (my $i = 1; $i < @fastas - 1; $i++) {
	$fastas[$i] = ">" . $fastas[$i] . "\n";
    }
    $fastas[$#fastas] = ">" . $fastas[$#fastas];
}

################################################################################
##### Ensure that the target sequence is the first in the FASTA output     #####
################################################################################
sub setTargetOnTop {
    if ($accession) {
	my @new_results; my @new_evalues; my @new_fastas;
	while (@results > 0) {
	    my $result = shift @results;
	    my $evalue = shift @evalues;
	    my $fastax = shift @fastas;

	    if ($result =~ /$accession/) {
		unshift @new_results, $result;
		push    @new_results, @results;
		undef   @results;

		unshift @new_evalues, $evalue;
		push    @new_evalues, @evalues;
		undef   @evalues;

		unshift @new_fastas,  $fastax;
		push    @new_fastas,  @fastas;
		undef   @fastas;
	    } else {
		push @new_results, $result;
		push @new_evalues, $evalue;
		push @new_fastas,  $fastax;
	    }
	}
	@results = @new_results;
	@evalues = @new_evalues;
	@fastas  = @new_fastas;
    } elsif ($fasta) {
	my $identical_match = -1;
	my $sequence_match  = -1;
	my $partial_match   = -1;

	my $full_fasta_text = "";
	open FTA, "$fasta"; while (<FTA>) { $full_fasta_text .= "$_"; }; close FTA;

	for (my $i = 0; $i < @results; $i++) {
	    my $fastaraw = "";
	    my @fastaraws = split(/\n/,$fastas[$i]); shift @fastaraws;
	    foreach (@fastaraws) { $fastaraw .= "$_"; }

	    if (($fastas[$i] eq $full_fasta_text) && ($identical_match == -1)) {
		$identical_match = $i;
	    }
	    if (($fastaraw eq $blastinput)        && ($sequence_match == -1)) {
		$sequence_match = $i;
	    }
	    if (($fastaraw =~ /$blastinput/)      && ($partial_match == -1)) {
		$partial_match = $i;
	    }
	}

	my $put_on_top;
	if ($identical_match != -1) {
	    $put_on_top = $identical_match;
	    $sequence_match = -1;
	    $partial_match  = -1;
	} elsif ($sequence_match != -1) {
	    $put_on_top = $sequence_match;
	    $partial_match = -1;
	} elsif ($partial_match != -1) {
	    $put_on_top = $partial_match;
	} else {
	    $put_on_top = -1;
	}

	# If $put_on_top == -1, then the target sequence did not have any full or
	#    partial sequence matches, therefore it should be prepended to the results
	# If $put_on_top == 0 && ($identical_match || $sequence_match), then the target
	#    is the first result in the list and nothing needs to be changed
	# If $put_on_top == 0 && $partial_match, then the target is an identical subselection
	#    of the first result in the list and should replace it
	# If $put_on_top > 0, then the target is the Nth result and this result should be
	#    removed and the target placed on tom
	if ($put_on_top == -1) {
	    unshift @results, "$fasta";
	    unshift @evalues, "0";
	    unshift @fastas,  "$full_fasta_text";
	} elsif (($put_on_top == 0) && ($partial_match != -1)) {
	    shift @results; unshift @results, $fasta;
	    shift @evalues; unshift @evalues, 0;
	    shift @fastas;  unshift @fastas,  $full_fasta_text;
	} elsif ($put_on_top > 0) {
	    my $j = $put_on_top - 1;
	    my $k = $put_on_top + 1;
	    my   @new_results = @results[0..$j];
	    push @new_results,  @results[$k..$#results];

	    my   @new_evalues = @evalues[0..$j];
	    push @new_evalues,  @evalues[$k..$#evalues];

	    my   @new_fastas  = @fastas[0..$j];
	    push @new_fastas,   @fastas[$k..$#fastas];

	    unshift @new_results, $fasta;
	    unshift @new_evalues, 0;
	    unshift @new_fastas,  $full_fasta_text;

	    undef @results; @results = @new_results;
	    undef @evalues; @evalues = @new_evalues;
	    undef @fastas;  @fastas  = @new_fastas;
	}
	
    } elsif ($raw) {
	my $sequence_match = -1;
	my $partial_match  = -1;

	my $rawToFasta = ">user RAW sequence input\n";
	my $tmpraw = $blastinput;
	while (length($tmpraw) > 0) {
	    if (length($tmpraw) > 60) {
		$rawToFasta .= substr($tmpraw,0,60) . "\n";
		substr($tmpraw,0,60) = "";
	    } else {
		$rawToFasta .= $tmpraw . "\n";
		$tmpraw = "";
	    }
	}

	for (my $i = 0; $i < @results; $i++) {
	    my $fastaraw = "";
	    my @fastaraws = split(/\n/,$fastas[$i]); shift @fastaraws;
	    foreach (@fastaraws) { $fastaraw .= "$_"; }

	    if (($fastaraw eq $blastinput)        && ($sequence_match == -1)) {
		$sequence_match = $i;
		print "Sequence Match  :: $i\n";
	    }
	    if (($fastaraw =~ /$blastinput/)      && ($partial_match == -1)) {
		$partial_match = $i;
		print "Partial Match   :: $i\n";
	    }
	}

	my $put_on_top;
	if ($sequence_match != -1) {
	    $put_on_top = $sequence_match;
	    $partial_match = -1;
	} elsif ($partial_match != -1) {
	    $put_on_top = $partial_match;
	} else {
	    $put_on_top = -1;
	}

	# If $put_on_top == -1, then the target sequence did not have any full or
	#    partial sequence matches, therefore it should be prepended to the results
	# If $put_on_top == 0 && $sequence_match, then the target
	#    is the first result in the list and nothing needs to be changed
	# If $put_on_top == 0 && $partial_match, then the target is an identical subselection
	#    of the first result in the list and should replace it
	# If $put_on_top > 0, then the target is the Nth result and this result should be
	#    removed and the target placed on tom
	if ($put_on_top == -1) {
	    unshift @results, "user RAW";
	    unshift @evalues, "0";
	    unshift @fastas,  "$rawToFasta";
	} elsif (($put_on_top == 0) && ($partial_match != -1)) {
	    shift @results; unshift @results, "user RAW";
	    shift @evalues; unshift @evalues, 0;
	    shift @fastas;  unshift @fastas,  $rawToFasta;
	} elsif ($put_on_top > 0) {
	    my $j = $put_on_top - 1;
	    my $k = $put_on_top + 1;
	    my   @new_results = @results[0..$j];
	    push @new_results,  @results[$k..$#results];

	    my   @new_evalues = @evalues[0..$j];
	    push @new_evalues,  @evalues[$k..$#evalues];

	    my   @new_fastas  = @fastas[0..$j];
	    push @new_fastas,   @fastas[$k..$#fastas];

	    unshift @new_results, "user RAW";
	    unshift @new_evalues, 0;
	    unshift @new_fastas,  $rawToFasta;

	    undef @results; @results = @new_results;
	    undef @evalues; @evalues = @new_evalues;
	    undef @fastas;  @fastas  = @new_fastas;
	}
	
    }
}

################################################################################
##### Calculate Sequence Identities to Target Sequence                     #####
################################################################################
sub calcSeqIds {
    $seqids[0]  = 100; # By definition, the seq id of a sequence to itself is 100
    $evalues[0] = 0;   # By definition, the evalue of a sequence to itself should be zero

    for (my $i = 1; $i < @fastas; $i++) {
	$seqids[$i] = clustalpairwise($fastas[0],$fastas[$i],$clustal_executable);
    }
}

################################################################################
##### Write Final Output                                                   #####
################################################################################
sub writeOutput {
    open FTA, ">${fnpfx}.fta";
    open TXT, ">${fnpfx}.txt";
    open CSV, ">${fnpfx}.csv";

    my $tmp = length($results[0]);
    if ($tmp < 9) { $tmp = 9; }
    printf TXT "%-${tmp}s     e-value          %7s\n", "accession", "% ident";
    print CSV "accession number,e-value,\% ident\n";
    for (my $i = 0; $i < @results; $i++) {
	print  FTA "$fastas[$i]";
	printf TXT "%-${tmp}s     %12.5g     %7d\n", $results[$i], $evalues[$i], $seqids[$i];
	print  CSV "$results[$i],$evalues[$i],$seqids[$i]\n";
    }

    close FTA;
    close TXT;
    close CSV;

    my $printstring = 
	"Output Files ::\n".
	" :: BLAST Results FASTA File      :: ${fnpfx}.fta\n".
	" :: E-Value/% Identity File (CSV) :: ${fnpfx}.csv\n".
	" :: E-Value/% Identity File (TXT) :: ${fnpfx}.txt\n".
	" :: BLAST HTML Output             :: ${fnpfx}.html\n".
	" :: BLAST XML Output              :: ${fnpfx}.xml\n".
	" :: Blast.pl Log File             :: ${fnpfx}.log\n";

    printDuo($printstring, 0);
}

################################################################################
##### Print to screen and log file                                         #####
################################################################################
sub printDuo {
    (my $message, my $quiet) = @_;
    if (!$quiet) {
	print LOG "$message";
	print     "$message";
    }
}

################################################################################
##### Help Message                                                         #####
################################################################################
sub help {

    my $help = "
Program:
 :: Blast.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: Blast.pl -a {accession number}     {other options}
 :: Blast.pl --fasta {FASTA file}      {other options}
 :: Blast.pl -r {RAW amino acid input} {other options}

Required Input: (Use only one)
 :: -a | --accession   :: String
 :: This should be a valid Swiss-Prot accession number.  For
 :: example, the human dopamine D5 receptor's accession
 :: number is P21918, so the input would be \"-a P21918\".

 :: --fasta            :: Filename
 :: This should be a valid FASTA file with one sequence.
 :: The amino acid portion of the FASTA file will be used
 :: for the BLAST search.

 :: -r | --raw         :: String
 :: This should be a protein sequence in single-letter
 :: amino acid format.

Optional Input:
 :: -d | --protdb      :: Keyword
 :: This keyword allows the user to select the protein
 :: database to be used in the BLAST search.  The valid
 :: keywords are:
 :: Bacteria_Archaea, Bacteria, Archaea, Viruses, Eukaryota,
 :: Viridiplantae, Fungi, Metazoa, Arthropoda, Vertebrata,
 :: Mammalia, Rodentia, Primates, Microbial_proteomes,
 :: Mitochondrion, ARATH, CAEEL, DROME, ECOLI, HUMAN, MOUSE,
 :: RAT, YEAST, SCHPO, PLAFA, Complete

 :: -e | --ethreshold  :: Float
 :: This value is a cutoff parameter for BLAST and is give
 :: in powers of ten.  Smaller cutoffs give results that are
 :: more closely related to the target.  This value should
 :: only be changed by those that are familiar with its
 :: usage.
 :: Examples:
 :: -e 100    (results will be loosely related to target)
 :: -e 0.001  (results will be closely related to target)

 :: -s | --sequences   :: Integer
 :: This is the initial number of sequences that the program
 :: searches for.  If completeness is turned on, then this
 :: value will be increased until completeness is reached.

 :: -c | --complete | --nocomplete :: No Input
 :: This flag will tell the program to run until a complete
 :: set of sequences is returned.  Completeness is defined
 :: as the complete set of sequences that satisfies the
 :: e-value threshold.  The \"--nocomplete\" option will turn
 :: completeness off if it is turned on by default.

 :: -i | --compiter    :: Integer
 :: Every time that completeness is not achieved, the target
 :: number of sequences will be increased by this amount.

 :: -m | --maxseqs     :: Integer
 :: This is the maximum number of sequences that the program
 :: will search for.

 :: -l | --filter | --nofilter :: No Input
 :: This flag will turn on BLAST's low complexity region
 :: filter.  This filter masks regions of low sequence
 :: complexity during the BLAST search.  In some cases this
 :: will mask features that give unrelated results, and in
 :: others it will mask features that are important to the
 :: function of the protein.  Thus, it is important to use
 :: this feature with caution.  The \"--nofilter\" option
 :: will turn off the filter if it is turned on by default.

 :: -t | --trembl | --notrembl :: No Input
 :: This flag will allow TrEMBL sequences to be included in
 :: the BLAST results.  The TrEMBL database is not curated,
 :: therefore there may be some repeated or unreliable
 :: sequences in the results.  The \"--notrembl\" option will
 :: turn off TrEMBL sequences if they are turned on by
 :: default.

 :: -g | --flagnongpcr | --noflagnongpcr :: No Input
 :: This flag notifies the user that there are sequences
 :: that may not be GPCRs.  The program checks with the
 :: webpage at http://www.gpcr.org/7tm/htmls/entries.html.
 :: It is likely that some GPCR sequences will be flagged
 :: incorrectly.  The \"--noflagnongpcr\" option will turn
 :: the flagging option off if it is turned on by default.

 :: -x | --cutnongpcr | --nocutnongpcr :: No Input
 :: This flag notifies the user that there are sequences
 :: that may not be GPCRs.  The program checks with the
 :: webpage at http://www.gpcr.org/7tm/htmls/entries.html.
 :: It is likely that some GPCR sequences will be flagged
 :: incorrectly.  Additionally, the flagged sequences will
 :: be removed from the final output.  The \"--nocutnongpcr\"
 :: option will turn the cutting option off if it is turned
 :: on by default.

 :: -n | --name        :: String
 :: When this input is used, all output files will be given
 :: this name. (e.g. {name}.fta, {name.csv}, etc.)

 :: --prefix           :: String
 :: When used with FASTA or RAW input, this functions as the
 :: \"-n {name}\" option.  When used with a Swiss-Prot
 :: accession number, this input will be prepended to all
 :: of the output files.  (e.g. {prefix}.P14416.fta)

 :: -q | --quiet       :: No Input
 :: This flag will turn off some of the output to the screen.

 :: -h | --help        :: No Input
 :: Prints this help message.

 :: --showdefaults     :: No Input
 :: Prints out the current defaults based on the .blast
 :: file being used.

Description:
 :: This program performs a BLAST search using the online
 :: server at http://www.expasy.org/tools/blast.  It then
 :: parses the results and produces a FASTA file of the
 :: resulting sequences.

 :: If the completeness flag is used, the BLAST search will
 :: be performed with an increasing target number of results
 :: until no new sequences are returned for the given 
 :: e-value threshold.

 :: If requested, potential non-GPCR sequences will be cut
 :: from or flagged in the results.

 :: When a Swiss-Prot accession number is used, the sequence
 :: corresponding to the number will always be the first
 :: sequence in the results.  When a FASTA file is used,
 :: then a sequence that matches the FASTA file exactly will
 :: be placed first.  If nothing matches the file (header
 :: and sequence), then the first result to match the FASTA
 :: sequence will be placed first in the results.  Should
 :: there not be an identically matching sequence, the
 :: program will place the original input at the beginning
 :: of the results and will remove the first sequence
 :: that has a partial identical match.  The same is done
 :: for RAW sequence input.

";
    die $help;
}

# v-- This line must be included --v 
1;
