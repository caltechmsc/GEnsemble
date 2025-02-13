package SequenceTools::SequenceTools;

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
#    push @INC, '/ul/griffith/perl5/lib/perl5/';
#    push @INC, '/ul/griffith/perl5/lib/perl5/x86_64-linux-thread-multi/';
}

use strict;
use warnings;
use base 'Exporter';
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

our $VERSION = '1.00'; 
our @EXPORT  = (
    "log",
    "sprint_sequence",
    "print_sequence",
    "sprint_fasta_from_hash",
    "get_fasta",
    "get_fasta_single",
    "parse_fasta",
    "load_fasta_single",
    "fasta_nseq",
    "expasy_blast_xml",
    "parse_blast_xml",
    "quick_parse_blast_xml",
    "set_on_top",
    "add_gpcr_sequences",
    "mafft",
    "pir2aln",
    "aln2pir",
    "toc",
    "tocf",
    );

################################################################################
##### Executables                                                          #####
################################################################################
our $mafft_bin   = "${Bin}/SequenceTools/mafft/mafft/libexec/mafft";
our $mafft_exe   = "${Bin}/SequenceTools/mafft/mafft";
our $clustal_exe = "${Bin}/SequenceTools/clustal/clustalw";

################################################################################
### Log
################################################################################

# Input:
#   1) Filehandle
#   2) String
# Return:
#   1) None (prints to filehandle and to screen)
sub log {
    my $fh  = $_[0];
    my $str = $_[1];

    print $fh $str;
    print     $str;
}

################################################################################
### Print amino acid sequences
################################################################################

# Input:
#   1) Sequence string
#   2) Print width
#   3) Line prefix
# Return:
#   1) Formatted string
sub sprint_sequence {
    my $seq   = $_[0];
    my $width = $_[1];
    my $pfx   = $_[2];
    
    if (! defined $width) { $width = 60; }
    if (! defined $pfx)   { $pfx   = ""; }

    my $txt = "";
    while (length($seq) > $width) {
	my $tmp = substr($seq,0,$width);
	substr($seq,0,$width) = "";
	$txt .= "${pfx}${tmp}\n";
    }
    if (length($seq) > 0) {
	$txt .= "${pfx}${seq}\n";
    }
    return $txt;
}

# Input:
#   1) Sequence string
#   2) Print width
#   3) Line prefix
# Return:
#   1) None (print to screen)
sub print_sequence {
    my $seq   = $_[0];
    my $width = $_[1];
    my $pfx   = $_[2];
    
    print sprint_sequence($seq,$width,$pfx);
}

# Input:
#   1) Blast Data Hash
# Return:
#   1) FASTA text string
#   2) CSV text string
sub sprint_fasta_from_hash {
    my %dat = %{$_[0]};
    my @accs = sort {$dat{$a}{order} <=> $dat{$b}{order}} keys %dat;
    my $fta = "";
    my $csv = "acc,db,eval,header\n";
    for (my $i = 0; $i < @accs; $i++) {
	my $acc  = $accs[$i];
	my $hdr  = $dat{$acc}{hdr}; $hdr =~ s/\"//g;
	my $seq  = $dat{$acc}{seq};
	my $db   = $dat{$acc}{db};
	my $eval = $dat{$acc}{eval};
	$fta .= $dat{$acc}{fasta};
	$csv .= sprintf "${acc},${db},%e,\"${hdr}\"\n", $eval;
    }
    return ($fta, $csv);
}

################################################################################
### FASTA
################################################################################

