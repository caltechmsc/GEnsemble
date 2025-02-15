#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
#    push @INC, '/ul/griffith/perl5/lib/perl5/';
#    push @INC, '/ul/griffith/perl5/lib/perl5/x86_64-linux-thread-multi/';
}

use strict;
use warnings;
use Cwd;
#use Data::Dumper;
#use Data::Table;
use File::Basename;
use File::Copy;
use File::Path;
use File::Spec;
use Getopt::Long qw(:config no_ignore_case);
use List::Util qw(min max sum);
#use List::MoreUtils qw(:all);
#use List::Compare;
use LWP::Simple;
use POSIX qw(ceil clock cuserid difftime floor getcwd getenv getlogin);
#use Storable;
use Sys::Hostname;
#use Text::CSV;
use Time::Local;
#use XML::Hash;

use SequenceTools::SequenceTools;

###
### Arguments & Variables
###
our $db      = "";
our $ethresh = 0.1;
our $tgtnseq = 10000;
our $pfx     = "";
our $validdb = "Archaea|Viruses|Eukaryota|Viridiplantae|Fungi|Metazoa|".
    "Arthropoda|Vertebrata|Mammalia|Rodentia|Primates|Microbial_proteomes|".
    "Mitochondrion|ARATH|CAEEL|DICDI|DROME|ECOLI|HUMAN|MOUSE|RAT|YEAST|SCHPO|PLAFA";

if (@ARGV == 0) { help(); }

my ($help, $acc_in, $fta_in, $filter, $trembl, $debug);

#ABCDEFGHIJKLMNOPQRSTUVWXYZ
# b    g ijklm o qrs uvwxyz
GetOptions ('h|help'          => \$help,
	    'a|acc=s'         => \$acc_in,
	    'f|fasta=s'       => \$fta_in,
	    'n|numseq=i'      => \$tgtnseq,
	    'e|ethresh=s'     => \$ethresh,
	    'd|db=s'          => \$db,
	    'c|filter'        => \$filter,
	    't|trembl'        => \$trembl,
	    'p|prefix=s'      => \$pfx,
	    'debug'           => \$debug);

if ($help) { help(); }

if ((!$acc_in) && (!$fta_in)) {
    die "Blast2 :: Must provide accession number (preferred) or fasta file\n";
} elsif ($acc_in && $fta_in) {
    die "Blast2 :: Cannot use both accession number and fasta file\n";
}

if (($ethresh !~ /^10*$/) && ($ethresh !~ /^0?\.0*1/)) {
    die "Blast2 :: E-Value threshold not valid: $ethresh\n";
}

if (($db ne "") && ($db !~ /$validdb/)) {
    my $tmp = "  $validdb";
    $tmp =~ s/\|/\n  /;
    die "Blast2 :: Database selection invalid: $db\n".
	"  Valid selections: (none) or:\n".
	$tmp;
}

############################################################
### Main Routine                                         ###
############################################################

###
### Blast input: accession number or file
###
my ($input, $fasta, $hdr, $seq, $search, $type);

# File Input
if ($fta_in) {
    $input = $fta_in;
    $type = "file";
    if ($fta_in !~ /(\S+)\.(seq|fta|fasta)$/) {
	die "Blast2 :: Fasta filename must end in .seq, .fta, or .fasta\n";
    }

    # Prefix
    $fta_in =~ /(\S+)\.(seq|fta|fasta)$/;
    if ($pfx eq "") { $pfx = $1; }

    # Check for file
    if (! -e $input) {
	die "Blast2 :: Could not find file: $input\n";
    }

    # Load Input File
    open FTA, "$input";
    $fasta = join("", <FTA>);
    close FTA;
    copy($input, "${pfx}.blast_search.fta");

    # Parse Sequence
    ($hdr, $seq) = parse_fasta($fasta);

    # Blast input
    $search = $seq;
}

