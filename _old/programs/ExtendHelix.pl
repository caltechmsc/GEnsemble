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
use Getopt::Long;
use List::Util qw(min max);
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

my $biogroup = "/project/Biogroup";
my $biosoft  = "${biogroup}/Software";
my $pwb      = "${biosoft}/GEnsemble/programs/utilities/playWithBGF/playWithBGF";
my $runmpsim = "${biosoft}/GEnsemble/programs/utilities/runMPSim.pl";
my $scream   = "${biosoft}/SCREAM/builds/current_build/SCREAM_wrap.py";
my $ff       = "${biogroup}/FF/dreiding-0.3.par";
my $merge    = "${biogroup}/scripts/BGFtools/mergeBGFs.py";
my $pair     = 1;
my $polyala  = "${biosoft}/GEnsemble/programs/utilities/polyalanines";

if (@ARGV == 0) { help(); }

my ($help, $bgf, $mfta, $debug);

#abcdefghijklmnopqrstuvwxyz
#abcdefg ijklmnopqrstuvwxyz
GetOptions ('h|help'          => \$help,
	    'b|bgf=s'         => \$bgf,
	    'm|mfta=s'        => \$mfta,
	    'p|pair=i'        => \$pair,
	    'debug'           => \$debug);

if ($help) { help(); }
if (!$bgf) {
    die "ExtendHelix :: Must provide a BGF file to work on!\n";
} elsif (! -e $bgf) {
    die "ExtendHelix :: Could not find specified BGF file :: $bgf\n";
}
if (!$mfta) {
    die "ExtendHelix :: Must provide a MFTA file corresponding to the BGF!\n";
} elsif (! -e $mfta) {
    die "ExtendHelix :: Could not find specified MFTA file :: $mfta\n";
}
if (($pair < 1) || ($pair > 4)) {
    die "ExtendHelix :: Pair value must be an integer between 1 and 4!\n";
}

############################################################
### Main Routine                                         ###
############################################################
print
    "ExtendHelix :: " . localtime() . "\n".
    " :: BGF File     :: $bgf\n".
    " :: MFTA File    :: $mfta\n".
    " :: MFTA TM Pair :: $pair\n\n";

(my $prefix = $bgf) =~ s/.bgf//;

# Load MFTA Data
my @ret = loadMFTA($mfta, $pair);
my %dat = %{$ret[0]};
my @chn = @{$ret[1]};
my $seq =   $ret[2];

# Load BGF Data
@ret = loadBGF($bgf, \%dat, \@chn);
%dat = %{$ret[0]};

# Parse Sequence
@ret = parseSeq($seq, \%dat, \@chn);
%dat = %{$ret[0]};

# Determine Extensions & Truncations
print "Extending/Truncating TMs ::\n";
@ret = detExtTrunc($seq, \%dat, \@chn);
my %mod = %{$ret[0]};

# Optimize Helix
print "Optimizing TMs ::\n";
foreach my $tm (@chn) {
    print "  TM ${tm}...";

    # TM not modified
    if ($mod{$tm} == 0) {
	print "skip...tm not modified...done\n";
	copy("tm${tm}.ext.bgf","tm${tm}.scr.min.bgf");
    }

    # TM modified
    else {
	# Alanize TM (A/G/P/S/T)
	# In:  tm${tm}.ext.bgf
	# Out: tm${tm}.ala.bgf
	print "ala...";
	alanizeTM($tm, \%dat, $seq);
	
	# Minimize TM (0.5 RMS Force)
	# In:  tm${tm}.ala.bgf
	# Out: tm${tm}.ala.min.bgf
	print "min...";
	minimizeTM("tm${tm}.ala.bgf", "tm${tm}.ala.min.bgf");
	
	# Replace Sidechains
	# In:  tm${tm}.ala.min.bgf
	# Out: tm${tm}.scr.bgf
	print "scr...";
	screamTM($tm, \%dat, $seq);

	# Minimize TM
	# In:  tm${tm}.scr.bgf
	# Out: tm${tm}.scr.min.bgf
	print "min...";
	minimizeTM("tm${tm}.scr.bgf", "tm${tm}.scr.min.bgf");
	print "done\n";
    }
}
print "\n";