# Input:
#   1) List of accession numbers (not array reference)
# Return: For more than one accession number
#   1) Error value
#   2) Reference to list of fastas
#   3) Reference to list of headers
#   4) Reference to list of sequences
#   5) Reference to list of urls
# Return: One accession number
#   1) Error value
#   2) Fasta string
#   3) Header string
#   4) Sequences string
#   5) Url string
sub get_fasta {
    my @accs = @_;

    my $txt = "";
    
    my @fastas = ();
    my @hdrs   = ();
    my @seqs   = ();
    my @urls   = ();
    my $err    = 0;

    # Status
    my $nseq = scalar @accs;
    my $ctr  = 0;
    open STATUS, ">blast_status.log";
    print STATUS "$ctr of $nseq loaded";
    close STATUS;

    # Obtain sequences
    while (@accs > 0) {
	# Sequence URL
	my $url =
	    "http://www.ebi.ac.uk/Tools/dbfetch/dbfetch?".
	    "db=uniprotkb&format=fasta&style=raw&Retrieve=Retrieve&id=";
	if (@accs >= 200) {
	    $ctr += 200;
	    $url .= join(",", splice(@accs, 0, 199) );
	} elsif (@accs > 0) {
	    $ctr += scalar @accs;
	    $url .= join(",", @accs);
	    @accs = ();
	}
	push @urls, $url;

	# Load URL
	my $tmp = get $url;

	# Status
	open STATUS, ">blast_status.log";
	print STATUS "$ctr of $nseq loaded";
	close STATUS;

	# Fail
	if (! defined $tmp) {
	    $err = "unknown error\n";
	    return ($err, \@fastas, \@hdrs, \@seqs, \@urls);
	} elsif ($tmp =~ /^error/i) {
	    return ($tmp, \@fastas, \@hdrs, \@seqs, \@urls);
	}

	# Succeed
	$txt .= $tmp;
    }

    # Split results into FASTA sequences, reformat
    @fastas = split(/\n\>/, $txt);
    for (my $i = 0; $i < @fastas; $i++) {
	if ($fastas[$i] !~ /^\>/) { $fastas[$i] = ">" . $fastas[$i]; }
	if ($fastas[$i] !~ /\n$/) { $fastas[$i] .= "\n"; }
    }

    # Headers / Sequences
    for (my $i = 0; $i < @fastas; $i++) {
	my ($hdr, $seq) = parse_fasta($fastas[$i]);
	push @hdrs, $hdr;
	push @seqs, $seq;
    }

    # Single Sequence
    if (@fastas == 1) {
	return ($err, $fastas[0], $hdrs[0], $seqs[0], $urls[0]);
    }

    # Multiple Sequences
    else {
	return ($err, \@fastas, \@hdrs, \@seqs, \@urls);
    }
}

# Input:
#   1) Accession Number
# Output:
#   1) Error string
#   2) Fasta string
#   3) Header string
#   4) Sequence string
#   5) Url string
sub get_fasta_single {
    my $acc = $_[0];

    # Url
    my $url = "http://www.uniprot.org/uniprot/${acc}.fasta";
    
    # Load
    my $fta = get $url;

    # Fail
    if (! defined $fta) {
	my $err = "unknown error\n";
	return ($err, "", "", "", $url);
    } elsif ($fta =~ /^error/i) {
	return ($fta, "", "", "", $url);
    }

    # Success
    my ($hdr,$seq) = parse_fasta($fta);
    return (0, $fta, $hdr, $seq, $url);
}

# Input:
#   1) Fasta String
# Output:
#   1) Header string
#   2) Sequence string
sub parse_fasta {
    my $fasta = $_[0];

    # Split into lines
    my @lines = split(/\n/, $fasta);

    # Header
    my $hdr = shift @lines;

    # Sequence
    my $seq = join("", @lines);
    $seq =~ s/\s//g;

    # Return
    return ($hdr, $seq);
}

# Input:
#   1) Fasta filename
# Output:
#   1) FASTA string
#   2) Header string
#   3) Sequence string
sub load_fasta_single {
    my $file = $_[0];
    open FTA, $file;
    my $txt = join("", <FTA>);
    close FTA;
    my ($hdr,$seq) = parse_fasta($txt);
    return ($txt,$hdr,$seq);
}

# Input:
#   1) Fasta String
# Output:
#   1) Number of sequences
sub fasta_nseq {
    my $fta = $_[0];
    my @split = split(/\n\>/, $fta);
    my $nseq = scalar @split;
    return $nseq;
}

################################################################################
### Expasy BLAST search
################################################################################