# Accession Number
elsif ($acc_in) {
    $input = $acc_in;
    $type = "accession";

    # Prefix
    if ($pfx eq "") { $pfx = $input; }

    # Load Sequence from Uniprot
    (my $err, $fasta, $hdr, $seq, my $url) = get_fasta_single($input);
    if (-e "blast_status.log") { unlink "blast_status.log"; }

    # Error
    if ($err) {
	# Record failed URL
	open URL, ">${pfx}.fail.url";
	print URL $url;
	close URL;

	# Exit
	die "Blast2 :: Unable to load sequence for: $input\n".
	    "       :: Failed URL: ${pfx}.fail.url\n";
    }
    
    # Print Sequence
    open FTA, ">${pfx}.blast_search.fta";
    print FTA $fasta;
    close FTA;

    # Blast input
    $search = $input;
}

# Open Log
my $logfile;
open $logfile, ">${pfx}.blast.log";

# Print Settings
log $logfile,
    "Blast2 :: " . localtime() . "\n".
    " :: Search Input       :: $input\n".
    " :: Target Seqs        :: $tgtnseq\n".
    " :: Database Subset    :: " . ($db eq "" ? "" : $db) . "\n".
    " :: E-Threshold        :: " . (sprintf "%.0e", $ethresh) . "\n".
    " :: Complexity Filter  :: " . ($filter ? "yes" : "no") . "\n".
    " :: Use TrEMBL Seqs    :: " . ($trembl ? "yes" : "no") . "\n\n".
    "Search Sequence: stored in ${pfx}.blast_search.fta\n".
    "  $hdr\n".
    sprint_sequence($seq,60,"  ") . "\n";

###
### Run BLAST
###
print "Running Blast (may take some time)\n";
my ($err, $xml, $url) =
    expasy_blast_xml($pfx, $search, $db, $tgtnseq, $ethresh, $trembl, $filter);

# Error
if ($err) {
    die "Blast2 :: Unable to load BLAST results from URL:\n".
 	"       :: Failed URL: ${pfx}.blast.url\n";
}

###
### Parse BLAST Results
###
my $quicknum = quick_parse_blast_xml($xml);
print "\nLoading Blast Results ($quicknum hits, may take some time)\n";
my @ret = parse_blast_xml($xml, $pfx, $tgtnseq);
my %dat    = %{$ret[0]};
my $maxev  =   $ret[1];
my $n_seq  =   $ret[2];
my $n_sp   =   $ret[3];
my $n_sp_n =   $ret[4];
my $n_sp_v =   $ret[5];
my $n_tr   =   $ret[6];
my $n_frag =   $ret[7];
my $n_kept =   $ret[8];
my $comp   =   $ret[9];
print "\n";
if (-e "blast_status.log") { unlink "blast_status.log"; }

# Print Statistics
log $logfile,
    sprintf
    "Statistics ::\n".
    " :: Complete?        :: $comp\n".
    " :: Max E-value      :: %8.3e\n".
    " :: Total Seqs.      :: %4d\n".
    " :: Total Kept       :: %4d\n".
    " :: Swiss-Prot Total :: %4d\n".
    "    Swiss-Prot Norm. :: %4d\n".
    "    Swiss-Prot Var.  :: %4d\n".
    " :: TrEMBL Seqs.     :: %4d\n".
    " :: Fragments Seqs.  :: %4d\n\n",
    $maxev, $n_seq, $n_kept, $n_sp, $n_sp_n, $n_sp_v, $n_tr, $n_frag;

# No sequences returned, but no obvious errors
if ($n_kept == 0) {
    log
	$logfile,
	"BLAST did not return any sequences for your search!\n".
	"Possible reasons:\n".
	" * No sequences are related to your target\n".
	" * The E-Value threshold is to restrictive\n\n".
	"Try these options:\n".
	" * Complexity filter: '-c'\n".
	" * TrEMBL Sequences: '-t'\n".
	" * Larger E-value threshold\n\n";
    exit;
}

###
### Set Target Sequence as First
###
@ret = set_on_top(\%dat, $input, $type, $hdr, $seq);
%dat = %{$ret[0]};