# Make Bundle
my $command = "$merge";
foreach my $tm (@chn) {
    $command .= " tm${tm}.scr.min.bgf";
}
$command .= " -o ${prefix}.extended.bgf";
`$command`;
cleanBGF("${prefix}.extended.bgf");

# Cleanup
foreach my $tm (@chn) {
    unlink "tm${tm}.bgf";
    unlink "tm${tm}.ext.bgf";
    unlink "tm${tm}.ala.bgf";
    unlink "tm${tm}.ala.min.bgf";
    unlink "tm${tm}.scr.bgf";
    unlink "tm${tm}.scr.min.bgf";
}

print "Final Extended/Truncated BGF: ${prefix}.extended.bgf\n\n";

exit;	




############################################################
### Subroutines                                          ###
############################################################

# Load MFTA
sub loadMFTA {
    my $mfta = $_[0];
    my $pair = $_[1];
	
    my %dat;
    my @chn;
    my $seq;
	
    open MFTA, "$mfta";
    while (<MFTA>) {
	if (/^\*\s+(\d+)tm\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)/) {
	    if ($pair == 1) {
		$dat{mfta}{$1}{start} = $2;
		$dat{mfta}{$1}{stop}  = $3;
	    } elsif ($pair == 2) {
		$dat{mfta}{$1}{start} = $4;
		$dat{mfta}{$1}{stop}  = $5;
	    } elsif ($pair == 3) {
		$dat{mfta}{$1}{start} = $6;
		$dat{mfta}{$1}{stop}  = $7;
	    } elsif ($pair == 4) {
		$dat{mfta}{$1}{start} = $8;
		$dat{mfta}{$1}{stop}  = $9;
	    }
	    push @chn, $1;
	} elsif (!/^\*/ && !/^\>/ && !/^\#/) {
	    $seq .= $_;
	    chomp $seq;
	}
    }
    close MFTA;

    my @chntmp = sort @chn;
    @chn = @chntmp;
	
    # Return
    return (\%dat, \@chn, $seq);
}

# Parse BGF
sub loadBGF {
    my $bgf =   $_[0];
    my %dat = %{$_[1]};
    my @chn = @{$_[2]};

    my %resnums;
    open BGF, "$bgf";
    while (<BGF>) {
	if (/^ATOM\s+\d+\s+N\s+(\S+)\s+(\S+)\s+(\d+)/) {
	    my $res3   = $1;
	    my $chn    = $2;
	    my $resnum = $3;
	    my $res1   = res3tores1($res3);
	    push @{$resnums{$chn}}, $resnum;
	}
    }
    close BGF;
    foreach my $i (@chn) {
	$dat{bgf}{$i}{start} = $resnums{$i}[0];
	$dat{bgf}{$i}{stop}  = $resnums{$i}[-1];
    }
	
    # Return
    return (\%dat);
}

# Parse Sequence
sub parseSeq {
    my $seq =   $_[0];
    my %dat = %{$_[1]};
    my @chn = @{$_[2]};
	
    foreach my $i (@chn) {
	for (my $j = 1; $j <= length($seq); $j++) {
	    if (($dat{mfta}{$i}{start} <= $j) && ($j <= $dat{mfta}{$i}{stop})) {
		$dat{mfta}{$i}{seq} .= substr($seq,$j,1);
	    }
	    if (($dat{bgf}{$i}{start} <= $j) && ($j <= $dat{bgf}{$i}{stop})) {
		$dat{bgf}{$i}{seq} .= substr($seq,$j,1);
	    }
    	}
    }
    
    # Return
    return (\%dat);
}