# Input:
#   1) Output prefix
#   2) Blast search input
#   3) Database subset
#   4) Number of sequences
#   5) E-threshold
#   6) TREMBL flag
#   7) Low-complexity filter flag
# Return:
#   1) Error value
#   2) XML string
#   3) URL string
sub expasy_blast_xml {
    my $prefix  = $_[0];
    my $search  = $_[1];
    my $db      = $_[2];
    my $nseq    = $_[3];
    my $ethresh = $_[4];
    my $trembl  = $_[5];
    my $filter  = $_[6];

    # URL
    my $url =
	"http://web.expasy.org/cgi-bin/blast/blast.pl?".
	"sequence=$search".
	"&action=Xml".
	"&dbtype=UniProtKB".
	"&protdb_section=$db".
	"&showsc=$nseq".
	"&showal=$nseq".
	"&ethr=$ethresh".
	"&Gap=T";
    if (!$trembl) {
	$url .= "&curated=on";
    }
    if ($filter) {
	$url .= "&Filter=T";
    } else {
	$url .= "&Filter=F";
    }

    # Record URL
    open URL, ">${prefix}.blast.url";
    print URL $url . "\n";
    close URL;

    # Load URL
    my $xml = get $url;

    # Fail
    if (! defined $xml) {
	return ("unknown error", $xml, $url);
    }

    # Error
    if ($xml =~ /^Error/) {
	return ($xml, $xml, $url);
    }

    # Success
    open XML, ">${prefix}.blast.xml";
    print XML $xml;
    close XML;
    if (-e "${prefix}.blast.xml.gz") { unlink "${prefix}.blast.xml.gz"; }
    `gzip ${prefix}.blast.xml`;

    # Return
    return (0, $xml, $url);
}

################################################################################
### Parse BLAST XML
################################################################################

# Input:
#   1) BLAST XML results
#   2) Output prefix
# Return:
#   1) BLAST results hash
#   2) Max E-value
#   3) # Sequences
#   4) # Swiss-Prot Sequences
#   5) # Swiss-Prot Normal Sequences
#   6) # Swiss-Prot Splice Sequences
#   7) # Trembl Sequences
#   8) # Kept (S-P Normal + Trembl)
#   9) Complete flag
sub parse_blast_xml {
    my $xml     = $_[0];
    my $pfx     = $_[1];
    my $tgtnseq = $_[2];

    # Split XML into Hits
    my @hits = split(/\<\/Hit\>/, $xml);
    pop @hits;

    # Data
    my $maxev  = -1;
    my $n_seq  = scalar(@hits);
    my $n_sp   = 0;
    my $n_sp_n = 0;
    my $n_sp_v = 0;
    my $n_tr   = 0;
    my $n_frag = 0;
    my $n_kept = 0;
    my $n_err  = 0;
    my $err    = "";
    my @accs   = ();
    my %dat    = ();
    my @elim   = ();

    ###
    ### Parse Hits
    ###
    for (my $i = 0; $i < @hits; $i++) {
	my $hit = $hits[$i];
	$hit =~ s/[\s\S]+\<Hit\>/\<Hit\>/;
	$hit .= "</Hit>";

	# Full accession string
	$hit =~ /\<Hit_accession\>(\S+)\<\/Hit_accession\>/;
	my $full = $1;

	# E-Value
	$hit =~ /\<Hsp_evalue\>(\S+)\<\/Hsp_evalue\>/;
	my $eval = $1;
	$maxev = max($maxev, $eval);

	# Header
	$hit =~ /\<Hit_def\>([\s\S]+)\<\/Hit_def\>/;
	my $hdr = $1;

	# Swiss-Prot
	if ($full =~ /^sp\!(\S+)\!/) {
	    my $acc = $1;

	    # Not fragment
	    if ($hdr !~ /\(fragment\)/i) {
		$n_sp++; $n_sp_n++; $n_kept++;
		push @accs, $acc;
		$dat{$acc}{order} = $i;
		$dat{$acc}{db}    = "sp";
		$dat{$acc}{eval}  = $eval;
	    }
	    
	    # Fragment
	    else {
		$n_frag++;
		push @elim, $acc;
	    }
	}

	# Trembl
	elsif ($full =~ /^tr!(\S+)\_/) {
	    my $acc = $1;

	    # Not fragment
	    if ($hdr !~ /\(fragment\)/i) {
		$n_tr++; $n_kept++;
		push @accs, $acc;
		$dat{$acc}{order} = $i;
		$dat{$acc}{db}    = "tr";
		$dat{$acc}{eval}  = $eval;
	    }

	    # Fragment
	    else {
		$n_frag++;
		push @elim, $acc;
	    }
	}

	# Swiss-Prot Variation
	elsif ($full =~ /^sp\!(\S+)-(\d+)/) {
	    my $acc = "${1}-${2}";
	    $n_sp++; $n_sp_v++;
	    push @elim, $acc;
	}

	# Other
	else { $n_err++; $err .= $hit; }
    }

    # Errors parsing XML
    if ($n_err > 0) {
	open ERR, ">${pfx}.blast.err";
	print ERR $err;
	close ERR;

	die "Blast2 :: Error parsing BLAST XML results.\n".
	    "       :: Unable to parse these hits: ${pfx}.blast.err"
    }

    ###
    ### Load Results
    ###
    my @ret = get_fasta(@accs);
    my $get_fasta_err = $ret[0];
    my @fastas = @{$ret[1]};
    my @hdrs   = @{$ret[2]};
    my @seqs   = @{$ret[3]};
    my @urls   = @{$ret[4]};

    # Load eliminated sequences
    @ret = get_fasta(@elim);
    my @elimfasta = @{$ret[1]};
    open ELIM, ">${pfx}.blast_elim.fta";
    print ELIM join("", @elimfasta);
    close ELIM;

    # Errors loading FASTA
    if ($get_fasta_err) {
	# Record failed URLs
	open URL, ">${pfx}.fail.url";
	print URL join("\n", @urls);
	close URL;

	# Exit
	die "Blast2 :: Unable to load sequences from BLAST results\n".
	    "       :: Failed URL: ${pfx}.fail.url";
    }

    # Load data into hash
    for (my $i = 0; $i < @accs; $i++) {
	my $acc = $accs[$i];
	$dat{$acc}{fasta} = $fastas[$i];
	$dat{$acc}{hdr}   = $hdrs[$i];
	$dat{$acc}{seq}   = $seqs[$i];
    }

    # Complete?
    my $complete = "yes";
    if ($n_seq == $tgtnseq) { $complete = "no"; }

    # Return
    return (\%dat, $maxev, $n_seq, $n_sp, $n_sp_n, $n_sp_v,
	    $n_tr, $n_frag, $n_kept, $complete);
}

