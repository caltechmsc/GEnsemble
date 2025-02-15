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
@bgfs = @ARGV;

foreach $bgf (@bgfs) {
    if ($bgf =~ /.bgf$/) {
	$outbgf = "$bgf"."H";
	`$sbin/fix-terminal-hydrogens.pl $bgf $outbgf`;
    }
}