# Determine extensions and truncations
sub detExtTrunc {
    my $seq =   $_[0];
    my %dat = %{$_[1]};
    my @chn = @{$_[2]};

    # Split BGF
    foreach my $i (@chn) {
	`$pwb $bgf -c $i -V on -no tm${i}.bgf`;
    }

    # Hash to log whether TM was modified
    my %mod = ();

    # Cycle through each TM
    foreach my $tm (@chn) {
	print " :: TM ${tm} ::\n";
	
	# $dat{bgf/mfta}{tm}{start/stop}
	my $ndiff = $dat{mfta}{$tm}{start} - $dat{bgf}{$tm}{start};
	my $cdiff = $dat{mfta}{$tm}{stop}  - $dat{bgf}{$tm}{stop};

	# No change to TM
	if (($ndiff == 0) && ($cdiff == 0)) {
	    $mod{$tm} = 0;
	}
	# Change to N- &/or C-term 
	else {
	    $mod{$tm} = 1;
	}

	copy("tm${tm}.bgf", "tm${tm}.ext.bgf");
	
	# N-term Extension
	if ($ndiff < 0) {
	    print "    N-term :: Extend from $dat{bgf}{$tm}{start} to $dat{mfta}{$tm}{start}\n";
	    extNTerm($tm, $dat{mfta}{$tm}{start}, $dat{bgf}{$tm}{start}, $seq);
	}
		
	# N-term Truncation
	if ($ndiff > 0) {
	    print "    N-term :: Truncate from $dat{bgf}{$tm}{start} to $dat{mfta}{$tm}{start}\n";
	    truncNTerm($tm, $dat{mfta}{$tm}{start}, $dat{bgf}{$tm}{stop}, $seq);
	}
		
	# N-term No Change
	if ($ndiff == 0) {
	    print "    N-term :: Keep at $dat{bgf}{$tm}{start}\n";
	}
	
	# N-term Extension
	if ($cdiff > 0) {
	    print "    C-term :: Extend from $dat{bgf}{$tm}{stop} to $dat{mfta}{$tm}{stop}\n";
	    extCTerm($tm, $dat{mfta}{$tm}{stop}, $dat{bgf}{$tm}{stop}, $seq);
	}
		
	# N-term Truncation
	if ($cdiff < 0) {
	    print "    C-term :: Truncate from $dat{bgf}{$tm}{stop} to $dat{mfta}{$tm}{stop}\n";
	    truncCTerm($tm, $dat{mfta}{$tm}{start}, $dat{mfta}{$tm}{stop}, $seq);
	}
		
	# N-term No Change
	if ($cdiff == 0) {
	    print "    C-term :: Keep at $dat{bgf}{$tm}{stop}\n";
	}
		
	# Clean BGF
	cleanBGF("tm${tm}.ext.bgf");
	print "\n";
    }

    return (\%mod);
}