# Print Results
my ($fta_results, $csv_results) = sprint_fasta_from_hash(\%dat);
open FTA, ">${pfx}.blast_results.fta";
print FTA $fta_results;
close FTA;
open CSV, ">${pfx}.blast_results.csv";
print CSV $csv_results;
close CSV;

# Print Output
log $logfile,
    "Output ::\n".
    " :: Sequences  :: ${pfx}.blast_results.fta\n".
    " :: E-Values   :: ${pfx}.blast_results.csv\n".
    " :: Search URL :: ${pfx}.blast.url\n".
    " :: BLAST XML  :: ${pfx}.blast.xml.gz\n".
    " :: Eliminated :: ${pfx}.blast_elim.fta\n".
    " :: Log File   :: ${pfx}.blast.log\n\n";

# Close Log
close $logfile;

# Done
exit;







############################################################
### Help                                                 ###
############################################################

sub help {

    my $help = "
Program:
 :: Blast2.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: Blast2.pl -a {accession number} -f {fasta file}
 ::           [other options]

Preferred Input:
 :: -a | --acc         :: Accession Number
 :: Uniprot accession number for search sequence
 :: This input is much preferred over FASTA file input

Alternate Input:
 :: -f | --fasta       :: FASTA File
 :: FASTA-formatted file for search sequence
 :: Use Uniprot accession number input instead if possible

Options:
 :: -n | --numseq      :: Integer > 0
 :: Target number of sequences to obtain.  Default = 10000

 :: -e | --ethresh     :: Int/Float
 :: E-value threshold.  Default = 0.1
 :: Must be in powers of 10: 100, 10, 1, 0.1, 0.01
 :: Smaller values result in stricter searches.

 :: -d | --db          :: Keyword
 :: Valid database subsets.  See below for options.
 :: Capitalization is important.

 :: -c | --filter      :: No Input
 :: Use BLAST low-complexity sequence filter.  This
 :: may cause relevant portions of the target sequence
 :: to be ignored.

 :: -t | --trembl      :: No Input
 :: Include sequences from the TrEMBL database.  This is
 :: not to be used unless there aren't enough sequences
 :: returned.  TrEMBL is a non-curated database.

 :: -p | --prefix      :: String
 :: Output file prefix.  Defaults to the accession number
 :: or the file prefix of the input fasta file.

 :: -h | --help        :: No Input
 :: Displays this help message.

Description:
 :: This program runs a BLAST search on the provided input.
 :: The preferred usage is to provide a valid Uniprot accession
 :: number, but a FASTA-formatted file can be provided instead.
 ::
 :: The user can adjust some common search parameters, such as
 :: the requested number of sequences, the E-value threshold,
 :: database subset, complexity filter, and TrEMBL sequences.
 ::
 :: The default number of sequences requested is 10000, which,
 :: while ridiculously high, should ensure that a *complete* set
 :: of sequences that pass the E-value threshold are returned.
 ::
 :: Fragments and Splice Sequences:
 :: Fragment sequences (sequences containing \"(fragment)\" in the
 :: header), and splice variant sequences are removed following
 :: the BLAST search.  These sequences are recorded to a separate
 :: FASTA output file in case you want to add some of them back
 :: into the main results.

Database Subsets:
 :: The following subsets of the database can be used:
 ::   Archaea, Viruses, Eukaryota, Viridiplantae, Fungi, Metazoa
 ::   Arthropoda, Vertebrata, Mammalia, Rodentia, Primates
 ::   Microbial_proteomes, Mitochondrion
 :: Or specific species:
 ::   ARATH, CAEEL, DICDI, DROME, ECOLI, HUMAN, MOUSE, RAT
 ::   YEAST, SCHPO, PLAFA
 ::
 :: Please note that CAPITALIZATION is important when setting
 :: a database subset

Usage:
 :: Blast2.pl -a {accession number} -f {fasta file}
 ::           [other options]

";

    die "$help";
}
