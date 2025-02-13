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

if (@ARGV == 0) { help(); }
foreach (@ARGV) { if (/^-h$/) { help(); } }

############################################################
### Main Routine                                         ###
############################################################

@files = @ARGV;

#Ordered by RankCNti

#Thet   H1   H2   H3   H4   H5   H6   H7  
#Phi   H1   H2   H3   H4   H5   H6   H7  
#Eta   H1   H2   H3   H4   H5   H6   H7  
#HPM    H1    H2    H3    H4    H5    H6    H7  
#CIntraH  CInterH   CTotal  NIntraH  NInterH   NTotal  RMSD  
#rankCih  rankCtl  rankNih  rankNtl  
#rankCti  rankNti  rankCNi  rankCNt 
#rankCNti RankCNti   SBHrank

#Thet    0    0    0    0    0    0    0  
#Phi    0    0    0    0    0    0    0  
#Eta    0    0    0    0    0    0    0  
#HPM  40.0  77.5 114.0 159.9 197.5 341.9 373.9    
#273.7   -409.8   -135.6    141.1   -362.9   -221.7  0.00       
#25        2        1        7     
#13.5      4.0     13.0      4.5      
#8.8        1        -1

# Check file type
$use_csv = 0;
$use_out = 0;
foreach $f (@files) {
    if ($f =~ /.out$/) { $use_out = 1; }
    if ($f =~ /.csv$/) { $use_csv = 1; }
}
if ($use_out && $use_csv) {
    die "ParseSCNOutput :: Cannot use mix of .out and .csv files!\n";
}
if ($use_out) {
    print
	"You appear to be using the text-formatted .out files.\n".
	"These files round the energy values way too much.  If\n".
	"you have CSV files, you should use those instead of the\n".
	"OUT files.\n".
	"\n";
    $value = "";
    while ($value !~ /^(y|n)$/i) {
	print "Do you want to proceed with the OUT files? [y/n] ";
	$value = <STDIN>;
	chomp $value;
    }
    if ($value =~ /^n$/i) {
	print
	    "\nYou have chosen not to proceed with the OUT files.\n\n".
	    "Exiting...\n\n";
	exit;
    } else {
	print
	    "\nProceeding against my better judgement with the OUT files.\n\n";
    }
}

# Load data from each file
foreach $f (@files) {
    open F, "$f";
    @lines = <F>;
    close F;
    while ($lines[0] !~ /^Thet/) { shift @lines; }
    shift @lines;

    # Parse each line
    foreach $line (@lines) {

	my @split = ();
	if ($f =~ /.out$/) {
	    $dat{"${f}.$line"}{source} = $f;
	    $dat{"${f}.$line"}{source} =~ s/.out$//;
	    @split = split(/\s+/, $line);
	} elsif ($f =~ /.csv$/) {
	    $dat{"${f}.$line"}{source} = $f;
	    $dat{"${f}.$line"}{source} =~ s/.csv$//;
	    @split = split(/\,/, $line);
	}

	# $f.$line is unique across all input files, assuming that
	# input files come from different template sources

	$dat{"${f}.$line"}{"t1"} = $split[1];
	$dat{"${f}.$line"}{"t2"} = $split[2];
	$dat{"${f}.$line"}{"t3"} = $split[3];
	$dat{"${f}.$line"}{"t4"} = $split[4];
	$dat{"${f}.$line"}{"t5"} = $split[5];
	$dat{"${f}.$line"}{"t6"} = $split[6];
	$dat{"${f}.$line"}{"t7"} = $split[7];

	$dat{"${f}.$line"}{"p1"} = $split[9];
	$dat{"${f}.$line"}{"p2"} = $split[10];
	$dat{"${f}.$line"}{"p3"} = $split[11];
	$dat{"${f}.$line"}{"p4"} = $split[12];
	$dat{"${f}.$line"}{"p5"} = $split[13];
	$dat{"${f}.$line"}{"p6"} = $split[14];
	$dat{"${f}.$line"}{"p7"} = $split[15];

	$dat{"${f}.$line"}{"e1"} = $split[17];
	$dat{"${f}.$line"}{"e2"} = $split[18];
	$dat{"${f}.$line"}{"e3"} = $split[19];
	$dat{"${f}.$line"}{"e4"} = $split[20];
	$dat{"${f}.$line"}{"e5"} = $split[21];
	$dat{"${f}.$line"}{"e6"} = $split[22];
	$dat{"${f}.$line"}{"e7"} = $split[23];

	$dat{"${f}.$line"}{"h1"} = $split[25];
	$dat{"${f}.$line"}{"h2"} = $split[26];
	$dat{"${f}.$line"}{"h3"} = $split[27];
	$dat{"${f}.$line"}{"h4"} = $split[28];
	$dat{"${f}.$line"}{"h5"} = $split[29];
	$dat{"${f}.$line"}{"h6"} = $split[30];
	$dat{"${f}.$line"}{"h7"} = $split[31];

	$dat{"${f}.$line"}{cintra} = $split[32];
	$dat{"${f}.$line"}{cinter} = $split[33];
	$dat{"${f}.$line"}{ctotal} = $split[34];
	$dat{"${f}.$line"}{nintra} = $split[35];
	$dat{"${f}.$line"}{ninter} = $split[36];
	$dat{"${f}.$line"}{ntotal} = $split[37];
	$dat{"${f}.$line"}{rmsd}   = $split[38];

	$dat{"${f}.$line"}{sbhrank} = $split[49];
    }
}