# N-term extension
sub extNTerm {
    my $tm  = $_[0];
    my $new = $_[1];
    my $old = $_[2];
    my $seq = $_[3];
	
    # Get PolyAla Extension
    my $extstart  = $new;
    my $extstop   = $old + 7;
    my $extlen    = $extstop - $extstart + 1;
    my $renumdiff = $extstart - 1;
    copy("${polyala}/ala${extlen}.bgf", "ext.old.bgf");
	
    # Renumber Extension
    open BGFIN,  "ext.old.bgf";
    open BGFOUT, ">ext.ren.bgf";
    while (<BGFIN>) {
	my $line = $_;
	if ($line =~ /^ATOM\s+\d+\s+\S+\s+\S+\s\S\s+(\d+)/) {
	    substr($line,25,4) = sprintf "%4d", $1 + $renumdiff;
	    print BGFOUT $line;
	} elsif ($line =~ /^DESCRP/) {
	    print BGFOUT "DESCRP\n";
	} elsif ($line !~ /^REMARK/) {
	    print BGFOUT $line;
	}
    }
    close BGFIN;
    close BGFOUT;
    unlink "ext.old.bgf";

    # Align Extension
    my $vmdscript =
	"mol new tm${tm}.ext.bgf type \{bgf\} first 0 last -1 step 1 waitfor 1\n".
	"mol new ext.ren.bgf type \{bgf\} first 0 last -1 step 1 waitfor 1\n".
	"set sel1 \[atomselect 0 \"name CA and resid $old to $extstop\"\]\n".
	"set sel2 \[atomselect 1 \"name CA and resid $old to $extstop\"\]\n".
	"set transformation_matrix \[measure fit \$sel2 \$sel1\]\n".
	"set move_sel \[atomselect 1 \"all\"\]\n".
	"\$move_sel move \$transformation_matrix\n".
	"animate write bgf ext.new.bgf beg 0 end 0 skip 1 1\n".
	"quit\n";
    open VMD, ">vmd.vmd";
    print VMD $vmdscript;
    close VMD;
    my $lines = `/exec/VMD/bin/vmd -dispdev text -e vmd.vmd`;
    unlink "vmd.vmd";
    unlink "ext.ren.bgf";
    cleanBGF("ext.new.bgf");

    # Connect Extension
    my $tmp = $old - 1;
    `$pwb ext.new.bgf -r '${extstart}...${tmp}A' -o ext.new.bgf`;
    open IN, "ext.new.bgf";
    my @lines = <IN>;
    close IN;
    open OUT, ">ext.new.bgf";
    while (my $line = shift(@lines)) {
	if ((substr($line, 0, 4) eq "ATOM")) {
	    substr($line,23,1) = "${tm}";
	    substr($line,24,6) = substr($line,25,6);
	}
	print OUT $line;
    }
    close OUT;
    `/ul/caglar/Python/GPCRassembler.py ext.new.bgf tm${tm}.ext.bgf -o tm${tm}.ext.new.bgf`;
    move("tm${tm}.ext.new.bgf","tm${tm}.ext.bgf");
    unlink "ext.new.bgf";
}

# N-term truncation
sub truncNTerm {
    my $tm         = $_[0];
    my $truncstart = $_[1];
    my $truncstop  = $_[2];
    my $seq        = $_[3];
	
    # Rechain as A so that PWB will work with it
    open IN, "tm${tm}.ext.bgf";
    my @lines = <IN>;
    close IN;
    open OUT, ">tm${tm}.ext.bgf";
    while (my $line = shift(@lines)) {
	if ((substr($line, 0, 4) eq "ATOM")) {
	    substr($line,23,1) = "A";
	}
	print OUT $line;
    }
    close OUT;

    # Truncate
    `$pwb tm${tm}.ext.bgf -r '${truncstart}...${truncstop}A' +H -o tm${tm}.ext.bgf`;

    # Rechain 
    open IN, "tm${tm}.ext.bgf";
    @lines = <IN>;
    close IN;
    open OUT, ">tm${tm}.ext.bgf";
    while (my $line = shift(@lines)) {
	if ((substr($line, 0, 4) eq "ATOM")) {
	    substr($line,23,1) = "${tm}";
	}
	print OUT $line;
    }
    close OUT;
}

