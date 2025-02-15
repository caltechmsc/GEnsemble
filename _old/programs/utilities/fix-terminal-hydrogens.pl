#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
}

use Cwd;
use File::Copy;
use Getopt::Long;
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

$sbin = $FindBin::Bin;
($infile, $outfile) = @ARGV;

if ($outfile eq $infile) { $finaloutfile = $outfile; $outfile = "tmp.bgf"; }

open BGF, "$infile";
while (<BGF>) {
    if (/^DESCRP\s+(\S+)/) {
	$bgfdescrp = $1;
	last;
    }
}

$bgfdescrp = substr($bgfdescrp,0,8);

copy("$sbin/../FF/Biograf330.par",".");
chmod 0775, "Biograf330.par";
copy("$sbin/../FF/Biograf330.cnv",".");
chmod 0775, "Biograf330.cnv";

$macro =
    "beginmacro
Top menu/in-out
   In-Out/read
   File types/BioDesign
     \"$infile\"
   In-Out/return
Top menu/build
   Build/connect
        $bgfdescrp
        return
      Connect/execute
      Connect/return
   Build/modify H
      Modify H/add all H
        $bgfdescrp
      Modify H/return
   Build/return
Top menu/in-out
   In-Out/write
   File types/BioDesign
     $bgfdescrp
     return
     \"$outfile\"
     \" \"
   In-Out/return
Top menu/exit
  \"OK\"
%
endmacro
";

open MACRO, ">fixH.macro"; print MACRO "$macro"; close MACRO;

system "/bin/tcsh -fc 'source $sbin/../Biograf/.cshrc; $sbin/../Biograf/bio_linux batbio Biograf fixH.macro >& ${outfile}.fixH.out'";

open BGF, "$outfile";
@BGFLINES = <BGF>;
close BGF;

open BGF, ">$outfile";
foreach $line (@BGFLINES) {
    if      ((substr($line, 13, 2) eq "HN")  &&
	     (substr($line, 19, 3) ne "PRO") &&
	     ((substr($line, 10, 2) eq " 2") || (substr($line, 10, 2) eq " 3"))) {
	substr($line,71,9) = "  0.15500";
    } elsif ((substr($line, 13, 2) eq "HN")  &&
	     (substr($line, 19, 3) eq "PRO") &&
	     (substr($line, 10, 2) eq " 2")) {
	substr($line,71,9) = "  0.00000";
    }
    print BGF "$line";
}
close BGF;

if ($finaloutfile) { move("$outfile","$finaloutfile"); }

unlink glob "Biograf330.*";
#unlink "fixH.macro";
#unlink "logfile.macro";
#unlink "${outfile}.fixH.out";

exit;