@confs = keys %dat;
$n = @confs;

# Energy orderings
@cinter = sort {$dat{$a}{cinter} <=> $dat{$b}{cinter}} keys %dat;
@ctotal = sort {$dat{$a}{ctotal} <=> $dat{$b}{ctotal}} keys %dat;
@ninter = sort {$dat{$a}{ninter} <=> $dat{$b}{ninter}} keys %dat;
@ntotal = sort {$dat{$a}{ntotal} <=> $dat{$b}{ntotal}} keys %dat;

$dat{$cinter[0]}{r_ci} = 1;
$dat{$ctotal[0]}{r_ct} = 1;
$dat{$ninter[0]}{r_ni} = 1;
$dat{$ntotal[0]}{r_nt} = 1;

$r_ci = 1;
$r_ct = 1;
$r_ni = 1;
$r_nt = 1;

# If the energy of conformation i is greater than the energy of conformation i-1
# then increase rank by 1, otherwise i and i-1 have same rank
for ($i = 1; $i < $n; $i++) {
    # Charged Interhelical Rank
    if ($dat{$cinter[$i]}{cinter} > $dat{$cinter[$i-1]}{cinter}) {
	$r_ci++;
    }
    $dat{$cinter[$i]}{r_ci} = $r_ci;

    # Charged Interhelical Rank
    if ($dat{$ctotal[$i]}{ctotal} > $dat{$ctotal[$i-1]}{ctotal}) {
	$r_ct++;
    }
    $dat{$ctotal[$i]}{r_ct} = $r_ct;

    # Neutral Interhelical Rank
    if ($dat{$ninter[$i]}{ninter} > $dat{$ninter[$i-1]}{ninter}) {
	$r_ni++;
    }
    $dat{$ninter[$i]}{r_ni} = $r_ni;

    # Neutral Total Rank
    if ($dat{$ntotal[$i]}{ntotal} > $dat{$ntotal[$i-1]}{ntotal}) {
	$r_nt++;
    }
    $dat{$ntotal[$i]}{r_nt} = $r_nt;
}

# Now we can get average rankings
for ($i = 0; $i < $n; $i++) {
    # Individual energy rankings for structure
    $r_ci = $dat{$confs[$i]}{r_ci};
    $r_ct = $dat{$confs[$i]}{r_ct};
    $r_ni = $dat{$confs[$i]}{r_ni};
    $r_nt = $dat{$confs[$i]}{r_nt};

    # Average rankings for structure
    $dat{$confs[$i]}{r_Cti}  = ($r_ct + $r_ci) / 2;
    $dat{$confs[$i]}{r_Nti}  = ($r_nt + $r_ni) / 2;
    $dat{$confs[$i]}{r_CNi}  = ($r_ci + $r_ni) / 2;
    $dat{$confs[$i]}{r_CNt}  = ($r_ct + $r_nt) / 2;
    $dat{$confs[$i]}{r_CNti} = ($r_ct + $r_ci + $r_nt + $r_ni) / 4;
}

# Get ordering of CNti ranking
@cnti = sort {$dat{$a}{r_CNti} <=> $dat{$b}{r_CNti}} keys %dat;
$dat{$cnti[0]}{R_CNti} = 1;
$R_CNti = 1;
for ($i = 1; $i < $n; $i++) {
    if ($dat{$cnti[$i]}{r_CNti} > $dat{$cnti[$i-1]}{r_CNti}) {
	$R_CNti++;
    }
    $dat{$cnti[$i]}{R_CNti} = $R_CNti;
}

# Print New Header
#CIntraH  CInterH   CTotal  NIntraH  NInterH   NTotal  RMSD  
#rankCih  rankCtl  rankNih  rankNtl  
#rankCti  rankNti  rankCNi  rankCNt 
#rankCNti RankCNti   SBHrank
open CSV, ">MultiSuperCombiNeutralize.csv";
print CSV
    "HPC,,,,,,,".
    "Theta,,,,,,,".
    "Phi,,,,,,,".
    "Eta,,,,,,,".
    "Source,".
    "Individual Energies,,,,,,,".
    "Individual Ranks,,,,".
    "Combined Ranks,,,,,,".
    "SBHrank\n";

print CSV
    "H1,H2,H3,H4,H5,H6,H7,".
    "H1,H2,H3,H4,H5,H6,H7,".
    "H1,H2,H3,H4,H5,H6,H7,".
    "H1,H2,H3,H4,H5,H6,H7,".
    "Source,".
    "CintraH,CInterH,CTotal,NIntraH,NInterH,NTotal,RMSD,".
    "rCi,rCt,rNi,rNt,".
    "rCti,rNti,rCNi,rCNt,".
    "rCNti,RankCNti,SBHrank\n";