# Input:  XML String
# Return: Appx. number of hits
sub quick_parse_blast_xml {
    my $xml = $_[0];
    my @hits = split(/\<\/Hit\>/, $xml);
    pop @hits;
    return scalar(@hits);
}

################################################################################
### Target Sequence First
################################################################################

# Input:
#   1) Data hash
#   2) Blast input (filename/accession)
#   3) input type (file/accession)
#   4) Header string
#   5) Sequence string
# Return:
#   1) Data hash
sub set_on_top {
    my %dat  = %{$_[0]};
    my $in   =   $_[1];
    my $type =   $_[2];
    my $hdr  =   $_[3];
    my $seq  =   $_[4];

    # Indices
    my $hdr_and_seq_match;
    my $seq_match;

    # List of accessions
    my @accs = sort {$dat{$a}{order} <=> $dat{$b}{order}} keys %dat;	

    # Cycle through accession numbers
    for (my $i = 0; $i < @accs; $i++) {

	# Accession number input: Accession index $i matches
	if (($type eq "accession") && ($accs[$i] eq $in)) {
	    $dat{$accs[$i]}{order} = -1; # Make sure it's first
	}

	# File input: Header & Sequence matches
	if (($type eq "file")
	    && ($hdr eq $dat{$accs[$i]}{hdr})
	    && ($seq eq $dat{$accs[$i]}{seq})) {

	    $hdr_and_seq_match = $accs[$i];
	}

	# File input: Sequence matches
	if (($type eq "file")
	    && ($seq eq $dat{$accs[$i]}{seq})
	    && (! defined$seq_match)) {

	    $seq_match = $accs[$i];
	}
    }

    # File input
    if ($type eq "file") {
	# Header & Seq Match: Set on top
	if ($hdr_and_seq_match) {
	    $dat{$hdr_and_seq_match}{order} = -1;
	}

	# Seq Match only: Set on top
	elsif ($seq_match) {
	    $dat{$seq_match}{order} = -1;
	}

	# No Match: Add new sequence
	else {
	    $hdr =~ s/^\>/\>user_input|/;
	    $dat{"input"}{order} = -1;
	    $dat{"input"}{hdr}   = $hdr;
	    $dat{"input"}{seq}   = $seq;
	    $dat{"input"}{fasta} = "${hdr}\n" . sprint_sequence($seq,60,"");
	    $dat{"input"}{db}    = "user";
	    $dat{"input"}{eval}  = -1;
	}
    }

    # Return
    return (\%dat);
}

################################################################################
### Add GPCR Sequences
################################################################################