# C-term extension
sub extCTerm {
    my $tm  = $_[0];
    my $new = $_[1];
    my $old = $_[2];
    my $seq = $_[3];
	
    # Get PolyAla Extension
    my $extstart  = $old - 7;
    my $extstop   = $new;
    my $extlen    = $extstop - $extstart + 1;
    my $renumdiff = $extstart - 1;
    copy("${polyala}/ala${extlen}.bgf", "ext.old.bgf");
	
    # Renumber Extension
    open BGFIN,  "ext.old.bgf";
    open BGFOUT, ">ext.ren.bgf";
    while (<BGFIN>) {
	my $line = $_;
	if ($line =~ /^ATOM\s+\d+\s+\S+\s+\S+\s\S\s+(\d+)/) {
	    substr($line,25,4) = sprintf "%4d", $1 + $renumdiff;
	    print BGFOUT $line;
	} elsif ($line =~ /^DESCRP/) {
	    print BGFOUT "DESCRP\n";
	} elsif ($line !~ /^REMARK/) {
	    print BGFOUT $line;
	}
    }
    close BGFIN;
    close BGFOUT;
    unlink "ext.old.bgf";

    # Align Extension
    my $vmdscript =
	"mol new tm${tm}.ext.bgf type \{bgf\} first 0 last -1 step 1 waitfor 1\n".
	"mol new ext.ren.bgf type \{bgf\} first 0 last -1 step 1 waitfor 1\n".
	"set sel1 \[atomselect 0 \"name CA and resid $extstart to $old\"\]\n".
	"set sel2 \[atomselect 1 \"name CA and resid $extstart to $old\"\]\n".
	"set transformation_matrix \[measure fit \$sel2 \$sel1\]\n".
	"set move_sel \[atomselect 1 \"all\"\]\n".
	"\$move_sel move \$transformation_matrix\n".
	"animate write bgf ext.new.bgf beg 0 end 0 skip 1 1\n".
	"quit\n";
    open VMD, ">vmd.vmd";
    print VMD $vmdscript;
    close VMD;
    my $lines = `/exec/VMD/bin/vmd -dispdev text -e vmd.vmd`;
    unlink "vmd.vmd";
    unlink "ext.ren.bgf";
    cleanBGF("ext.new.bgf");
    
    # Connect Extension
    my $tmp = $old + 1;
    `$pwb ext.new.bgf -r '${tmp}...${extstop}A' -o ext.new.bgf`;
    open IN, "ext.new.bgf";
    my @lines = <IN>;
    close IN;
    open OUT, ">ext.new.bgf";
    while (my $line = shift(@lines)) {
	if ((substr($line, 0, 4) eq "ATOM")) {
	    substr($line,23,1) = "${tm}";
	    substr($line,24,6) = substr($line,25,6);
	}
	print OUT $line;
    }
    close OUT;
    `/ul/caglar/Python/GPCRassembler.py ext.new.bgf tm${tm}.ext.bgf -o tm${tm}.ext.new.bgf`;
    move("tm${tm}.ext.new.bgf","tm${tm}.ext.bgf");
    unlink "ext.new.bgf";
}

# C-term truncation
sub truncCTerm {
    my $tm         = $_[0];
    my $truncstart = $_[1];
    my $truncstop  = $_[2];
    my $seq        = $_[3];

    # Rechain as A so that PWB will work with it
    open IN, "tm${tm}.ext.bgf";
    my @lines = <IN>;
    close IN;
    open OUT, ">tm${tm}.ext.bgf";
    while (my $line = shift(@lines)) {
	if ((substr($line, 0, 4) eq "ATOM")) {
	    substr($line,23,1) = "A";
	}
	print OUT $line;
    }
    close OUT;

    # Truncate
    `$pwb tm${tm}.ext.bgf -r '${truncstart}...${truncstop}A' +H -o tm${tm}.ext.bgf`;

    # Rechain 
    open IN, "tm${tm}.ext.bgf";
    @lines = <IN>;
    close IN;
    open OUT, ">tm${tm}.ext.bgf";
    while (my $line = shift(@lines)) {
	if ((substr($line, 0, 4) eq "ATOM")) {
	    substr($line,23,1) = "${tm}";
	}
	print OUT $line;
    }
    close OUT;
}
	