open TXT, ">MultiSuperCombiNeutralize.txt";
printf TXT
    "%-4s %5s %5s %5s %5s %5s %5s %5s ".
    "%-4s %5s %5s %5s %5s %5s %5s %5s ".
    "%-4s %5s %5s %5s %5s %5s %5s %5s ".
    "%-4s %6s %6s %6s %6s %6s %6s %6s ".
    "%10s %10s %10s %10s %10s %10s %8s ".
    "%8s %8s %8s %8s %8s %8s %8s %8s %8s %8s %8s %s\n",
    
    "Thet","H1","H2","H3","H4","H5","H6","H7",
    "Phi", "H1","H2","H3","H4","H5","H6","H7",
    "Eta", "H1","H2","H3","H4","H5","H6","H7",
    "HPM", "H1","H2","H3","H4","H5","H6","H7",
    "CIntraH", "CInterH", "CTotal", "NIntraH", "NInterH", "NTotal", "RMSD",
    "rankCih", "rankCtl", "rankNih", "rankNtl",
    "rankCti", "rankNti", "rankCNi", "rankCNt",
    "rankCNti", "RankCNti", "SBHrank", "Source";

# Print New Data
for ($i = 0; $i < $n; $i++) {
    printf CSV
	"%f,%f,%f,%f,%f,%f,%f,".
	"%d,%d,%d,%d,%d,%d,%d,".
	"%d,%d,%d,%d,%d,%d,%d,".
	"%d,%d,%d,%d,%d,%d,%d,%s,".
	"%f,%f,%f,%f,%f,%f,%f,".
	"%d,%d,%d,%d,".
	"%f,%f,%f,%f,".
	"%f,%f,%d\n",
	$dat{$cnti[$i]}{h1}, $dat{$cnti[$i]}{h2}, $dat{$cnti[$i]}{h3}, $dat{$cnti[$i]}{h4},
	$dat{$cnti[$i]}{h5}, $dat{$cnti[$i]}{h6}, $dat{$cnti[$i]}{h7}, 

	$dat{$cnti[$i]}{t1}, $dat{$cnti[$i]}{t2}, $dat{$cnti[$i]}{t3}, $dat{$cnti[$i]}{t4},
	$dat{$cnti[$i]}{t5}, $dat{$cnti[$i]}{t6}, $dat{$cnti[$i]}{t7}, 

	$dat{$cnti[$i]}{p1}, $dat{$cnti[$i]}{p2}, $dat{$cnti[$i]}{p3}, $dat{$cnti[$i]}{p4},
	$dat{$cnti[$i]}{p5}, $dat{$cnti[$i]}{p6}, $dat{$cnti[$i]}{p7}, 

	$dat{$cnti[$i]}{e1}, $dat{$cnti[$i]}{e2}, $dat{$cnti[$i]}{e3}, $dat{$cnti[$i]}{e4},
	$dat{$cnti[$i]}{e5}, $dat{$cnti[$i]}{e6}, $dat{$cnti[$i]}{e7}, $dat{$cnti[$i]}{source},

	$dat{$cnti[$i]}{cintra}, $dat{$cnti[$i]}{cinter}, $dat{$cnti[$i]}{ctotal},
	$dat{$cnti[$i]}{nintra}, $dat{$cnti[$i]}{ninter}, $dat{$cnti[$i]}{ntotal},
	$dat{$cnti[$i]}{rmsd},
 
	$dat{$cnti[$i]}{r_ci}, $dat{$cnti[$i]}{r_ct},
	$dat{$cnti[$i]}{r_ni}, $dat{$cnti[$i]}{r_nt}, 

	$dat{$cnti[$i]}{r_Cti}, $dat{$cnti[$i]}{r_Nti},
	$dat{$cnti[$i]}{r_CNi}, $dat{$cnti[$i]}{r_CNt},

	$dat{$cnti[$i]}{r_CNti}, $dat{$cnti[$i]}{R_CNti}, $dat{$cnti[$i]}{sbhrank};

    printf TXT
	"%-4s %5d %5d %5d %5d %5d %5d %5d ".
	"%-4s %5d %5d %5d %5d %5d %5d %5d ".
	"%-4s %5d %5d %5d %5d %5d %5d %5d ".
	"%-4s %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f ".
	"%10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %8.2f ".
	"%8d %8d %8d %8d %8.2f %8.2f %8.2f %8.2f %8.2f %8d %8d %s\n",

    	"Thet", $dat{$cnti[$i]}{t1}, $dat{$cnti[$i]}{t2}, $dat{$cnti[$i]}{t3},
	$dat{$cnti[$i]}{t4}, $dat{$cnti[$i]}{t5}, $dat{$cnti[$i]}{t6}, $dat{$cnti[$i]}{t7}, 

	"Phi", $dat{$cnti[$i]}{p1}, $dat{$cnti[$i]}{p2}, $dat{$cnti[$i]}{p3},
	$dat{$cnti[$i]}{p4}, $dat{$cnti[$i]}{p5}, $dat{$cnti[$i]}{p6}, $dat{$cnti[$i]}{p7}, 

	"Eta", $dat{$cnti[$i]}{e1}, $dat{$cnti[$i]}{e2}, $dat{$cnti[$i]}{e3},
	$dat{$cnti[$i]}{e4}, $dat{$cnti[$i]}{e5}, $dat{$cnti[$i]}{e6}, $dat{$cnti[$i]}{e7},

	"HPM", $dat{$cnti[$i]}{h1}, $dat{$cnti[$i]}{h2}, $dat{$cnti[$i]}{h3},
	$dat{$cnti[$i]}{h4}, $dat{$cnti[$i]}{h5}, $dat{$cnti[$i]}{h6}, $dat{$cnti[$i]}{h7}, 

	$dat{$cnti[$i]}{cintra}, $dat{$cnti[$i]}{cinter}, $dat{$cnti[$i]}{ctotal},
	$dat{$cnti[$i]}{nintra}, $dat{$cnti[$i]}{ninter}, $dat{$cnti[$i]}{ntotal},
	$dat{$cnti[$i]}{rmsd},

	$dat{$cnti[$i]}{r_ci}, $dat{$cnti[$i]}{r_ct},
	$dat{$cnti[$i]}{r_ni}, $dat{$cnti[$i]}{r_nt}, 

	$dat{$cnti[$i]}{r_Cti}, $dat{$cnti[$i]}{r_Nti},
	$dat{$cnti[$i]}{r_CNi}, $dat{$cnti[$i]}{r_CNt},

	$dat{$cnti[$i]}{r_CNti}, $dat{$cnti[$i]}{R_CNti},
	$dat{$cnti[$i]}{sbhrank}, $dat{$cnti[$i]}{source};

}
close CSV;
close TXT;