# Input:
#   1) FASTA string (1 or more sequences)
# Return:
#   1) FASTA string with new sequences
#   2) reference to array of added sequences
#   3) reference to array of sequences already present
sub add_gpcr_sequences {
    my $fta = $_[0];

    ###
    ### Input Sequences
    ###

    # Split FASTA
    my @fastas = split(/\n\>/, $fta);
    for (my $i = 0; $i < @fastas; $i++) {
	if ($fastas[$i] !~ /^\>/) { $fastas[$i] = ">" . $fastas[$i]; }
	if ($fastas[$i] !~ /\n$/) { $fastas[$i] .= "\n"; }
    }
    
    # Headers / Sequences
    my @hdrs = ();
    my @seqs = ();
    for (my $i = 0; $i < @fastas; $i++) {
	my ($hdr, $seq) = parse_fasta($fastas[$i]);
	push @hdrs, $hdr;
	push @seqs, $seq;
    }

    ###
    ### GPCR Sequences
    ###
    my @gpcrs = glob "${Bin}/SequenceTools/gpcr_fasta/*.fta";
    my @added = ();
    my @present = ();
    foreach my $gpcr (@gpcrs) {
	my ($fasta, $hdr, $seq) = load_fasta_single($gpcr);
	my $gpcr = basename($gpcr);
	$gpcr =~ /^(\S+)\.(\S+)\.fta/;
	my $name = $1;
	my $acc  = $2;
	my $add  = 1;
	$hdr =~ /^(\S+)\s+([\s\S]+)/;
	my $hdr2 = $2;

	# Cycle through input sequences
	# If header & sequence match, do not add
	for (my $i = 0; $i < @fastas; $i++) {
	    # Match?
	    if (($hdr eq $hdrs[$i]) &&
		($seq eq $seqs[$i])) {
		$add = 0;
	    }
	}

	# Add
	if ($add) {
	    push @added, sprintf "%6s - %-11s - %s", $acc, $name, $hdr2;
	    push @fastas, $fasta;
	    push @hdrs, $hdr;
	    push @seqs, $seq;
	}

	# Already Present
	else {
	    push @present, sprintf "%6s - %-11s - %s", $acc, $name, $hdr2;
	}
    }

    ###
    ### Print new list
    ###
    $fta = join("", @fastas);

    # Return
    return ($fta, \@added, \@present);
}

################################################################################
### MAFFT
################################################################################

# Input:
#   1) FASTA file (2 or more sequences)
#   2) Flag to turn on fast mode
# Return:
#   1) PIR filename
#   2) ALN filename
sub mafft {
    my $fta   = $_[0];
    my $pfx   = $_[1];
    my $fast  = $_[2];
    my $nproc = $_[3];

    # Settings
    my $set = "--genafpair";
    if ($fast) {
	$set = "--retree 2 --maxiterate 0";
    }

    # Set up MAFFT Environment
    undef $ENV{MAFFT_BINARIES};

    # Run MAFFT
    my $cmd = "(${mafft_exe} --thread $nproc --anysymbol".
	" $set $fta > ${pfx}.pir) >& ${pfx}.mafft.out";
    `$cmd`;

    # PIR to ALN
    my $pir = "${pfx}.pir";
    my $aln = pir2aln($pir);
    return ($pir,$aln);
}

################################################################################
### pir2aln - PIR file to ALN file
################################################################################
sub pir2aln {
    my $f = shift;
    (my $nf = $f) =~ s/.pir$/.aln/;

    # Convert PIR to ALN
    `$clustal_exe -infile=${f} -convert -outfile=${nf}`;

    return "$nf";
}

################################################################################
### aln2pir - ALN file to PIR file
################################################################################
sub aln2pir {
    my $f = shift;
    (my $nf = $f) =~ s/.aln$/.pir/;

    # Convert PIR to ALN
    `$clustal_exe -infile=${f} -convert -outfile=${nf} -output=PIR`;

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

# Input:
#   1) Start time
# Return:
#   1) Elapsed time
sub toc {
    return time() - $_[0];
}

# Input:
#   1) Number of seconds
# Return:
#   1) Formatted time
sub tocf {
    my $elapsed = $_[0];

    my $days = floor($elapsed / (24 * 60 * 60));
    $elapsed -= $days * 24 * 60 * 60;

    my $hours = floor($elapsed / (60 * 60));
    $elapsed -= $hours * 60 * 60;

    my $mins = floor($elapsed / 60);
    $elapsed -= $mins * 60;

    my $secs = $elapsed;

    # Return
    if ($days > 0) {
	return "${days} d, ${hours} h, ${mins} m, ${secs} s";
    } elsif ($hours > 0) {
	return "${hours} h, ${mins} m, ${secs} s";
    } elsif ($mins > 0) {
	return "${mins} m, ${secs} s";
    } else {
	return "${secs} s";
    }
}






















# v-- This line must be included --v 
1;