# Alanize TM (A/G/P/S/T)
# In:  tm${tm}.ext.bgf
# Out: tm${tm}.ala.bgf
sub alanizeTM {
    my $tm  =   $_[0];
    my %dat = %{$_[1]};
    my $seq =   $_[2];

    my $start = $dat{mfta}{$tm}{start};
    my $stop  = $dat{mfta}{$tm}{stop};
    my $reslist = "";

    # Residue list
    for (my $i = $start; $i <= $stop; $i++) {
	if (substr($seq, $i - 1, 1) =~ /(A|G|P|S|T)/) {
	    $reslist .= " " . substr($seq, $i - 1, 1) . "${i}_${tm}";
	} else {
	    $reslist .= " A${i}_${tm}";
	}
    }
	
    # Scream
    `$scream tm${tm}.ext.bgf 05 FULL 0.0 $reslist >& /dev/null`;

    # Check Output
    if (! -e "best_1.bgf") {
	die "ExtendHelix :: Alanization failed for TM $tm.\n";
    } else {
	move("best_1.bgf", "tm${tm}.ala.bgf");
	unlink "Anneal-Energies.txt";
	unlink "Field1.bgf";
	unlink "Residue-E.txt";
	unlink "scream.out";
	unlink "scream.par";
	unlink "timing.txt";
    }
}
	
# Minimize TM (0.5 RMS Force)
sub minimizeTM {
    my $in = $_[0];
    my $out = $_[1];
	
    # Minimize to 0.5 RMS Force
    `$runmpsim $in -f $ff -l 0 -s 1000 -t 0.5 minvac >& /dev/null`;

    # Cleanup
    (my $pfx = $in) =~ s/.bgf//;
    unlink glob "${pfx}_minvac.snap*";
    unlink "${pfx}_minvac.ctl";
    unlink "${pfx}_minvac.out";
    unlink "${pfx}_minvac.traj1";
    move("${pfx}_minvac.fin.bgf", $out);
}

# Replace Sidechains
# In:  tm${tm}.ala.min.bgf
# Out: tm${tm}.scr.bgf
sub screamTM {
    my $tm  =   $_[0];
    my %dat = %{$_[1]};
    my $seq =   $_[2];
    my $start = $dat{mfta}{$tm}{start};
    my $stop  = $dat{mfta}{$tm}{stop};
    my $reslist = "";

    # Residue list
    for (my $i = $start; $i <= $stop; $i++) {
	$reslist .= " " . substr($seq, $i - 1, 1) . "${i}_${tm}";
    }
	
    # Scream
    `$scream tm${tm}.ala.min.bgf 05 FULL 0.0 $reslist >& /dev/null`;

    # Check Output
    if (! -e "best_1.bgf") {
	die "ExtendHelix :: Scream failed for TM $tm.\n";
    } else {
	move("best_1.bgf", "tm${tm}.scr.min.bgf");
	unlink "Anneal-Energies.txt";
	unlink "Field1.bgf";
	unlink "Residue-E.txt";
	unlink "scream.out";
	unlink "scream.par";
	unlink "timing.txt";
    }
}

# Clean up a BGF
sub cleanBGF {
    my $bgf = $_[0]; # BGF to Clean

    # Temporary files
    (my $tmp1 = $bgf) =~ s/.bgf/.tmp1.bgf/;
    (my $tmp2 = $bgf) =~ s/.bgf/.tmp2.bgf/;
    (my $tmp3 = $bgf) =~ s/.bgf/.tmp3.bgf/;

    # Fix things: Fix atom ordering, assign charges, make SCREAM compatible
    my $screambuilds = "${biosoft}/SCREAM/builds/current_build/utilities/";
    `${screambuilds}/Make_SCREAM_compatible_Bgf.py  $bgf  $tmp1`;
    `${screambuilds}/fix_atom_ordering              $tmp1 $tmp2`;
    `/ul/victor/Python/bin/Assign_CHARMM_charges.py $tmp2 $tmp3`;
    move($tmp3,$bgf);
    unlink $tmp1;
    unlink $tmp2;
}