# Generate Histogram Data
# For each TM & Ranking :: Eta, Theta, Phi, Source :: Top 10, 100, All
# Rankings
@order_cinter = sort {$dat{$a}{cinter} <=> $dat{$b}{cinter}} keys %dat;
@order_ctotal = sort {$dat{$a}{ctotal} <=> $dat{$b}{ctotal}} keys %dat;
@order_ninter = sort {$dat{$a}{ninter} <=> $dat{$b}{ninter}} keys %dat;
@order_ntotal = sort {$dat{$a}{ntotal} <=> $dat{$b}{ntotal}} keys %dat;
@order_r_Cti  = sort {$dat{$a}{r_Cti}  <=> $dat{$b}{r_Cti}}  keys %dat;
@order_r_Nti  = sort {$dat{$a}{r_Nti}  <=> $dat{$b}{r_Nti}}  keys %dat;
@order_r_CNi  = sort {$dat{$a}{r_CNi}  <=> $dat{$b}{r_CNi}}  keys %dat;
@order_r_CNt  = sort {$dat{$a}{r_CNt}  <=> $dat{$b}{r_CNt}}  keys %dat;
@order_r_CNti = sort {$dat{$a}{r_CNti} <=> $dat{$b}{r_CNti}} keys %dat;
my %etas;
my %thetas;
my %phis;
my %sources;
for ($i = 0; $i < $n; $i++) {
    for ($tm = 1; $tm <= 7; $tm++) {
	# Cinter
	$e = $dat{$order_cinter[$i]}{"e${tm}"};
	$t = $dat{$order_cinter[$i]}{"t${tm}"};
	$p = $dat{$order_cinter[$i]}{"p${tm}"};
	$s = $dat{$order_cinter[$i]}{source};
	$etas{$e}    = 1;
	$thetas{$t}  = 1;
	$phis{$p}    = 1;
	$sources{$s} = 1;
	if ($i < 10) {
	    $hist{$tm}{cinter}{10}{e}{$e}++;
	    $hist{$tm}{cinter}{10}{t}{$t}++;
	    $hist{$tm}{cinter}{10}{p}{$p}++;
	    $hist{$tm}{cinter}{10}{s}{$s}++;
	}
	if ($i < 100) {
	    $hist{$tm}{cinter}{100}{e}{$e}++;
	    $hist{$tm}{cinter}{100}{t}{$t}++;
	    $hist{$tm}{cinter}{100}{p}{$p}++;
	    $hist{$tm}{cinter}{100}{s}{$s}++;
	}
	$hist{$tm}{cinter}{all}{e}{$e}++;
	$hist{$tm}{cinter}{all}{t}{$t}++;
	$hist{$tm}{cinter}{all}{p}{$p}++;
	$hist{$tm}{cinter}{all}{s}{$s}++;

	# Ctotal
	$e = $dat{$order_ctotal[$i]}{"e${tm}"};
	$t = $dat{$order_ctotal[$i]}{"t${tm}"};
	$p = $dat{$order_ctotal[$i]}{"p${tm}"};
	$s = $dat{$order_ctotal[$i]}{source};
	$etas{$e}    = 1;
	$thetas{$t}  = 1;
	$phis{$p}    = 1;
	$sources{$s} = 1;
	if ($i < 10) {
	    $hist{$tm}{ctotal}{10}{e}{$e}++;
	    $hist{$tm}{ctotal}{10}{t}{$t}++;
	    $hist{$tm}{ctotal}{10}{p}{$p}++;
	    $hist{$tm}{ctotal}{10}{s}{$s}++;
	}
	if ($i < 100) {
	    $hist{$tm}{ctotal}{100}{e}{$e}++;
	    $hist{$tm}{ctotal}{100}{t}{$t}++;
	    $hist{$tm}{ctotal}{100}{p}{$p}++;
	    $hist{$tm}{ctotal}{100}{s}{$s}++;
	}
	$hist{$tm}{ctotal}{all}{e}{$e}++;
	$hist{$tm}{ctotal}{all}{t}{$t}++;
	$hist{$tm}{ctotal}{all}{p}{$p}++;
	$hist{$tm}{ctotal}{all}{s}{$s}++;

	# Ninter
	$e = $dat{$order_ninter[$i]}{"e${tm}"};
	$t = $dat{$order_ninter[$i]}{"t${tm}"};
	$p = $dat{$order_ninter[$i]}{"p${tm}"};
	$s = $dat{$order_ninter[$i]}{source};
	$etas{$e}    = 1;
	$thetas{$t}  = 1;
	$phis{$p}    = 1;
	$sources{$s} = 1;
	if ($i < 10) {
	    $hist{$tm}{ninter}{10}{e}{$e}++;
	    $hist{$tm}{ninter}{10}{t}{$t}++;
	    $hist{$tm}{ninter}{10}{p}{$p}++;
	    $hist{$tm}{ninter}{10}{s}{$s}++;
	}
	if ($i < 100) {
	    $hist{$tm}{ninter}{100}{e}{$e}++;
	    $hist{$tm}{ninter}{100}{t}{$t}++;
	    $hist{$tm}{ninter}{100}{p}{$p}++;
	    $hist{$tm}{ninter}{100}{s}{$s}++;
	}
	$hist{$tm}{ninter}{all}{e}{$e}++;
	$hist{$tm}{ninter}{all}{t}{$t}++;
	$hist{$tm}{ninter}{all}{p}{$p}++;
	$hist{$tm}{ninter}{all}{s}{$s}++;

	# Ntotal
	$e = $dat{$order_ntotal[$i]}{"e${tm}"};
	$t = $dat{$order_ntotal[$i]}{"t${tm}"};
	$p = $dat{$order_ntotal[$i]}{"p${tm}"};
	$s = $dat{$order_ntotal[$i]}{source};
	$etas{$e}    = 1;
	$thetas{$t}  = 1;
	$phis{$p}    = 1;
	$sources{$s} = 1;
	if ($i < 10) {
	    $hist{$tm}{ntotal}{10}{e}{$e}++;
	    $hist{$tm}{ntotal}{10}{t}{$t}++;
	    $hist{$tm}{ntotal}{10}{p}{$p}++;
	    $hist{$tm}{ntotal}{10}{s}{$s}++;
	}
	if ($i < 100) {
	    $hist{$tm}{ntotal}{100}{e}{$e}++;
	    $hist{$tm}{ntotal}{100}{t}{$t}++;
	    $hist{$tm}{ntotal}{100}{p}{$p}++;
	    $hist{$tm}{ntotal}{100}{s}{$s}++;
	}
	$hist{$tm}{ntotal}{all}{e}{$e}++;
	$hist{$tm}{ntotal}{all}{t}{$t}++;
	$hist{$tm}{ntotal}{all}{p}{$p}++;
	$hist{$tm}{ntotal}{all}{s}{$s}++;

	# r_Cti
	$e = $dat{$order_r_Cti[$i]}{"e${tm}"};
	$t = $dat{$order_r_Cti[$i]}{"t${tm}"};
	$p = $dat{$order_r_Cti[$i]}{"p${tm}"};
	$s = $dat{$order_r_Cti[$i]}{source};
	$etas{$e}    = 1;
	$thetas{$t}  = 1;
	$phis{$p}    = 1;
	$sources{$s} = 1;
	if ($i < 10) {
	    $hist{$tm}{r_Cti}{10}{e}{$e}++;
	    $hist{$tm}{r_Cti}{10}{t}{$t}++;
	    $hist{$tm}{r_Cti}{10}{p}{$p}++;
	    $hist{$tm}{r_Cti}{10}{s}{$s}++;
	}
	if ($i < 100) {
	    $hist{$tm}{r_Cti}{100}{e}{$e}++;
	    $hist{$tm}{r_Cti}{100}{t}{$t}++;
	    $hist{$tm}{r_Cti}{100}{p}{$p}++;
	    $hist{$tm}{r_Cti}{100}{s}{$s}++;
	}
	$hist{$tm}{r_Cti}{all}{e}{$e}++;
	$hist{$tm}{r_Cti}{all}{t}{$t}++;
	$hist{$tm}{r_Cti}{all}{p}{$p}++;
	$hist{$tm}{r_Cti}{all}{s}{$s}++;

	# r_Nti
	$e = $dat{$order_r_Nti[$i]}{"e${tm}"};
	$t = $dat{$order_r_Nti[$i]}{"t${tm}"};
	$p = $dat{$order_r_Nti[$i]}{"p${tm}"};
	$s = $dat{$order_r_Nti[$i]}{source};
	$etas{$e}    = 1;
	$thetas{$t}  = 1;
	$phis{$p}    = 1;
	$sources{$s} = 1;
	if ($i < 10) {
	    $hist{$tm}{r_Nti}{10}{e}{$e}++;
	    $hist{$tm}{r_Nti}{10}{t}{$t}++;
	    $hist{$tm}{r_Nti}{10}{p}{$p}++;
	    $hist{$tm}{r_Nti}{10}{s}{$s}++;
	}
	if ($i < 100) {
	    $hist{$tm}{r_Nti}{100}{e}{$e}++;
	    $hist{$tm}{r_Nti}{100}{t}{$t}++;
	    $hist{$tm}{r_Nti}{100}{p}{$p}++;
	    $hist{$tm}{r_Nti}{100}{s}{$s}++;
	}
	$hist{$tm}{r_Nti}{all}{e}{$e}++;
	$hist{$tm}{r_Nti}{all}{t}{$t}++;
	$hist{$tm}{r_Nti}{all}{p}{$p}++;
	$hist{$tm}{r_Nti}{all}{s}{$s}++;

	# r_CNi
	$e = $dat{$order_r_CNi[$i]}{"e${tm}"};
	$t = $dat{$order_r_CNi[$i]}{"t${tm}"};
	$p = $dat{$order_r_CNi[$i]}{"p${tm}"};
	$s = $dat{$order_r_CNi[$i]}{source};
	$etas{$e}    = 1;
	$thetas{$t}  = 1;
	$phis{$p}    = 1;
	$sources{$s} = 1;
	if ($i < 10) {
	    $hist{$tm}{r_CNi}{10}{e}{$e}++;
	    $hist{$tm}{r_CNi}{10}{t}{$t}++;
	    $hist{$tm}{r_CNi}{10}{p}{$p}++;
	    $hist{$tm}{r_CNi}{10}{s}{$s}++;
	}
	if ($i < 100) {
	    $hist{$tm}{r_CNi}{100}{e}{$e}++;
	    $hist{$tm}{r_CNi}{100}{t}{$t}++;
	    $hist{$tm}{r_CNi}{100}{p}{$p}++;
	    $hist{$tm}{r_CNi}{100}{s}{$s}++;
	}
	$hist{$tm}{r_CNi}{all}{e}{$e}++;
	$hist{$tm}{r_CNi}{all}{t}{$t}++;
	$hist{$tm}{r_CNi}{all}{p}{$p}++;
	$hist{$tm}{r_CNi}{all}{s}{$s}++;

	# r_CNt
	$e = $dat{$order_r_CNt[$i]}{"e${tm}"};
	$t = $dat{$order_r_CNt[$i]}{"t${tm}"};
	$p = $dat{$order_r_CNt[$i]}{"p${tm}"};
	$s = $dat{$order_r_CNt[$i]}{source};
	$etas{$e}    = 1;
	$thetas{$t}  = 1;
	$phis{$p}    = 1;
	$sources{$s} = 1;
	if ($i < 10) {
	    $hist{$tm}{r_CNt}{10}{e}{$e}++;
	    $hist{$tm}{r_CNt}{10}{t}{$t}++;
	    $hist{$tm}{r_CNt}{10}{p}{$p}++;
	    $hist{$tm}{r_CNt}{10}{s}{$s}++;
	}
	if ($i < 100) {
	    $hist{$tm}{r_CNt}{100}{e}{$e}++;
	    $hist{$tm}{r_CNt}{100}{t}{$t}++;
	    $hist{$tm}{r_CNt}{100}{p}{$p}++;
	    $hist{$tm}{r_CNt}{100}{s}{$s}++;
	}
	$hist{$tm}{r_CNt}{all}{e}{$e}++;
	$hist{$tm}{r_CNt}{all}{t}{$t}++;
	$hist{$tm}{r_CNt}{all}{p}{$p}++;
	$hist{$tm}{r_CNt}{all}{s}{$s}++;

	# r_CNti
	$e = $dat{$order_r_CNti[$i]}{"e${tm}"};
	$t = $dat{$order_r_CNti[$i]}{"t${tm}"};
	$p = $dat{$order_r_CNti[$i]}{"p${tm}"};
	$s = $dat{$order_r_CNti[$i]}{source};
	$etas{$e}    = 1;
	$thetas{$t}  = 1;
	$phis{$p}    = 1;
	$sources{$s} = 1;
	if ($i < 10) {
	    $hist{$tm}{r_CNti}{10}{e}{$e}++;
	    $hist{$tm}{r_CNti}{10}{t}{$t}++;
	    $hist{$tm}{r_CNti}{10}{p}{$p}++;
	    $hist{$tm}{r_CNti}{10}{s}{$s}++;
	}
	if ($i < 100) {
	    $hist{$tm}{r_CNti}{100}{e}{$e}++;
	    $hist{$tm}{r_CNti}{100}{t}{$t}++;
	    $hist{$tm}{r_CNti}{100}{p}{$p}++;
	    $hist{$tm}{r_CNti}{100}{s}{$s}++;
	}
	$hist{$tm}{r_CNti}{all}{e}{$e}++;
	$hist{$tm}{r_CNti}{all}{t}{$t}++;
	$hist{$tm}{r_CNti}{all}{p}{$p}++;
	$hist{$tm}{r_CNti}{all}{s}{$s}++;
    }
}