# 3-Letter amino acid to 1-letter amino acid
sub res3tores1 {
    (my $aa) = @_;
    if    ($aa =~ /ALA/) { return "A"; }
    elsif ($aa =~ /ARG/) { return "R"; }
    elsif ($aa =~ /ARN/) { return "R"; } # Neutral ARG
    elsif ($aa =~ /ASN/) { return "N"; }
    elsif ($aa =~ /ASP/) { return "D"; }
    elsif ($aa =~ /APP/) { return "D"; } # Neutral ASP
    elsif ($aa =~ /CYS/) { return "C"; }
    elsif ($aa =~ /CYX/) { return "X"; } # Disulfide CYS
    elsif ($aa =~ /GLU/) { return "E"; }
    elsif ($aa =~ /GLP/) { return "E"; } # Neutral GLU
    elsif ($aa =~ /GLN/) { return "Q"; }
    elsif ($aa =~ /GLY/) { return "G"; }
    elsif ($aa =~ /HIS/) { return "H"; }
    elsif ($aa =~ /HSD/) { return "H"; }
    elsif ($aa =~ /HSE/) { return "H"; }
    elsif ($aa =~ /HIE/) { return "H"; }
    elsif ($aa =~ /HSP/) { return "H"; }
    elsif ($aa =~ /ILE/) { return "I"; }
    elsif ($aa =~ /LEU/) { return "L"; }
    elsif ($aa =~ /LYS/) { return "K"; }
    elsif ($aa =~ /LYN/) { return "K"; } # Neutral LYS
    elsif ($aa =~ /MET/) { return "M"; }
    elsif ($aa =~ /PHE/) { return "F"; }
    elsif ($aa =~ /PRO/) { return "P"; }
    elsif ($aa =~ /SER/) { return "S"; }
    elsif ($aa =~ /THR/) { return "T"; }
    elsif ($aa =~ /TRP/) { return "W"; }
    elsif ($aa =~ /TYR/) { return "Y"; }
    elsif ($aa =~ /VAL/) { return "V"; }
    else                 { return $aa; }
}

############################################################
### Help                                                 ###
############################################################

sub help {

    my $help = "
Program:
 :: .pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: ExtendHelix.pl -b {bgf} -m {mfta} -p {pair}

Input:
 :: -b | --bgf  :: Filename
 :: BGF of 7TM bundle with helices to extend or truncate.
 :: CAN NOT HAVE LOOPS!

 :: -m | --mfta :: Filename
 :: MFTA corresponding to BGF protein with TM start/stop
 :: values for extensions/truncations.

 :: -p | --pair :: Integer [1-4]
 :: Pair of start/stop values for extensions/truncations
 :: in the MFTA file.  Default is first pair.

 :: -h | --help        :: No Input
 :: Displays this help message.

Description:
 :: This program extends or truncates the helices in the 7TM
 :: BGF bundle based on start/stop values provided in a MFTA
 :: file.  The program determines the current start/stop
 :: values for the protein based on the provided BGF.
 ::
 :: If a TM needs to be truncated, then the residues are
 :: removed with PlayWith BGF.
 ::
 :: If a TM needs to be extended, the following procedure is
 :: used:
 :: * Obtain canonical polyalanine helix with a length that
 ::   is 8 residues longer than the length of the extension
 :: * Using VMD, align the extra 8 residues to the first or
 ::   last 8 residues of the TM region
 :: * Remove the overlapping 8 residues from the canonical
 ::   helix, connect the aligned extension to the TM region
 ::
 :: If a TM is either extended or truncated, then the
 :: following procedure is applied:
 :: 1) Alanize entire TM region, keeping all G/P/S/T
 :: 2) Minimize TM region (1000 steps, 0.5 RMS Force, minvac)
 :: 3) Scream all residues back into place
 :: 4) Minimize TM region (1000 steps, 0.5 RMS Force, minvac)
 ::
 :: The final output bundle is rebuilt from the modified
 :: helices.

Usage:
 :: ExtendHelix.pl -b {bgf} -m {mfta} -p {pair}

";

    die "$help";
}