foreach $set ("cinter", "ctotal", "ninter", "ntotal", "r_Cti", "r_Nti", "r_CNi", "r_CNt", "r_CNti") {
    open CSV, ">hist_${set}.csv";

    # TM1-7 :: E/T/P/S :: 10 100
    print CSV "Eta/10,,,,,,,,,Eta/100,,,,,,,,,Eta/All\n";
    print CSV
	"Eta,TM1,TM2,TM3,TM4,TM5,TM6,TM7,,".
	"Eta,TM1,TM2,TM3,TM4,TM5,TM6,TM7,,".
	"Eta,TM1,TM2,TM3,TM4,TM5,TM6,TM7\n";
    undef @tmp; @tmp = sort {$a <=> $b} keys %etas;
    for ($i = 0; $i < @tmp; $i++) {
	$e = $tmp[$i];
	printf CSV
	    "%d,%d,%d,%d,%d,%d,%d,%d,,".
	    "%d,%d,%d,%d,%d,%d,%d,%d,,".
	    "%d,%d,%d,%d,%d,%d,%d,%d\n",
	    $e, $hist{1}{$set}{10}{e}{$e}, $hist{2}{$set}{10}{e}{$e},
	    $hist{3}{$set}{10}{e}{$e}, $hist{4}{$set}{10}{e}{$e},
	    $hist{5}{$set}{10}{e}{$e}, $hist{6}{$set}{10}{e}{$e},
	    $hist{7}{$set}{10}{e}{$e},
	    $e, $hist{1}{$set}{100}{e}{$e}, $hist{2}{$set}{100}{e}{$e},
	    $hist{3}{$set}{100}{e}{$e}, $hist{4}{$set}{100}{e}{$e},
	    $hist{5}{$set}{100}{e}{$e}, $hist{6}{$set}{100}{e}{$e},
	    $hist{7}{$set}{100}{e}{$e},
	    $e, $hist{1}{$set}{all}{e}{$e}, $hist{2}{$set}{all}{e}{$e},
	    $hist{3}{$set}{all}{e}{$e}, $hist{4}{$set}{all}{e}{$e},
	    $hist{5}{$set}{all}{e}{$e}, $hist{6}{$set}{all}{e}{$e},
	    $hist{7}{$set}{all}{e}{$e};
    }
    print CSV "\n";

    print CSV "Phi/10,,,,,,,,,Phi/100,,,,,,,,,Phi/All\n";
    print CSV
	"Phi,TM1,TM2,TM3,TM4,TM5,TM6,TM7,,".
	"Phi,TM1,TM2,TM3,TM4,TM5,TM6,TM7,,".
	"Phi,TM1,TM2,TM3,TM4,TM5,TM6,TM7\n";
    undef @tmp; @tmp = sort {$a <=> $b} keys %phis;
    for ($i = 0; $i < @tmp; $i++) {
	$p = $tmp[$i];
	printf CSV
	    "%d,%d,%d,%d,%d,%d,%d,%d,,".
	    "%d,%d,%d,%d,%d,%d,%d,%d,,".
	    "%d,%d,%d,%d,%d,%d,%d,%d\n",
	    $p, $hist{1}{$set}{10}{p}{$p}, $hist{2}{$set}{10}{p}{$p},
	    $hist{3}{$set}{10}{p}{$p}, $hist{4}{$set}{10}{p}{$p},
	    $hist{5}{$set}{10}{p}{$p}, $hist{6}{$set}{10}{p}{$p},
	    $hist{7}{$set}{10}{p}{$p},
	    $p, $hist{1}{$set}{100}{p}{$p}, $hist{2}{$set}{100}{p}{$p},
	    $hist{3}{$set}{100}{p}{$p}, $hist{4}{$set}{100}{p}{$p},
	    $hist{5}{$set}{100}{p}{$p}, $hist{6}{$set}{100}{p}{$p},
	    $hist{7}{$set}{100}{p}{$p},
	    $p, $hist{1}{$set}{all}{p}{$p}, $hist{2}{$set}{all}{p}{$p},
	    $hist{3}{$set}{all}{p}{$p}, $hist{4}{$set}{all}{p}{$p},
	    $hist{5}{$set}{all}{p}{$p}, $hist{6}{$set}{all}{p}{$p},
	    $hist{7}{$set}{all}{p}{$p};
    }
    print CSV "\n";

    print CSV "Theta/10,,,,,,,,,Theta/100,,,,,,,,,Theta/All\n";
    print CSV
	"Theta,TM1,TM2,TM3,TM4,TM5,TM6,TM7,,".
	"Theta,TM1,TM2,TM3,TM4,TM5,TM6,TM7,,".
	"Theta,TM1,TM2,TM3,TM4,TM5,TM6,TM7\n";
    undef @tmp; @tmp = sort {$a <=> $b} keys %thetas;
    for ($i = 0; $i < @tmp; $i++) {
	$t = $tmp[$i];
	printf CSV
	    "%d,%d,%d,%d,%d,%d,%d,%d,,".
	    "%d,%d,%d,%d,%d,%d,%d,%d,,".
	    "%d,%d,%d,%d,%d,%d,%d,%d\n",
	    $t, $hist{1}{$set}{10}{t}{$t}, $hist{2}{$set}{10}{t}{$t},
	    $hist{3}{$set}{10}{t}{$t}, $hist{4}{$set}{10}{t}{$t},
	    $hist{5}{$set}{10}{t}{$t}, $hist{6}{$set}{10}{t}{$t},
	    $hist{7}{$set}{10}{t}{$t},
	    $t, $hist{1}{$set}{100}{t}{$t}, $hist{2}{$set}{100}{t}{$t},
	    $hist{3}{$set}{100}{t}{$t}, $hist{4}{$set}{100}{t}{$t},
	    $hist{5}{$set}{100}{t}{$t}, $hist{6}{$set}{100}{t}{$t},
	    $hist{7}{$set}{100}{t}{$t},
	    $t, $hist{1}{$set}{all}{t}{$t}, $hist{2}{$set}{all}{t}{$t},
	    $hist{3}{$set}{all}{t}{$t}, $hist{4}{$set}{all}{t}{$t},
	    $hist{5}{$set}{all}{t}{$t}, $hist{6}{$set}{all}{t}{$t},
	    $hist{7}{$set}{all}{t}{$t};
    }
    print CSV "\n";

    print CSV "Source/10,,,,,,,,,Source/100,,,,,,,,,Source/All\n";
    print CSV
	"Source,TM1,TM2,TM3,TM4,TM5,TM6,TM7,,".
	"Source,TM1,TM2,TM3,TM4,TM5,TM6,TM7,,".
	"Source,TM1,TM2,TM3,TM4,TM5,TM6,TM7\n";
    undef @tmp; @tmp = sort {$a cmp $b} keys %sources;
    for ($i = 0; $i < @tmp; $i++) {
	$s = $tmp[$i];
	printf CSV
	    "%s,%d,%d,%d,%d,%d,%d,%d,,".
	    "%s,%d,%d,%d,%d,%d,%d,%d,,".
	    "%s,%d,%d,%d,%d,%d,%d,%d\n",
	    $s, $hist{1}{$set}{10}{s}{$s}, $hist{2}{$set}{10}{s}{$s},
	    $hist{3}{$set}{10}{s}{$s}, $hist{4}{$set}{10}{s}{$s},
	    $hist{5}{$set}{10}{s}{$s}, $hist{6}{$set}{10}{s}{$s},
	    $hist{7}{$set}{10}{s}{$s},
	    $s, $hist{1}{$set}{100}{s}{$s}, $hist{2}{$set}{100}{s}{$s},
	    $hist{3}{$set}{100}{s}{$s}, $hist{4}{$set}{100}{s}{$s},
	    $hist{5}{$set}{100}{s}{$s}, $hist{6}{$set}{100}{s}{$s},
	    $hist{7}{$set}{100}{s}{$s},
	    $s, $hist{1}{$set}{all}{s}{$s}, $hist{2}{$set}{all}{s}{$s},
	    $hist{3}{$set}{all}{s}{$s}, $hist{4}{$set}{all}{s}{$s},
	    $hist{5}{$set}{all}{s}{$s}, $hist{6}{$set}{all}{s}{$s},
	    $hist{7}{$set}{all}{s}{$s};
    }
}


exit;



############################################################
### Help                                                 ###
############################################################

sub help {

    my $help = "
Program:
 :: ParseSCNOutput.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: ParseSCNOutput.pl {list of SCN output files}

Description:
 :: Reads in SuperCombiNeutralize output files and combines
 :: them.  Recalculates all of the different rankings and
 :: outputs a new CSV file.  Also creates histograms for
 :: eta rotations, phi tilts, theta tilts, and source file.
 :: The histograms find the number of occurrences of each
 :: rotation in the top 10, top 100, and all structures.
 ::
 :: Output:
 :: * MultiSuperCombiNeutralize.csv
 :: * hist_{scoring rank}.csv
 ::
 :: Note: While you *CAN* use SuperCombiNeutralize's
 :: .out files, you *REALLY* should use the .csv files
 :: instead!

";

    die "$help";
}
